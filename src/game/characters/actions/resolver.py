"""Deterministic resolution of data-driven actions."""

from __future__ import annotations

from dataclasses import replace

from .definitions import ActionDefinition, ActionRequest, ActionResult
from .validation import ActionValidator
from ..primitives.composition import PrimitiveComposition
from ..primitives.definitions import PrimitiveDefinition, PrimitiveRequest
from ..primitives.playback import PrimitivePlayback


class ActionResolver:
    """Resolves actions through the existing primitive playback system."""

    def __init__(
        self,
        actions: dict[str, ActionDefinition],
        compositions: dict[str, PrimitiveComposition],
        primitives: dict[str, PrimitiveDefinition],
    ) -> None:
        self._actions = actions
        self._compositions = compositions
        self._primitives = primitives
        self._validator = ActionValidator()

    def resolve(self, request: ActionRequest) -> ActionResult:
        definition = self._actions.get(request.action_id)

        if definition is None:
            return ActionResult(
                action_id=request.action_id,
                valid=False,
                errors=("unknown action",),
            )

        validation = self._validator.validate(definition)

        if not validation.valid:
            return ActionResult(
                action_id=request.action_id,
                valid=False,
                errors=validation.errors,
            )

        composition = self._compositions.get(definition.composition_id)

        if composition is None:
            return ActionResult(
                action_id=request.action_id,
                valid=False,
                errors=("unknown composition",),
            )

        bound_requests = list(composition.requests)

        for binding in definition.bindings:
            if binding.primitive_index >= len(bound_requests):
                return ActionResult(
                    action_id=request.action_id,
                    valid=False,
                    errors=(
                        "binding primitive_index exceeds composition request count",
                    ),
                )

            primitive_request = bound_requests[binding.primitive_index]

            if binding.use_direction:
                primitive_request = replace(
                    primitive_request,
                    direction_x=request.direction_x,
                    direction_y=request.direction_y,
                )

            if binding.use_intensity:
                primitive_request = replace(
                    primitive_request,
                    intensity=request.intensity,
                )

            bound_requests[binding.primitive_index] = primitive_request

        resolved_composition = PrimitiveComposition(
            composition_id=composition.composition_id,
            requests=tuple(bound_requests),
        )

        playback = PrimitivePlayback.resolve(
            resolved_composition,
            self._primitives,
        )

        return ActionResult(
            action_id=request.action_id,
            valid=True,
            phase_results=(),
            playback_result=playback,
            total_duration=playback.total_duration,
            final_rotation_degrees=playback.final_rotation_degrees,
        )
