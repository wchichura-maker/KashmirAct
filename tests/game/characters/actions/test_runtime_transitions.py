from __future__ import annotations

import unittest

from src.game.characters.actions.conditions import BooleanCondition
from src.game.characters.actions.definitions import (
    ActionContext,
    ActionDefinition,
    ActionPhase,
    ActionRequest,
    TransitionRule,
)
from src.game.characters.actions.resolver import ActionResolver
from src.game.characters.actions.runtime import ActionRuntime
from src.game.characters.actions.transitions import ActionTransitionResolver
from src.game.characters.primitives.composition import PrimitiveComposition
from src.game.characters.primitives.definitions import (
    PrimitiveDefinition,
    PrimitiveRequest,
)


class ActionRuntimeTransitionIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.primitives = {
            "step": PrimitiveDefinition(
                primitive_id="step",
                duration=0.2,
                distance=1.0,
            ),
            "turn": PrimitiveDefinition(
                primitive_id="turn",
                duration=0.1,
                rotation_degrees=90.0,
            ),
            "lunge": PrimitiveDefinition(
                primitive_id="lunge",
                duration=0.5,
                distance=3.0,
            ),
        }

        self.compositions = {
            "composition_step": PrimitiveComposition(
                composition_id="composition_step",
                requests=(
                    PrimitiveRequest(
                        primitive_id="step",
                    ),
                ),
            ),
            "composition_turn": PrimitiveComposition(
                composition_id="composition_turn",
                requests=(
                    PrimitiveRequest(
                        primitive_id="turn",
                    ),
                ),
            ),
            "composition_lunge": PrimitiveComposition(
                composition_id="composition_lunge",
                requests=(
                    PrimitiveRequest(
                        primitive_id="lunge",
                    ),
                ),
            ),
        }

        self.actions = {
            "step": ActionDefinition(
                action_id="step",
                phases=(ActionPhase.EXECUTION,),
                composition_id="composition_step",
                transitions=(
                    TransitionRule(
                        from_action="step",
                        to_action="lunge",
                        min_time=0.2,
                    ),
                ),
            ),
            "turn": ActionDefinition(
                action_id="turn",
                phases=(ActionPhase.EXECUTION,),
                composition_id="composition_turn",
                transitions=(
                    TransitionRule(
                        from_action="turn",
                        to_action="step",
                        min_time=0.1,
                    ),
                ),
            ),
            "lunge": ActionDefinition(
                action_id="lunge",
                phases=(ActionPhase.EXECUTION,),
                composition_id="composition_lunge",
            ),
        }

        self.action_resolver = ActionResolver(
            actions=self.actions,
            compositions=self.compositions,
            primitives=self.primitives,
        )

        self.transition_resolver = ActionTransitionResolver(
            self.actions
        )

    def make_runtime(
        self,
        context: ActionContext | None = None,
    ) -> ActionRuntime:
        return ActionRuntime(
            action_resolver=self.action_resolver,
            transition_resolver=self.transition_resolver,
            context=context,
        )

    def test_runtime_executes_step_to_lunge_transition(self) -> None:
        result = self.action_resolver.resolve(
            ActionRequest(action_id="step")
        )

        runtime = self.make_runtime()

        runtime.start(result)
        runtime.advance(0.2)

        state = runtime.state()

        self.assertTrue(state.completed)
        self.assertTrue(state.transition_ready)

        options = runtime.transition_options()

        self.assertEqual(
            options.next_actions,
            ("lunge",),
        )

        next_action = runtime.transition_to()

        self.assertIsNotNone(next_action)
        self.assertEqual(next_action.action_id, "lunge")
        self.assertTrue(runtime.state().active)
        self.assertEqual(runtime.state().action_id, "lunge")

    def test_same_runtime_mechanism_executes_turn_to_step(self) -> None:
        result = self.action_resolver.resolve(
            ActionRequest(action_id="turn")
        )

        runtime = self.make_runtime()

        runtime.start(result)
        runtime.advance(0.1)

        options = runtime.transition_options()

        self.assertEqual(
            options.next_actions,
            ("step",),
        )

        next_action = runtime.transition_to()

        self.assertIsNotNone(next_action)
        self.assertEqual(next_action.action_id, "step")
        self.assertTrue(runtime.state().active)

    def test_transition_priority_is_preserved_by_runtime(self) -> None:
        actions = dict(self.actions)

        actions["step"] = ActionDefinition(
            action_id="step",
            phases=(ActionPhase.EXECUTION,),
            composition_id="composition_step",
            transitions=(
                TransitionRule(
                    from_action="step",
                    to_action="lunge",
                    min_time=0.2,
                    priority=10,
                ),
                TransitionRule(
                    from_action="step",
                    to_action="turn",
                    min_time=0.2,
                    priority=1,
                ),
            ),
        )

        resolver = ActionTransitionResolver(actions)

        action_resolver = ActionResolver(
            actions=actions,
            compositions=self.compositions,
            primitives=self.primitives,
        )

        result = action_resolver.resolve(
            ActionRequest(action_id="step")
        )

        runtime = ActionRuntime(
            action_resolver=action_resolver,
            transition_resolver=resolver,
        )

        runtime.start(result)
        runtime.advance(0.2)

        self.assertEqual(
            runtime.transition_options().next_actions,
            ("lunge", "turn"),
        )

        next_action = runtime.transition_to()

        self.assertIsNotNone(next_action)
        self.assertEqual(next_action.action_id, "lunge")

    def test_conditions_are_evaluated_by_transition_runtime(self) -> None:
        actions = dict(self.actions)

        actions["step"] = ActionDefinition(
            action_id="step",
            phases=(ActionPhase.EXECUTION,),
            composition_id="composition_step",
            transitions=(
                TransitionRule(
                    from_action="step",
                    to_action="lunge",
                    min_time=0.2,
                    conditions=(
                        BooleanCondition(
                            key="can_chain",
                            expected=True,
                        ),
                    ),
                ),
            ),
        )

        resolver = ActionTransitionResolver(actions)

        result = self.action_resolver.resolve(
            ActionRequest(action_id="step")
        )

        runtime = ActionRuntime(
            action_resolver=self.action_resolver,
            transition_resolver=resolver,
            context=ActionContext(
                boolean_values={"can_chain": False}
            ),
        )

        runtime.start(result)
        runtime.advance(0.2)

        self.assertEqual(
            runtime.transition_options().next_actions,
            (),
        )

        runtime = ActionRuntime(
            action_resolver=self.action_resolver,
            transition_resolver=resolver,
            context=ActionContext(
                boolean_values={"can_chain": True}
            ),
        )

        runtime.start(result)
        runtime.advance(0.2)

        self.assertEqual(
            runtime.transition_options().next_actions,
            ("lunge",),
        )


if __name__ == "__main__":
    unittest.main()
