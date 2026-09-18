# Architecture — Bootstrap 0

KashmirAct is structured so systems can represent categories of content before that content exists.

```text
ENGINE LAYER          engine/ + project.godot (provisional Godot 4.6)
        ↓
ADAPTERS              engine/godot/adapters/
        ↓
GAME SYSTEMS          src/game/
        ↓
CORE RULES / DATA     src/core/ + data/
```

## Layer contracts

| Layer | Owns | Must not own |
|---|---|---|
| Core | Rules, IDs, events, deterministic simulation, data contracts | UI, VFX, animation assets, Godot Nodes, editor-only APIs |
| Game | Runtime systems using Core (movement, combat, telemetry, enemy) | Final presentation authority, mutation of Core rules from UI |
| Data | Gameplay definitions | Presentation meshes, hardcoded character exceptions |
| Assets | Meshes, animations, materials, audio, VFX | Gameplay truth |
| Engine | Godot project, scenes, adapters | Authoritative combat formulas |
| Tests | Evidence | Gameplay authority |
| Tools | Validation, debug, pipeline | Gameplay mutation |
| UI | Observation and development overlay | Gameplay state authority |

P0 spec §49–§50 remains binding: UI observes; telemetry observes; animation is not damage authority; VFX is not gameplay authority.

## Future action pipeline (not implemented)

The initial tree must not contradict:

```text
INPUT
  → INTENT
  → ACTION REQUEST
  → TRANSITION SYSTEM
  → STATE MACHINE
  → COMPONENTS
  → ANIMATION / IK / PHYSICS
  → COMBAT
  → EVENTS
  → TELEMETRY
```

Input is not an action. An action is not a state. Hardware events, AI, replay, simulation, and future network input should produce a common intent representation.

## Procedurality and generalization

Systems must be general rules, not exceptions for the first character, first sword, or first animation set. Differences belong in data, resources, contracts, adapters, or components.

This is an architectural constraint. It is not a request to implement procedural generation in Bootstrap 0.

## What exists now

Directories, contracts as documentation, source-of-truth files, and a Godot project stub.

## What does not exist yet

No character controller, combat, animation graph, IK, enemy AI, telemetry runtime, or tests of gameplay.
