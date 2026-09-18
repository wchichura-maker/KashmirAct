class_name KashmirLocomotionResult
extends RefCounted

var velocity: Vector3
var desired_direction: Vector3
var desired_speed: float


func _init(
    p_velocity: Vector3 = Vector3.ZERO,
    p_desired_direction: Vector3 = Vector3.ZERO,
    p_desired_speed: float = 0.0
) -> void:
    velocity = p_velocity
    desired_direction = p_desired_direction
    desired_speed = p_desired_speed