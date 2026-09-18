# Engine layer

Godot 4.6 is the provisional P0 engine. This folder holds adapters so Core and Game do not import engine presentation types.

```text
ENGINE LAYER
    ↓
ADAPTERS        engine/godot/adapters/
    ↓
GAME SYSTEMS    src/game/
    ↓
CORE / DATA     src/core/  data/
```

`project.godot` remains at the repository root because that is how Godot opens a project. That file is a stub, not a production engine decision.
