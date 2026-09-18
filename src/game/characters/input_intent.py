"""Portable character input contracts.

This module contains no Godot dependency and no player-specific logic.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt


@dataclass(frozen=True)
class InputIntent:
    """Normalized intention produced by any input source.

    The source may be:
    - physical player input
    - AI
    - replay
    - deterministic simulation
    - future network input

    The locomotion system must not know which source produced it.
    """

    move_x: float = 0.0
    move_y: float = 0.0
    look_x: float = 0.0
    look_y: float = 0.0

    request_sprint: bool = False
    request_dodge: bool = False
    request_block: bool = False
    request_primary_action: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "move_x", self._normalize_axis(self.move_x))
        object.__setattr__(self, "move_y", self._normalize_axis(self.move_y))
        object.__setattr__(self, "look_x", self._normalize_axis(self.look_x))
        object.__setattr__(self, "look_y", self._normalize_axis(self.look_y))

        length = sqrt(self.move_x * self.move_x + self.move_y * self.move_y)

        if length > 1.0:
            object.__setattr__(self, "move_x", self.move_x / length)
            object.__setattr__(self, "move_y", self.move_y / length)

    @staticmethod
    def _normalize_axis(value: float) -> float:
        return max(-1.0, min(1.0, float(value)))

    @property
    def move_magnitude(self) -> float:
        return sqrt(self.move_x * self.move_x + self.move_y * self.move_y)

    @property
    def has_movement(self) -> bool:
        return self.move_magnitude > 0.0

    @classmethod
    def idle(cls) -> "InputIntent":
        return cls()

    @classmethod
    def move(
        cls,
        x: float,
        y: float,
        *,
        sprint: bool = False,
    ) -> "InputIntent":
        return cls(
            move_x=x,
            move_y=y,
            request_sprint=sprint,
        )
