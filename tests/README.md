# Tests

| Suite | Purpose |
|---|---|
| `unit/` | Isolated Core rules (IDs, attributes, events, validator) |
| `integration/` | Cross-system contracts (empty until systems exist) |
| `simulation/` | Headless combat resolver / determinism (not yet) |
| `generalization/` | Same Core with different actors; adding a type must not require Core edits |

Run:

```text
python3 tools/validation/run_core_tests.py
```

Godot / combat runtime tests do not apply until those systems exist.

P0 spec §43 items covered now: stamina consumption, stamina clamp. The rest wait for later phases.
