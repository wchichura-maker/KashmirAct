"""Portable locomotion data definitions.

MovementProfile describes movement capability.
It does not know about Godot, CharacterBody3D, animation or input.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MovementProfile:
    """Data-driven locomotion parameters."""

    walk_speed: float = 3.0
    sprint_speed: float = 5.5

    acceleration: float = 18.0
    deceleration: float = 24.0

    rotation_speed: float = 10.0

    def __post_init__(self) -> None:
        if self.walk_speed < 0.0:
            raise ValueError("walk_speed must be >= 0")

        if self.sprint_speed < 0.0:
            raise ValueError("sprint_speed must be >= 0")

        if self.acceleration <= 0.0:
            raise ValueError("acceleration must be > 0")

        if self.deceleration <= 0.0:
            raise ValueError("deceleration must be > 0")

        if self.rotation_speed <= 0.0:
            raise ValueError("rotation_speed must be > 0")

        if self.sprint_speed < self.walk_speed:
            raise ValueError("sprint_speed must be >= walk_speed")
