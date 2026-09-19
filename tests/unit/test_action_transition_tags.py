import unittest

from src.game.characters.actions.definitions import (
    ActionContext,
    ActionDefinition,
    ActionPhase,
    TransitionRule,
)
from src.game.characters.actions.transitions import ActionTransitionResolver


class ActionTransitionTagTests(unittest.TestCase):

    def test_required_tag_allows_transition(self):
        actions = {
            "block": ActionDefinition(
                action_id="block",
                phases=(ActionPhase.EXECUTION,),
                composition_id="block.composition",
                transitions=(
                    TransitionRule(
                        from_action="block",
                        to_action="parry",
                        required_tags=("defending",),
                    ),
                ),
            )
        }

        resolver = ActionTransitionResolver(actions)

        result = resolver.resolve(
            current_action="block",
            elapsed_time=0.0,
            context=ActionContext(tags=("defending",)),
        )

        self.assertEqual(result, ("parry",))

    def test_missing_required_tag_blocks_transition(self):
        actions = {
            "block": ActionDefinition(
                action_id="block",
                phases=(ActionPhase.EXECUTION,),
                composition_id="block.composition",
                transitions=(
                    TransitionRule(
                        from_action="block",
                        to_action="parry",
                        required_tags=("defending",),
                    ),
                ),
            )
        }

        resolver = ActionTransitionResolver(actions)

        result = resolver.resolve(
            current_action="block",
            elapsed_time=0.0,
            context=ActionContext(),
        )

        self.assertEqual(result, ())

    def test_blocked_tag_prevents_transition(self):
        actions = {
            "attack": ActionDefinition(
                action_id="attack",
                phases=(ActionPhase.EXECUTION,),
                composition_id="attack.composition",
                transitions=(
                    TransitionRule(
                        from_action="attack",
                        to_action="dodge",
                        blocked_tags=("stunned",),
                    ),
                ),
            )
        }

        resolver = ActionTransitionResolver(actions)

        result = resolver.resolve(
            current_action="attack",
            elapsed_time=0.0,
            context=ActionContext(tags=("stunned",)),
        )

        self.assertEqual(result, ())

    def test_blocked_tag_allows_transition_when_absent(self):
        actions = {
            "attack": ActionDefinition(
                action_id="attack",
                phases=(ActionPhase.EXECUTION,),
                composition_id="attack.composition",
                transitions=(
                    TransitionRule(
                        from_action="attack",
                        to_action="dodge",
                        blocked_tags=("stunned",),
                    ),
                ),
            )
        }

        resolver = ActionTransitionResolver(actions)

        result = resolver.resolve(
            current_action="attack",
            elapsed_time=0.0,
            context=ActionContext(),
        )

        self.assertEqual(result, ("dodge",))

    def test_required_and_blocked_tags_can_be_combined(self):
        actions = {
            "block": ActionDefinition(
                action_id="block",
                phases=(ActionPhase.EXECUTION,),
                composition_id="block.composition",
                transitions=(
                    TransitionRule(
                        from_action="block",
                        to_action="parry",
                        required_tags=("defending",),
                        blocked_tags=("stunned",),
                    ),
                ),
            )
        }

        resolver = ActionTransitionResolver(actions)

        valid = resolver.resolve(
            current_action="block",
            elapsed_time=0.0,
            context=ActionContext(
                tags=("defending",),
            ),
        )

        blocked = resolver.resolve(
            current_action="block",
            elapsed_time=0.0,
            context=ActionContext(
                tags=("defending", "stunned"),
            ),
        )

        self.assertEqual(valid, ("parry",))
        self.assertEqual(blocked, ())


if __name__ == "__main__":
    unittest.main()
