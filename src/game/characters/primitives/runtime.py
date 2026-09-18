"""Deterministic runtime resolver for movement primitives."""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt

from .definitions import PrimitiveDefinition, PrimitiveRequest


@dataclass(frozen=True)
class PrimitiveResult:
    """Resolved movement produced by a primitive."""

    primitive_id: str

    velocity_x: float
    velocity_y: float

    rotation_degrees: float

    displacement_x: float
    displacement_y: float

    phase: str

    completed: bool

    events: tuple[str, ...] = ()

    @property
    def displacement(self) -> float:
        return sqrt(
            self.displacement_x * self.displacement_x
            + self.displacement_y * self.displacement_y
        )


class PrimitiveResolver:
    """Resolves primitive data without actor, weapon or skill knowledge."""

    @staticmethod
    def resolve(
        definition: PrimitiveDefinition,
        request: PrimitiveRequest,
    ) -> PrimitiveResult:

        if request.primitive_id != definition.primitive_id:
            raise ValueError(
                "request primitive_id does not match definition primitive_id"
            )

        length = sqrt(
            request.direction_x * request.direction_x
            + request.direction_y * request.direction_y
        )

        if length > 0.0:
            direction_x = request.direction_x / length
            direction_y = request.direction_y / length
        else:
            direction_x = 0.0
            direction_y = 0.0

        distance = definition.distance * request.intensity

        duration = (
            request.duration_override
            if request.duration_override is not None
            else definition.duration
        )

        velocity_magnitude = (
            distance / duration
            if duration > 0.0
            else 0.0
        )

        return PrimitiveResult(
            primitive_id=definition.primitive_id,
            velocity_x=direction_x * velocity_magnitude,
            velocity_y=direction_y * velocity_magnitude,
            rotation_degrees=definition.rotation_degrees,
            displacement_x=direction_x * distance,
            displacement_y=direction_y * distance,
            phase="active",
            completed=True,
            events=(),
        )
