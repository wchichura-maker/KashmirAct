"""Deterministic sequential playback of movement primitive compositions."""

from __future__ import annotations

from dataclasses import dataclass

from .composition import PrimitiveComposition, PrimitiveCompositionResolver
from .definitions import PrimitiveDefinition, PrimitiveRequest
from .runtime import PrimitiveResult


@dataclass(frozen=True)
class PrimitivePlaybackStep:
    index: int
    result: PrimitiveResult
    elapsed_before: float
    elapsed_after: float


@dataclass(frozen=True)
class PrimitivePlaybackResult:
    composition_id: str
    steps: tuple[PrimitivePlaybackStep, ...]
    completed: bool
    total_duration: float
    final_rotation_degrees: float = 0.0


class PrimitivePlayback:
    @staticmethod
    def resolve(
        composition: PrimitiveComposition,
        catalog: dict[str, PrimitiveDefinition],
    ) -> PrimitivePlaybackResult:
        composition_result = PrimitiveCompositionResolver.resolve(
            composition,
            catalog,
        )

        steps: list[PrimitivePlaybackStep] = []
        elapsed = 0.0

        for index, result in enumerate(
            composition_result.primitive_results
        ):
            definition = catalog[result.primitive_id]

            duration = (
                composition.requests[index].duration_override
                if composition.requests[index].duration_override is not None
                else definition.duration
            )

            elapsed_before = elapsed
            elapsed += duration

            steps.append(
                PrimitivePlaybackStep(
                    index=index,
                    result=result,
                    elapsed_before=elapsed_before,
                    elapsed_after=elapsed,
                )
            )

        return PrimitivePlaybackResult(
            composition_id=composition_result.composition_id,
            steps=tuple(steps),
            completed=composition_result.completed,
            total_duration=elapsed,
            final_rotation_degrees=composition_result.final_rotation_degrees,
        )