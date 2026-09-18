# Data

Gameplay definitions as data, not as scattered Core conditionals.

Schema version: `"0.1"`.

## Present (Phase 02)

- `rules/entity_types.json` — registered ID prefixes
- `rules/attributes.json` — `attribute_health_001`, `attribute_stamina_001`

Numeric health/stamina bounds (0–100, default 100) are a documented P0 laboratory choice. The spec names the attributes but does not specify magnitudes.

## Not authored yet

- motion primitives: STEP, TURN, SWING
- attacks: ATTACK_A / B / C
- weapon: `sword_001`
- dodge / block / parry definitions
- movement config
