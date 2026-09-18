# KashmirAct

KashmirAct is a 3D real-time Action RPG. The player does not simply choose a class. They build, through how they play, the character they become.

This repository is developed **system-first**. Content is a consequence of systems. Prototype 0 (P0) is a technical laboratory, not a production vertical slice.

## Current state

**P0 Phase 03.4.** Core data, entity IDs, immutable events, Rule Validator, input/intent, locomotion, Godot runtime, and the minimum runtime scene are implemented. Interactive movement validation remains the current gate.

P0 must prove this chain:

```text
PLAYER INPUT
â†’ MOVEMENT / INTENT
â†’ MOTION PRIMITIVE
â†’ WEAPON
â†’ ANIMATION / IK
â†’ HIT DETECTION
â†’ DAMAGE
â†’ TELEMETRY
â†’ BEHAVIOR ANALYSIS
â†’ PATTERN DETECTION
```

## Philosophy

- System before content
- Data before UI
- Simulation before effects
- Prototype before production
- Metrics before opinion
- Deterministic rules before generative AI
- Evidence before success claims

Build the system once. Generalize it. Then add content.

## Source of truth

The original documents are preserved unaltered:

| Document | Authority | Path |
|---|---|---|
| Foundation v0.1 | Vision, confirmed vs provisional decisions | [docs/foundation/KashmirAct_Fundacao_v0.1.md](docs/foundation/KashmirAct_Fundacao_v0.1.md) |
| P0 Specification v0.1 | Executable P0 technical spec | [docs/p0/KashmirAct_Prototype0_Specification_v0.1.md](docs/p0/KashmirAct_Prototype0_Specification_v0.1.md) |

Operational constitution: [.kashmir/constitution.md](.kashmir/constitution.md)

Authority, architecture, decisions, and gaps:

- [docs/architecture/AUTHORITY.md](docs/architecture/AUTHORITY.md)
- [docs/architecture/ARCHITECTURE.md](docs/architecture/ARCHITECTURE.md)
- [docs/architecture/DECISIONS.md](docs/architecture/DECISIONS.md)
- [docs/architecture/GAPS.md](docs/architecture/GAPS.md)

## Engine

Godot 4.6 is the **provisional** P0 prototyping engine. It is not a final production decision.

Core rules and data must remain portable. Unreal Engine 5 remains a serious production candidate if animation, motion matching, Control Rig, or physics integration become central bottlenecks.

See [project/config/engine.json](project/config/engine.json).

## Layout

```text
docs/          source-of-truth documents (unaltered originals + architecture notes)
src/core/      engine-independent rules, data, events, IDs, simulation
src/game/      game systems built on Core (not the engine)
src/ui/        development UI only in P0
data/          gameplay definitions (data-driven)
assets/        presentation assets
engine/        engine adapters (Godot first, provisional)
tests/         unit, integration, simulation, generalization
tools/         validation, debug, pipeline
project/       project configuration
.kashmir/      constitution and knowledge graph
```

Core â‰  Game â‰  Data â‰  Assets â‰  Tests â‰  Tools â‰  Engine.

## Out of scope for P0

VR, MMORPG, multiplayer, open-world streaming, professions, deep crafting, full Skill Composer, Discovery Agent, LLM-driven gameplay, procedural world generation, and production art.

## Next

The smallest next step is P0 Phase 03: Player controller â€” input to logical intent â€” still without combat resolution.
