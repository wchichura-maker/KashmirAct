# Tests

| Suite | Purpose |
|---|---|
| `unit/` | Isolated Core rules (stamina, damage, validation) |
| `integration/` | Cross-system contracts |
| `simulation/` | Headless combat resolver / determinism |
| `generalization/` | Same Core with Character A and Character B; adding content must not require Core exceptions |

No gameplay tests exist yet because no gameplay code exists. Do not add tests that cannot fail against real logic.

P0 spec §43 lists the minimum tests that must exist before P0 PASS.
