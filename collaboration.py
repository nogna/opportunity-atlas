"""Collaboration rules for field-level editing in the current Workspace draft."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta


BROWSER_DISPLAY_NAME_KEY = "opportunity-atlas.display-name"
AUTOSAVE_DEBOUNCE = timedelta(milliseconds=750)
LOCK_INACTIVITY_TIMEOUT = timedelta(minutes=2)


class FieldLockedError(ValueError):
    """Raised when another Team member already owns a field-level edit lock."""

    def __init__(self, field_id: str, holder: str):
        self.field_id = field_id
        self.holder = holder
        super().__init__(f"{holder} is editing {field_id}.")


class FieldNotLockedByMemberError(ValueError):
    """Raised when someone writes a field without owning its edit lock."""


@dataclass(frozen=True)
class FieldLock:
    field_id: str
    holder: str
    acquired_at: datetime
    last_activity_at: datetime


@dataclass(frozen=True)
class AutoSave:
    field_id: str
    value: object
    saved_by: str
    saved_at: datetime


@dataclass
class _EditingField:
    lock: FieldLock
    pending_value: object | None = None
    changed_at: datetime | None = None


def choose_display_name(value: str) -> str:
    """Return the display name that the browser should persist for this Team member."""
    if not isinstance(value, str) or not (display_name := value.strip()):
        raise ValueError("Choose a display name before editing the Workspace.")
    return display_name


class Collaboration:
    """Coordinates draft-field editing without merging simultaneous text changes."""

    def __init__(self) -> None:
        self._editing_fields: dict[str, _EditingField] = {}

    def start_editing(self, field_id: str, display_name: str, *, at: datetime) -> FieldLock:
        """Acquire a field-level lock, or reveal the Team member currently holding it."""
        field_id = self._field_id(field_id)
        display_name = choose_display_name(display_name)
        self._expire_inactive_locks(at)
        editing = self._editing_fields.get(field_id)
        if editing and editing.lock.holder != display_name:
            raise FieldLockedError(field_id, editing.lock.holder)
        if editing:
            return editing.lock

        lock = FieldLock(field_id, display_name, acquired_at=at, last_activity_at=at)
        self._editing_fields[field_id] = _EditingField(lock=lock)
        return lock

    def record_input(self, field_id: str, display_name: str, value: object, *, at: datetime) -> FieldLock:
        """Record a keystroke-level update, retaining only the latest value for auto-save."""
        field_id = self._field_id(field_id)
        display_name = choose_display_name(display_name)
        self._expire_inactive_locks(at)
        editing = self._editing_fields.get(field_id)
        if not editing or editing.lock.holder != display_name:
            raise FieldNotLockedByMemberError("Start editing the field before changing it.")

        editing.lock = FieldLock(
            field_id=field_id,
            holder=display_name,
            acquired_at=editing.lock.acquired_at,
            last_activity_at=at,
        )
        editing.pending_value = value
        editing.changed_at = at
        return editing.lock

    def due_auto_saves(self, *, at: datetime) -> list[AutoSave]:
        """Return the latest values whose 750 ms debounce window has elapsed."""
        saves: list[AutoSave] = []
        for editing in self._editing_fields.values():
            if editing.changed_at is None or at - editing.changed_at < AUTOSAVE_DEBOUNCE:
                continue
            saves.append(
                AutoSave(
                    field_id=editing.lock.field_id,
                    value=editing.pending_value,
                    saved_by=editing.lock.holder,
                    saved_at=at,
                )
            )
            editing.pending_value = None
            editing.changed_at = None
        self._expire_inactive_locks(at)
        return saves

    def lock_for(self, field_id: str, *, at: datetime) -> FieldLock | None:
        """Return the visible current holder, releasing locks idle for two minutes."""
        field_id = self._field_id(field_id)
        self._expire_inactive_locks(at)
        editing = self._editing_fields.get(field_id)
        return editing.lock if editing else None

    def _expire_inactive_locks(self, at: datetime) -> None:
        expired = [
            field_id
            for field_id, editing in self._editing_fields.items()
            if at - editing.lock.last_activity_at >= LOCK_INACTIVITY_TIMEOUT
        ]
        for field_id in expired:
            del self._editing_fields[field_id]

    @staticmethod
    def _field_id(value: str) -> str:
        if not isinstance(value, str) or not (field_id := value.strip()):
            raise ValueError("A field lock requires a field identifier.")
        return field_id
