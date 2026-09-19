"""Deterministic runtime state for resolved actions."""

from __future__ import annotations

from dataclasses import dataclass
from math import isclose



@dataclass(frozen=True)
class ActionRuntimeState:
    """Immutable snapshot of an action runtime."""

    action_id: str
    active: bool
    completed: bool
    interrupted: bool
    current_primitive_index: int
    elapsed_time: float


class ActionRuntime:
    """Advances a resolved action through its primitive timeline."""

    def __init__(self) -> None:
        self._action: ActionResult | None = None
        self._elapsed_time = 0.0
        self._current_primitive_index = 0
        self._active = False
        self._completed = False
        self._interrupted = False

    def start(self, action: ActionResult) -> ActionRuntimeState:
        if not action.valid:
            raise ValueError("cannot start an invalid action")

        if action.playback_result is None:
            raise ValueError("cannot start an action without playback")

        self._action = action
        self._elapsed_time = 0.0
        self._current_primitive_index = 0
        self._active = True
        self._completed = False
        self._interrupted = False

        if not action.playback_result.steps:
            self._active = False
            self._completed = True

        return self.state()

    def advance(self, delta_time: float) -> ActionRuntimeState:
        if delta_time < 0.0:
            raise ValueError("delta_time cannot be negative")

        if not self._active:
            return self.state()

        self._elapsed_time += delta_time

        playback = self._action.playback_result
        steps = playback.steps

        if self._elapsed_time >= playback.total_duration or isclose(self._elapsed_time, playback.total_duration, rel_tol=1e-09, abs_tol=1e-09):
            self._elapsed_time = playback.total_duration
            self._current_primitive_index = len(steps)
            self._active = False
            self._completed = True
            return self.state()

        for index, step in enumerate(steps):
            if step.elapsed_before <= self._elapsed_time < step.elapsed_after:
                self._current_primitive_index = index
                break

        return self.state()

    def interrupt(self) -> ActionRuntimeState:
        if self._active:
            self._active = False
            self._interrupted = True

        return self.state()

    def state(self) -> ActionRuntimeState:
        if self._action is None:
            return ActionRuntimeState(
                action_id="",
                active=False,
                completed=False,
                interrupted=False,
                current_primitive_index=-1,
                elapsed_time=0.0,
            )

        return ActionRuntimeState(
            action_id=self._action.action_id,
            active=self._active,
            completed=self._completed,
            interrupted=self._interrupted,
            current_primitive_index=self._current_primitive_index,
            elapsed_time=self._elapsed_time,
        )
