#!/usr/bin/env python3
"""KashmirAct structure gate.

The validator evolves with the active P0 implementation phase.
Fundamental source documents remain immutable; implementation files are
validated according to explicit phase allowances.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

FOUNDATION = ROOT / "docs/foundation/KashmirAct_Fundacao_v0.1.md"
P0_SPEC = ROOT / "docs/p0/KashmirAct_Prototype0_Specification_v0.1.md"

EXPECTED_HASHES = {
    FOUNDATION: "993d0e6d87573719418b7f9f88f0a67a1de654ced4c3cd30db95d5ce8bfd1f16",
    P0_SPEC: "4c457561f9bbee9b63648bfff5b7e4de2f99443b6171034f0f0b86120ab6d351",
}

REQUIRED_PATHS = [
    "README.md",
    ".gitignore",
    ".gdignore",
    "project.godot",
    "docs/foundation/KashmirAct_Fundacao_v0.1.md",
    "docs/p0/KashmirAct_Prototype0_Specification_v0.1.md",
    "docs/p0/phases/PHASE_02.md",
    "docs/p0/phases/PHASE_03.md",
    "docs/architecture/AUTHORITY.md",
    "docs/architecture/ARCHITECTURE.md",
    "docs/architecture/DECISIONS.md",
    "docs/architecture/GAPS.md",
    "docs/architecture/LAYER_MAP.md",
    ".kashmir/constitution.md",
    ".kashmir/knowledge_graph/graph.json",
    "project/config/engine.json",
    "project/config/p0_scope.json",
    "src/core/README.md",
    "src/core/__init__.py",
    "src/core/ids/entity_id.py",
    "src/core/data/attributes.py",
    "src/core/data/catalog.py",
    "src/core/events/bus.py",
    "src/core/rules/validator.py",
    "src/game/README.md",
    "src/ui/README.md",
    "engine/godot/README.md",
    "data/README.md",
    "data/rules/entity_types.json",
    "data/rules/attributes.json",
    "assets/README.md",
    "tests/generalization/README.md",
    "tests/unit/test_ids.py",
    "tests/unit/test_attributes.py",
    "tests/unit/test_events.py",
    "tools/validation/validate_structure.py",
    "tools/validation/run_core_tests.py",
]

REQUIRED_DIRS = [
    "src/core/contracts",
    "src/core/data",
    "src/core/events",
    "src/core/ids",
    "src/core/rules",
    "src/core/simulation",
    "src/game/actors",
    "src/game/characters",
    "src/game/combat",
    "src/game/equipment",
    "src/game/actions",
    "src/game/animation",
    "src/game/enemy",
    "src/game/telemetry",
    "src/game/debug",
    "engine/godot/adapters",
    "data/actions",
    "data/characters",
    "data/equipment",
    "data/rules",
    "assets/characters",
    "assets/weapons",
    "assets/animations",
    "assets/materials",
    "assets/environments",
    "assets/vfx",
    "assets/audio",
    "tests/unit",
    "tests/integration",
    "tests/simulation",
    "tests/generalization",
    "tools/debug",
    "tools/pipeline",
]

# Gameplay implementation remains prohibited inside the portable source tree.
FORBIDDEN_GAMEPLAY_GLOBS = [
    "src/**/*.gd",
    "src/**/*.cs",
]

# Phase 03.3 is the first explicitly authorized Godot runtime slice.
# New Godot gameplay modules must be added to this list only when their
# corresponding phase is architecturally approved.
PHASE_03_ALLOWED_ENGINE_GLOBS = [
    "engine/godot/adapters/input_adapter.gd",
    "engine/godot/characters/input_intent.gd",
    "engine/godot/characters/movement_profile.gd",
    "engine/godot/characters/locomotion_result.gd",
    "engine/godot/characters/locomotion_controller.gd",
    "engine/godot/characters/character_runtime.gd",
    "engine/godot/scenes/main.gd",
    "engine/godot/scenes/main.tscn",
    "engine/godot/characters/heavy_movement_profile.gd",
    "engine/godot/debug/primitive_visual_harness.gd",
    "engine/godot/debug/action_playback_runtime.gd",
    "engine/godot/adapters/primitive_adapter.gd",
    "engine/godot/adapters/primitive_playback_adapter.gd",
    "engine/godot/adapters/primitive_result.gd",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def matches_any(path: Path, patterns: list[str]) -> bool:
    rel = relative(path)
    return any(Path(rel).match(pattern) for pattern in patterns)


def main() -> int:
    errors: list[str] = []

    for rel in REQUIRED_PATHS:
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"MISSING FILE: {rel}")

    for rel in REQUIRED_DIRS:
        path = ROOT / rel
        if not path.is_dir():
            errors.append(f"MISSING DIR: {rel}")

    for path, expected in EXPECTED_HASHES.items():
        if not path.is_file():
            continue

        actual = sha256(path)

        if actual != expected:
            errors.append(
                f"HASH MISMATCH: {path.relative_to(ROOT)} "
                f"expected {expected} got {actual}"
            )

    # Explicitly forbidden implementation classes.
    for pattern in FORBIDDEN_GAMEPLAY_GLOBS:
        for hit in ROOT.glob(pattern):
            errors.append(
                f"UNEXPECTED GAMEPLAY FILE: {hit.relative_to(ROOT)}"
            )

    # Godot runtime scripts are allowed only through the active phase allowlist.
    for hit in ROOT.glob("engine/**/*.gd"):
        if not matches_any(hit, PHASE_03_ALLOWED_ENGINE_GLOBS):
            errors.append(
                f"UNAUTHORIZED GODOT RUNTIME FILE: {hit.relative_to(ROOT)}"
            )

    engine = (
        ROOT / "project/config/engine.json"
    ).read_text(encoding="utf-8")

    if '"final_production_decision": false' not in engine:
        errors.append(
            "engine.json must keep Godot as a non-final production decision"
        )

    if errors:
        print("FAIL")

        for item in errors:
            print(f"  - {item}")

        return 1

    print("PASS")
    print(f"  files checked: {len(REQUIRED_PATHS)}")
    print(f"  dirs checked: {len(REQUIRED_DIRS)}")
    print(f"  foundation sha256: {EXPECTED_HASHES[FOUNDATION]}")
    print(f"  p0 spec sha256: {EXPECTED_HASHES[P0_SPEC]}")
    print("  phase 03.3 Godot runtime allowlist: active")
    print("  unauthorized combat/godot gameplay implementation: none")
    print("  core phase 02 (ids/attributes/events): present")

    return 0


if __name__ == "__main__":
    sys.exit(main())
