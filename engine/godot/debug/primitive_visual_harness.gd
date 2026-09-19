extends Node

@export var character: CharacterBody3D

var primitive_adapter := KashmirPrimitiveAdapter.new()
var playback_adapter := KashmirPrimitivePlaybackAdapter.new()
var playback_runtime := KashmirActionPlaybackRuntime.new()
var playback_running := false
var sequence_running := false
var playback_data: Dictionary = {}

func _result_from_dictionary(data: Dictionary) -> KashmirPrimitiveResult:
	var velocity_data: Dictionary = data.get("velocity", {})
	var displacement_data: Dictionary = data.get("displacement", {})

	var typed_events: Array[String] = []

	for event_name in data.get("events", []):
		typed_events.append(str(event_name))

	return KashmirPrimitiveResult.new(
		data.get("primitive_id", ""),
		Vector3(
			velocity_data.get("x", 0.0),
			0.0,
			velocity_data.get("y", 0.0)
		),
		data.get("rotation_degrees", 0.0),
		Vector3(
			displacement_data.get("x", 0.0),
			0.0,
			displacement_data.get("y", 0.0)
		),
		data.get("phase", ""),
		data.get("completed", false),
		typed_events
	)

func _ready() -> void:
	if character == null:
		character = get_parent().get_node("Character")


func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_1:
			_run_primitive("res://data/actions/primitive_step.json")
		elif event.keycode == KEY_2:
			_run_composition("res://data/actions/composition_step_turn_lunge.json")

func _physics_process(delta: float) -> void:
	if not playback_running:
		return

	var state := playback_runtime.advance(delta)
	var step_data := playback_runtime.consume_step()

	if not step_data.is_empty():
		var result_data: Dictionary = step_data.get("result", {})
		var result := _result_from_dictionary(result_data)

		if result != null:
			primitive_adapter.apply_result(character, result)

			print(
				"Playback step executed: ",
				step_data.get("index", -1),
				" primitive=",
				result.primitive_id,
				" elapsed=",
				state.get("elapsed_time", 0.0)
			)

	if state.get("completed", false):
		playback_running = false

		print(
			"Composition playback completed: ",
			playback_data.get("composition_id", "")
		)

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
	if playback_running:
		return

	var data := _load_json(path)

	if data.is_empty():
		return

	playback_data = data
	playback_runtime.load_playback(playback_data)
	playback_running = true

	print(
		"Composition playback started: ",
		playback_data.get("composition_id", ""),
		" duration=",
		playback_data.get("total_duration", 0.0)
	)


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
