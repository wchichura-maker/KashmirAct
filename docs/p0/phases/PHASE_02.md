# P0 Phase 02 — Core data + IDs + events

**Status:** PASS (structure + unit + generalization evidence)  
**Gameplay / Godot runtime:** not applicable  
**Combat:** not implemented

## INPUT

P0 spec §7 (attributes), §8 (IDs), §29 (event bus), §37 (validator reason codes), §51 (explicit errors), §54 Phase 02.

## IMPLEMENTATION

- Entity IDs: `{type}_{unique}`, type registry from data, IDs not derived from display names
- AttributeDefinition / AttributeRuntime with the required operations
- Immutable `CoreEvent` + in-memory `EventBus`
- Rule Validator for IDs and attributes; missing primitive/attack/weapon catalogs return UNKNOWN_* instead of guessing
- Data: `data/rules/entity_types.json`, `data/rules/attributes.json`

Python 3 reference only (ADR-0010). No player controller, no scenes, no combat.

## TEST

```text
python3 tools/validation/validate_structure.py
python3 tools/validation/run_core_tests.py
```

## EVIDENCE

Recorded when the commands above print PASS. Covered P0 §43 items: stamina consumption, stamina clamp.

Not covered: hit/miss, block, parry, dodge i-frames, attack validation against a real catalog, telemetry export, pattern detection.

## STATUS

PASS for Phase 02 scope only. P0 as a whole is not PASS.
