"""Public domain boundary for a versioned Opportunity Atlas Workspace."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from uuid import uuid4

from ranking import rank_opportunities


_ATLAS_MAP_NAMES = (
    "The Amber Current",
    "The Saffron Passage",
    "The Meridian Isles",
    "The Starlit Sound",
)

# The first Map-core slice intentionally keeps a small, shared evaluation lens.
# Chart Room may later add richer evidence and configurable lenses.
ISLAND_EVALUATION_DIMENSION_IDS = ("value", "readiness", "effort")

# The Chart Room holds only material a team has explicitly authored.  AI lenses
# are deliberately not a persistence field: they remain transient guidance in
# the interface until a person turns an idea into their own wording.
CHART_ROOM_FIELD_IDS = (
    "workflow_problem",
    "ai_change",
    "outcome",
    "evidence",
    "unknowns",
    "workflow_sketch",
    "readiness_data",
    "safeguards_risk",
    "ownership_adoption",
    "learning_action",
)


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
    # Lightweight, individually authored inputs stay separate from the Map
    # until somebody explicitly transfers one into an Island.
    scouting_notes: list[dict] = field(default_factory=list)
    # Archived Islands are retained separately from the living Map so their
    # reasoned removal can be compared to an Expedition snapshot and reversed.
    archived_islands: list[dict] = field(default_factory=list)
    # Expeditions preserve a time-specific commitment without freezing the Map.
    # The active Expedition is the most recent confirmed one; earlier ones are
    # retained as past records rather than being rewritten when the Map moves.
    expeditions: list[dict] = field(default_factory=list)
    # ``decision_frame.goal`` is retained only to read older persisted data.
    map_focus: str | None = None

    @property
    def name(self) -> str:
        return self.custom_name or _ATLAS_MAP_NAMES[(self.number - 1) % len(_ATLAS_MAP_NAMES)]

    @property
    def north_star(self) -> str | None:
        """Read-only strategy context for the Map, not Map-owned data."""
        return self.decision_frame.get("strategy")

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
        decision_frame: dict | None = None,
        opportunities: list[dict],
        dimensions: list[dict],
        assessments: dict,
        shortlist: list[str] | None = None,
        custom_name: str | None = None,
        map_focus: str | None = None,
    ) -> "Workspace":
        frame = deepcopy(decision_frame or {})
        focus = map_focus if map_focus is not None else frame.get("goal")
        return cls(
            iterations=[
                Iteration(
                    number=1,
                    decision_frame=frame,
                    opportunities=deepcopy(opportunities),
                    dimensions=deepcopy(dimensions),
                    assessments=deepcopy(assessments),
                    shortlist=deepcopy(shortlist or []),
                    custom_name=custom_name,
                    map_focus=focus,
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
            map_focus=deepcopy(source.map_focus),
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

    def update_current_map(
        self,
        *,
        map_focus: str | None = None,
        name: str | None = None,
    ) -> Iteration:
        """Update the current Opportunity Map's team-authored metadata.

        ``None`` means the caller did not change that field.  Empty strings are
        rejected so the Map always remains understandable when a team does add
        a value.
        """
        current = self.current_iteration
        if map_focus is not None:
            if not map_focus.strip():
                raise ValueError("Map focus cannot be empty.")
            current.map_focus = map_focus.strip()
        if name is not None:
            if not name.strip():
                raise ValueError("Map name cannot be empty.")
            current.custom_name = name.strip()
        return current

    def add_opportunity(self, opportunity: dict) -> dict:
        current = self.current_iteration
        if not opportunity.get("id") or not opportunity.get("title"):
            raise ValueError("An Opportunity needs an id and title.")
        if any(item["id"] == opportunity["id"] for item in current.opportunities):
            raise ValueError("An Opportunity with this id already exists.")
        current.opportunities.append(deepcopy(opportunity))
        return current.opportunities[-1]

    def archive_island(self, *, opportunity_id: str, reason: str) -> dict:
        """Remove an Island from the active Map while retaining its provenance.

        This is deliberately a small domain seam for comparison and future Map
        controls. The #29 view itself remains read-only.
        """
        if not isinstance(reason, str) or not reason.strip():
            raise ValueError("Archiving an Island requires a reason.")
        current = self.current_iteration
        island = next(
            (candidate for candidate in current.opportunities if candidate["id"] == opportunity_id),
            None,
        )
        if island is None:
            raise ValueError("The Island does not belong to this Map.")
        current.opportunities = [
            candidate for candidate in current.opportunities if candidate["id"] != opportunity_id
        ]
        archive = {
            "island": deepcopy(island),
            "reason": reason.strip(),
            "archived_at": self._timestamp(),
        }
        current.archived_islands.append(archive)
        return archive

    def restore_archived_island(self, opportunity_id: str) -> dict:
        """Return a reasoned archived Island to the active living Map."""
        current = self.current_iteration
        index = next(
            (
                position
                for position, archive in enumerate(current.archived_islands)
                if archive["island"]["id"] == opportunity_id
            ),
            None,
        )
        if index is None:
            raise ValueError("The Island is not archived on this Map.")
        archive = current.archived_islands.pop(index)
        current.opportunities.append(deepcopy(archive["island"]))
        return current.opportunities[-1]

    @property
    def current_expedition(self) -> dict | None:
        """Return the Map's one active Expedition, if a team has confirmed one."""
        return next(
            (
                expedition
                for expedition in reversed(self.current_iteration.expeditions)
                if expedition.get("status") == "active"
            ),
            None,
        )

    def confirm_expedition(self, *, charters: list[dict]) -> dict:
        """Confirm Island-specific Charters and preserve the current Map state.

        An Expedition does not formulate a new Map-wide goal or recalculate an
        Island ranking. Each Charter simply says what the team will learn or do
        next for one selected, already-charted Island.
        """
        if not isinstance(charters, list) or not charters:
            raise ValueError("An Expedition needs at least one Island Charter.")

        current = self.current_iteration
        known_islands = {island["id"] for island in current.opportunities}
        validated_charters = []
        selected_island_ids = set()
        optional_fields = ("participants", "intended_outcome", "decision_evidence")
        for charter in charters:
            if not isinstance(charter, dict):
                raise ValueError("Each Island Charter must be an object.")
            island_id = charter.get("island_id")
            if island_id not in known_islands:
                raise ValueError("A selected Island does not belong to this Map.")
            if island_id in selected_island_ids:
                raise ValueError("An Island can have only one Charter in an Expedition.")
            action = charter.get("next_learning_action")
            if not isinstance(action, str) or not action.strip():
                raise ValueError("Each Island Charter needs a next learning action.")
            normalized = {"island_id": island_id, "next_learning_action": action.strip()}
            for field_name in optional_fields:
                value = charter.get(field_name, "")
                if not isinstance(value, str):
                    raise ValueError("Island Charter fields must be text.")
                normalized[field_name] = value.strip()
            selected_island_ids.add(island_id)
            validated_charters.append(normalized)

        active = self.current_expedition
        if active is not None:
            active["status"] = "past"
            active["became_past_at"] = self._timestamp()

        snapshot = {
            "name": current.name,
            "north_star": current.north_star,
            "islands": deepcopy(current.opportunities),
            "scouting_notes": deepcopy(current.scouting_notes),
        }
        expedition = {
            "id": f"expedition-{uuid4().hex}",
            "status": "active",
            "selected_island_ids": [charter["island_id"] for charter in validated_charters],
            "charters": validated_charters,
            "map_snapshot": snapshot,
            "confirmed_at": self._timestamp(),
        }
        current.expeditions.append(expedition)
        return expedition

    def map_changes_for_expedition(self, expedition_id: str) -> dict:
        """Compare a confirmed Expedition's immutable Map snapshot to today.

        The comparison is deliberately a derived, read-only view.  The Map is
        still the team's living source of truth, so it needs neither manually
        named versions nor a mandatory explanation every time it evolves.
        """
        expedition = next(
            (
                candidate
                for candidate in self.current_iteration.expeditions
                if candidate["id"] == expedition_id
            ),
            None,
        )
        if expedition is None:
            raise ValueError("The Expedition does not belong to this Map.")

        snapshot_by_id = {
            island["id"]: island for island in expedition["map_snapshot"]["islands"]
        }
        snapshot_notes = expedition["map_snapshot"].get("scouting_notes")
        snapshot_notes_by_id = {note["id"] for note in snapshot_notes or []}
        current_by_id = {
            island["id"]: island for island in self.current_iteration.opportunities
        }

        added = [
            {"island": deepcopy(island)}
            for island in self.current_iteration.opportunities
            if island["id"] not in snapshot_by_id
        ]
        added_scouting_notes = [
            deepcopy(note)
            for note in self.current_iteration.scouting_notes
            if (
                note["id"] not in snapshot_notes_by_id
                and (
                    snapshot_notes is not None
                    or note.get("created_at", "") > expedition["confirmed_at"]
                )
            )
            and not note.get("transferred_to_island_id")
        ]
        changed = []
        for island in expedition["map_snapshot"]["islands"]:
            current_island = current_by_id.get(island["id"])
            if current_island is None or current_island == island:
                continue
            before_values = island.get("evaluation", {})
            after_values = current_island.get("evaluation", {})
            value_changes = [
                {
                    "id": value_id,
                    "before": before_values.get(value_id, {}).get("score"),
                    "after": after_values.get(value_id, {}).get("score"),
                }
                for value_id in sorted(set(before_values) | set(after_values))
                if before_values.get(value_id, {}).get("score")
                != after_values.get(value_id, {}).get("score")
            ]
            changed.append(
                {
                    "before": deepcopy(island),
                    "after": deepcopy(current_island),
                    "value_changes": value_changes,
                }
            )
        archived_by_id = {
            archive["island"]["id"]: archive
            for archive in self.current_iteration.archived_islands
        }
        archived = [
            {
                "island": deepcopy(archived_by_id[island["id"]]["island"]),
                "reason": archived_by_id[island["id"]]["reason"],
            }
            for island in expedition["map_snapshot"]["islands"]
            if island["id"] in archived_by_id
        ]
        newly_stronger_unselected = self._newly_stronger_unselected_islands(
            expedition=expedition,
            snapshot_by_id=snapshot_by_id,
            current_by_id=current_by_id,
        )
        return {
            "added": added,
            "added_scouting_notes": added_scouting_notes,
            "changed": changed,
            "archived": archived,
            "newly_stronger_unselected": newly_stronger_unselected,
            "has_changes": bool(added or added_scouting_notes or changed or archived),
        }

    @staticmethod
    def _map_value_signal(island: dict) -> float | None:
        """Derive a comparable current Map signal without storing a rank.

        This is intentionally a read-only comparison aid, not an Expedition
        ranking model. It uses only the visible Island values and normalises
        lower effort so a higher signal remains more favourable.
        """
        evaluation = island.get("evaluation", {})
        scores = []
        for dimension in ISLAND_EVALUATION_DIMENSION_IDS:
            value = evaluation.get(dimension, {}).get("score")
            if not isinstance(value, int):
                continue
            scores.append(6 - value if dimension == "effort" else value)
        return sum(scores) / len(scores) if scores else None

    def _newly_stronger_unselected_islands(
        self,
        *,
        expedition: dict,
        snapshot_by_id: dict[str, dict],
        current_by_id: dict[str, dict],
    ) -> list[dict]:
        """Find new crossovers, not pre-existing selection trade-offs."""
        selected_ids = set(expedition["selected_island_ids"])
        selected_current = [
            current_by_id[island_id]
            for island_id in selected_ids
            if island_id in current_by_id
        ]
        notices = []
        for island_id, island in current_by_id.items():
            if island_id in selected_ids:
                continue
            island_score = self._map_value_signal(island)
            if island_score is None:
                continue
            prior_island_score = self._map_value_signal(snapshot_by_id.get(island_id, {}))
            for selected in selected_current:
                selected_score = self._map_value_signal(selected)
                if selected_score is None or island_score <= selected_score:
                    continue
                prior_selected_score = self._map_value_signal(snapshot_by_id.get(selected["id"], {}))
                was_previously_stronger = (
                    prior_island_score is not None
                    and prior_selected_score is not None
                    and prior_island_score > prior_selected_score
                )
                if not was_previously_stronger:
                    notices.append(
                        {
                            "island_id": island_id,
                            "selected_island_id": selected["id"],
                            "island_score": island_score,
                            "selected_island_score": selected_score,
                        }
                    )
        return notices

    def add_scouting_note(self, *, title: str, body: str, author: str) -> dict:
        """Capture an individual's early thought without adding an Island.

        A Scouting note is intentionally not team-authored Map material.  It
        only becomes an Island through ``transfer_scouting_note`` below.
        """
        if not isinstance(title, str) or not title.strip():
            raise ValueError("A Scouting note needs a title.")
        if not isinstance(body, str) or not body.strip():
            raise ValueError("A Scouting note needs some text.")
        if not isinstance(author, str) or not author.strip():
            raise ValueError("A Scouting note needs its author's name.")
        note = {
            "id": f"note-{uuid4().hex}",
            "title": title.strip(),
            "body": body.strip(),
            "author": author.strip(),
            "created_at": self._timestamp(),
            "transferred_to_island_id": None,
        }
        self.current_iteration.scouting_notes.append(note)
        return note

    def transfer_scouting_note(self, *, note_id: str, island_title: str) -> dict:
        """Create an Island explicitly and retain the note as provenance."""
        if not isinstance(island_title, str) or not island_title.strip():
            raise ValueError("An Island needs a name.")
        note = next(
            (candidate for candidate in self.current_iteration.scouting_notes if candidate["id"] == note_id),
            None,
        )
        if note is None:
            raise ValueError("The Scouting note does not belong to this Map.")
        if note.get("transferred_to_island_id"):
            raise ValueError("This Scouting note has already been transferred into an Island.")

        island = self.add_opportunity(
            {
                "id": f"island-{uuid4().hex}",
                "title": island_title.strip(),
                "description": note["body"],
                # Keep the original contribution intact and visibly distinct
                # from later team-authored evidence or Chart Room material.
                "scouting_note": deepcopy(note),
            }
        )
        note["transferred_to_island_id"] = island["id"]
        island["scouting_note"]["transferred_to_island_id"] = island["id"]
        return island

    def update_opportunity(
        self,
        opportunity_id: str,
        *,
        title: str | None = None,
        detail: str | None = None,
        next_move: str | None = None,
        ai_formulation: str | None = None,
        evaluation: dict | None = None,
        chart_room: dict | None = None,
    ) -> dict:
        """Develop an Island while preserving its original team note.

        AI wording is stored separately from team-authored detail so it cannot
        silently replace the team's original contribution.
        """
        current = self.current_iteration
        opportunity = next(
            (item for item in current.opportunities if item["id"] == opportunity_id), None
        )
        if opportunity is None:
            raise ValueError("The Island does not belong to this Map.")
        if title is not None:
            if not title.strip():
                raise ValueError("An Island needs a name.")
            opportunity["title"] = title.strip()
        for key, value in {
            "detail": detail,
            "next_move": next_move,
            "ai_formulation": ai_formulation,
        }.items():
            if value is not None:
                opportunity[key] = value.strip()
        if evaluation is not None:
            opportunity["evaluation"] = self._validated_evaluation(evaluation)
        if chart_room is not None:
            opportunity["chart_room"] = self._validated_chart_room(chart_room)
        return opportunity

    @staticmethod
    def _validated_chart_room(chart_room: dict) -> dict:
        """Keep Chart Room material explicitly team-authored and inspectable."""
        if not isinstance(chart_room, dict):
            raise ValueError("Chart Room material must be an object.")
        validated = {}
        for field_id, value in chart_room.items():
            if field_id not in CHART_ROOM_FIELD_IDS:
                raise ValueError(f"Unknown Chart Room field '{field_id}'.")
            if not isinstance(value, str):
                raise ValueError("Chart Room fields must be text.")
            validated[field_id] = value.strip()
        return validated

    @staticmethod
    def _validated_evaluation(evaluation: dict) -> dict:
        """Keep a team's visible values and their reasons together on an Island."""
        if not isinstance(evaluation, dict):
            raise ValueError("Island evaluation values must be an object.")
        validated = {}
        for dimension, value in evaluation.items():
            if dimension not in ISLAND_EVALUATION_DIMENSION_IDS:
                raise ValueError(f"Unknown Island evaluation value '{dimension}'.")
            if not isinstance(value, dict):
                raise ValueError("Each Island evaluation value must include a score and rationale.")
            score = value.get("score")
            rationale = value.get("rationale")
            if not isinstance(score, int) or not 1 <= score <= 5:
                raise ValueError("Island evaluation scores must be whole numbers from 1 to 5.")
            if not isinstance(rationale, str) or not rationale.strip():
                raise ValueError("Each Island evaluation score needs a team rationale.")
            validated[dimension] = {"score": score, "rationale": rationale.strip()}
        return validated

    def to_dict(self) -> dict:
        return {"iterations": [asdict(iteration) for iteration in self.iterations]}

    @classmethod
    def from_dict(cls, payload: dict) -> "Workspace":
        iterations = []
        for item in payload["iterations"]:
            serialized = deepcopy(item)
            serialized.setdefault("scouting_notes", [])
            serialized.setdefault("archived_islands", [])
            serialized.setdefault("expeditions", [])
            # Old persisted Workspaces stored focus only in the Decision Frame.
            serialized.setdefault("map_focus", serialized.get("decision_frame", {}).get("goal"))
            # A short-lived prototype stored North Star on the Iteration. Keep
            # its value as generic strategy context while migrating old data.
            legacy_north_star = serialized.pop("north_star", None)
            if legacy_north_star and not serialized.get("decision_frame", {}).get("strategy"):
                serialized.setdefault("decision_frame", {})["strategy"] = legacy_north_star
            iterations.append(Iteration(**serialized))
        if not iterations:
            raise ValueError("A Workspace requires an Iteration.")
        return cls(iterations=iterations)
