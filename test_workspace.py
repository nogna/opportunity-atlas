import unittest

from workspace import Workspace


class WorkspaceOpportunityMapTests(unittest.TestCase):
    def test_team_can_confirm_an_adjusted_expedition_without_freezing_the_map(self):
        workspace = self._workspace()
        workspace.add_opportunity(
            {"id": "case-summary", "title": "Case summary assistant", "summary": "A rough team note."}
        )
        workspace.add_opportunity(
            {"id": "reply-coach", "title": "Reply coach", "summary": "A rough team note."}
        )

        workspace.update_expedition_evaluations(
            {
                "case-summary": {"impact": 5, "readiness": 2},
                "reply-coach": {"impact": 3, "readiness": 5},
            }
        )
        expedition = workspace.confirm_expedition(
            ordered_island_ids=["case-summary", "reply-coach"]
        )

        self.assertEqual(["reply-coach", "case-summary"], expedition["suggested_order"])
        self.assertEqual(["case-summary", "reply-coach"], expedition["ordered_island_ids"])
        self.assertEqual(
            {"case-summary": {"impact": 5, "readiness": 2}, "reply-coach": {"impact": 3, "readiness": 5}},
            expedition["evaluations"],
        )
        self.assertTrue(workspace.current_iteration.is_editable)

        workspace.update_opportunity("case-summary", detail="The Map keeps evolving.")
        self.assertNotEqual(
            "The Map keeps evolving.",
            expedition["islands"][0].get("detail"),
        )

        restored = Workspace.from_dict(workspace.to_dict())
        self.assertEqual(expedition, restored.current_iteration.expeditions[0])

    def test_first_map_exposes_its_focus_strategy_context_and_generated_atlas_name(self):
        workspace = Workspace.start(
            map_focus="Improve the support experience.",
            decision_frame={"strategy": "Helpful AI with accountable human decisions."},
            opportunities=[],
            dimensions=[],
            assessments={},
        )

        current = workspace.current_iteration

        self.assertEqual("Improve the support experience.", current.map_focus)
        self.assertEqual("Helpful AI with accountable human decisions.", current.north_star)
        self.assertEqual("The Amber Current", current.name)
        self.assertNotIn("north_star", workspace.to_dict()["iterations"][0])
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

    def test_legacy_north_star_is_migrated_to_read_only_strategy_context(self):
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

        self.assertEqual("Legacy strategy", workspace.current_iteration.north_star)
        self.assertNotIn("north_star", workspace.to_dict()["iterations"][0])

    @staticmethod
    def _workspace():
        return Workspace.start(
            map_focus="Improve the support experience.",
            decision_frame={"strategy": "Helpful AI with accountable human decisions."},
            custom_name="The Amber Current",
            opportunities=[],
            dimensions=[],
            assessments={},
        )


if __name__ == "__main__":
    unittest.main()
