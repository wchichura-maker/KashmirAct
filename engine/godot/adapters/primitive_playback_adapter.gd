class_name KashmirPrimitivePlaybackAdapter
extends RefCounted


var primitive_adapter := KashmirPrimitiveAdapter.new()


func apply_playback(
	character: CharacterBody3D,
	playback_data: Dictionary
) -> void:
	if character == null:
		return

	var steps: Array = playback_data.get("steps", [])

	for step_data in steps:
		var result_data: Dictionary = step_data.get("result", {})

		var result := _result_from_dictionary(result_data)

		if result == null:
			continue

		primitive_adapter.apply_result(
			character,
			result
		)


func _result_from_dictionary(
	data: Dictionary
) -> KashmirPrimitiveResult:
	var velocity_data: Dictionary = data.get(
		"velocity",
		{}
	)

	var displacement_data: Dictionary = data.get(
		"displacement",
		{}
	)

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