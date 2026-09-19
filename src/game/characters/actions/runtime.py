from __future__ import annotations

from dataclasses import dataclass
from math import isclose

from .definitions import ActionContext, ActionRequest, ActionResult
from .resolver import ActionResolver
from .transitions import ActionTransitionResolver


@dataclass(frozen=True)
class ActionRuntimeState:
    action_id: str
    active: bool
    completed: bool
    interrupted: bool
    current_primitive_index: int
    elapsed_time: float
    transition_ready: bool = False


@dataclass(frozen=True)
class ActionTransitionResult:
    from_action: str
    next_actions: tuple[str, ...]


class ActionRuntime:
    def __init__(
        self,
        action_resolver: ActionResolver | None = None,
        transition_resolver: ActionTransitionResolver | None = None,
        context: ActionContext | None = None,
    ) -> None:
        self._action: ActionResult | None = None
        self._elapsed_time = 0.0
        self._current_primitive_index = 0
        self._active = False
        self._completed = False
        self._interrupted = False
        self._action_resolver = action_resolver
        self._transition_resolver = transition_resolver
        self._context = context or ActionContext()

    def start(self, action: ActionResult) -> ActionRuntimeState:
        if not action.valid:
            raise ValueError("Cannot start an invalid action.")

        if action.playback_result is None:
            raise ValueError("Cannot start an action without playback data.")

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
            raise ValueError("delta_time cannot be negative.")

        if not self._active:
            return self.state()

        self._elapsed_time += delta_time

        playback = self._action.playback_result
        steps = playback.steps

        if (
            self._elapsed_time >= playback.total_duration
            or isclose(
                self._elapsed_time,
                playback.total_duration,
                rel_tol=0.0,
                abs_tol=1e-9,
            )
        ):
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

    def transition_options(
        self,
        context: ActionContext | None = None,
    ) -> ActionTransitionResult:
        if self._action is None:
            return ActionTransitionResult("", ())

        if self._transition_resolver is None:
            return ActionTransitionResult(self._action.action_id, ())

        resolved_context = context or self._context

        next_actions = self._transition_resolver.resolve(
            current_action=self._action.action_id,
            elapsed_time=self._elapsed_time,
            context=resolved_context,
        )

        return ActionTransitionResult(
            from_action=self._action.action_id,
            next_actions=next_actions,
        )

    def transition_to(
        self,
        context: ActionContext | None = None,
    ) -> ActionResult | None:
        if self._action_resolver is None:
            return None

        options = self.transition_options(context)

        if not options.next_actions:
            return None

        next_action_id = options.next_actions[0]

        next_action = self._action_resolver.resolve(
            ActionRequest(action_id=next_action_id)
        )

        if not next_action.valid:
            return None

        self.start(next_action)
        return next_action

    def state(self) -> ActionRuntimeState:
        if self._action is None:
            return ActionRuntimeState(
                action_id="",
                active=False,
                completed=False,
                interrupted=False,
                current_primitive_index=-1,
                elapsed_time=0.0,
                transition_ready=False,
            )

        transition_ready = bool(
            self._transition_resolver is not None
            and self.transition_options().next_actions
        )

        return ActionRuntimeState(
            action_id=self._action.action_id,
            active=self._active,
            completed=self._completed,
            interrupted=self._interrupted,
            current_primitive_index=self._current_primitive_index,
            elapsed_time=self._elapsed_time,
            transition_ready=transition_ready,
        )
