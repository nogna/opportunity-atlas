import unittest

from workspace import Workspace


class WorkspaceOpportunityMapTests(unittest.TestCase):
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
