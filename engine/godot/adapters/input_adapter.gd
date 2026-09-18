class_name KashmirInputAdapter
extends RefCounted


func read_intent() -> KashmirInputIntent:
    var movement := Input.get_vector(
        "move_left",
        "move_right",
        "move_forward",
        "move_backward"
    )

    return KashmirInputIntent.new(
        movement.x,
        movement.y,
        0.0,
        0.0,
        Input.is_action_pressed("sprint"),
        Input.is_action_just_pressed("dodge"),
        Input.is_action_pressed("block"),
        Input.is_action_just_pressed("primary_action")
    )