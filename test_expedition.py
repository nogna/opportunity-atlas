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

    def test_map_changes_compare_the_living_map_with_an_expedition_snapshot(self):
        atlas = workspace()
        expedition = atlas.confirm_expedition(
            charters=[{"island_id": "triage", "next_learning_action": "Check alert candidates."}]
        )

        atlas.update_opportunity("triage", title="Support pattern triage")
        atlas.archive_island(
            opportunity_id="renewal", reason="Renewal preparation no longer belongs to this team’s Map."
        )
        atlas.add_opportunity(
            {"id": "handoff", "title": "Shift handoff brief", "summary": "Prepare a handoff."}
        )

        changes = atlas.map_changes_for_expedition(expedition["id"])

        self.assertEqual(["handoff"], [change["island"]["id"] for change in changes["added"]])
        self.assertEqual("triage", changes["changed"][0]["before"]["id"])
        self.assertEqual("Support signal triage", changes["changed"][0]["before"]["title"])
        self.assertEqual("Support pattern triage", changes["changed"][0]["after"]["title"])
        self.assertEqual(["renewal"], [change["island"]["id"] for change in changes["archived"]])
        self.assertEqual(
            "Renewal preparation no longer belongs to this team’s Map.",
            changes["archived"][0]["reason"],
        )
        self.assertTrue(changes["has_changes"])

    def test_map_changes_keep_new_scouting_notes_distinct_from_new_islands(self):
        atlas = workspace()
        expedition = atlas.confirm_expedition(
            charters=[{"island_id": "triage", "next_learning_action": "Check alert candidates."}]
        )

        atlas.add_scouting_note(
            title="Repeated escalation theme",
            body="Several account managers mentioned the same escalation pattern.",
            author="Mika",
        )
        atlas.add_opportunity(
            {"id": "handoff", "title": "Shift handoff brief", "summary": "Prepare a handoff."}
        )

        changes = atlas.map_changes_for_expedition(expedition["id"])

        self.assertEqual(["handoff"], [item["island"]["id"] for item in changes["added"]])
        self.assertEqual(
            ["Repeated escalation theme"],
            [item["title"] for item in changes["added_scouting_notes"]],
        )

    def test_map_changes_only_list_new_untransferred_scouting_notes(self):
        atlas = workspace()
        expedition = atlas.confirm_expedition(
            charters=[{"island_id": "triage", "next_learning_action": "Check alert candidates."}]
        )
        note = atlas.add_scouting_note(
            title="Potential handoff gap",
            body="A possible handoff issue needs a closer look.",
            author="Mika",
        )

        island = atlas.transfer_scouting_note(note_id=note["id"], island_title="Handoff gap finder")
        changes = atlas.map_changes_for_expedition(expedition["id"])

        self.assertEqual([island["id"]], [item["island"]["id"] for item in changes["added"]])
        self.assertEqual([], changes["added_scouting_notes"])

    def test_legacy_snapshot_does_not_reclassify_existing_scouting_notes_as_new(self):
        atlas = workspace()
        note = atlas.add_scouting_note(
            title="Existing signal",
            body="This was already on the Map before confirmation.",
            author="Mika",
        )
        expedition = atlas.confirm_expedition(
            charters=[{"island_id": "triage", "next_learning_action": "Check alert candidates."}]
        )
        expedition["map_snapshot"].pop("scouting_notes")

        changes = atlas.map_changes_for_expedition(expedition["id"])

        self.assertEqual([], changes["added_scouting_notes"])
        self.assertIsNone(note["transferred_to_island_id"])

    def test_map_changes_notices_when_current_unselected_island_newly_overtakes_selected_one(self):
        atlas = workspace()
        expedition = atlas.confirm_expedition(
            charters=[{"island_id": "triage", "next_learning_action": "Check alert candidates."}]
        )

        atlas.update_opportunity(
            "renewal",
            evaluation={"value": {"score": 5, "rationale": "A larger opportunity than first understood."}},
        )
        atlas.update_opportunity(
            "triage",
            evaluation={"value": {"score": 2, "rationale": "The expected benefit is lower than expected."}},
        )

        changes = atlas.map_changes_for_expedition(expedition["id"])

        self.assertEqual(
            [
                {
                    "island_id": "renewal",
                    "selected_island_id": "triage",
                    "island_score": 5.0,
                    "selected_island_score": 2.0,
                }
            ],
            changes["newly_stronger_unselected"],
        )

    def test_map_changes_keep_previous_and_current_evaluation_values_for_changed_islands(self):
        atlas = workspace()
        expedition = atlas.confirm_expedition(
            charters=[{"island_id": "triage", "next_learning_action": "Check alert candidates."}]
        )

        atlas.update_opportunity(
            "triage",
            evaluation={"value": {"score": 3, "rationale": "The expected benefit is still being tested."}},
        )

        (change,) = atlas.map_changes_for_expedition(expedition["id"])["changed"]

        self.assertEqual(5, change["before"]["evaluation"]["value"]["score"])
        self.assertEqual(3, change["after"]["evaluation"]["value"]["score"])
        self.assertEqual(
            [{"id": "value", "before": 5, "after": 3}],
            change["value_changes"],
        )

    def test_restored_island_is_no_longer_shown_as_archived_since_the_snapshot(self):
        atlas = workspace()
        expedition = atlas.confirm_expedition(
            charters=[{"island_id": "triage", "next_learning_action": "Check alert candidates."}]
        )
        atlas.archive_island(opportunity_id="renewal", reason="Temporarily out of scope.")
        atlas.restore_archived_island("renewal")

        changes = atlas.map_changes_for_expedition(expedition["id"])

        self.assertEqual([], changes["archived"])

    def test_map_changes_are_empty_when_the_living_map_still_matches_its_snapshot(self):
        atlas = workspace()
        expedition = atlas.confirm_expedition(
            charters=[{"island_id": "triage", "next_learning_action": "Check alert candidates."}]
        )

        changes = atlas.map_changes_for_expedition(expedition["id"])

        self.assertEqual(
            {
                "added": [],
                "added_scouting_notes": [],
                "changed": [],
                "archived": [],
                "newly_stronger_unselected": [],
                "has_changes": False,
            },
            changes,
        )

    def test_map_changes_reject_an_expedition_from_another_map(self):
        atlas = workspace()

        with self.assertRaisesRegex(ValueError, "does not belong"):
            atlas.map_changes_for_expedition("expedition-not-on-this-map")

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
