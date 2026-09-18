# P0 Phase 04 — Motion Primitives

Status: SPECIFICATION

## Objective

Prove that reusable movement primitives can be executed independently and later composed into actions.

## Core Principle

MOVEMENT != ATTACK

A movement primitive is a reusable behavioral unit.

An attack, skill, technique or player-created action is a composition of primitives plus context, rules, timing and effects.

## Runtime Concept

INPUT
→ INTENT
→ ACTION REQUEST
→ PRIMITIVE RESOLUTION
→ LOCOMOTION RESULT
→ ENGINE ADAPTER

## Initial Primitive Set

- Move
- Accelerate
- Decelerate
- Turn
- Step
- Lunge
- Retreat
- Strafe
- Jump
- Stop

## Primitive Contract

Each primitive must expose a data-driven definition containing:

- stable identifier
- duration
- movement parameters
- rotation parameters
- acceleration parameters
- constraints
- tags
- cancellation policy

Execution must receive a request containing:

- primitive identifier
- direction
- intensity
- optional duration override
- execution context

Execution must produce a result containing:

- velocity
- rotation
- displacement
- phase
- completion state
- emitted events

## Architectural Requirements

1. Primitive implementations must not depend on weapons.
2. Primitive implementations must not depend on attacks.
3. Primitive implementations must not depend on player identity.
4. Primitive implementations must not depend on animation.
5. Primitive implementations must not depend on Godot nodes.
6. Primitive definitions must be data-driven.
7. Primitive execution must be deterministic where possible.
8. Content-specific exceptions are forbidden in the primitive core.
9. New weapons must be able to consume existing primitives.
10. New techniques must be able to consume existing primitives.

## Composition Principle

A future action may be represented as:

Primitive A
→ Primitive B
→ Primitive C
→ Primitive D

Example:

LateralStep
→ Turn
→ Lunge
→ Turn

This composition must not require modifications to the primitive implementations.

## Generalization Gate

The primitive system is not considered architecturally validated until:

1. One humanoid implementation executes the primitives.
2. A second structurally different movement profile executes the same primitives.
3. Both use the same primitive contracts.
4. No character-specific branch is added to the primitive core.
5. No weapon-specific branch is added to the primitive core.
6. Headless tests validate the same contracts independently from Godot.

## P0.4 Initial Acceptance

The prototype must demonstrate:

- Step
- Lunge
- Turn
- Strafe

executing independently.

The prototype must demonstrate at least one composition:

Step
→ Turn
→ Lunge

The composition must produce a perceptibly different movement sequence from the individual primitives.

## Non-Goals

This phase does not implement:

- combat
- hit detection
- damage
- weapons
- animation
- IK
- combo system
- skill discovery
- player-created skills
- procedural animation

## Evidence

Required before declaring P0.4 complete:

- unit tests
- generalization tests
- deterministic execution tests
- runtime demonstration
- no content-specific branches
- source-control diff inspection

## Architectural Rule

Adding a new primitive may extend the primitive registry/data set.

Adding a new weapon, attack or technique must not require modification of the primitive core.

## Next Phase

P0.5 — Action System and composition.

The Action System consumes validated primitives and provides the first layer capable of composing player actions.