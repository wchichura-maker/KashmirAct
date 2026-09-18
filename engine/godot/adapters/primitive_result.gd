class_name KashmirPrimitiveResult
extends RefCounted


var primitive_id: String
var velocity: Vector3
var rotation_degrees: float
var displacement: Vector3
var phase: String
var completed: bool
var events: Array[String]


func _init(
    p_primitive_id: String = "",
    p_velocity: Vector3 = Vector3.ZERO,
    p_rotation_degrees: float = 0.0,
    p_displacement: Vector3 = Vector3.ZERO,
    p_phase: String = "",
    p_completed: bool = false,
    p_events: Array[String] = []
) -> void:
    primitive_id = p_primitive_id
    velocity = p_velocity
    rotation_degrees = p_rotation_degrees
    displacement = p_displacement
    phase = p_phase
    completed = p_completed
    events = p_events.duplicate()