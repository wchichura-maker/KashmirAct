class_name KashmirCharacterRuntime
extends CharacterBody3D

@export var movement_profile: KashmirMovementProfile

var locomotion_controller := KashmirLocomotionController.new()
var input_adapter := KashmirInputAdapter.new()

var current_intent := KashmirInputIntent.idle()
var current_locomotion_result := KashmirLocomotionResult.new()


func _ready() -> void:
    if movement_profile == null:
        movement_profile = KashmirMovementProfile.new()


func _physics_process(delta: float) -> void:
    current_intent = input_adapter.read_intent()

    current_locomotion_result = locomotion_controller.resolve(
        current_intent,
        movement_profile,
        velocity,
        delta
    )

    velocity.x = current_locomotion_result.velocity.x
    velocity.z = current_locomotion_result.velocity.z

    move_and_slide()

    _update_debug_rotation(delta)


func _update_debug_rotation(delta: float) -> void:
    var direction := current_locomotion_result.desired_direction

    if direction.length_squared() <= 0.000001:
        return

    var target_angle := atan2(direction.x, direction.z)

    rotation.y = lerp_angle(
        rotation.y,
        target_angle,
        minf(movement_profile.rotation_speed * delta, 1.0)
    )