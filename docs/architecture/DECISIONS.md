# Architectural decisions — Bootstrap 0

Status values: `confirmed` (Foundation), `provisional` (explicitly not final), `bootstrap` (this execution, required to start P0).

## ADR-0001 — Engine for P0

- **Status:** provisional
- **Decision:** Godot 4.6 is the P0 prototyping platform.
- **Not decided:** production engine. Unreal Engine 5 remains a candidate.
- **Source:** Foundation v0.1 §35–36, P0 spec §1 and §66.
- **Constraint:** core rules and data architecture stay portable.

## ADR-0002 — Layered repository layout

- **Status:** bootstrap
- **Decision:** Core ≠ Game ≠ Data ≠ Assets ≠ Tests ≠ Tools ≠ Engine.
- **Why:** P0 spec directory is Godot-shaped; Foundation requires engine portability. Bootstrap 0 maps P0 modules onto a portable tree (see `LAYER_MAP.md`).
- **Not decided:** final Godot scene hierarchy.

## ADR-0003 — Source documents are immutable originals

- **Status:** bootstrap
- **Decision:** Foundation v0.1 and P0 spec v0.1 live unaltered under `docs/`. Architecture notes interpret; they do not replace.

## ADR-0004 — Input ≠ Action ≠ State

- **Status:** confirmed as architecture, not implemented
- **Decision:** raw input converts to logical intent. Actions, transitions, states, and components remain distinct.
- **Source:** P0 spec §9, Bootstrap 0 action architecture.

## ADR-0005 — Data-driven gameplay definitions

- **Status:** confirmed as architecture, not implemented
- **Decision:** prefer data for costs, timings, profiles, requirements, and constraints. Do not hardcode the first character, weapon, or animation as Core exceptions.
- **Source:** Foundation §43, P0 spec §7, §18, §66.

## ADR-0006 — P0 is a laboratory

- **Status:** confirmed
- **Decision:** P0 proves the technical chain. It is not a vertical slice, MMO, or content production phase.
- **Source:** P0 spec §0, §2.

## ADR-0007 — AI is not gameplay authority

- **Status:** confirmed
- **Decision:** generative AI may assist development. It must not determine combat rules, validation, or discovery validity. Rule Validator remains mandatory.
- **Source:** Foundation §32–33, P0 spec §67.

## ADR-0008 — Deferred folders

- **Status:** bootstrap
- **Decision:** do not create `skills/`, `world/`, `professions/`, `economy/`, or other P1–P3 trees until those prototypes start.
- **Why:** YAGNI. Empty trees are not architecture.

## ADR-0009 — Godot project stub at repository root

- **Status:** bootstrap / provisional engine binding
- **Decision:** `project.godot` lives at repo root so the P0 engine can open the project. `.gdignore` excludes docs/tests/tools.
- **Not implemented:** scenes, autoloads, input map, main scene.
