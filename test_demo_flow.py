"""Acceptance contract for the no-setup judge demo Workspace."""

import unittest

import app


class SeededDemoFlowTests(unittest.TestCase):
    def test_seeded_workspace_opens_a_fresh_map_for_exploration(self):
        """A judge starts with one living Map, not misleading reassessment history."""
        workspace = app.Workspace.from_dict(app.DEFAULT_WORKSPACE.to_dict())

        self.assertEqual(1, len(workspace.iterations))
        (current,) = workspace.iterations

        self.assertTrue(current.is_editable)
        self.assertIsNone(current.source_iteration_number)
        self.assertIsNone(current.next_opportunity_decision)
        self.assertEqual("The Amber Current", current.name)
        self.assertTrue(current.map_focus)
        self.assertTrue(current.north_star)
        self.assertEqual([], current.dimensions)
        self.assertEqual({}, current.assessments)
        self.assertEqual([], current.shortlist)
        self.assertEqual(
            {
                "ticket-triage",
                "renewal-brief",
            },
            {item["id"] for item in current.opportunities},
        )


if __name__ == "__main__":
    unittest.main()
