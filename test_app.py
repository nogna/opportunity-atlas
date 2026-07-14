import unittest
from copy import deepcopy

import app


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


if __name__ == "__main__":
    unittest.main()
