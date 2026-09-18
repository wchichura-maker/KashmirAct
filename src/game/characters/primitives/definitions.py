"""Data contracts for reusable movement primitives."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class PrimitiveDefinition:
    """Data-only definition of a reusable movement primitive."""

    primitive_id: str
    duration: float
    distance: float = 0.0
    rotation_degrees: float = 0.0
    acceleration: float = 0.0
    constraints: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    cancellable: bool = True

    def __post_init__(self) -> None:
        if not self.primitive_id:
            raise ValueError("primitive_id must not be empty")

        if self.duration <= 0.0:
            raise ValueError("duration must be > 0")

        if self.distance < 0.0:
            raise ValueError("distance must be >= 0")

        if self.acceleration < 0.0:
            raise ValueError("acceleration must be >= 0")

        if not isinstance(self.cancellable, bool):
            raise ValueError("cancellable must be bool")


@dataclass(frozen=True)
class PrimitiveRequest:
    """Runtime request for executing a primitive."""

    primitive_id: str
    direction_x: float = 0.0
    direction_y: float = 0.0
    intensity: float = 1.0
    duration_override: float | None = None
    context: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.primitive_id:
            raise ValueError("primitive_id must not be empty")

        if self.intensity < 0.0:
            raise ValueError("intensity must be >= 0")

        if self.duration_override is not None:
            if self.duration_override <= 0.0:
                raise ValueError("duration_override must be > 0")
