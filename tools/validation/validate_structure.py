#!/usr/bin/env python3
"""Bootstrap 0 structure gate. Not a gameplay test."""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

FOUNDATION = ROOT / "docs/foundation/KashmirAct_Fundacao_v0.1.md"
P0_SPEC = ROOT / "docs/p0/KashmirAct_Prototype0_Specification_v0.1.md"

# Recorded from the Bootstrap 0 input documents.
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

FORBIDDEN_GAMEPLAY_GLOBS = [
    "src/**/*.gd",
    "src/**/*.cs",
    "engine/**/*.tscn",
    "engine/**/*.gd",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
                f"HASH MISMATCH: {path.relative_to(ROOT)} expected {expected} got {actual}"
            )

    for pattern in FORBIDDEN_GAMEPLAY_GLOBS:
        for hit in ROOT.glob(pattern):
            errors.append(f"UNEXPECTED GAMEPLAY FILE: {hit.relative_to(ROOT)}")

    engine = (ROOT / "project/config/engine.json").read_text(encoding="utf-8")
    if '"final_production_decision": false' not in engine:
        errors.append("engine.json must keep Godot as a non-final production decision")

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
    print("  combat/godot gameplay implementation: none")
    print("  core phase 02 (ids/attributes/events): present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
