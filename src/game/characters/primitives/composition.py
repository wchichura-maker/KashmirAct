"""Deterministic composition of reusable movement primitives."""

from __future__ import annotations

from dataclasses import dataclass
from math import cos, radians, sin

from .definitions import PrimitiveDefinition, PrimitiveRequest
from .runtime import PrimitiveResolver, PrimitiveResult


@dataclass(frozen=True)
class PrimitiveComposition:
    """Ordered collection of primitive execution requests."""

    composition_id: str
    requests: tuple[PrimitiveRequest, ...]

    def __post_init__(self) -> None:
        if not self.composition_id:
            raise ValueError("composition_id must not be empty")


@dataclass(frozen=True)
class PrimitiveCompositionResult:
    """Resolved result of an ordered primitive composition."""

    composition_id: str
    primitive_results: tuple[PrimitiveResult, ...]
    completed: bool
    final_rotation_degrees: float = 0.0


class PrimitiveCompositionResolver:
    """Resolves primitive requests using a shared primitive catalog."""

    @staticmethod
    def resolve(
        composition: PrimitiveComposition,
        catalog: dict[str, PrimitiveDefinition],
    ) -> PrimitiveCompositionResult:
        results: list[PrimitiveResult] = []
        rotation_degrees = 0.0

        for request in composition.requests:
            definition = catalog[request.primitive_id]

            local_x = request.direction_x
            local_y = request.direction_y

            angle = radians(rotation_degrees)
            cos_angle = cos(angle)
            sin_angle = sin(angle)

            world_x = local_x * cos_angle - local_y * sin_angle
            world_y = local_x * sin_angle + local_y * cos_angle

            resolved_request = PrimitiveRequest(
                primitive_id=request.primitive_id,
                direction_x=world_x,
                direction_y=world_y,
                intensity=request.intensity,
                duration_override=request.duration_override,
                context=request.context,
            )

            result = PrimitiveResolver.resolve(
                definition,
                resolved_request,
            )

            results.append(result)
            rotation_degrees += definition.rotation_degrees

        return PrimitiveCompositionResult(
            composition_id=composition.composition_id,
            primitive_results=tuple(results),
            completed=True,
            final_rotation_degrees=rotation_degrees,
        )
