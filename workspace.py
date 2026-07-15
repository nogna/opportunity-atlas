"""Public domain boundary for a versioned Opportunity Atlas Workspace."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone


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
    ) -> Iteration:
        current = self.current_iteration
        if current.is_set:
            raise ValueError("A set Iteration cannot be changed.")
        if not rationale.strip():
            raise ValueError("A Next Opportunity decision requires a rationale.")
        if next_opportunity_id not in current.shortlist:
            raise ValueError("The Next Opportunity must belong to the Shortlist.")

        current.next_opportunity_decision = {
            "opportunity_id": next_opportunity_id,
            "rationale": rationale,
            "recorded_by": recorded_by,
            "recorded_at": self._timestamp(),
        }
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
        )
        self.iterations.append(next_iteration)
        return next_iteration

    def current_ranking(self) -> list[dict]:
        current = self.current_iteration
        total_weight = sum(item.get("weight", 0) for item in current.dimensions)
        if not total_weight:
            return []
        results = []
        for opportunity in current.opportunities:
            scores = current.assessments.get(opportunity["id"], {})
            if any(dimension.get("weight", 0) and dimension["id"] not in scores for dimension in current.dimensions):
                continue
            total = sum(scores[dimension["id"]] * dimension.get("weight", 0) for dimension in current.dimensions)
            results.append({"opportunity_id": opportunity["id"], "score": total / total_weight})
        return sorted(results, key=lambda result: (-result["score"], result["opportunity_id"]))

    @staticmethod
    def _timestamp() -> str:
        return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    def rename_current_iteration(self, custom_name: str | None) -> Iteration:
        current = self.current_iteration
        if current.is_set:
            raise ValueError("A set Iteration cannot be renamed.")
        current.custom_name = custom_name.strip() if custom_name else None
        return current

    def to_dict(self) -> dict:
        return {"iterations": [asdict(iteration) for iteration in self.iterations]}

    @classmethod
    def from_dict(cls, payload: dict) -> "Workspace":
        iterations = [Iteration(**deepcopy(item)) for item in payload["iterations"]]
        if not iterations:
            raise ValueError("A Workspace requires an Iteration.")
        return cls(iterations=iterations)
