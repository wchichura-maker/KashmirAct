"""Portable deterministic locomotion resolver."""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt

from .input_intent import InputIntent
from .movement_profile import MovementProfile


@dataclass(frozen=True)
class MotionState:
    """Engine-independent kinematic state."""

    velocity_x: float = 0.0
    velocity_y: float = 0.0

    @property
    def speed(self) -> float:
        return sqrt(
            self.velocity_x * self.velocity_x
            + self.velocity_y * self.velocity_y
        )


@dataclass(frozen=True)
class LocomotionResult:
    """Result produced by the locomotion resolver."""

    motion: MotionState
    desired_direction_x: float
    desired_direction_y: float

    @property
    def desired_speed(self) -> float:
        return sqrt(
            self.desired_direction_x * self.desired_direction_x
            + self.desired_direction_y * self.desired_direction_y
        )


class LocomotionController:
    """Pure deterministic locomotion resolver.

    This class deliberately has no knowledge of:
    - Godot
    - CharacterBody3D
    - Player
    - Enemy
    - animation
    - camera
    - input devices
    """

    @staticmethod
    def resolve(
        intent: InputIntent,
        profile: MovementProfile,
        current: MotionState,
        delta: float,
    ) -> LocomotionResult:

        if delta < 0.0:
            raise ValueError("delta must be >= 0")

        desired_x = intent.move_x
        desired_y = intent.move_y

        desired_length = sqrt(
            desired_x * desired_x
            + desired_y * desired_y
        )

        if desired_length > 0.0:
            desired_x /= desired_length
            desired_y /= desired_length

        target_speed = (
            profile.sprint_speed
            if intent.request_sprint
            else profile.walk_speed
        )

        target_x = desired_x * target_speed
        target_y = desired_y * target_speed

        acceleration = (
            profile.acceleration
            if desired_length > 0.0
            else profile.deceleration
        )

        max_change = acceleration * delta

        next_x = LocomotionController._move_toward(
            current.velocity_x,
            target_x,
            max_change,
        )

        next_y = LocomotionController._move_toward(
            current.velocity_y,
            target_y,
            max_change,
        )

        return LocomotionResult(
            motion=MotionState(
                velocity_x=next_x,
                velocity_y=next_y,
            ),
            desired_direction_x=desired_x,
            desired_direction_y=desired_y,
        )

    @staticmethod
    def _move_toward(
        current: float,
        target: float,
        amount: float,
    ) -> float:

        if current < target:
            return min(current + amount, target)

        if current > target:
            return max(current - amount, target)

        return target
