"""Data contracts for the P0.5 Action System."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ActionPhase(str, Enum):
    """Lifecycle phases of an action."""

    WINDUP = "windup"
    EXECUTION = "execution"
    RECOVERY = "recovery"


@dataclass(frozen=True)
class TransitionRule:
    """Data-driven rule describing a possible action transition."""

    from_action: str
    to_action: str
    conditions: tuple[Any, ...] = ()
    required_tags: tuple[str, ...] = ()
    blocked_tags: tuple[str, ...] = ()
    min_time: float = 0.0
    max_time: float | None = None
    priority: int = 0

    def __post_init__(self) -> None:
        if not self.from_action:
            raise ValueError("from_action cannot be empty")

        if not self.to_action:
            raise ValueError("to_action cannot be empty")

        if self.min_time < 0.0:
            raise ValueError("min_time cannot be negative")

        if self.max_time is not None and self.max_time < 0.0:
            raise ValueError("max_time cannot be negative")

        if self.max_time is not None and self.max_time < self.min_time:
            raise ValueError("max_time cannot be smaller than min_time")


@dataclass(frozen=True)
class ActionRequestBinding:
    """Maps ActionRequest values to one primitive request."""

    primitive_index: int
    use_direction: bool = False
    use_intensity: bool = False

    def __post_init__(self) -> None:
        if self.primitive_index < 0:
            raise ValueError("primitive_index cannot be negative")


@dataclass(frozen=True)
class ActionDefinition:
    """Immutable data definition of an action."""

    action_id: str
    phases: tuple[ActionPhase, ...]
    composition_id: str
    bindings: tuple[ActionRequestBinding, ...] = ()
    tags: tuple[str, ...] = ()
    conditions: tuple[Any, ...] = ()
    transitions: tuple[TransitionRule, ...] = ()
    cancellable: bool = True
    cancel_windows: tuple[ActionPhase, ...] = ()

    def __post_init__(self) -> None:
        if not self.action_id:
            raise ValueError("action_id cannot be empty")

        if not self.composition_id:
            raise ValueError("composition_id cannot be empty")

        if not self.phases:
            raise ValueError("action must contain at least one phase")

        if not isinstance(self.cancellable, bool):
            raise ValueError("cancellable must be a bool")


@dataclass(frozen=True)
class ActionRequest:
    """Runtime request to resolve an action."""

    action_id: str
    direction_x: float = 0.0
    direction_y: float = 0.0
    intensity: float = 1.0
    context: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.action_id:
            raise ValueError("action_id cannot be empty")

        if self.intensity < 0.0:
            raise ValueError("intensity cannot be negative")


@dataclass(frozen=True)
class ActionResult:
    """Deterministic result produced by resolving an action."""

    action_id: str
    valid: bool
    phase_results: tuple[Any, ...] = ()
    playback_result: Any | None = None
    total_duration: float = 0.0
    final_rotation_degrees: float = 0.0
    events: tuple[str, ...] = ()
    errors: tuple[str, ...] = ()


@dataclass(frozen=True)
class ActionContext:
    """Runtime context used when validating and resolving an action."""

    tags: tuple[str, ...] = ()
    scalar_values: dict[str, float] = field(default_factory=dict)
    boolean_values: dict[str, bool] = field(default_factory=dict)
    identifiers: dict[str, str] = field(default_factory=dict)
