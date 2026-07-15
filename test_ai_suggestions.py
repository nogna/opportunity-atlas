import unittest

from ai_suggestions import apply_suggested_weights, suggest_for_iteration
from workspace import Workspace


class AiSuggestionTests(unittest.TestCase):
    def setUp(self):
        self.workspace = Workspace.start(decision_frame={"goal": "Improve support quality"}, opportunities=[], dimensions=[{"id": "strategic-alignment", "weight": 1, "direction": "higher"}], assessments={})

    def test_suggestions_are_labelled_and_do_not_persist_a_candidate(self):
        suggestions = suggest_for_iteration(self.workspace.current_iteration)
        self.assertTrue(suggestions["candidates"][0]["assumptions"])
        self.assertTrue(suggestions["candidates"][0]["uncertainties"])
        self.assertEqual([], self.workspace.current_iteration.opportunities)

    def test_team_can_explicitly_apply_weights_after_review(self):
        weights = suggest_for_iteration(self.workspace.current_iteration)["weight_suggestion"]
        apply_suggested_weights(self.workspace.current_iteration, weights)
        self.assertEqual(2, self.workspace.current_iteration.dimensions[0]["weight"])

