"""Acceptance tests for an Expedition made from Island Charters."""

import unittest

from workspace import Workspace


def workspace():
    return Workspace.start(
        decision_frame={"strategy": "Help teams make accountable AI choices."},
        custom_name="Customer Support",
        opportunities=[
            {
                "id": "triage",
                "title": "Support signal triage",
                "summary": "Spot repeated support issues.",
                "evaluation": {"value": {"score": 5, "rationale": "High volume."}},
            },
            {"id": "renewal", "title": "Renewal brief", "summary": "Prepare renewal calls."},
        ],
        dimensions=[],
        assessments={},
    )


class ExpeditionTests(unittest.TestCase):
    def test_confirming_charters_creates_an_active_expedition_with_an_immutable_map_snapshot(self):
        atlas = workspace()

        expedition = atlas.confirm_expedition(
            charters=[
                {
                    "island_id": "triage",
                    "next_learning_action": "Review two weeks of alert candidates with support leads.",
                    "participants": "Support leads",
                    "intended_outcome": "A trusted alert baseline",
                    "decision_evidence": "A lead accepts or rejects each candidate.",
                }
            ]
        )

        self.assertEqual("active", expedition["status"])
        self.assertEqual(["triage"], expedition["selected_island_ids"])
        self.assertEqual("Customer Support", expedition["map_snapshot"]["name"])
        self.assertEqual("Support signal triage", expedition["map_snapshot"]["islands"][0]["title"])
        self.assertEqual("Support leads", expedition["charters"][0]["participants"])

        atlas.update_opportunity("triage", title="Changed on the living Map")

        self.assertEqual("Support signal triage", expedition["map_snapshot"]["islands"][0]["title"])
        self.assertEqual("Changed on the living Map", atlas.current_iteration.opportunities[0]["title"])

    def test_a_new_expedition_makes_the_previous_expedition_past(self):
        atlas = workspace()
        first = atlas.confirm_expedition(
            charters=[{"island_id": "triage", "next_learning_action": "Check alert candidates."}]
        )
        second = atlas.confirm_expedition(
            charters=[{"island_id": "renewal", "next_learning_action": "Interview two account managers."}]
        )

        self.assertEqual("past", first["status"])
        self.assertEqual("active", second["status"])
        self.assertEqual(second["id"], atlas.current_expedition["id"])

    def test_each_selected_island_needs_its_own_next_learning_action(self):
        atlas = workspace()

        with self.assertRaisesRegex(ValueError, "next learning action"):
            atlas.confirm_expedition(
                charters=[{"island_id": "triage", "next_learning_action": " "}]
            )

        with self.assertRaisesRegex(ValueError, "does not belong"):
            atlas.confirm_expedition(
                charters=[{"island_id": "missing", "next_learning_action": "Check it."}]
            )


if __name__ == "__main__":
    unittest.main()
