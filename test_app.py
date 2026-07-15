import unittest
from copy import deepcopy
from datetime import datetime, timedelta, timezone

import app
from collaboration import Collaboration
from ranking import DEFAULT_DIMENSION_IDS, validate_rubric


def rank(portfolio):
    def score(use_case):
        total_weight = sum(item["weight"] for item in portfolio["dimensions"])
        total = 0
        for dimension in portfolio["dimensions"]:
            raw = use_case["assessments"][dimension["id"]][0]
            total += (6 - raw if dimension["direction"] == "lower" else raw) * dimension["weight"]
        return total / total_weight
    return sorted(portfolio["use_cases"], key=score, reverse=True)


class PortfolioTests(unittest.TestCase):
    def test_default_portfolio_has_explainable_assessments(self):
        portfolio = deepcopy(app.DEFAULT_PORTFOLIO)
        dimensions = {item["id"] for item in portfolio["dimensions"]}
        for use_case in portfolio["use_cases"]:
            self.assertEqual(dimensions, set(use_case["assessments"]))
            self.assertTrue(all(rationale for _, rationale in use_case["assessments"].values()))

    def test_lower_is_better_dimensions_are_normalized(self):
        portfolio = {"dimensions": [{"id": "risk", "weight": 100, "direction": "lower"}], "use_cases": [{"id": "low", "assessments": {"risk": [1, "low"]}}, {"id": "high", "assessments": {"risk": [5, "high"]}}]}
        self.assertEqual("low", rank(portfolio)[0]["id"])

    def test_weight_changes_can_change_the_ranking(self):
        portfolio = {"dimensions": [{"id": "value", "weight": 100, "direction": "higher"}, {"id": "effort", "weight": 0, "direction": "lower"}], "use_cases": [{"id": "ambitious", "assessments": {"value": [5, ""], "effort": [5, ""]}}, {"id": "quick", "assessments": {"value": [3, ""], "effort": [1, ""]}}]}
        self.assertEqual("ambitious", rank(portfolio)[0]["id"])
        portfolio["dimensions"][0]["weight"] = 0
        portfolio["dimensions"][1]["weight"] = 100
        self.assertEqual("quick", rank(portfolio)[0]["id"])

    def test_clean_portfolio_clamps_weights(self):
        portfolio = deepcopy(app.DEFAULT_PORTFOLIO)
        portfolio["dimensions"][0]["weight"] = 999
        self.assertEqual(100, app.clean_portfolio(portfolio)["dimensions"][0]["weight"])

    def test_workspace_seed_uses_complete_default_rubric_and_returns_ranking(self):
        payload = app.workspace_payload(app.DEFAULT_WORKSPACE)

        self.assertEqual(
            set(DEFAULT_DIMENSION_IDS),
            {item["id"] for item in payload["iterations"][-1]["dimensions"]},
        )
        self.assertEqual(
            ["ticket-triage", "renewal-brief"],
            [item["opportunity_id"] for item in payload["ranking"]],
        )

    def test_auto_save_changes_the_editable_decision_frame_after_the_pause(self):
        workspace = app.Workspace.from_dict(app.DEFAULT_WORKSPACE.to_dict())
        collaboration = Collaboration()
        at = datetime(2026, 7, 15, tzinfo=timezone.utc)
        collaboration.start_editing("decision-frame.goal", "Albin", at=at)
        collaboration.record_input(
            "decision-frame.goal", "Albin", "Choose a grounded next workflow.", at=at
        )

        for save in collaboration.due_auto_saves(at=at + timedelta(milliseconds=750)):
            app.apply_auto_save(workspace, save.field_id, save.value)

        self.assertEqual(
            "Choose a grounded next workflow.",
            workspace.current_iteration.decision_frame["goal"],
        )

    def test_default_rubric_cannot_drop_a_default_dimension(self):
        dimensions = app.DEFAULT_WORKSPACE.current_iteration.dimensions[:-1]

        with self.assertRaisesRegex(ValueError, "must remain present"):
            validate_rubric(dimensions)


if __name__ == "__main__":
    unittest.main()
