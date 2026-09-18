# P0 Phase 03 — Input → Intent → Locomotion → Godot

**Status:** 03.4 IMPLEMENTED — awaiting interactive runtime validation

## Phase 03.1 — Contracts

Implemented:

- `InputIntent`
- `MovementProfile`
- input-source agnosticism
- data-driven movement parameters

Evidence:

- Player-like input and AI-like input use the same intent contract.
- Humanoid and heavy-creature configurations use the same movement profile contract.

## Phase 03.2 — Resolver

Implemented:

- `MotionState`
- `LocomotionResult`
- deterministic `LocomotionController`

The resolver receives:

`InputIntent + MovementProfile + MotionState + delta`

and produces:

`LocomotionResult`

The resolver has no dependency on:

- Godot
- CharacterBody3D
- Player
- Enemy
- animation
- camera
- hardware input

## Phase 03.3 — Godot Runtime

Implemented:

- `KashmirInputIntent`
- `KashmirMovementProfile`
- `KashmirLocomotionResult`
- `KashmirLocomotionController`
- `KashmirInputAdapter`
- `KashmirCharacterRuntime`

Runtime chain:

`Hardware Input → Input Adapter → InputIntent → LocomotionController → CharacterBody3D`

The runtime controller applies the locomotion result to `CharacterBody3D`.

The Godot runtime does not replace the Python headless reference.

## Generalization requirement

The same locomotion contract must operate with:

1. distinct input sources
2. distinct movement profiles
3. distinct runtime character implementations

No character-specific branch is permitted in the locomotion resolver.

## Runtime boundary

Python:

- headless reference
- deterministic unit/generalization validation
- no Godot dependency

GDScript:

- Godot runtime implementation
- input adapter
- CharacterBody3D integration

Godot runtime code must not become the authority for:

- combat formulas
- item rules
- progression
- skill validity
- economy
- persistent identity

## Current Runtime Scope

Implemented:

- WASD intent
- sprint intent
- dodge request
- block request
- primary-action request
- walk speed
- sprint speed
- acceleration
- deceleration
- CharacterBody3D movement
- orientation toward movement direction

Not implemented:

- camera-relative movement
- animation
- combat
- weapons
- dodge execution
- block execution
- parry
- stamina
- IK

These belong to later phases.

## Validation Gate

Phase 03.3 passes structural validation only when:

1. Core tests pass.
2. Godot project opens without parser errors.
3. Phase 03 runtime scripts load.
4. No unauthorized Godot gameplay script exists.
5. No gameplay implementation has been introduced into `src/`.
6. Godot remains provisional as the production engine.

The runtime scene validation is a separate gate.

## Next gate

Create the minimum playable Godot scene:

`CharacterBody3D + collision + floor + camera + runtime`

Then validate actual movement.

## Architectural Rule

Python remains the headless reference implementation.

GDScript is the Godot runtime implementation of the same conceptual contracts.

Neither implementation may become the authority for content-specific exceptions.

New runtime systems require explicit phase authorization rather than silently broadening the validator.

## Phase 03.4 — Minimal Runtime Scene

Implemented:

- `Main` runtime scene
- technical floor
- `CharacterBody3D`
- collision
- capsule placeholder
- camera
- directional light
- main scene configuration

Purpose:

Prove that the validated locomotion chain executes inside Godot.

Runtime test:

`W/A/S/D → InputAdapter → InputIntent → LocomotionController → CharacterBody3D`

This scene is intentionally non-production.

It contains no:

- combat
- weapons
- animation
- stamina
- IK
- final character asset
- final camera system

## Interactive Gate

Phase 03.4 passes when:

1. Godot opens the main scene.
2. The character is visible.
3. The character remains constrained by the floor.
4. WASD moves the character.
5. Releasing movement causes deceleration.
6. Sprint changes target movement speed.
7. Movement direction changes orientation.
8. No runtime errors occur.

The interactive gate is separate from the structural and headless gates.
