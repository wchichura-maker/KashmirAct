#!/usr/bin/env python3
"""Run Phase 02 Core tests. Not a Godot / combat harness."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))
sys.path.insert(0, str(ROOT))


def main() -> int:
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"), pattern="test_*.py", top_level_dir=str(ROOT))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.wasSuccessful():
        print("PASS")
        print(f"  tests: {result.testsRun}")
        print("  failures: 0")
        print("  errors: 0")
        return 0
    print("FAIL")
    print(f"  tests: {result.testsRun}")
    print(f"  failures: {len(result.failures)}")
    print(f"  errors: {len(result.errors)}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
