# KASHMIRACT — PROTOTYPE 0 SPECIFICATION
## Version 0.1 — Executable Technical Specification

**Project:** KashmirAct  
**Prototype:** P0 / Prototype 0  
**Status:** Implementation specification  
**Foundation:** KashmirAct_Fundacao_v0.1.md  
**Initial Engine:** Godot 4.6  
**Engine Decision:** Provisional; P0 must preserve portability of the core rules and data architecture  
**Target:** Single-player, third-person, real-time Action RPG technical prototype

---

# 0. PURPOSE

Prototype 0 exists to validate the technical feasibility of the core KashmirAct loop before investment in world production, deep crafting, professions, emergent classes, advanced AI, multiplayer, or final art.

The P0 must prove:

PLAYER INPUT
→ MOVEMENT / INTENT
→ MOTION PRIMITIVE
→ WEAPON
→ ANIMATION / IK
→ HIT DETECTION
→ DAMAGE
→ TELEMETRY
→ BEHAVIOR ANALYSIS
→ PATTERN DETECTION

The prototype is a laboratory, not a vertical slice.

The primary engineering principle is:

> SYSTEM BEFORE CONTENT.

Secondary principles:

- DATA BEFORE UI.
- SIMULATION BEFORE EFFECTS.
- PROTOTYPE BEFORE PRODUCTION.
- METRICS BEFORE OPINION.
- DETERMINISTIC RULES BEFORE GENERATIVE AI.
- EVIDENCE BEFORE SUCCESS CLAIMS.

---

# 1. SOURCE OF TRUTH AND AUTHORITY

The P0 is derived from the KashmirAct Foundation v0.1.

The Foundation establishes:

- third-person 3D;
- real-time combat;
- motion primitives;
- composed abilities;
- deterministic validation;
- behavioral progression;
- combat telemetry;
- procedural hand IK;
- weapon alignment;
- layered animation;
- future discovery systems;
- future item creation;
- future NPC/reputation systems.

P0 implements only the minimum infrastructure required to validate these foundations.

No P0 implementation may silently redefine a Foundation decision.

When a technical decision is not defined by the Foundation, it must be recorded as a provisional P0 decision.

---

# 2. P0 NON-GOALS

The following are explicitly outside P0:

- VR;
- MMORPG;
- multiplayer;
- open-world streaming;
- final world design;
- extensive lore;
- quest system;
- factions;
- complex NPC simulation;
- economy;
- marketplace;
- professions;
- deep crafting;
- item evolution;
- full Skill Composer;
- full Discovery Agent;
- LLM-driven gameplay decisions;
- procedural world generation;
- final character art;
- final VFX;
- final audio;
- large content libraries.

P0 must not grow into an uncontrolled production prototype.

---

# 3. SUCCESS GATE

P0 is PASS only when all mandatory acceptance tests pass.

## 3.1 Core acceptance criteria

1. Player moves in third person.
2. Camera follows and can orient independently.
3. Player attacks with a sword.
4. At least three attacks exist.
5. The three attacks produce mechanically or visually distinguishable results.
6. Dodge works.
7. Block works.
8. Parry works.
9. Stamina is consumed and regenerated.
10. Hit detection is separated from damage calculation.
11. Weapon data is separate from presentation.
12. Hand IK aligns the hand to the weapon.
13. Enemy can attack.
14. Combat is governed by deterministic rules.
15. Combat events generate telemetry.
16. Telemetry can be inspected.
17. A behavioral profile can be generated.
18. Repeated action sequences can be detected.
19. A detected sequence can produce a valid candidate representation.
20. Debug tools expose system state.

## 3.2 Decisive demonstration

The following sequence must be recorded:

DODGE
→ TURN
→ SWING

The system must store it as structured gameplay events.

It must then identify the repeated sequence when sufficient repetitions occur.

The system must be capable of producing:

PATTERN DETECTED
DODGE → TURN → SWING

This does not yet constitute full skill discovery. It validates the infrastructure required for P1.

---

# 4. TECHNICAL ARCHITECTURE

## 4.1 High-level modules

KashmirAct P0:

CORE
├── Rules
├── Data
├── Events
├── Deterministic Simulation
└── Save / Session Data

CHARACTER
├── Controller
├── Movement
├── Orientation
├── State
├── Animation
└── IK

COMBAT
├── Input
├── Intent
├── Motion Primitives
├── Attacks
├── Hit Detection
├── Damage
├── Stamina
└── Combat State

WEAPON
├── Definition
├── Runtime Instance
├── Grip
└── Attack Profile

ENEMY
├── Controller
├── State Machine
├── Combat
└── Targeting

TELEMETRY
├── Event Recorder
├── Session
├── Aggregator
├── Behavior Analyzer
└── Pattern Detector

TOOLS
├── Debug Overlay
├── Hitbox Visualizer
├── IK Visualizer
├── State Inspector
├── Telemetry Viewer
└── Test Harness

ARENA
└── P0 Test Environment

---

# 5. DIRECTORY STRUCTURE

Recommended structure:

KashmirAct/
├── project.godot
├── README.md
├── .gitignore
│
├── .kashmir/
│   ├── constitution.md
│   └── knowledge_graph/
│
├── core/
│   ├── rules/
│   ├── data/
│   ├── events/
│   ├── simulation/
│   └── session/
│
├── character/
│   ├── player/
│   ├── controller/
│   ├── movement/
│   ├── state/
│   ├── animation/
│   └── ik/
│
├── combat/
│   ├── input/
│   ├── intent/
│   ├── primitives/
│   ├── attacks/
│   ├── hit_detection/
│   ├── damage/
│   ├── stamina/
│   └── state/
│
├── weapons/
│   ├── definitions/
│   ├── instances/
│   └── profiles/
│
├── enemy/
│   ├── controller/
│   ├── state/
│   └── combat/
│
├── telemetry/
│   ├── recorder/
│   ├── analysis/
│   └── patterns/
│
├── arena/
│   ├── scenes/
│   ├── environment/
│   └── spawn/
│
├── tools/
│   ├── debug/
│   ├── telemetry/
│   └── tests/
│
├── assets/
│   ├── characters/
│   ├── weapons/
│   ├── animations/
│   ├── materials/
│   └── vfx/
│
└── scenes/
    └── p0_main.tscn

---

# 6. GODOT SCENE ARCHITECTURE

## 6.1 Main scene

p0_main.tscn

Root:

P0Game
├── World
│   ├── Arena
│   ├── Lighting
│   └── Navigation
├── Player
├── Enemy
├── CameraRig
├── Systems
│   ├── CombatSystem
│   ├── TelemetrySystem
│   ├── PatternSystem
│   └── DebugSystem
└── UI
    ├── DebugOverlay
    └── TelemetryPanel

## 6.2 Player

PlayerRoot
├── CharacterBody3D
├── CollisionShape3D
├── Visual
│   └── Skeleton3D
├── AnimationTree
├── WeaponSocket
│   └── Sword
├── IKTargets
│   ├── RightHand
│   ├── LeftHand
│   └── LookTarget
├── Hurtbox
├── StateController
└── PlayerController

The exact node hierarchy may change if required by Godot implementation, but contracts between systems must remain stable.

---

# 7. CORE DATA MODEL

The system must be data-driven.

Gameplay definitions must not depend on hardcoded references to individual animations wherever avoidable.

## 7.1 Attribute data

AttributeDefinition:

- id
- display_name
- min_value
- max_value
- default_value

P0 attributes:

- health
- stamina

## 7.2 Runtime attribute

AttributeRuntime:

- definition_id
- current_value
- max_value
- regeneration_rate

Required operations:

- get_value()
- set_value()
- modify()
- consume()
- regenerate()
- is_empty()
- is_full()

---

# 8. ENTITY IDENTIFIERS

Every persistent or runtime-relevant entity must have a unique ID.

Format:

entity_type + unique identifier.

Examples:

player_001
enemy_001
weapon_sword_001
attack_sword_basic_001
primitive_swing_001

IDs must not be derived from display names.

IDs must remain stable when display names change.

---

# 9. PLAYER CONTROLLER

## 9.1 Responsibilities

PlayerController is responsible for:

- reading player input;
- generating intent;
- requesting movement;
- requesting combat actions;
- requesting dodge;
- requesting block;
- requesting parry.

It must not calculate final damage.

## 9.2 Input abstraction

Raw input must be converted into logical actions.

Logical actions:

MOVE
LOOK
ATTACK
BLOCK
DODGE
JUMP
SPRINT
LOCK_TARGET (optional P0)

The combat layer consumes logical intent rather than hardware-specific events.

---

# 10. CAMERA

## 10.1 Requirements

Third-person camera.

Must support:

- horizontal rotation;
- vertical rotation;
- follow target;
- configurable distance;
- configurable height;
- configurable sensitivity;
- collision avoidance if feasible;
- camera-relative movement.

## 10.2 Camera independence

Camera direction and character facing must be separate concepts.

Required data:

camera_forward
camera_right
movement_vector
character_forward
attack_direction

---

# 11. MOVEMENT SYSTEM

## 11.1 Movement states

IDLE
WALK
RUN
SPRINT
AIRBORNE
DODGE
RECOVERY

## 11.2 Parameters

MovementConfig:

- walk_speed
- run_speed
- sprint_speed
- acceleration
- deceleration
- rotation_speed
- jump_velocity
- gravity
- dodge_speed
- dodge_duration
- dodge_recovery

All values must be configurable data.

## 11.3 Movement intent

MovementIntent:

- direction
- magnitude
- sprint_requested
- jump_requested
- timestamp

The movement system resolves intent into actual velocity.

---

# 12. CHARACTER ORIENTATION

The character must support independent concepts:

- body direction;
- movement direction;
- camera direction;
- target direction;
- weapon direction;
- attack direction.

P0 does not require literal independent bone control.

The body orientation must be sufficient to make attack direction observable.

---

# 13. CHARACTER STATE MACHINE

Minimum states:

NEUTRAL
MOVING
ATTACKING
DODGING
BLOCKING
PARRYING
HIT
RECOVERY
DEAD

State transitions must be explicit.

Every state must define:

- enter;
- update;
- exit;
- permitted actions;
- interrupted actions;
- movement behavior.

No state may rely exclusively on animation name to determine gameplay state.

---

# 14. MOTION PRIMITIVE SYSTEM

Motion primitives are reusable gameplay components.

## 14.1 P0 primitives

Primitive 001:
STEP

Primitive 002:
TURN

Primitive 003:
SWING

## 14.2 Primitive schema

MotionPrimitive:

- id
- type
- duration
- movement_delta
- rotation_delta
- stamina_cost
- interruptible
- animation_reference
- tags
- conditions

## 14.3 Primitive execution

PrimitiveExecutor:

validate()
start()
update()
complete()
interrupt()

The executor must emit events:

PRIMITIVE_STARTED
PRIMITIVE_COMPLETED
PRIMITIVE_INTERRUPTED

---

# 15. ATTACK SYSTEM

An attack is a composition of stages.

Minimum conceptual pipeline:

TRIGGER
→ PREPARATION
→ MOVEMENT
→ WEAPON
→ EFFECT
→ IMPACT
→ RECOVERY

P0 may simplify stages, but the data architecture must preserve them.

## 15.1 AttackDefinition

Fields:

- id
- display_name
- primitive_sequence
- weapon_requirements
- stamina_cost
- startup_duration
- active_duration
- recovery_duration
- hitbox_profile
- damage_profile
- interrupt_rules
- tags

## 15.2 P0 attacks

ATTACK_A:
SWING

ATTACK_B:
STEP → SWING

ATTACK_C:
TURN → SWING

The exact animation may be reused during early development, but gameplay data must distinguish the attacks.

---

# 16. ATTACK PHASES

Minimum runtime phases:

IDLE
STARTUP
ACTIVE
RECOVERY
CANCELLED

Only ACTIVE may apply hit detection unless explicitly configured otherwise.

Telemetry must record phase transitions.

---

# 17. WEAPON SYSTEM

## 17.1 Weapon definition

WeaponDefinition:

- id
- type
- weight
- length
- balance
- durability
- damage_base
- attack_profile
- grip_profile
- animation_profile

## 17.2 Runtime weapon

WeaponInstance:

- unique_id
- definition_id
- owner_id
- condition
- created_at
- modifiers

P0 may keep condition and modifiers inactive, but the schema should exist.

## 17.3 Sword

Required first weapon:

sword_001

It must have:

- visible mesh;
- collision/hit representation;
- grip point;
- weapon root;
- weapon direction;
- attack profile.

---

# 18. WEAPON ALIGNMENT

Weapon alignment must expose:

- grip transform;
- weapon origin;
- weapon forward;
- weapon tip;
- weapon base.

The weapon must follow the designated hand/socket.

The system must permit later replacement of the sword without rewriting the character controller.

---

# 19. HAND IK

## 19.1 Objective

Validate procedural hand alignment.

P0 requirement:

The primary hand must remain aligned to the weapon grip during combat.

## 19.2 IK inputs

- skeleton;
- hand target;
- pole/constraint where applicable;
- weapon grip transform;
- IK weight.

## 19.3 IK states

DISABLED
BLEND_IN
ACTIVE
BLEND_OUT

## 19.4 Acceptance

Move or rotate the weapon and verify that the hand follows correctly.

The IK implementation may use the capabilities available in Godot 4.6, but the gameplay layer must not depend on a specific IK implementation.

---

# 20. ANIMATION ARCHITECTURE

P0 uses:

BASE LOCOMOTION
→ COMBAT MOTION
→ PROCEDURAL IK
→ WEAPON ALIGNMENT
→ SECONDARY MOTION

AnimationTree should manage blending where practical.

Gameplay state must drive animation parameters.

Animation must not become the authoritative source of combat rules.

---

# 21. HIT DETECTION

## 21.1 Separation

Hit detection and damage calculation must be separate systems.

HitDetection:

- identifies collision;
- identifies attacker;
- identifies target;
- identifies attack;
- identifies contact point;
- identifies contact timing.

DamageResolver:

- receives a valid hit;
- calculates damage;
- produces CombatResult.

## 21.2 Hit event

HitEvent:

- event_id
- timestamp
- attacker_id
- target_id
- attack_id
- weapon_id
- position
- direction
- phase

---

# 22. DAMAGE SYSTEM

P0 formula:

damage = base_damage × attack_multiplier

Optional modifiers may be supported but should remain minimal.

DamageResolver must be deterministic for identical inputs.

CombatResult:

- hit
- damage
- blocked
- parried
- interrupted
- target_health_after

---

# 23. DODGE

DodgeDefinition:

- duration;
- direction_source;
- speed;
- stamina_cost;
- invulnerability_window;
- recovery_duration.

The dodge direction must be derived from movement input when available.

If no movement input exists, use character/camera-relative fallback.

Telemetry must record:

DODGE_STARTED
DODGE_COMPLETED
DODGE_SUCCESS
DODGE_FAILURE

---

# 24. BLOCK

BlockDefinition:

- stamina_cost_per_event or per_second;
- damage_reduction;
- movement_multiplier;
- allowed_attacks;
- interrupt_rules.

P0 block may use a constant damage reduction.

---

# 25. PARRY

ParryDefinition:

- startup;
- active_window;
- recovery;
- stamina_cost;
- successful_response.

A successful parry must produce a deterministic result.

Example:

Player parry active
+
Enemy attack contact
=
Enemy interrupted.

Telemetry must distinguish attempted and successful parries.

---

# 26. STAMINA SYSTEM

P0 uses stamina for:

- sprint;
- dodge;
- attack;
- block/parry where configured.

Stamina must:

- consume;
- regenerate;
- clamp to [0, max];
- prevent actions when insufficient.

No floating-point drift should cause invalid values.

---

# 27. ENEMY SYSTEM

P0 enemy is a deterministic combat test target.

## 27.1 States

IDLE
DETECT
APPROACH
ATTACK
RECOVER
HIT
BLOCK
PARRY
DEAD

## 27.2 Enemy requirements

- detect player;
- approach player;
- attack;
- receive damage;
- react to dodge/block/parry;
- die.

No sophisticated behavior tree is required.

---

# 28. ENEMY ATTACK

Enemy attack must have:

- telegraph;
- startup;
- active;
- recovery.

The timing must be deterministic.

The enemy must generate the same attack profile under the same conditions.

---

# 29. COMBAT EVENT BUS

Combat systems communicate through events.

Required events:

INPUT_ACTION
MOVEMENT_STARTED
MOVEMENT_STOPPED
PRIMITIVE_STARTED
PRIMITIVE_COMPLETED
ATTACK_STARTED
ATTACK_ACTIVE
ATTACK_HIT
ATTACK_MISSED
DODGE_STARTED
DODGE_COMPLETED
BLOCK_STARTED
BLOCK_HIT
PARRY_STARTED
PARRY_SUCCESS
PARRY_FAILURE
DAMAGE_APPLIED
ENTITY_DIED
STAMINA_CHANGED

Events must be immutable after publication.

---

# 30. TELEMETRY SYSTEM

Telemetry is mandatory.

## 30.1 Event structure

CombatTelemetryEvent:

- event_id
- session_id
- timestamp
- actor_id
- target_id
- event_type
- action_id
- primitive_id
- attack_id
- weapon_id
- position
- direction
- distance_to_target
- stamina_before
- stamina_after
- result

Fields may be null when irrelevant.

## 30.2 Storage

P0 should support:

- in-memory session;
- JSON export.

Example:

telemetry/session_YYYYMMDD_HHMMSS.json

---

# 31. TELEMETRY RECORDER

Responsibilities:

start_session()
record_event()
end_session()
export_session()

The recorder must never modify gameplay state.

It observes gameplay.

---

# 32. BEHAVIOR ANALYZER

The first version must be deterministic/statistical.

No LLM is required.

Input:

telemetry events.

Output:

BehaviorProfile.

Fields:

- aggression;
- mobility;
- defense_usage;
- dodge_frequency;
- parry_frequency;
- block_frequency;
- attack_frequency;
- preferred_weapon;
- preferred_range;
- repeated_sequences.

Values should be normalized where practical to [0,1].

---

# 33. BEHAVIOR PROFILE

Example:

{
  "aggression": 0.72,
  "mobility": 0.91,
  "defense_usage": 0.38,
  "dodge_frequency": 0.66,
  "parry_frequency": 0.41,
  "preferred_range": 1.7,
  "preferred_weapon": "sword_001"
}

The profile is descriptive.

It must not directly modify character attributes in P0.

---

# 34. PATTERN DETECTOR

P0 implements a lightweight sequential pattern detector.

Input:

ordered primitive/action events.

Example:

DODGE
TURN
SWING

Repeated sequences should be counted.

Minimum detection requirements:

- sequence length: 2–5 events;
- minimum repetitions: configurable;
- ignore irrelevant telemetry;
- preserve ordering;
- distinguish actor;
- provide occurrence count.

Output:

PatternCandidate:

- pattern_id;
- sequence;
- occurrences;
- confidence;
- first_seen;
- last_seen.

---

# 35. PATTERN CONFIDENCE

P0 confidence may use a simple deterministic formula based on:

- occurrence count;
- consistency;
- total action count;
- sequence rarity.

The formula must be documented in code.

No generative model may determine validity.

---

# 36. MOCK DISCOVERY CANDIDATE

When a pattern crosses the configured threshold:

PatternDetector emits:

PATTERN_DETECTED

Example:

DODGE → TURN → SWING

CandidateGenerator creates:

candidate_001

with:

- source_pattern_id;
- primitive_sequence;
- estimated duration;
- estimated stamina;
- source telemetry references.

P0 stops here.

Simulation and persistent skill discovery belong to P1.

---

# 37. RULE VALIDATOR

The Rule Validator is mandatory even in P0.

It validates:

- valid primitive IDs;
- valid attack IDs;
- valid weapon requirements;
- stamina feasibility;
- duration validity;
- parameter bounds.

Result:

VALID
or
INVALID + reason codes.

Example reason codes:

UNKNOWN_PRIMITIVE
INVALID_SEQUENCE
NEGATIVE_DURATION
INVALID_STAMINA_COST
MISSING_WEAPON_REQUIREMENT

---

# 38. DETERMINISTIC SIMULATION CORE

P0 must separate rules from visual presentation.

A future simulation layer will allow candidate testing without rendering.

P0 minimum implementation:

CombatResolver must be callable without depending on UI or VFX.

Example:

resolve_attack(attacker_state, attack_definition, weapon_definition, target_state)

returns CombatResult.

This is the architectural seed for the P1 combat simulator.

---

# 39. SAVE / SESSION MODEL

P0 does not require a full production save system.

It must support export of:

- player session;
- telemetry;
- behavior profile;
- detected patterns.

The data format should be versioned.

Example:

schema_version: "0.1"

---

# 40. DEBUG SYSTEM

Debug mode must be globally toggleable.

Required visualizations:

F1 — hitboxes
F2 — hurtboxes
F3 — IK
F4 — collision
F5 — character state
F6 — telemetry
F7 — motion primitives
F8 — stamina
F9 — attack phase
F10 — weapon trajectory

Keys are provisional and may change.

The important requirement is that every core system be observable.

---

# 41. DEBUG OVERLAY

Minimum display:

FPS
Frame time
Player state
Current primitive
Current attack
Attack phase
Stamina
Health
Target
Distance
Last hit
Last damage
IK state
Telemetry event count
Detected patterns

---

# 42. WEAPON TRAJECTORY DEBUG

When enabled, display:

- weapon root;
- weapon base;
- weapon tip;
- sampled trajectory;
- active hit window.

This is mandatory for diagnosing combat quality.

---

# 43. TEST HARNESS

P0 must include automated tests where practical.

Minimum tests:

1. stamina consumption;
2. stamina clamp;
3. damage calculation;
4. hit/miss;
5. block reduction;
6. parry timing;
7. dodge invulnerability;
8. primitive validation;
9. attack validation;
10. telemetry recording;
11. behavior aggregation;
12. sequence detection.

---

# 44. DETERMINISM TEST

Run identical input sequences twice.

Expected:

- same state transitions;
- same stamina values;
- same hit results;
- same damage;
- same telemetry event types/order;
- same detected pattern.

Timestamps may differ unless simulation time is explicitly controlled.

---

# 45. P0 ARENA

The arena should be intentionally simple.

Requirements:

- flat navigable floor;
- enough space for combat;
- walls or simple obstacles;
- lighting sufficient to inspect animation;
- neutral background;
- spawn point for player;
- spawn point for enemy.

No environment art production is required.

---

# 46. CONTENT REQUIREMENT

Minimum assets:

1 humanoid player
1 humanoid enemy
1 sword
basic animations for:

idle
walk
run
sprint
attack
dodge
block
parry
hit
death

Animations may be placeholder or sourced from temporary production assets.

The prototype must prioritize system behavior over visual quality.

---

# 47. P0 INPUT MAP

Suggested mapping:

WASD — movement
Mouse — camera
LMB — attack
RMB — block
Space — dodge
Shift — sprint
Q — parry
F1–F10 — debug

The exact mapping is not part of the gameplay architecture.

---

# 48. FRAME / UPDATE RESPONSIBILITIES

Gameplay systems should avoid unnecessary per-frame global work.

Suggested responsibility:

Input:
per frame

Movement:
physics tick

Combat:
physics/gameplay tick

Hit detection:
combat active windows

Telemetry:
event-driven

Behavior analysis:
session or periodic batch

Pattern detection:
event-driven or batched

Debug:
frame/render update

---

# 49. DATA OWNERSHIP

Rules:

CORE owns authoritative gameplay definitions.

ENTITY owns runtime state.

COMBAT resolves combat outcomes.

WEAPON owns weapon definitions and instances.

TELEMETRY observes and records.

DEBUG observes.

UI observes.

No UI system may become an authority for gameplay state.

---

# 50. DEPENDENCY RULES

Allowed:

UI → systems
Debug → systems
Telemetry → events
Combat → Core
Character → Core
Weapon → Core
Enemy → Combat/Core

Forbidden:

Core → UI
Core → Debug
Combat rules → UI
Telemetry → gameplay mutation
Animation → damage authority
VFX → gameplay authority

---

# 51. ERROR HANDLING

Every validation failure must produce an explicit reason.

Never silently fall back from invalid gameplay data.

Development builds should log:

ERROR
WARNING
INFO

Critical gameplay errors must include:

system
entity
operation
data ID
reason

---

# 52. LOGGING

Required categories:

CORE
CHARACTER
MOVEMENT
COMBAT
WEAPON
ANIMATION
IK
ENEMY
TELEMETRY
PATTERN
TEST

Logging must be configurable.

Production-style builds should permit disabling verbose debug logs.

---

# 53. PERFORMANCE TARGET

P0 is not a final performance benchmark.

However, the target should be:

stable real-time gameplay in the test arena;

minimal avoidable allocations during combat;

event recording should not create noticeable frame spikes;

debug visualizations may be more expensive and can be disabled.

Performance measurements must be recorded rather than judged subjectively.

---

# 54. DEVELOPMENT ORDER

Implementation must follow this order unless evidence requires a documented deviation.

PHASE 01
Project + Git + architecture

PHASE 02
Core data + IDs + events

PHASE 03
Player controller

PHASE 04
Camera

PHASE 05
Movement

PHASE 06
Weapon data + sword

PHASE 07
Motion primitives

PHASE 08
Attack system

PHASE 09
Hit detection

PHASE 10
Damage

PHASE 11
Stamina

PHASE 12
Dodge

PHASE 13
Block

PHASE 14
Parry

PHASE 15
Enemy

PHASE 16
Animation

PHASE 17
IK

PHASE 18
Telemetry

PHASE 19
Behavior analyzer

PHASE 20
Pattern detector

PHASE 21
Debug tools

PHASE 22
Automated tests

PHASE 23
P0 validation

PHASE 24
Minimal polish

---

# 55. IMPLEMENTATION GATES

Every phase must have:

INPUT
IMPLEMENTATION
TEST
EVIDENCE
STATUS

Allowed status:

NOT_STARTED
IN_PROGRESS
BLOCKED
PASS
FAIL

A phase cannot be marked PASS because the code "looks correct."

PASS requires observable evidence.

---

# 56. MINIMUM VERTICAL SYSTEM

Before polishing, the following must work end-to-end:

Player
→ moves
→ equips sword
→ performs attack
→ primitive executes
→ animation executes
→ IK aligns hand
→ hitbox activates
→ enemy is hit
→ damage is resolved
→ telemetry is recorded.

Only after this chain works should defense and behavioral analysis be added.

---

# 57. P0 TEST SCENARIOS

## T01 — Basic Movement

Input:
WASD

Expected:
player moves correctly relative to camera.

## T02 — Camera Independence

Rotate camera without movement.

Expected:
camera rotates independently from movement intent.

## T03 — Basic Attack

Input:
LMB

Expected:
attack begins, active window occurs, recovery occurs.

## T04 — Attack Hit

Enemy within hit range.

Expected:
damage applied exactly once.

## T05 — Attack Miss

Enemy outside hit range.

Expected:
no damage.

## T06 — Dodge

Enemy attacks during dodge invulnerability.

Expected:
no damage.

## T07 — Block

Enemy hits during block.

Expected:
damage reduced according to BlockDefinition.

## T08 — Parry

Enemy hits during parry active window.

Expected:
enemy interrupted.

## T09 — IK

Change weapon transform.

Expected:
hand follows grip.

## T10 — Telemetry

Perform attack.

Expected:
events recorded.

## T11 — Pattern

Repeat:

DODGE → TURN → SWING

Expected:
pattern detected after threshold.

## T12 — Determinism

Replay identical sequence.

Expected:
identical gameplay results.

---

# 58. TELEMETRY EXAMPLE

Example session:

{
  "schema_version": "0.1",
  "session_id": "session_001",
  "events": [
    {
      "event_type": "DODGE_STARTED",
      "actor_id": "player_001"
    },
    {
      "event_type": "PRIMITIVE_STARTED",
      "primitive_id": "turn_001",
      "actor_id": "player_001"
    },
    {
      "event_type": "ATTACK_STARTED",
      "attack_id": "attack_003",
      "actor_id": "player_001"
    }
  ]
}

Exact serialization implementation may differ.

---

# 59. PATTERN EXAMPLE

Input sequence:

DODGE
TURN
SWING

Repeated 8 times.

Output:

{
  "pattern_id": "pattern_001",
  "sequence": [
    "DODGE",
    "TURN",
    "SWING"
  ],
  "occurrences": 8,
  "confidence": 0.92
}

Confidence formula must be deterministic and documented.

---

# 60. CANDIDATE EXAMPLE

Pattern:

DODGE → TURN → SWING

Candidate:

{
  "candidate_id": "candidate_001",
  "source_pattern_id": "pattern_001",
  "sequence": [
    "DODGE",
    "TURN",
    "SWING"
  ],
  "status": "VALID"
}

This candidate is not yet a permanent skill.

---

# 61. P0 UI

Only a development UI is required.

No final HUD.

Minimum:

Health
Stamina
Current state
Current attack
Target
Telemetry count
Detected pattern notification

Example:

PATTERN DETECTED
DODGE → TURN → SWING
Occurrences: 8

---

# 62. P0 ART DIRECTION

Visuals are temporary.

Priorities:

1. silhouette readability;
2. animation readability;
3. weapon readability;
4. hit readability;
5. IK visibility;
6. system debugging.

Do not invest in final shaders, environment dressing, or cinematic presentation.

---

# 63. AUDIO

Audio is optional for initial technical validation.

If implemented:

- attack;
- hit;
- block;
- parry;
- dodge;
- death.

Audio must not be required for gameplay correctness.

---

# 64. VFX

Minimal VFX only.

Required if used:

- hit confirmation;
- block;
- parry.

VFX must be triggered from gameplay events.

Gameplay must never be triggered by VFX completion.

---

# 65. FUTURE COMPATIBILITY

P0 architecture must anticipate:

P1:
Ability Composer
Skill Graph
Candidate Generator
Combat Simulator
Discovery Agent

P2:
Blacksmith
Materials
Blueprints
Quality
Item Identity
Item History

P3:
Multiple styles
Emergent archetypes
NPC
Reputation

The P0 should therefore avoid hardcoding assumptions such as:

- one attack per weapon;
- one animation per attack;
- one fixed character class;
- one fixed material;
- one fixed weapon;
- one fixed ability tree.

---

# 66. ENGINE PORTABILITY

Core gameplay definitions and deterministic logic should be isolated enough that an eventual migration to Unreal or another engine is technically conceivable.

This does not require engine abstraction for every Godot API.

It requires avoiding unnecessary coupling of core game rules to:

- scene presentation;
- UI;
- animation assets;
- rendering;
- editor-only systems.

---

# 67. AI POLICY IN P0

No generative AI is authoritative.

AI may be used for:

- development assistance;
- code assistance;
- analysis tooling;
- documentation;
- optional candidate suggestions.

Gameplay truth remains:

CORE RULES
→ VALIDATOR
→ DETERMINISTIC SYSTEMS

The future Discovery Agent must operate under this hierarchy.

---

# 68. P0 DEVELOPMENT AGENT REQUIREMENTS

When Kashmir AI Studio assists development, it must:

1. inspect the real project state before modification;
2. never assume file structure;
3. make minimal changes;
4. validate that an edit was actually applied;
5. test after modifications;
6. compare creation/update/removal contracts;
7. use objective evidence before declaring success;
8. avoid repeating previously identified implementation errors;
9. preserve the Project Constitution;
10. document architectural decisions.

---

# 69. SOURCE CONTROL

Every meaningful milestone should be committed.

Suggested milestones:

p0-00-project
p0-01-core
p0-02-player
p0-03-movement
p0-04-combat
p0-05-weapon
p0-06-defense
p0-07-enemy
p0-08-ik
p0-09-telemetry
p0-10-pattern
p0-11-tests
p0-12-validation

Commit messages should describe what changed, not merely "update."

---

# 70. ISSUE CLASSIFICATION

Issues must be classified:

P0-BLOCKER
P0-CRITICAL
P0-MAJOR
P0-MINOR
P0-TOOLING
P0-POLISH

Blockers prevent prototype validation.

Polish must never delay architectural validation unless it affects readability or debugging.

---

# 71. DEFINITION OF DONE

A system is DONE only if:

- implementation exists;
- data contract exists;
- dependencies are known;
- test exists;
- test passes;
- debug visibility exists where relevant;
- no known blocker remains;
- evidence is recorded.

---

# 72. P0 FINAL DEMONSTRATION

The final P0 demonstration should be a continuous recording/session showing:

1. arena;
2. player movement;
3. camera;
4. sword;
5. three attacks;
6. dodge;
7. block;
8. parry;
9. enemy;
10. hit detection;
11. stamina;
12. IK;
13. debug overlays;
14. telemetry;
15. behavior profile;
16. repeated DODGE → TURN → SWING;
17. pattern detection;
18. candidate generation;
19. automated test results.

---

# 73. FINAL P0 GATE

P0 PASS requires:

CORE:
PASS

CHARACTER:
PASS

MOVEMENT:
PASS

COMBAT:
PASS

WEAPON:
PASS

ANIMATION:
PASS

IK:
PASS

ENEMY:
PASS

TELEMETRY:
PASS

BEHAVIOR:
PASS

PATTERN:
PASS

DEBUG:
PASS

TESTS:
PASS

DETERMINISM:
PASS

If any core category is FAIL, P0 is not complete.

---

# 74. P0 OUTPUTS

The completed P0 must produce:

1. runnable Godot project;
2. source code;
3. data definitions;
4. P0 arena;
5. player;
6. enemy;
7. sword;
8. animation setup;
9. IK setup;
10. telemetry JSON export;
11. behavior profile output;
12. pattern detector output;
13. automated test report;
14. debug tools;
15. P0 validation report;
16. updated project knowledge graph;
17. documented provisional technical decisions.

---

# 75. TRANSITION TO P1

P1 may begin only after the P0 Gate is PASS.

P1 will extend:

Motion Primitive
→ Ability Composition
→ Candidate Generation
→ Simulation
→ Validation
→ Discovery

The Foundation defines P1 as the stage for:

- Ability Composer;
- Skill Graph;
- Candidate Generator;
- Combat Simulator;
- Discovery Agent.

P0 must not prematurely implement the full P1 system.

---

# 76. FINAL ARCHITECTURAL PRINCIPLE

KashmirAct P0 is successful when it demonstrates that gameplay can be represented as composable, observable, deterministic systems.

The fundamental chain is:

PLAYER ACTION
→ INTENT
→ MOTION
→ WEAPON
→ ANIMATION
→ IK
→ COLLISION
→ RESULT
→ TELEMETRY
→ BEHAVIOR
→ PATTERN

The prototype is not trying to prove that KashmirAct is already a complete RPG.

It is trying to prove that the technical foundation can support the future game.

> The system must be capable of explaining what the player did, why the game produced a result, and how that behavior can become data for future discovery.

**END OF SPECIFICATION**
