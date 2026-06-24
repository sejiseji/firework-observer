# Decision Log

Use this for lightweight decisions that do not need a full ADR.

## Format

```md
## YYYY-MM-DD Decision title

Decision:
Reason:
Alternatives:
Impact:
```

## 2026-06-23 Protect standalone main.py as reference prototype

Decision:
Treat the standalone `main.py` as a protected reference prototype until its behavior is inspected and a migration strategy is documented.

Reason:
The current good-feeling firework box behavior may exist in `main.py`, while the long-term project structure lives under `src/pyxel_goal_game/`.

Alternatives:
Continue developing `main.py` as the main implementation, or immediately migrate it into the package structure.

Impact:
T0002 must not modify `main.py`. Before T0003 gameplay work, complete `T0002.5` to reconcile the standalone prototype with the package architecture.

## 2026-06-23 Use one-goal-at-a-time staged firework implementation

Decision:
Codex should execute only the next eligible incomplete task from `goals/task_queue.json`, complete validation and logs, then stop. Firework preset work is split into `T0003.0` through `T0003.8` instead of one broad T0003 task.

Reason:
Adding many firework types in one pass risks losing the current good-feeling prototype behavior, mixing environment issues with implementation issues, and making visual regressions hard to isolate.

Alternatives:
Implement several presets in one broad patch, or keep a single vague "implement first deterministic burst preset" task.

Impact:
Future sessions should use `docs/prompts/goal_driven_mode.md`. Presets must be added one at a time after T0002 and T0002.5 are complete.

## 2026-06-23 Treat T0004 as prototype viewpoint migration

Decision:
`T0004` should mean recreating the protected `main.py` viewpoint/camera behavior on the package side, not inventing a new camera feature.

Reason:
The current viewing feel is part of the good prototype behavior that may live in `main.py`. A generic camera task could drift away from that feel.

Alternatives:
Leave T0004 as a vague camera adjustment task, or implement new camera behavior before reconciling `main.py`.

Impact:
T0004 depends on T0002.5 migration notes and should preserve the 256x144 transparent box viewing feel.

## 2026-06-24 Link screen profiles with in-box scenery architecture

Decision:
Document screen profiles and future scenery architecture together before firework preset implementation.

Reason:
Larger landscape profiles change the observation box size, camera focal length, camera distance, UI placement, max particle count, scenery proportions, and render order. Future scenery must exist as static 3D line geometry inside the same observation box as fireworks, so it needs the same box-relative coordinate and projection assumptions.

Alternatives:
Treat screen size as an isolated constant change, or draw scenery as a 2D screen-space background behind the box.

Impact:
`T0002.7` records screen and scenery planning before `T0003.0`. Future work should add `T0002.8` for screen profile configuration and `T0006.*` for staged scenery data and rendering. Scenery must not bypass the `Camera3D` projection pipeline.
