#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.game.characters.primitives import (
    PrimitiveComposition,
    PrimitiveDefinition,
    PrimitivePlayback,
    PrimitiveRequest,
    PrimitiveResolver,
)


OUTPUT_DIR = ROOT / "data/actions"


def serialize_result(result) -> dict:
    return {
        "primitive_id": result.primitive_id,
        "velocity": {
            "x": result.velocity_x,
            "y": result.velocity_y,
        },
        "rotation_degrees": result.rotation_degrees,
        "displacement": {
            "x": result.displacement_x,
            "y": result.displacement_y,
        },
        "phase": result.phase,
        "completed": result.completed,
        "events": list(result.events),
    }


def main() -> None:
    step = PrimitiveDefinition(
        primitive_id="primitive_step",
        duration=0.20,
        distance=1.2,
        rotation_degrees=0.0,
        acceleration=10.0,
        constraints=("grounded",),
        tags=("movement", "step"),
        cancellable=True,
    )

    turn = PrimitiveDefinition(
        primitive_id="primitive_turn",
        duration=0.10,
        distance=0.0,
        rotation_degrees=90.0,
        acceleration=0.0,
        constraints=("grounded",),
        tags=("movement", "turn"),
        cancellable=True,
    )

    lunge = PrimitiveDefinition(
        primitive_id="primitive_lunge",
        duration=0.50,
        distance=3.0,
        rotation_degrees=0.0,
        acceleration=20.0,
        constraints=("grounded",),
        tags=("movement", "lunge"),
        cancellable=True,
    )

    catalog = {
        step.primitive_id: step,
        turn.primitive_id: turn,
        lunge.primitive_id: lunge,
    }

    step_request = PrimitiveRequest(
        primitive_id="primitive_step",
        direction_x=0.0,
        direction_y=1.0,
        intensity=1.0,
    )

    step_result = PrimitiveResolver.resolve(
        step,
        step_request,
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    step_output = OUTPUT_DIR / "primitive_step.json"
    step_output.write_text(
        json.dumps(
            serialize_result(step_result),
            indent=2,
        ),
        encoding="utf-8",
    )

    composition = PrimitiveComposition(
        composition_id="composition_step_turn_lunge",
        requests=(
            PrimitiveRequest(
                "primitive_step",
                direction_y=1.0,
            ),
            PrimitiveRequest(
                "primitive_turn",
            ),
            PrimitiveRequest(
                "primitive_lunge",
                direction_y=1.0,
            ),
        ),
    )

    playback = PrimitivePlayback.resolve(
        composition,
        catalog,
    )

    composition_payload = {
        "composition_id": playback.composition_id,
        "completed": playback.completed,
        "total_duration": playback.total_duration,
        "final_rotation_degrees": playback.final_rotation_degrees,
        "steps": [
            {
                "index": step.index,
                "elapsed_before": step.elapsed_before,
                "elapsed_after": step.elapsed_after,
                "result": serialize_result(step.result),
            }
            for step in playback.steps
        ],
    }

    composition_output = (
        OUTPUT_DIR / "composition_step_turn_lunge.json"
    )

    composition_output.write_text(
        json.dumps(
            composition_payload,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(
        "PASS: primitive fixture exported to "
        f"{step_output}"
    )
    print(
        "PASS: composition fixture exported to "
        f"{composition_output}"
    )


if __name__ == "__main__":
    main()