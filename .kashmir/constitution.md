# KashmirAct — Project Constitution

Derived from Foundation v0.1 and P0 specification v0.1. This document does not replace those sources.

## Identity

KashmirAct is an independent project. It is not the previous Kashmir project.

It is a 3D real-time Action RPG. The player does not simply choose a class. They build, through how they play, the character they become.

Items, abilities, and combat styles must be results of systems, not only pre-authored content.

## Confirmed (Foundation v0.1)

- development name: KashmirAct
- independent from the previous Kashmir project
- experience inspired by Overgeared, without VR, without using that IP
- Action RPG, third person, real-time combat
- progression from behavior
- emergent classes
- professions
- deep item creation
- ability composition
- discovery AI (future, under rules)
- combat telemetry
- candidate simulation
- item authorship and history

## Provisional (must not be finalized silently)

- Godot 4.6 as P0 engine
- single-player as first target
- future multiplayer
- open world
- final network architecture
- final camera / lock-on format
- definitive profession list

## Out of initial scope

VR; full MMO; dozens of maps; hundreds of NPCs; crafting of every category; extensive narrative; final art production.

## Development principles

1. System before content.
2. Data before UI.
3. Simulation before effects.
4. Prototype before production.
5. Metrics before opinion.
6. Deterministic rules before generative AI.
7. Evidence before declaring success.

## P0 purpose

Prove technical feasibility of the core loop in a small arena before world production, deep crafting, professions, emergent classes, advanced AI, or multiplayer.

P0 is a laboratory, not a vertical slice.

## Authority of rules vs AI

AI may observe, analyze, suggest, simulate, generate candidates, and describe.

AI may not break combat rules, economy, progression, save integrity, item identity, or server authority.

Gameplay truth:

```text
CORE RULES → VALIDATOR → DETERMINISTIC SYSTEMS
```

## Data ownership (P0 spec)

- CORE owns authoritative gameplay definitions.
- ENTITY owns runtime state.
- COMBAT resolves combat outcomes.
- WEAPON owns weapon definitions and instances.
- TELEMETRY observes and records.
- DEBUG observes.
- UI observes.

No UI system may become an authority for gameplay state.

## IDs

Every persistent or runtime-relevant entity has a unique ID of the form `entity_type + unique identifier`. IDs are not derived from display names and stay stable when names change.

## Evidence

A system is done only if implementation, data contract, dependencies, test, passing evidence, and relevant debug visibility exist. Looking correct is not PASS.

## Procedurality

Fundamental systems must not be built in a way that blocks future procedurality. Prefer general rules over content-specific exceptions.

## Generalization

A system that works for one character must be able to work for another compatible character, rig, weapon, animation set, or movement profile without Core exceptions of the form `if character == X`.
