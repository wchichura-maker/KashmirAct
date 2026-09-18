class_name KashmirInputIntent
extends RefCounted

var move_x: float
var move_y: float
var look_x: float
var look_y: float

var request_sprint: bool
var request_dodge: bool
var request_block: bool
var request_primary_action: bool


func _init(
    p_move_x: float = 0.0,
    p_move_y: float = 0.0,
    p_look_x: float = 0.0,
    p_look_y: float = 0.0,
    p_request_sprint: bool = false,
    p_request_dodge: bool = false,
    p_request_block: bool = false,
    p_request_primary_action: bool = false
) -> void:
    move_x = p_move_x
    move_y = p_move_y
    look_x = p_look_x
    look_y = p_look_y

    request_sprint = p_request_sprint
    request_dodge = p_request_dodge
    request_block = p_request_block
    request_primary_action = p_request_primary_action

    _normalize_axes()


static func idle() -> KashmirInputIntent:
    return KashmirInputIntent.new()


func _normalize_axes() -> void:
    move_x = clampf(move_x, -1.0, 1.0)
    move_y = clampf(move_y, -1.0, 1.0)
    look_x = clampf(look_x, -1.0, 1.0)
    look_y = clampf(look_y, -1.0, 1.0)

    var length := Vector2(move_x, move_y).length()

    if length > 1.0:
        move_x /= length
        move_y /= length


func get_move_vector() -> Vector2:
    return Vector2(move_x, move_y)


func get_move_magnitude() -> float:
    return Vector2(move_x, move_y).length()