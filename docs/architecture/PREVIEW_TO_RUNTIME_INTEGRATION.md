# Preview To Runtime Integration

This document defines the contract for promoting the first-generation manual preview into the package runtime.

The goal is not to copy `tools/preview_firework_box.py` into production. The goal is to extract the stable behavior proven by the preview into package-side runtime modules while keeping the preview available as a development harness and regression viewer.

## Why Integrate Now

The manual preview has reached the intended first-generation visual direction. It now contains the core observation-box feel, mature firework presets, CITY staging, shell launch visuals, interior stars, glitter residue, random/salvo show controls, and camera comfort tuning.

Further stable behavior should not remain trapped in `tools/preview_firework_box.py`. Runtime work should promote those behaviors into `src/pyxel_goal_game/` in small package-side slices.

The protected standalone `main.py` remains a reference prototype. This integration does not authorize modifying it.

## Frozen First-Generation Feature Set

The first official runtime should preserve these preview-proven behaviors:

- `classic` remains the default profile.
- `iphone16_balanced` remains the primary portrait visual target: screen `236x512`, box `120x260x120`.
- The scene is a 3D cuboid observation box using package-side `Camera3D` and `WireBox` projection.
- Firework presets are Kiku, Ring, Spiral, Willow, Peony, Multi-ring, Senrin, and Halo.
- Rising launch objects are firework shells, not rockets.
- Firework shells use the short white/yellow/brown shell tail, not a full launch-to-current path line.
- Primary burst radius uses the compact 80% scale and deterministic bounded wobble.
- Trail eligibility decisions use pre-radius-scale speed.
- Glitter residue is short-lived, sparse, and visually secondary.
- CITY is the active scenery direction alongside EMPTY.
- CITY includes 48 building cuboids, central boulevard, grounded tower, ferris wheel, signs, sparse windows, and the two-blue interleaved building color pattern.
- Building bottom-face perimeter edges remain omitted so buildings feel grounded into the cut floor plane.
- Interior stars attach to the top face and upper side faces only.
- Top-face star visibility is relaxed for shallow viewing angles.
- Side-face star visibility remains stricter.
- Stars are not drawn on exterior-facing surfaces.
- Auto rotate has slow, normal, and fast modes with reduced speed-dependent pitch sway.
- Existing development controls remain available for parity review: sequential cycle, random firework type, single launch, auto launch, persistent 1-5 salvos, random-count salvo, height variation, scenery toggle, star toggle, auto rotate, rotate speed, debug HUD, manual rotation, and zoom.

## Explicitly Postponed

These are intentionally outside the first runtime promotion:

- UFO ambient events.
- New firework presets beyond Halo.
- Ferris wheel animation.
- Gameplay scoring.
- Conversation, story, or event systems.
- Combat, collection, objective, or win/lose loops.
- Mobile-specific deployment.
- Main `main.py` handoff.
- Sound, unless a later task explicitly stabilizes it.

## Preview-Only Versus Runtime

The preview remains useful and should not be deleted or made dependent on production-only entrypoints. It should become a development harness that can compare runtime behavior against the first-generation visual target.

Preview-only concerns may include:

- Debug HUD text.
- Manual visual stress workflows.
- Capture/smoke-only hooks.
- Extra inspection controls that are not required by the release runtime.

Runtime should not import `tools/preview_firework_box.py`. Shared behavior must move into package modules.

## Extraction Targets

Existing pure package modules should remain shared foundations:

- `screen_profiles.py`
- `camera3d.py`
- `wire_box.py`
- `firework_presets.py`
- `firework_bursts.py`
- `salvo_patterns.py`
- `scenery_presets.py`
- `ambient_box_stars.py`

Preview-local behavior to promote includes:

- Active runtime state for shells, particles, secondary bursts, glitter residue, salvos, toggles, and selected firework type.
- Shell launch scheduling, height variation, random type selection, and persistent salvo behavior.
- Camera auto-rotate modes and speed-dependent pitch sway.
- Rendering order for box, interior stars, CITY, shells, particles, glitter residue, front box edges, and HUD.
- Pyxel input mapping for development controls.

`T0005.1` introduced the first package-side scaffold:

- `src/pyxel_goal_game/runtime/__init__.py`
- `src/pyxel_goal_game/runtime/state.py`
- `src/pyxel_goal_game/runtime/show_controller.py`

This scaffold is Pyxel-independent and import-safe. It models selected profile, selected firework kind, active scenery, first-generation toggles, salvo count mode, auto-rotate speed mode, frame count, and seed base. It also provides pure state-transition helpers for preview-equivalent control actions. The preview is not yet migrated to use this scaffold.

`T0005.2` introduced package-side camera motion settings:

- `src/pyxel_goal_game/runtime/camera_motion.py`

The module is Pyxel-independent and stores the settled auto-rotate comfort values: `slow=0.0035`, `normal=0.0065`, `fast=0.0100`, plus speed-dependent pitch sway scales. The manual preview now consumes these package-side settings for auto-rotate speed and pitch sway. Rendering, input ownership, and broader preview state extraction are still pending.

## Pure Logic And Pyxel Boundary

Pure modules must not import Pyxel.

Keep Pyxel calls isolated at app/input/render boundaries. The package runtime may render with Pyxel, but generation, geometry, schedule construction, and reusable configuration should remain testable without opening a Pyxel window.

Runtime modules must not depend on `tools/`. The dependency direction should be:

```text
pure package modules
  -> runtime state/controller
  -> runtime input/render/app
  -> optional tools preview harness
```

## Proposed Runtime Module Boundaries

Do not create these modules in this documentation task. They are the recommended target shape for follow-up implementation.

```text
src/pyxel_goal_game/runtime/
  __init__.py
  app.py
  state.py
  input.py
  render.py
  show_controller.py
  camera_motion.py
  visual_config.py
```

Responsibilities:

- `app.py`: Pyxel app loop boundary, initialization, and lifecycle.
- `state.py`: runtime state, active fireworks, scheduled salvos, active shells, active particles, glitter residue, toggles, selected profile, selected firework kind, selected scenery, and selected camera mode.
- `input.py`: maps keys to runtime actions without embedding generation logic.
- `render.py`: Pyxel-bound drawing, draw order, box, CITY, stars, shells, particles, glitter residue, and optional HUD.
- `show_controller.py`: single launch, salvo launch, random firework selection, height variation, scheduled launches, and secondary burst triggering.
- `camera_motion.py`: auto rotate ON/OFF, speed modes, speed-dependent pitch sway, and manual rotation helpers if cleanly extractable.
- `visual_config.py`: stable visual constants promoted from preview, without over-abstracting values that still need tuning.

## Migration Order

Use small follow-up tasks:

1. `T0005.1`: Extract preview runtime state/controller scaffold.
2. `T0005.2`: Extract camera motion and auto-rotate comfort settings.
3. `T0005.3`: Extract show launch/salvo scheduling.
4. `T0005.4`: Add runtime renderer using package state.
5. `T0005.5`: Add official runtime entrypoint.
6. `T0005.6`: Decide `main.py` handoff.

Each task should keep the preview working and should avoid changing visual tuning unless the task explicitly says it is a tuning task.

## Protected main.py Policy

`main.py` remains protected unless a task explicitly authorizes changing it.

The first official package runtime should be added without overwriting or thinning `main.py`. If the official runtime is accepted later, `main.py` may become a thin launcher, but that decision must be made in a separate task.

## Risks And Guardrails

Risks:

- Importing from `tools/preview_firework_box.py` would make a temporary harness part of production architecture.
- Moving everything in one patch would mix state, input, rendering, scheduling, and visual tuning regressions.
- Changing `main.py` early would remove the protected reference prototype.
- Moving Pyxel calls into pure modules would weaken deterministic tests.
- Re-tuning visuals during extraction would make parity failures hard to diagnose.

Guardrails:

- Keep extraction tasks small.
- Keep visual tuning tasks separate from runtime migration tasks.
- Preserve preview parity after each extraction.
- Use `iphone16_balanced` as the primary visual review target.
- Keep `classic` as the compatibility/default baseline.
- Run the full validation suite after each migration step.

## First Official Runtime Acceptance Criteria

The first official runtime is acceptable when it:

- Does not import from `tools/`.
- Keeps `main.py` unchanged until an explicit handoff task.
- Supports the `iphone16_balanced` visual target.
- Preserves the 3D cuboid observation box.
- Preserves the eight first-generation firework presets.
- Preserves shell launch, shell tail, compact burst radius, deterministic wobble, pre-scale trail decisions, and glitter residue.
- Preserves CITY, boulevard, tower, ferris wheel, signs, windows, and 48-building density.
- Preserves interior star placement and visibility rules.
- Preserves auto-rotate comfort settings.
- Preserves deterministic behavior where the preview already has deterministic generation or scheduling.
- Passes compile, tests, ruff, check_all, and smoke coverage.
- Keeps the preview available as a regression viewer.
