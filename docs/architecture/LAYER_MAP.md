# Layer map — P0 spec folders → repository layout

The P0 specification recommends a Godot-oriented tree (`core/`, `character/`, `combat/`, `weapons/`, …). Bootstrap 0 uses a portable tree so Core is not coupled to the engine.

This is a mapping, not a silent rewrite of the P0 spec.

| P0 spec (section 5) | Repository location | Notes |
|---|---|---|
| `project.godot` | `/project.godot` | Stub only. Engine choice remains provisional. |
| `.kashmir/constitution.md` | `.kashmir/constitution.md` | Operational constitution. |
| `.kashmir/knowledge_graph/` | `.kashmir/knowledge_graph/` | Seed graph only. |
| `core/rules` | `src/core/rules` | Engine-independent. |
| `core/data` | `src/core/data` + `data/` | Contracts vs content definitions. |
| `core/events` | `src/core/events` | |
| `core/simulation` | `src/core/simulation` | Deterministic resolver seed for P1. |
| `core/session` | reserved; not created yet | P0 save/session comes after Core events. |
| `character/` | `src/game/characters` + `src/game/actors` | Generic actor/character systems, not a single player class. |
| `combat/` | `src/game/combat` | |
| `weapons/` | `src/game/equipment` + `data/equipment` | Weapons are equipment. First content is `sword_001`. |
| `enemy/` | `src/game/enemy` | Deterministic P0 test target. |
| `telemetry/` | `src/game/telemetry` | Observes; does not mutate gameplay. |
| `arena/` | `assets/environments` + future `engine/godot/scenes` | No arena scene in Bootstrap 0. |
| `tools/` | `tools/` | |
| `assets/` | `assets/` | |
| `scenes/p0_main.tscn` | future `engine/godot/scenes/` | Not created. |

Folders required by later prototypes (Skill Composer, professions, world, economy) are **not** created here.
