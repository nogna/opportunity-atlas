import os
import unittest

import app


class ChartRoomEmptinessTests(unittest.TestCase):
    def test_all_blank_or_whitespace_fields_count_as_empty(self):
        self.assertFalse(app._chart_room_has_content({}))
        self.assertFalse(app._chart_room_has_content({"workflow_problem": "   "}))

    def test_any_non_blank_field_counts_as_non_empty(self):
        self.assertTrue(app._chart_room_has_content({"outcome": "Faster reviews."}))


class EmptyIslandChallengeTests(unittest.TestCase):
    def test_returns_one_of_the_curated_local_lines_without_a_network_call(self):
        result = app.local_empty_island_challenge()
        self.assertEqual("local", result["source"])
        self.assertTrue(result["empty"])
        self.assertIn(result["message"], app.EMPTY_ISLAND_CHALLENGE_LINES)


class ChallengeResponseParsingTests(unittest.TestCase):
    def test_parses_three_labelled_sections_into_bullet_lists(self):
        text = (
            "MISSING:\n- No evidence recorded\n- No named owner\n"
            "CHALLENGE:\n- Outcome claims speed but Evidence is empty\n"
            "PITFALL:\n- No baseline means you can't prove impact later\n"
        )
        parsed = app._parse_challenge_response(text)
        self.assertEqual(["No evidence recorded", "No named owner"], parsed["missing_or_thin"])
        self.assertEqual(["Outcome claims speed but Evidence is empty"], parsed["worth_challenging"])
        self.assertEqual(["No baseline means you can't prove impact later"], parsed["common_pitfall"])

    def test_missing_sections_return_empty_lists_rather_than_raising(self):
        parsed = app._parse_challenge_response("MISSING:\n- Nothing filled in\n")
        self.assertEqual(["Nothing filled in"], parsed["missing_or_thin"])
        self.assertEqual([], parsed["worth_challenging"])
        self.assertEqual([], parsed["common_pitfall"])


class OpenAiChallengeUnavailableTests(unittest.TestCase):
    def test_raises_a_clean_unavailable_error_when_no_api_key_is_set(self):
        original = os.environ.pop("OPENAI_API_KEY", None)
        try:
            with self.assertRaisesRegex(ValueError, "AI review is unavailable right now."):
                app.openai_challenge_island({"workflow_problem": "x"}, {}, {})
        finally:
            if original is not None:
                os.environ["OPENAI_API_KEY"] = original


if __name__ == "__main__":
    unittest.main()
