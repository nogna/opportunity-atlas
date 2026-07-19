import unittest

from workspace import Workspace


class WorkspaceOpportunityMapTests(unittest.TestCase):
    def test_first_map_exposes_its_focus_generated_atlas_name_and_workspace_north_star(self):
        workspace = Workspace.start(
            map_focus="Improve the support experience.",
            ai_strategy="Helpful AI with accountable human decisions.",
            opportunities=[],
            dimensions=[],
            assessments={},
        )

        current = workspace.current_iteration

        self.assertEqual("Improve the support experience.", current.map_focus)
        self.assertEqual("Helpful AI with accountable human decisions.", workspace.ai_strategy)
        self.assertIsNone(workspace.ai_vision)
        self.assertEqual("The Amber Current", current.name)
        serialized = workspace.to_dict()
        self.assertEqual("Helpful AI with accountable human decisions.", serialized["ai_strategy"])
        self.assertIsNone(serialized["ai_vision"])
        self.assertTrue(current.is_editable)
        self.assertIsNone(current.source_iteration_number)

    def test_team_can_edit_map_metadata_while_the_first_map_is_open(self):
        workspace = self._workspace()

        updated = workspace.update_current_map(
            map_focus="Find the most valuable support workflow to improve.",
            name="The Saffron Passage",
        )

        self.assertEqual(
            "Find the most valuable support workflow to improve.", updated.map_focus
        )
        self.assertEqual("The Saffron Passage", updated.name)
        self.assertNotIn("goal", updated.decision_frame)

    def test_map_metadata_rejects_blank_values(self):
        workspace = self._workspace()

        with self.assertRaisesRegex(ValueError, "Map focus"):
            workspace.update_current_map(map_focus=" ")
        with self.assertRaisesRegex(ValueError, "Map name"):
            workspace.update_current_map(name=" ")

    def test_adding_an_island_persists_on_the_current_map(self):
        workspace = self._workspace()

        island = workspace.add_opportunity(
            {"id": "case-summary", "title": "Case summary assistant", "summary": "A rough team note."}
        )

        self.assertEqual("case-summary", island["id"])
        self.assertEqual([island], workspace.current_iteration.opportunities)

        restored = Workspace.from_dict(workspace.to_dict())
        self.assertEqual("The Amber Current", restored.current_iteration.name)
        self.assertEqual("Improve the support experience.", restored.current_iteration.map_focus)
        self.assertEqual([island], restored.current_iteration.opportunities)

    def test_team_can_develop_an_island_without_replacing_its_original_note(self):
        workspace = self._workspace()
        workspace.add_opportunity(
            {
                "id": "case-summary",
                "title": "Case summary assistant",
                "summary": "A rough team note.",
            }
        )

        island = workspace.update_opportunity(
            "case-summary",
            detail="Help support leads prepare a case summary before escalation.",
            next_move="Ask two support leads to review a sample.",
            ai_formulation="Potential AI formulation: draft a cited case summary for lead review.",
        )

        self.assertEqual("A rough team note.", island["summary"])
        self.assertEqual(
            "Help support leads prepare a case summary before escalation.", island["detail"]
        )
        self.assertEqual(
            "Ask two support leads to review a sample.", island["next_move"]
        )
        self.assertEqual(
            "Potential AI formulation: draft a cited case summary for lead review.",
            island["ai_formulation"],
        )

        restored = Workspace.from_dict(workspace.to_dict())
        self.assertEqual(island, restored.current_iteration.opportunities[0])

    def test_island_core_and_evaluation_values_are_saved_on_the_island(self):
        workspace = self._workspace()
        workspace.add_opportunity(
            {
                "id": "case-summary",
                "title": "Case summary assistant",
                "summary": "A direct team-created Island.",
            }
        )

        island = workspace.update_opportunity(
            "case-summary",
            detail="Help escalation leads prepare accountable case summaries.",
            evaluation={
                "value": {"score": 4, "rationale": "Escalation leads lose time gathering context."},
                "readiness": {"score": 3, "rationale": "Ticket data is available but fragmented."},
                "effort": {"score": 2, "rationale": "Start with one support queue."},
            },
        )

        self.assertEqual(
            4, island["evaluation"]["value"]["score"]
        )
        self.assertEqual(
            "Ticket data is available but fragmented.",
            island["evaluation"]["readiness"]["rationale"],
        )
        restored = Workspace.from_dict(workspace.to_dict())
        self.assertEqual(island["evaluation"], restored.current_iteration.opportunities[0]["evaluation"])

    def test_chart_room_persists_team_hypothesis_evidence_unknowns_and_optional_details(self):
        workspace = self._workspace()
        workspace.add_opportunity({"id": "case-summary", "title": "Case summary assistant"})

        island = workspace.update_opportunity(
            "case-summary",
            chart_room={
                "workflow_problem": "Escalation leads gather account context from three systems.",
                "ai_change": "Draft a cited case summary for lead review.",
                "outcome": "Leads begin escalation with a reliable shared brief.",
                "evidence": "Two leads described the repeated context-gathering work.",
                "unknowns": "We have not measured preparation time yet.",
                "readiness_data": "Confirm read access and source consistency.",
                "safeguards_risk": "A lead verifies every cited source before sending.",
                "ownership_adoption": "Support operations owns the review routine.",
                "learning_action": "Measure a week of current preparation time.",
            },
        )

        self.assertEqual(
            "Draft a cited case summary for lead review.",
            island["chart_room"]["ai_change"],
        )
        self.assertNotIn("ai_suggestion", island["chart_room"])
        restored = Workspace.from_dict(workspace.to_dict())
        self.assertEqual(island["chart_room"], restored.current_iteration.opportunities[0]["chart_room"])

    def test_chart_room_rejects_unknown_or_non_text_team_fields(self):
        workspace = self._workspace()
        workspace.add_opportunity({"id": "case-summary", "title": "Case summary assistant"})

        with self.assertRaisesRegex(ValueError, "Unknown Chart Room field"):
            workspace.update_opportunity(
                "case-summary", chart_room={"ai_suggestion": "Pretend this is evidence."}
            )
        with self.assertRaisesRegex(ValueError, "must be text"):
            workspace.update_opportunity(
                "case-summary", chart_room={"evidence": ["not a team note"]}
            )

    def test_team_member_can_capture_a_scouting_note_before_it_is_an_island(self):
        workspace = self._workspace()

        note = workspace.add_scouting_note(
            title="A rough thought from the support floor",
            body="Could AI help spot patterns in escalations before the weekly review?",
            author="Mika",
        )

        self.assertEqual("Mika", note["author"])
        self.assertIsNone(note["transferred_to_island_id"])
        self.assertEqual([], workspace.current_iteration.opportunities)

        restored = Workspace.from_dict(workspace.to_dict())
        self.assertEqual(note, restored.current_iteration.scouting_notes[0])

    def test_explicit_transfer_creates_an_island_and_preserves_note_as_provenance(self):
        workspace = self._workspace()
        note = workspace.add_scouting_note(
            title="Escalation signals",
            body="Could AI help spot patterns in escalations before the weekly review?",
            author="Mika",
        )

        island = workspace.transfer_scouting_note(
            note_id=note["id"], island_title="Escalation signal triage"
        )

        self.assertEqual("Escalation signal triage", island["title"])
        self.assertEqual(note["id"], island["scouting_note"]["id"])
        self.assertEqual("Mika", island["scouting_note"]["author"])
        self.assertEqual(note["body"], island["scouting_note"]["body"])
        self.assertNotIn("evidence", island.get("chart_room", {}))
        self.assertEqual(island["id"], workspace.current_iteration.scouting_notes[0]["transferred_to_island_id"])

        restored = Workspace.from_dict(workspace.to_dict())
        self.assertEqual(note["body"], restored.current_iteration.opportunities[0]["scouting_note"]["body"])

    def test_scouting_note_transfer_rejects_blank_fields_and_a_second_transfer(self):
        workspace = self._workspace()
        with self.assertRaisesRegex(ValueError, "Scouting note needs"):
            workspace.add_scouting_note(title="", body="A thought", author="Mika")

        note = workspace.add_scouting_note(title="A thought", body="Explore this", author="Mika")
        with self.assertRaisesRegex(ValueError, "Island needs a name"):
            workspace.transfer_scouting_note(note_id=note["id"], island_title=" ")

        workspace.transfer_scouting_note(note_id=note["id"], island_title="A real Island")
        with self.assertRaisesRegex(ValueError, "already been transferred"):
            workspace.transfer_scouting_note(note_id=note["id"], island_title="Another Island")

    def test_island_evaluation_rejects_a_score_without_a_team_rationale(self):
        workspace = self._workspace()
        workspace.add_opportunity(
            {"id": "case-summary", "title": "Case summary assistant"}
        )

        with self.assertRaisesRegex(ValueError, "rationale"):
            workspace.update_opportunity(
                "case-summary",
                evaluation={"value": {"score": 4, "rationale": " "}},
            )

    def test_island_evaluation_rejects_values_the_map_cannot_display(self):
        workspace = self._workspace()
        workspace.add_opportunity(
            {"id": "case-summary", "title": "Case summary assistant"}
        )

        with self.assertRaisesRegex(ValueError, "Unknown Island evaluation"):
            workspace.update_opportunity(
                "case-summary",
                evaluation={"risk": {"score": 2, "rationale": "Needs review."}},
            )

    def test_living_map_still_allows_island_changes_after_legacy_decision_data(self):
        workspace = self._workspace()
        workspace.current_iteration.next_opportunity_decision = {"opportunity_id": "legacy"}

        island = workspace.add_opportunity(
            {"id": "case-summary", "title": "Case summary assistant"}
        )
        updated = workspace.update_opportunity(
            island["id"], detail="The Map remains editable after an Expedition snapshot."
        )

        self.assertEqual(
            "The Map remains editable after an Expedition snapshot.", updated["detail"]
        )

    def test_legacy_per_iteration_north_star_lifts_to_workspace_level_ai_strategy(self):
        workspace = Workspace.from_dict(
            {
                "iterations": [
                    {
                        "number": 1,
                        "decision_frame": {"goal": "Old focus"},
                        "opportunities": [],
                        "dimensions": [],
                        "assessments": {},
                        "north_star": "Legacy strategy",
                    }
                ]
            }
        )

        self.assertEqual("Legacy strategy", workspace.ai_strategy)
        self.assertIsNone(workspace.ai_vision)
        self.assertNotIn("north_star", workspace.to_dict()["iterations"][0])

    def test_legacy_decision_frame_strategy_lifts_to_workspace_level_ai_strategy(self):
        workspace = Workspace.from_dict(
            {
                "iterations": [
                    {
                        "number": 1,
                        "decision_frame": {"strategy": "An older single strategy string."},
                        "opportunities": [],
                        "dimensions": [],
                        "assessments": {},
                    }
                ]
            }
        )

        self.assertEqual("An older single strategy string.", workspace.ai_strategy)
        self.assertIsNone(workspace.ai_vision)

    def test_workspace_level_north_star_is_not_overridden_by_stale_legacy_data(self):
        workspace = Workspace.from_dict(
            {
                "iterations": [
                    {
                        "number": 1,
                        "decision_frame": {"strategy": "A stale per-Iteration strategy."},
                        "opportunities": [],
                        "dimensions": [],
                        "assessments": {},
                    }
                ],
                "ai_vision": "The current Workspace vision.",
                "ai_strategy": "The current Workspace strategy.",
            }
        )

        self.assertEqual("The current Workspace vision.", workspace.ai_vision)
        self.assertEqual("The current Workspace strategy.", workspace.ai_strategy)

    def test_update_north_star_sets_fields_independently_and_rejects_blank_values(self):
        workspace = self._workspace()

        workspace.update_north_star(ai_vision="Why we use AI at all.")
        self.assertEqual("Why we use AI at all.", workspace.ai_vision)
        self.assertEqual("Helpful AI with accountable human decisions.", workspace.ai_strategy)

        workspace.update_north_star(ai_strategy="This quarter's focus.")
        self.assertEqual("Why we use AI at all.", workspace.ai_vision)
        self.assertEqual("This quarter's focus.", workspace.ai_strategy)

        with self.assertRaisesRegex(ValueError, "AI vision"):
            workspace.update_north_star(ai_vision=" ")
        with self.assertRaisesRegex(ValueError, "AI strategy"):
            workspace.update_north_star(ai_strategy=" ")

    def test_north_star_survives_a_new_iteration(self):
        workspace = self._workspace()
        workspace.update_north_star(ai_vision="An enduring purpose.")
        workspace.current_iteration.next_opportunity_decision = {"opportunity_id": "legacy"}

        workspace.start_next_iteration(what_changed="A new planning cycle began.")

        self.assertEqual("An enduring purpose.", workspace.ai_vision)
        self.assertEqual("Helpful AI with accountable human decisions.", workspace.ai_strategy)

    @staticmethod
    def _workspace():
        return Workspace.start(
            map_focus="Improve the support experience.",
            ai_strategy="Helpful AI with accountable human decisions.",
            custom_name="The Amber Current",
            opportunities=[],
            dimensions=[],
            assessments={},
        )


if __name__ == "__main__":
    unittest.main()
