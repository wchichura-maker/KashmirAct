# Game

Game systems sit on Core. They are still engine-portable at the rules level; engine adapters live under `engine/`.

P0-relevant reserved modules:

```text
actors/       generic entity/actor runtime
characters/   character controller, movement, orientation, state
combat/       intent, primitives, attacks, hit detection, damage, stamina, defense
equipment/    weapon definitions and instances (first content: sword)
actions/      action requests distinct from input and from state
animation/    animation driving from gameplay state (not rule authority)
enemy/        deterministic combat test target
telemetry/    observe and record; never mutate gameplay
debug/        observation only
```

Not created here (later prototypes): skills composer, world, professions, economy, full AI layers.
