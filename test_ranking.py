import unittest

from ranking import DEFAULT_DIMENSION_IDS, default_rubric, rank_opportunities, validate_dimensions, validate_rubric


class RankingBehaviorTests(unittest.TestCase):
    def test_default_rubric_defines_the_agreed_favourable_dimensions_and_anchors(self):
        dimensions = default_rubric()

        self.assertEqual(
            (
                "expected-value",
                "strategic-alignment",
                "data-readiness",
                "delivery-ease",
                "risk-manageability",
                "evidence-confidence",
            ),
            tuple(dimension["id"] for dimension in dimensions),
        )
        self.assertEqual(DEFAULT_DIMENSION_IDS, tuple(dimension["id"] for dimension in dimensions))
        self.assertTrue(all(dimension["direction"] == "higher" for dimension in dimensions))
        self.assertTrue(all(dimension["anchors"].keys() == {1, 3, 5} for dimension in dimensions))
        self.assertTrue(all(dimension["weight"] == 1 for dimension in dimensions))

    def test_inverse_custom_dimension_normalizes_lower_scores_before_weighting(self):
        ranking = rank_opportunities(
            opportunities=[
                {"id": "easy", "title": "Easy delivery"},
                {"id": "hard", "title": "Hard delivery"},
            ],
            dimensions=[{"id": "effort", "name": "Effort", "weight": 1, "direction": "lower", "anchors": {1: "Light", 3: "Moderate", 5: "Major"}}],
            assessments={"easy": {"effort": 1}, "hard": {"effort": 5}},
        )

        self.assertEqual(["easy", "hard"], [entry["opportunity_id"] for entry in ranking])
        self.assertEqual([5.0, 1.0], [entry["score"] for entry in ranking])
        self.assertEqual(5, ranking[0]["contributions"][0]["favourable_score"])

    def test_missing_weighted_assessment_is_unranked_with_the_missing_dimension(self):
        ranking = rank_opportunities(
            opportunities=[{"id": "complete", "title": "Complete"}, {"id": "missing", "title": "Missing"}],
            dimensions=[
                {"id": "value", "name": "Value", "weight": 1, "direction": "higher"},
                {"id": "readiness", "name": "Readiness", "weight": 1, "direction": "higher"},
            ],
            assessments={"complete": {"value": 5, "readiness": 3}, "missing": {"value": 5}},
        )

        self.assertEqual("ranked", ranking[0]["state"])
        self.assertEqual("missing", ranking[1]["opportunity_id"])
        self.assertEqual("unranked", ranking[1]["state"])
        self.assertEqual(["readiness"], ranking[1]["missing_dimension_ids"])
        self.assertIsNone(ranking[1]["rank"])

    def test_zero_weight_dimension_neither_requires_an_assessment_nor_changes_score(self):
        ranking = rank_opportunities(
            opportunities=[{"id": "candidate", "title": "Candidate"}],
            dimensions=[
                {"id": "value", "name": "Value", "weight": 100, "direction": "higher"},
                {"id": "ignored", "name": "Ignored", "weight": 0, "direction": "higher"},
            ],
            assessments={"candidate": {"value": 4}},
        )

        self.assertEqual("ranked", ranking[0]["state"])
        self.assertEqual(4.0, ranking[0]["score"])
        self.assertEqual(["value"], [item["dimension_id"] for item in ranking[0]["contributions"]])

    def test_equal_weighted_scores_share_rank_and_are_sorted_alphabetically(self):
        ranking = rank_opportunities(
            opportunities=[
                {"id": "beta", "title": "Beta"},
                {"id": "alpha", "title": "Alpha"},
                {"id": "gamma", "title": "Gamma"},
            ],
            dimensions=[{"id": "value", "name": "Value", "weight": 1, "direction": "higher"}],
            assessments={"beta": {"value": 5}, "alpha": {"value": 5}, "gamma": {"value": 3}},
        )

        self.assertEqual(["alpha", "beta", "gamma"], [entry["opportunity_id"] for entry in ranking])
        self.assertEqual([1, 1, 3], [entry["rank"] for entry in ranking])

    def test_custom_dimension_needs_direction_and_all_anchors_before_a_nonzero_weight(self):
        with self.assertRaisesRegex(ValueError, "Custom Evaluation dimension 'novelty'.*direction.*1, 3, and 5"):
            validate_dimensions([{"id": "novelty", "name": "Novelty", "weight": 1}])

        validate_dimensions([{"id": "novelty", "name": "Novelty", "weight": 0}])

    def test_rubric_validation_does_not_allow_a_default_dimension_to_be_removed(self):
        incomplete_rubric = default_rubric()[1:]

        with self.assertRaisesRegex(ValueError, "must remain present.*expected-value"):
            validate_rubric(incomplete_rubric)

    def test_assessments_must_have_whole_number_scores_from_one_to_five(self):
        with self.assertRaisesRegex(ValueError, "whole-number score from 1 to 5"):
            rank_opportunities(
                opportunities=[{"id": "candidate", "title": "Candidate"}],
                dimensions=[{"id": "value", "name": "Value", "weight": 1, "direction": "higher"}],
                assessments={"candidate": {"value": 3.5}},
            )

    def test_ranking_explanation_preserves_assessment_rationale_and_confidence(self):
        ranking = rank_opportunities(
            opportunities=[{"id": "candidate", "title": "Candidate"}],
            dimensions=[{"id": "value", "name": "Value", "weight": 1, "direction": "higher"}],
            assessments={
                "candidate": {
                    "value": {
                        "score": 4,
                        "rationale": "Interviewed users report a repeated delay.",
                        "confidence": "medium",
                    }
                }
            },
        )

        contribution = ranking[0]["contributions"][0]
        self.assertEqual("Interviewed users report a repeated delay.", contribution["rationale"])
        self.assertEqual("medium", contribution["confidence"])


if __name__ == "__main__":
    unittest.main()
