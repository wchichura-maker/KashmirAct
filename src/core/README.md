# Core

Authoritative gameplay definitions and deterministic logic. Core must be callable without UI, VFX, or a renderer (P0 spec §38, §66).

```text
contracts/    interfaces and shared shapes
data/         runtime data types (not content libraries)
events/       immutable event contracts
ids/          entity ID rules
rules/        validators and rule tables
simulation/   deterministic resolvers
```

## ID rule (P0 spec §8)

Format: `entity_type + unique identifier`.

Examples: `player_001`, `enemy_001`, `weapon_sword_001`, `attack_sword_basic_001`, `primitive_swing_001`.

IDs are not derived from display names.

## Forbidden

Core must not import engine UI, scenes, animation assets, or debug drawing.

Bootstrap 0 does not implement these systems. Folders exist to preserve the boundary.
