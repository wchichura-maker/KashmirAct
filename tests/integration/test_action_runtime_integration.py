import unittest

from src.game.characters.actions import ActionContext, ActionDefinition, ActionPhase, ActionRequest, ActionResolver, ActionRuntime, TransitionRule
from src.game.characters.actions.transitions import ActionTransitionResolver
from src.game.characters.actions.cancellation import ActionCancellationResolver
from src.game.characters.primitives import PrimitiveComposition, PrimitiveDefinition, PrimitiveRequest

class ActionRuntimeIntegrationTests(unittest.TestCase):
    def setUp(self):
        step = PrimitiveDefinition(primitive_id="step", duration=0.20, distance=1.0)
        lunge = PrimitiveDefinition(primitive_id="lunge", duration=0.10, distance=2.0)
        step_composition = PrimitiveComposition(composition_id="step.composition", requests=(PrimitiveRequest(primitive_id="step"),))
        lunge_composition = PrimitiveComposition(composition_id="lunge.composition", requests=(PrimitiveRequest(primitive_id="lunge"),))
        self.step = ActionDefinition(action_id="step", phases=(ActionPhase.EXECUTION,), composition_id="step.composition", transitions=(TransitionRule(from_action="step", to_action="lunge", min_time=0.10),), cancellable=True, cancel_windows=(ActionPhase.EXECUTION,))
        self.lunge = ActionDefinition(action_id="lunge", phases=(ActionPhase.EXECUTION,), composition_id="lunge.composition")
        self.actions = {"step": self.step, "lunge": self.lunge}
        self.resolver = ActionResolver(actions=self.actions, compositions={"step.composition": step_composition, "lunge.composition": lunge_composition}, primitives={"step": step, "lunge": lunge})
        self.transition_resolver = ActionTransitionResolver(self.actions)
        self.cancellation_resolver = ActionCancellationResolver()

    def test_runtime_elapsed_time_drives_transition_resolution(self):
        result = self.resolver.resolve(ActionRequest(action_id="step"))
        runtime = ActionRuntime()
        state = runtime.start(result)
        runtime.advance(0.10)
        state = runtime.state()
        next_actions = self.transition_resolver.resolve(current_action=state.action_id, elapsed_time=state.elapsed_time, context=ActionContext())
        self.assertEqual(next_actions, ("lunge",))

    def test_runtime_can_start_resolved_transition(self):
        result = self.resolver.resolve(ActionRequest(action_id="step"))
        runtime = ActionRuntime()
        runtime.start(result)
        runtime.advance(0.10)
        state = runtime.state()
        next_actions = self.transition_resolver.resolve(current_action=state.action_id, elapsed_time=state.elapsed_time, context=ActionContext())
        next_result = self.resolver.resolve(ActionRequest(action_id=next_actions[0]))
        next_state = runtime.start(next_result)
        self.assertEqual(next_state.action_id, "lunge")
        self.assertTrue(next_state.active)

    def test_cancellation_remains_independent_from_runtime(self):
        self.assertTrue(self.cancellation_resolver.can_cancel(self.step, ActionPhase.EXECUTION))
        self.assertFalse(self.cancellation_resolver.can_cancel(self.step, ActionPhase.WINDUP))

if __name__ == "__main__":
    unittest.main()
from src.game.characters.actions.transitions import ActionTransitionResolver
