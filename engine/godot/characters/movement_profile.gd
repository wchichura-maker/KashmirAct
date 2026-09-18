class_name KashmirMovementProfile
extends Resource

@export var walk_speed: float = 4.0
@export var sprint_speed: float = 7.0
@export var acceleration: float = 20.0
@export var deceleration: float = 25.0
@export var rotation_speed: float = 10.0


func _init() -> void:
    _validate()


func _validate() -> void:
    assert(walk_speed >= 0.0)
    assert(sprint_speed >= walk_speed)
    assert(acceleration > 0.0)
    assert(deceleration > 0.0)
    assert(rotation_speed > 0.0)