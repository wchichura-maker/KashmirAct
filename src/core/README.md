# Core

Authoritative gameplay definitions and deterministic logic. Core must be callable without UI, VFX, or a renderer (P0 spec §38, §66).

Phase 02 implements a **Python 3 reference** of IDs, attributes, events, and validation. This is not a production language decision and not a Godot replacement. Engine adapters come later.

```text
contracts/    reason codes and VALID / INVALID results
data/         AttributeDefinition, AttributeRuntime, catalog loader
events/       immutable CoreEvent + in-memory bus
ids/          entity ID parse / make
rules/        Rule Validator (IDs, attributes, explicit UNKNOWN_* for missing catalogs)
simulation/   not implemented (Phase 10 / P1 seed)
```

## ID rule (P0 spec §8)

Format: `{entity_type}_{unique}`

Examples: `player_001`, `enemy_001`, `weapon_sword_001`, `attack_sword_basic_001`, `primitive_swing_001`.

IDs are not derived from display names.

## Attributes (P0 spec §7)

P0 definitions in `data/rules/attributes.json`:

- `attribute_health_001`
- `attribute_stamina_001`

Runtime operations: `get_value`, `set_value`, `modify`, `consume`, `regenerate`, `is_empty`, `is_full`.

## Events (P0 spec §29)

Events are frozen after publication. Unknown types are rejected and not stored.

## Forbidden

Core must not import engine UI, scenes, animation assets, or debug drawing.

## Tests

```text
python3 tools/validation/run_core_tests.py
```
