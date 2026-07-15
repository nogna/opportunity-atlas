"""Explainable Ranking behaviour for an Opportunity Atlas Iteration.

This module deliberately owns only derived ranking.  It accepts the raw
Opportunity, Evaluation dimension, and Assessment records held by Workspace
without changing any of them.
"""

from __future__ import annotations

from copy import deepcopy
from numbers import Real


DEFAULT_DIMENSION_IDS = (
    "expected-value",
    "strategic-alignment",
    "data-readiness",
    "delivery-ease",
    "risk-manageability",
    "evidence-confidence",
)


_DEFAULT_RUBRIC = (
    {
        "id": "expected-value",
        "name": "Expected value",
        "definition": "The magnitude and reach of the expected user or business outcome.",
        "anchors": {
            1: "A marginal, local improvement.",
            3: "A meaningful improvement for one workflow or team.",
            5: "A material, measurable outcome across a priority workflow or organization.",
        },
    },
    {
        "id": "strategic-alignment",
        "name": "Strategic alignment",
        "definition": "How directly the Opportunity advances the Decision frame's stated goal.",
        "anchors": {
            1: "A weak or indirect connection.",
            3: "Supports one stated priority.",
            5: "Directly advances the primary decision goal or a critical organizational priority.",
        },
    },
    {
        "id": "data-readiness",
        "name": "Data readiness",
        "definition": "Whether needed data is available, usable, permitted, and understood.",
        "anchors": {
            1: "Required data is missing, inaccessible, or prohibited.",
            3: "Relevant data exists but needs cleanup, access work, or validation.",
            5: "Suitable data is available, permitted, and well understood.",
        },
    },
    {
        "id": "delivery-ease",
        "name": "Delivery ease",
        "definition": "The relative ease across integration, change management, evaluation, and delivery work.",
        "anchors": {
            1: "Major, multi-team effort with substantial dependencies or change management.",
            3: "Moderate cross-functional delivery work.",
            5: "A light, contained change with few dependencies.",
        },
    },
    {
        "id": "risk-manageability",
        "name": "Risk manageability",
        "definition": "How limited, understood, and mitigable legal, safety, privacy, operational, and adoption risks are.",
        "anchors": {
            1: "Major unmitigated risks.",
            3: "Material risks with credible mitigations.",
            5: "Limited, understood risks with straightforward mitigations.",
        },
    },
    {
        "id": "evidence-confidence",
        "name": "Evidence confidence",
        "definition": "The strength and corroboration of the team's Evidence.",
        "anchors": {
            1: "Mostly assumptions or anecdotes with little corroboration.",
            3: "Some relevant qualitative or quantitative Evidence, with important gaps remaining.",
            5: "Multiple credible, relevant sources or direct measurements supporting the Opportunity.",
        },
    },
)


def default_rubric() -> list[dict]:
    """Return an editable, equal-weighted copy of the standard rubric."""
    dimensions = deepcopy(_DEFAULT_RUBRIC)
    for order, dimension in enumerate(dimensions):
        dimension.update({"direction": "higher", "weight": 1, "display_order": order, "is_default": True})
    return dimensions


def validate_dimensions(dimensions: list[dict]) -> None:
    """Reject a weighted custom dimension whose scoring meaning is undefined."""
    for dimension in dimensions:
        weight = _weight(dimension)
        if weight < 0:
            raise ValueError("An Evaluation dimension weight cannot be negative.")
        if dimension.get("id") in DEFAULT_DIMENSION_IDS:
            continue
        if weight and (dimension.get("direction") not in {"higher", "lower"} or not _has_all_anchors(dimension)):
            identifier = dimension.get("id", "unnamed")
            raise ValueError(
                f"Custom Evaluation dimension '{identifier}' needs a direction and 1, 3, and 5 scoring anchors before it can have a non-zero weight."
            )


def validate_rubric(dimensions: list[dict]) -> None:
    """Validate an editable Iteration rubric, including its non-removable defaults."""
    validate_dimensions(dimensions)
    present_ids = {dimension.get("id") for dimension in dimensions}
    missing_ids = [identifier for identifier in DEFAULT_DIMENSION_IDS if identifier not in present_ids]
    if missing_ids:
        raise ValueError(
            "Default Evaluation dimensions must remain present: " + ", ".join(missing_ids) + "."
        )


def rank_opportunities(*, opportunities: list[dict], dimensions: list[dict], assessments: dict) -> list[dict]:
    """Return ranked and visibly unranked Opportunities without mutating inputs.

    Scores are normalized so the displayed weighted score always has 5 as its
    most favourable value.  Ranked entries precede unranked entries.  Within a
    shared score, titles are alphabetical and the entries share a competition
    rank (1, 1, 3).
    """
    all_weights = [_weight(dimension) for dimension in dimensions]
    if any(weight < 0 for weight in all_weights):
        raise ValueError("An Evaluation dimension weight cannot be negative.")
    active_dimensions = [dimension for dimension, weight in zip(dimensions, all_weights) if weight > 0]
    _validate_ranking_dimensions(active_dimensions)
    total_weight = sum(_weight(dimension) for dimension in active_dimensions)

    ranked: list[dict] = []
    unranked: list[dict] = []
    for opportunity in opportunities:
        opportunity_id = opportunity["id"]
        title = opportunity.get("title", opportunity_id)
        opportunity_assessments = assessments.get(opportunity_id, {})
        missing = [dimension["id"] for dimension in active_dimensions if dimension["id"] not in opportunity_assessments]
        if missing or not active_dimensions:
            entry = {
                "opportunity_id": opportunity_id,
                "title": title,
                "state": "unranked",
                "rank": None,
                "score": None,
                "missing_dimension_ids": missing,
                "contributions": [],
            }
            if not active_dimensions:
                entry["reason"] = "no_weighted_dimensions"
            unranked.append(entry)
            continue

        contributions = []
        weighted_total = 0.0
        for dimension in active_dimensions:
            raw_score = _assessment_score(opportunity_assessments[dimension["id"]])
            favourable_score = 6 - raw_score if dimension["direction"] == "lower" else raw_score
            weight = _weight(dimension)
            weighted_total += favourable_score * weight
            contributions.append(
                {
                    "dimension_id": dimension["id"],
                    "weight": weight,
                    "raw_score": raw_score,
                    "favourable_score": favourable_score,
                    "weighted_score": favourable_score * weight,
                    **_assessment_context(opportunity_assessments[dimension["id"]]),
                }
            )
        ranked.append(
            {
                "opportunity_id": opportunity_id,
                "title": title,
                "state": "ranked",
                "rank": None,
                "score": weighted_total / total_weight,
                "missing_dimension_ids": [],
                "contributions": contributions,
            }
        )

    ranked.sort(key=lambda entry: (-entry["score"], _title_key(entry)))
    previous_score = None
    for index, entry in enumerate(ranked, start=1):
        if entry["score"] != previous_score:
            rank = index
            previous_score = entry["score"]
        entry["rank"] = rank
    unranked.sort(key=_title_key)
    return ranked + unranked


def _validate_ranking_dimensions(dimensions: list[dict]) -> None:
    for dimension in dimensions:
        if not dimension.get("id"):
            raise ValueError("An Evaluation dimension needs an id.")
        if dimension.get("direction") not in {"higher", "lower"}:
            raise ValueError(f"Evaluation dimension '{dimension['id']}' needs a higher or lower direction.")


def _assessment_score(assessment: object) -> int:
    score = assessment.get("score") if isinstance(assessment, dict) else assessment
    if isinstance(score, bool) or not isinstance(score, int) or not 1 <= score <= 5:
        raise ValueError("An Assessment needs a whole-number score from 1 to 5.")
    return score


def _assessment_context(assessment: object) -> dict:
    """Expose assessment context when present without inventing an indicator scheme."""
    if not isinstance(assessment, dict):
        return {}
    return {
        key: assessment[key]
        for key in ("rationale", "confidence")
        if key in assessment
    }


def _weight(dimension: dict) -> float:
    weight = dimension.get("weight", 0)
    if isinstance(weight, bool) or not isinstance(weight, Real):
        raise ValueError("An Evaluation dimension weight must be a number.")
    return float(weight)


def _has_all_anchors(dimension: dict) -> bool:
    anchors = dimension.get("anchors")
    if not isinstance(anchors, dict):
        return False
    return all(anchors.get(score) or anchors.get(str(score)) for score in (1, 3, 5))


def _title_key(entry: dict) -> tuple[str, str]:
    return (str(entry["title"]).casefold(), entry["opportunity_id"])
