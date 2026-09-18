# Gaps and unresolved items

Recorded because they are unspecified or explicitly provisional. Do not fill these by invention.

## Provisional decisions (must not be treated as final)

1. Engine: Godot 4.6 for P0 prototyping; Unreal Engine 5 remains a production candidate.
2. Single-player is the first target; multiplayer is future.
3. Open world is not decided for production.
4. Final network architecture is not defined.
5. Final camera format and lock-on are not defined (lock-on is optional in P0).
6. Definitive profession list is not defined.

## Unspecified for Bootstrap 0 / P0

7. License for the repository is not specified.
8. CI workflow is not specified.
9. Exact animation source (placeholder vs temporary production assets) is not chosen.
10. Exact IK solver (`TwoBoneIK3D` vs others) is left to Godot 4.6 capabilities; gameplay must not depend on one solver.
11. Input map in P0 spec §47 is suggested, not architectural.
12. Audio is optional for initial technical validation.
13. Determinism tests allow timestamp differences unless simulation time is controlled.
14. Session/save format beyond `schema_version: "0.1"` is not fully specified.
15. Pattern confidence formula is required to be documented in code when implemented; it does not exist yet.
16. Health / stamina numeric bounds are unspecified in the Foundation and P0 spec. ADR-0011 records laboratory values 0–100 / default 100. Not final balance.
17. Attribute regeneration rates are unspecified. Phase 02 default is `0` until the stamina system (Phase 11) configures them.


## Conflicts identified

18. **Directory tree:** P0 spec §5 is Godot-module shaped (`core/`, `character/`, `weapons/`). Bootstrap 0 requires `src/core` vs `src/game` and engine portability. **Resolution:** mapping in `LAYER_MAP.md`. Both descriptions are preserved. Implementation follows the portable tree.
19. **Development order vs folder creation:** P0 spec §54 starts with Project + Git + architecture (this bootstrap). Later phases must not be pre-implemented as empty systems.

## Not gaps

- P0 non-goals (VR, MMO, crafting, Skill Composer, …) are exclusions, not missing work for this execution.
