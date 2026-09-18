class_name KashmirPrimitiveAdapter
extends RefCounted


func apply_result(
	character: CharacterBody3D,
	result: KashmirPrimitiveResult
) -> void:
	if character == null:
		return

	var world_displacement := character.global_transform.basis * result.displacement

	character.global_position += world_displacement
	character.rotation.y += deg_to_rad(result.rotation_degrees)