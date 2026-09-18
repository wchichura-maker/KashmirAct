extends Node3D

@onready var character: KashmirCharacterRuntime = $Character
@onready var camera: Camera3D = $Camera3D

const CAMERA_OFFSET := Vector3(0.0, 5.0, 8.0)


func _ready() -> void:
    print("KASHMIRACT P0 — PHASE 03.4")
    print("Runtime scene initialized.")
    print("Input → Intent → Locomotion → CharacterBody3D")

    camera.global_position = character.global_position + CAMERA_OFFSET


func _process(_delta: float) -> void:
    camera.global_position = character.global_position + CAMERA_OFFSET