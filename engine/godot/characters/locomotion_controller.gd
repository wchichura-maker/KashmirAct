class_name KashmirLocomotionController
extends RefCounted


func resolve(
    intent: KashmirInputIntent,
    profile: KashmirMovementProfile,
    current_velocity: Vector3,
    delta: float
) -> KashmirLocomotionResult:
    assert(delta >= 0.0)

    var input_vector := intent.get_move_vector()

    var desired_direction := Vector3(
        input_vector.x,
        0.0,
        input_vector.y
    )

    if desired_direction.length_squared() > 1.0:
        desired_direction = desired_direction.normalized()

    var has_movement := desired_direction.length_squared() > 0.000001
    var desired_speed := 0.0

    if has_movement:
        desired_speed = (
            profile.sprint_speed
            if intent.request_sprint
            else profile.walk_speed
        )

    var target_velocity := (
        desired_direction * desired_speed
        if has_movement
        else Vector3.ZERO
    )

    var rate := (
        profile.acceleration
        if has_movement
        else profile.deceleration
    )

    var next_velocity := current_velocity.move_toward(
        target_velocity,
        rate * delta
    )

    return KashmirLocomotionResult.new(
        next_velocity,
        desired_direction,
        desired_speed
    )