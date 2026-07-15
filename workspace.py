"""Public domain boundary for a versioned Opportunity Atlas Workspace."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone

from ranking import rank_opportunities


@dataclass
class Iteration:
    number: int
    decision_frame: dict
    opportunities: list[dict]
    dimensions: list[dict]
    assessments: dict
    shortlist: list[str] = field(default_factory=list)
    custom_name: str | None = None
    what_changed: str | None = None
    source_iteration_number: int | None = None
    created_at: str | None = None
    next_opportunity_decision: dict | None = None
    decision_snapshot: dict | None = None
    archive_decisions: list[dict] = field(default_factory=list)
    inherited_opportunities: dict[str, dict] = field(default_factory=dict)

    @property
    def name(self) -> str:
        return self.custom_name or f"Iteration {self.number}"

    @property
    def is_set(self) -> bool:
        return self.next_opportunity_decision is not None

    @property
    def is_editable(self) -> bool:
        return not self.is_set


@dataclass
class Workspace:
    iterations: list[Iteration] = field(default_factory=list)

    @classmethod
    def start(
        cls,
        *,
        decision_frame: dict,
        opportunities: list[dict],
        dimensions: list[dict],
        assessments: dict,
        shortlist: list[str] | None = None,
        custom_name: str | None = None,
    ) -> "Workspace":
        return cls(
            iterations=[
                Iteration(
                    number=1,
                    decision_frame=deepcopy(decision_frame),
                    opportunities=deepcopy(opportunities),
                    dimensions=deepcopy(dimensions),
                    assessments=deepcopy(assessments),
                    shortlist=deepcopy(shortlist or []),
                    custom_name=custom_name,
                )
            ]
        )

    @property
    def current_iteration(self) -> Iteration:
        return self.iterations[-1]

    def set_current_iteration(
        self,
        *,
        next_opportunity_id: str,
        rationale: str,
        recorded_by: str,
        unranked_override_rationale: str | None = None,
    ) -> Iteration:
        current = self.current_iteration
        if current.is_set:
            raise ValueError("A set Iteration cannot be changed.")
        if not rationale.strip():
            raise ValueError("A Next Opportunity decision requires a rationale.")
        if next_opportunity_id not in current.shortlist:
            raise ValueError("The Next Opportunity must belong to the Shortlist.")
        selected_ranking = next(
            item
            for item in self.current_ranking()
            if item["opportunity_id"] == next_opportunity_id
        )
        if selected_ranking["state"] == "unranked" and not (
            unranked_override_rationale and unranked_override_rationale.strip()
        ):
            raise ValueError(
                "Choosing an unranked Next Opportunity requires an override rationale."
            )

        current.next_opportunity_decision = {
            "opportunity_id": next_opportunity_id,
            "rationale": rationale,
            "recorded_by": recorded_by,
            "recorded_at": self._timestamp(),
        }
        if selected_ranking["state"] == "unranked":
            current.next_opportunity_decision["unranked_override_rationale"] = (
                unranked_override_rationale.strip()
            )
        current.decision_snapshot = {
            "ranking": self.current_ranking(),
            "dimensions": deepcopy(current.dimensions),
        }
        return current

    def start_next_iteration(
        self,
        *,
        what_changed: str,
        custom_name: str | None = None,
    ) -> Iteration:
        source = self.current_iteration
        if not source.is_set:
            raise ValueError("Set the current Iteration before starting the next one.")
        if not what_changed.strip():
            raise ValueError("A new Iteration requires a what changed note.")

        next_iteration = Iteration(
            number=source.number + 1,
            decision_frame=deepcopy(source.decision_frame),
            opportunities=deepcopy(source.opportunities),
            dimensions=deepcopy(source.dimensions),
            assessments=deepcopy(source.assessments),
            shortlist=deepcopy(source.shortlist),
            custom_name=custom_name,
            what_changed=what_changed,
            source_iteration_number=source.number,
            created_at=self._timestamp(),
            inherited_opportunities={
                opportunity["id"]: {
                    "opportunity": deepcopy(opportunity),
                    "assessment": deepcopy(source.assessments.get(opportunity["id"])),
                    "shortlisted": opportunity["id"] in source.shortlist,
                }
                for opportunity in source.opportunities
            },
        )
        self.iterations.append(next_iteration)
        return next_iteration

    def review_inherited_opportunities(self) -> list[dict]:
        """Return the source Opportunities for the current carry-forward review."""
        current = self.current_iteration
        if current.source_iteration_number is None:
            raise ValueError("The first Iteration has no inherited Opportunities to review.")

        archive_by_id = {
            archive["opportunity_id"]: archive for archive in current.archive_decisions
        }
        return [
            {
                "opportunity": deepcopy(inherited["opportunity"]),
                "source_iteration_number": current.source_iteration_number,
                "previously_not_pursuing": bool(
                    inherited["opportunity"].get("not_pursuing_decision")
                ),
                "archived": (
                    opportunity_id in archive_by_id
                    and archive_by_id[opportunity_id].get("restored_at") is None
                ),
            }
            for opportunity_id, inherited in sorted(current.inherited_opportunities.items())
        ]

    def archive_inherited_opportunity(self, *, opportunity_id: str, reason: str) -> dict:
        """Archive one inherited Opportunity from the current draft Iteration."""
        current = self.current_iteration
        self._require_editable_carry_forward_draft(current)
        if not reason.strip():
            raise ValueError("An Archive decision requires a reason.")
        inherited = current.inherited_opportunities.get(opportunity_id)
        if inherited is None:
            raise ValueError("Only inherited Opportunities can be archived during carry-forward review.")
        if any(
            decision["opportunity_id"] == opportunity_id
            and decision.get("restored_at") is None
            for decision in current.archive_decisions
        ):
            raise ValueError("This inherited Opportunity is already archived.")

        current.opportunities = [
            opportunity
            for opportunity in current.opportunities
            if opportunity["id"] != opportunity_id
        ]
        current.assessments.pop(opportunity_id, None)
        current.shortlist = [
            candidate_id
            for candidate_id in current.shortlist
            if candidate_id != opportunity_id
        ]
        archive = {
            "opportunity_id": opportunity_id,
            "reason": reason,
            "source_iteration_number": current.source_iteration_number,
            "source_opportunity_summary": self._opportunity_summary(
                inherited["opportunity"]
            ),
            "archived_at": self._timestamp(),
        }
        current.archive_decisions.append(archive)
        return archive

    def restore_inherited_opportunity(self, opportunity_id: str) -> dict:
        """Restore an archived inherited Opportunity into the current draft."""
        current = self.current_iteration
        self._require_editable_carry_forward_draft(current)
        inherited = current.inherited_opportunities.get(opportunity_id)
        if inherited is None:
            raise ValueError("Only inherited Opportunities can be restored during carry-forward review.")
        archive = next(
            (
                decision
                for decision in reversed(current.archive_decisions)
                if decision["opportunity_id"] == opportunity_id
                and decision.get("restored_at") is None
            ),
            None,
        )
        if archive is None:
            raise ValueError("This inherited Opportunity is not archived.")

        opportunity = deepcopy(inherited["opportunity"])
        current.opportunities.append(opportunity)
        if inherited["assessment"] is not None:
            current.assessments[opportunity_id] = deepcopy(inherited["assessment"])
        if inherited["shortlisted"]:
            current.shortlist.append(opportunity_id)
        archive["restored_at"] = self._timestamp()
        return opportunity

    @staticmethod
    def _opportunity_summary(opportunity: dict) -> dict:
        summary_keys = ("id", "title", "target_user", "affected_workflow")
        return {
            key: deepcopy(opportunity[key])
            for key in summary_keys
            if key in opportunity
        }

    @staticmethod
    def _require_editable_carry_forward_draft(iteration: Iteration) -> None:
        if iteration.is_set:
            raise ValueError("A set Iteration cannot be changed.")
        if iteration.source_iteration_number is None:
            raise ValueError("Only a new Iteration has a carry-forward review.")

    def current_ranking(self) -> list[dict]:
        current = self.current_iteration
        return rank_opportunities(
            opportunities=current.opportunities,
            dimensions=current.dimensions,
            assessments=current.assessments,
        )

    @staticmethod
    def _timestamp() -> str:
        return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    def rename_current_iteration(self, custom_name: str | None) -> Iteration:
        current = self.current_iteration
        if current.is_set:
            raise ValueError("A set Iteration cannot be renamed.")
        current.custom_name = custom_name.strip() if custom_name else None
        return current

    def add_opportunity(self, opportunity: dict) -> dict:
        current = self.current_iteration
        if not current.is_editable:
            raise ValueError("A set Iteration cannot be changed.")
        if not opportunity.get("id") or not opportunity.get("title"):
            raise ValueError("An Opportunity needs an id and title.")
        if any(item["id"] == opportunity["id"] for item in current.opportunities):
            raise ValueError("An Opportunity with this id already exists.")
        current.opportunities.append(deepcopy(opportunity))
        return current.opportunities[-1]

    def to_dict(self) -> dict:
        return {"iterations": [asdict(iteration) for iteration in self.iterations]}

    @classmethod
    def from_dict(cls, payload: dict) -> "Workspace":
        iterations = [Iteration(**deepcopy(item)) for item in payload["iterations"]]
        if not iterations:
            raise ValueError("A Workspace requires an Iteration.")
        return cls(iterations=iterations)
