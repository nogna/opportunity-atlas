import unittest

from workspace import Workspace


class WorkspaceBehaviorTests(unittest.TestCase):
    def test_setting_the_current_draft_preserves_the_decision_snapshot(self):
        workspace = Workspace.start(
            decision_frame={"goal": "Improve support quality"},
            opportunities=[{"id": "triage", "title": "Ticket triage"}],
            dimensions=[{"id": "value", "weight": 100, "direction": "higher"}],
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
        self.assertEqual("triage", completed.decision_snapshot["ranking"][0]["opportunity_id"])
        self.assertEqual(5.0, completed.decision_snapshot["ranking"][0]["score"])
        self.assertEqual([{"id": "value", "weight": 100, "direction": "higher"}], completed.decision_snapshot["dimensions"])

    def test_unranked_shortlist_opportunity_needs_a_separate_override_rationale(self):
        workspace = Workspace.start(
            decision_frame={"goal": "Improve support quality"},
            opportunities=[{"id": "triage", "title": "Ticket triage"}],
            dimensions=[{"id": "value", "weight": 100, "direction": "higher"}],
            assessments={"triage": {}},
            shortlist=["triage"],
        )

        with self.assertRaisesRegex(ValueError, "override rationale"):
            workspace.set_current_iteration(
                next_opportunity_id="triage", rationale="It is strategically urgent.", recorded_by="Albin"
            )

        completed = workspace.set_current_iteration(
            next_opportunity_id="triage",
            rationale="It is strategically urgent.",
            unranked_override_rationale="Evidence collection starts with the pilot.",
            recorded_by="Albin",
        )
        self.assertEqual(
            "Evidence collection starts with the pilot.",
            completed.next_opportunity_decision["unranked_override_rationale"],
        )

    def test_new_iteration_copies_a_set_iteration_and_preserves_its_history(self):
        workspace = Workspace.start(
            decision_frame={"goal": "Improve support quality"},
            opportunities=[{"id": "triage", "title": "Ticket triage"}],
            dimensions=[{"id": "value", "weight": 100, "direction": "higher"}],
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
            dimensions=[{"id": "value", "weight": 100, "direction": "higher"}],
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
            dimensions=[{"id": "value", "weight": 100, "direction": "higher"}],
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

    def test_carry_forward_review_identifies_inherited_opportunities_including_previously_set_aside_ones(self):
        workspace = self._completed_workspace(
            opportunities=[
                {"id": "triage", "title": "Ticket triage"},
                {
                    "id": "summaries",
                    "title": "Case summaries",
                    "not_pursuing_decision": {"rationale": "Too little demand"},
                },
            ],
            assessments={"triage": {"value": 5}, "summaries": {"value": 2}},
            shortlist=["triage"],
        )
        workspace.start_next_iteration(what_changed="A new support strategy.")

        review = workspace.review_inherited_opportunities()

        self.assertEqual(["summaries", "triage"], [item["opportunity"]["id"] for item in review])
        self.assertTrue(review[0]["previously_not_pursuing"])
        self.assertFalse(review[0]["archived"])
        self.assertFalse(review[1]["previously_not_pursuing"])
        self.assertEqual(1, review[1]["source_iteration_number"])

    def test_archiving_an_inherited_opportunity_records_its_reason_and_source_summary(self):
        workspace = self._completed_workspace(
            opportunities=[
                {
                    "id": "triage",
                    "title": "Ticket triage",
                    "target_user": "Support agents",
                    "affected_workflow": "Ticket routing",
                }
            ],
            assessments={"triage": {"value": 5}},
            shortlist=["triage"],
        )
        workspace.start_next_iteration(what_changed="The workflow is now automated elsewhere.")

        archive = workspace.archive_inherited_opportunity(
            opportunity_id="triage",
            reason="The new platform already handles routing.",
        )

        self.assertEqual([], workspace.current_iteration.opportunities)
        self.assertEqual("The new platform already handles routing.", archive["reason"])
        self.assertEqual(1, archive["source_iteration_number"])
        self.assertEqual(
            {"id": "triage", "title": "Ticket triage", "target_user": "Support agents", "affected_workflow": "Ticket routing"},
            archive["source_opportunity_summary"],
        )
        self.assertTrue(archive["archived_at"].endswith("Z"))

    def test_an_archived_inherited_opportunity_can_be_restored_while_the_iteration_is_a_draft(self):
        workspace = self._completed_workspace()
        workspace.start_next_iteration(what_changed="New evidence arrived.")
        workspace.archive_inherited_opportunity(
            opportunity_id="triage",
            reason="We thought the data was unavailable.",
        )

        restored = workspace.restore_inherited_opportunity("triage")

        self.assertEqual("triage", restored["id"])
        self.assertEqual(["triage"], [item["id"] for item in workspace.current_iteration.opportunities])
        archive = workspace.current_iteration.archive_decisions[0]
        self.assertTrue(archive["restored_at"].endswith("Z"))
        self.assertEqual("triage", workspace.review_inherited_opportunities()[0]["opportunity"]["id"])
        self.assertFalse(workspace.review_inherited_opportunities()[0]["archived"])

    def test_archive_decisions_persist_and_cannot_change_after_the_iteration_is_set(self):
        workspace = self._completed_workspace(
            opportunities=[
                {"id": "triage", "title": "Ticket triage"},
                {"id": "summaries", "title": "Case summaries"},
            ],
            assessments={"triage": {"value": 5}, "summaries": {"value": 4}},
            shortlist=["triage", "summaries"],
        )
        workspace.start_next_iteration(what_changed="New evidence arrived.")
        workspace.archive_inherited_opportunity(
            opportunity_id="triage",
            reason="The workflow has been retired.",
        )

        restored = Workspace.from_dict(workspace.to_dict())

        archive = restored.current_iteration.archive_decisions[0]
        self.assertEqual("The workflow has been retired.", archive["reason"])
        self.assertEqual({"id": "triage", "title": "Ticket triage"}, archive["source_opportunity_summary"])
        restored.set_current_iteration(
            next_opportunity_id="summaries",
            rationale="An archive does not erase the history of the decision.",
            recorded_by="Albin",
        )
        with self.assertRaisesRegex(ValueError, "set Iteration"):
            restored.restore_inherited_opportunity("triage")

    @staticmethod
    def _completed_workspace(*, opportunities=None, assessments=None, shortlist=None):
        workspace = Workspace.start(
            decision_frame={"goal": "Improve support quality"},
            opportunities=opportunities or [{"id": "triage", "title": "Ticket triage"}],
            dimensions=[{"id": "value", "weight": 100, "direction": "higher"}],
            assessments=assessments or {"triage": {"value": 5}},
            shortlist=shortlist or ["triage"],
        )
        workspace.set_current_iteration(
            next_opportunity_id="triage",
            rationale="It addresses the highest-volume pain first.",
            recorded_by="Albin",
        )
        return workspace


if __name__ == "__main__":
    unittest.main()
