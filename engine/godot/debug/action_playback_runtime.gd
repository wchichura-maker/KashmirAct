class_name KashmirActionPlaybackRuntime
extends RefCounted

var playback_data: Dictionary = {}
var elapsed_time: float = 0.0
var current_step_index: int = -1
var completed: bool = false

var _last_consumed_step_index: int = -1


func load_playback(data: Dictionary) -> void:
	playback_data = data.duplicate(true)
	elapsed_time = 0.0
	current_step_index = -1
	completed = false
	_last_consumed_step_index = -1


func advance(delta: float) -> Dictionary:
	if completed:
		return _state()

	if delta < 0.0:
		push_error("ActionPlaybackRuntime does not accept negative delta.")
		return _state()

	elapsed_time += delta

	var steps: Array = playback_data.get("steps", [])

	if steps.is_empty():
		completed = true
		return _state()

	var next_index := _find_step_index(steps)

	if next_index != -1:
		current_step_index = next_index
	elif elapsed_time >= float(playback_data.get("total_duration", 0.0)):
		current_step_index = -1
		completed = true

	return _state()


func consume_step() -> Dictionary:
	if current_step_index < 0:
		return {}

	if current_step_index == _last_consumed_step_index:
		return {}

	var steps: Array = playback_data.get("steps", [])

	if current_step_index >= steps.size():
		return {}

	_last_consumed_step_index = current_step_index

	var step_data: Dictionary = steps[current_step_index]
	return step_data.duplicate(true)


func _find_step_index(steps: Array) -> int:
	for index in range(steps.size()):
		var step_data: Dictionary = steps[index]

		var elapsed_before := float(step_data.get("elapsed_before", 0.0))
		var elapsed_after := float(step_data.get("elapsed_after", 0.0))

		if elapsed_time >= elapsed_before and elapsed_time < elapsed_after:
			return index

	return -1


func _state() -> Dictionary:
	return {
		"elapsed_time": elapsed_time,
		"current_step_index": current_step_index,
		"completed": completed,
	}