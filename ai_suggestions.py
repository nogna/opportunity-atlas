"""Review-first, non-persisting suggestions for a Workspace draft."""

from copy import deepcopy


def suggest_for_iteration(iteration):
    """Return advisory candidates, weights, and trade-offs; never mutate Iteration."""
    goal = iteration.decision_frame.get("goal", "the team goal")
    candidates = [
        {
            "id": "ai-draft-support-workflow",
            "title": "AI-assisted workflow discovery",
            "description": f"Explore an AI-assisted step that advances: {goal}",
            "assumptions": ["A repeatable workflow exists.", "A human remains accountable for consequential decisions."],
            "uncertainties": ["The relevant data source and volume need team confirmation."],
        }
    ]
    weights = []
    for dimension in iteration.dimensions:
        weight = 1
        rationale = "A balanced starting point while the team validates its Decision Frame."
        if dimension["id"] == "strategic-alignment":
            weight, rationale = 2, "The Decision Frame makes strategic fit especially important."
        weights.append({"dimension_id": dimension["id"], "weight": weight, "rationale": rationale})
    return {
        "candidates": candidates,
        "weight_suggestion": weights,
        "trade_offs": "Compare the shortlisted opportunities’ value, delivery ease, and evidence gaps; this is not a recommendation.",
    }


def apply_suggested_weights(iteration, suggested_weights):
    """Apply a team-approved proposal and return the now-editable dimensions."""
    if not iteration.is_editable:
        raise ValueError("A set Iteration cannot be changed.")
    proposed = {item["dimension_id"]: item["weight"] for item in suggested_weights}
    dimensions = deepcopy(iteration.dimensions)
    for dimension in dimensions:
        if dimension["id"] in proposed:
            dimension["weight"] = proposed[dimension["id"]]
    iteration.dimensions = dimensions
    return dimensions
