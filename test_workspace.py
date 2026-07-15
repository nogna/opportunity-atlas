import unittest

from workspace import Workspace


class WorkspaceBehaviorTests(unittest.TestCase):
    def test_setting_the_current_draft_preserves_the_decision_snapshot(self):
        workspace = Workspace.start(
            decision_frame={"goal": "Improve support quality"},
            opportunities=[{"id": "triage", "title": "Ticket triage"}],
            dimensions=[{"id": "value", "weight": 100}],
            assessments={"triage": {"value": 5}},
            shortlist=["triage"],
        )

        completed = workspace.set_current_iteration(
            next_opportunity_id="triage",
            rationale="It addresses the highest-volume pain first.",
            recorded_by="Albin",
        )

        self.assertTrue(completed.is_set)
        self.assertFalse(completed.is_editable)
        self.assertEqual("triage", completed.next_opportunity_decision["opportunity_id"])
        self.assertEqual("Albin", completed.next_opportunity_decision["recorded_by"])
        self.assertEqual([{"opportunity_id": "triage", "score": 5.0}], completed.decision_snapshot["ranking"])
        self.assertEqual([{"id": "value", "weight": 100}], completed.decision_snapshot["dimensions"])

    def test_new_iteration_copies_a_set_iteration_and_preserves_its_history(self):
        workspace = Workspace.start(
            decision_frame={"goal": "Improve support quality"},
            opportunities=[{"id": "triage", "title": "Ticket triage"}],
            dimensions=[{"id": "value", "weight": 100}],
            assessments={"triage": {"value": 5}},
            shortlist=["triage"],
        )
        completed = workspace.set_current_iteration(
            next_opportunity_id="triage",
            rationale="It addresses the highest-volume pain first.",
            recorded_by="Albin",
        )

        next_draft = workspace.start_next_iteration(
            what_changed="Customer data can now be used for this workflow.",
            custom_name="Data-ready reassessment",
        )
        next_draft.dimensions[0]["weight"] = 60

        self.assertTrue(completed.is_set)
        self.assertFalse(completed.is_editable)
        self.assertTrue(next_draft.is_editable)
        self.assertEqual(2, next_draft.number)
        self.assertEqual(1, next_draft.source_iteration_number)
        self.assertEqual("Customer data can now be used for this workflow.", next_draft.what_changed)
        self.assertEqual("Data-ready reassessment", next_draft.name)
        self.assertEqual(100, completed.dimensions[0]["weight"])

    def test_custom_name_can_change_only_while_iteration_is_a_draft(self):
        workspace = Workspace.start(
            decision_frame={"goal": "Improve support quality"},
            opportunities=[{"id": "triage", "title": "Ticket triage"}],
            dimensions=[{"id": "value", "weight": 100}],
            assessments={"triage": {"value": 5}},
            shortlist=["triage"],
        )

        workspace.rename_current_iteration("Support quality exploration")
        workspace.set_current_iteration(
            next_opportunity_id="triage",
            rationale="It addresses the highest-volume pain first.",
            recorded_by="Albin",
        )

        self.assertEqual("Support quality exploration", workspace.current_iteration.name)
        with self.assertRaisesRegex(ValueError, "set Iteration"):
            workspace.rename_current_iteration("A different name")

    def test_serialized_workspace_preserves_current_draft_and_set_history(self):
        workspace = Workspace.start(
            decision_frame={"goal": "Improve support quality"},
            opportunities=[{"id": "triage", "title": "Ticket triage"}],
            dimensions=[{"id": "value", "weight": 100}],
            assessments={"triage": {"value": 5}},
            shortlist=["triage"],
        )
        workspace.set_current_iteration(
            next_opportunity_id="triage",
            rationale="It addresses the highest-volume pain first.",
            recorded_by="Albin",
        )
        workspace.start_next_iteration(
            what_changed="New evidence arrived.",
        )

        restored = Workspace.from_dict(workspace.to_dict())

        self.assertEqual(2, len(restored.iterations))
        self.assertTrue(restored.iterations[0].is_set)
        self.assertTrue(restored.current_iteration.is_editable)
        self.assertEqual("New evidence arrived.", restored.current_iteration.what_changed)


if __name__ == "__main__":
    unittest.main()
