extends Node

@export var character: CharacterBody3D

var primitive_adapter := KashmirPrimitiveAdapter.new()
var playback_adapter := KashmirPrimitivePlaybackAdapter.new()
var sequence_running := false

func _ready() -> void:
	if character == null:
		character = get_parent().get_node("Character")


func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_1:
			_run_primitive("res://data/actions/primitive_step.json")
		elif event.keycode == KEY_2:
			_run_composition("res://data/actions/composition_step_turn_lunge.json")


func _run_primitive(path: String) -> void:
	if sequence_running:
		return

	sequence_running = true

	var result := _load_result(path)

	if result == null:
		sequence_running = false
		return

	primitive_adapter.apply_result(character, result)

	print("Primitive executed: ", result.primitive_id, " displacement=", result.displacement, " rotation=", result.rotation_degrees)

	sequence_running = false


func _run_composition(path: String) -> void:
	if sequence_running:
		return

	sequence_running = true

	var playback_data := _load_json(path)

	if playback_data.is_empty():
		sequence_running = false
		return

	playback_adapter.apply_playback(character, playback_data)

	print("Composition executed: ", playback_data.get("composition_id", ""), " duration=", playback_data.get("total_duration", 0.0), " final_rotation=", playback_data.get("final_rotation_degrees", 0.0))

	sequence_running = false


func _load_result(path: String) -> KashmirPrimitiveResult:
	var data := _load_json(path)

	if data.is_empty():
		return null

	var velocity_data: Dictionary = data.get("velocity", {})
	var displacement_data: Dictionary = data.get("displacement", {})

	var typed_events: Array[String] = []

	for event_name in data.get("events", []):
		typed_events.append(str(event_name))

	return KashmirPrimitiveResult.new(
		data.get("primitive_id", ""),
		Vector3(velocity_data.get("x", 0.0), 0.0, velocity_data.get("y", 0.0)),
		data.get("rotation_degrees", 0.0),
		Vector3(displacement_data.get("x", 0.0), 0.0, displacement_data.get("y", 0.0)),
		data.get("phase", ""),
		data.get("completed", false),
		typed_events
	)


func _load_json(path: String) -> Dictionary:
	var file := FileAccess.open(path, FileAccess.READ)

	if file == null:
		push_error("Unable to open JSON: " + path)
		return {}

	var data = JSON.parse_string(file.get_as_text())

	if not data is Dictionary:
		push_error("Invalid JSON dictionary: " + path)
		return {}

	return data
