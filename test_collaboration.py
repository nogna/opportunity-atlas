import unittest
from datetime import datetime, timedelta, timezone

from collaboration import (
    BROWSER_DISPLAY_NAME_KEY,
    Collaboration,
    FieldLockedError,
    choose_display_name,
)


NOW = datetime(2026, 7, 15, 9, 0, tzinfo=timezone.utc)


class CollaborationBehaviorTests(unittest.TestCase):
    def test_a_team_member_chooses_a_non_empty_display_name_for_browser_storage(self):
        self.assertEqual("Albin", choose_display_name("  Albin  "))
        self.assertEqual("opportunity-atlas.display-name", BROWSER_DISPLAY_NAME_KEY)
        with self.assertRaisesRegex(ValueError, "display name"):
            choose_display_name("   ")

    def test_editing_an_unlocked_field_makes_the_holder_visible_and_blocks_others(self):
        collaboration = Collaboration()
        lock = collaboration.start_editing(
            field_id="opportunity:ticket-triage:title",
            display_name="Albin",
            at=NOW,
        )

        self.assertEqual("Albin", lock.holder)
        self.assertEqual(lock, collaboration.lock_for(lock.field_id, at=NOW))
        with self.assertRaises(FieldLockedError) as raised:
            collaboration.start_editing(lock.field_id, "Sam", at=NOW)
        self.assertEqual("Albin", raised.exception.holder)

    def test_latest_field_value_auto_saves_only_after_a_750ms_pause(self):
        collaboration = Collaboration()
        field_id = "workspace:decision-frame:goal"
        collaboration.start_editing(field_id, "Albin", at=NOW)
        collaboration.record_input(field_id, "Albin", "Improve support", at=NOW)
        collaboration.record_input(
            field_id,
            "Albin",
            "Improve support quality",
            at=NOW + timedelta(milliseconds=400),
        )

        self.assertEqual([], collaboration.due_auto_saves(at=NOW + timedelta(milliseconds=1149)))
        self.assertEqual(
            [(field_id, "Improve support quality")],
            [(save.field_id, save.value) for save in collaboration.due_auto_saves(at=NOW + timedelta(milliseconds=1150))],
        )

    def test_field_lock_expires_after_two_minutes_of_inactivity(self):
        collaboration = Collaboration()
        field_id = "opportunity:ticket-triage:expected-outcome"
        collaboration.start_editing(field_id, "Albin", at=NOW)
        collaboration.record_input(field_id, "Albin", "Faster detection", at=NOW)

        self.assertIsNotNone(collaboration.lock_for(field_id, at=NOW + timedelta(seconds=119)))
        self.assertIsNone(collaboration.lock_for(field_id, at=NOW + timedelta(seconds=120)))
        self.assertEqual("Sam", collaboration.start_editing(field_id, "Sam", at=NOW + timedelta(seconds=120)).holder)


if __name__ == "__main__":
    unittest.main()
