# Preview To Runtime Integration

This document defines the contract for promoting the first-generation manual preview into the package runtime.

The goal is not to copy `tools/preview_firework_box.py` into production. The goal is to extract the stable behavior proven by the preview into package-side runtime modules while keeping the preview available as a development harness and regression viewer.

## Why Integrate Now

The manual preview has reached the intended first-generation visual direction. It now contains the core observation-box feel, mature firework presets, CITY staging, shell launch visuals, interior stars, glitter residue, random/salvo show controls, and camera comfort tuning.

Further stable behavior should not remain trapped in `tools/preview_firework_box.py`. Runtime work should promote those behaviors into `src/pyxel_goal_game/` in small package-side slices.

The standalone `main.py` has completed its handoff and is now intended to be a thin launcher to the official package runtime.

## Frozen First-Generation Feature Set

The first official runtime should preserve these preview-proven behaviors:

- `classic` remains the default profile.
- `iphone16_balanced` remains the primary portrait visual target: screen `236x512`, box `120x260x120`.
- The scene is a 3D cuboid observation box using package-side `Camera3D` and `WireBox` projection.
- Firework presets are Kiku, Sphere Bloom, Smile, Ring, Spiral, Willow, Long Willow, Peony, Multi-ring, Senrin, and Halo.
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

- Additional firework presets beyond Smile.
- Ferris wheel animation.
- Gameplay scoring.
- Conversation, story, or event systems.
- Combat, collection, objective, or win/lose loops.
- Mobile-specific deployment.
- Further `main.py` logic changes beyond thin-launcher delegation.

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

`T0005.3` introduced package-side show scheduling:

- `src/pyxel_goal_game/runtime/show_schedule.py`

The module is Pyxel-independent and builds immutable launch schedules for single launches, fixed-count salvos, random-count salvos, random firework kind selection, and height variation. The manual preview now consumes these schedules and converts them into its existing shell objects. Shell simulation, particle spawning, rendering, and the official runtime app are still pending.

`T0005.4` introduced the first official package-side runtime app:

- `src/pyxel_goal_game/runtime/app.py`
- `src/pyxel_goal_game/runtime/input.py`
- `src/pyxel_goal_game/runtime/render.py`
- `src/pyxel_goal_game/runtime/effects.py`
- `scripts/run_runtime_app.py`

The official runtime app is launched separately from protected `main.py`:

```bash
.venv/bin/python scripts/run_runtime_app.py --profile iphone16_balanced
```

The runtime app owns the Pyxel loop, input boundary, rendering boundary, active shells, active particles, secondary bursts, and glitter residue. It uses package-side runtime state, controller, camera motion, and show scheduling modules. It does not import `tools/preview_firework_box.py`. The preview remains available as a regression viewer.

Remaining parity risks should be reviewed in `T0005.5`: visual exactness between preview and official runtime, any missing smoke coverage specific to the official entrypoint, and whether `main.py` should remain a protected reference or later become a thin launcher.

`T0005.5` recorded the runtime parity review:

- `docs/research/runtime_parity_review_20260626.md`

Manual review found official runtime parity OK for `iphone16_balanced`. Startup, controls, CITY, stars, shell tail, glitter residue, all first-generation firework kinds, salvos, height variation, auto-rotate comfort, and `R + H + 0` stress mode were accepted. The handoff decision is `READY`: `main.py` may become a thin launcher to the official runtime in a separate explicit task.

`T0005.6` applied the handoff. `main.py` is now a thin launcher to `pyxel_goal_game.runtime.app.main` and does not contain runtime logic or import from `tools/`.

`T0005.6.1` made the launcher robust for simple public startup. The runtime CLI normalizes Pyxel wrapper arguments such as `pyxel run main.py`, and the default runtime profile is `iphone16_balanced`.

`T0006.0` added the first official runtime audio layer. Audio is runtime-only for now: high-register, quiet music-box BGM loops on the BGM music channels, low restrained explosion SFX plays on burst events with a short cooldown, and `M` toggles audio on/off. The preview remains a visual development harness.

`T0006.1` extended the BGM. Runtime audio now uses channels 0-2 for melody, arpeggio accompaniment, and sparse shimmer/counter notes. Channel 3 remains reserved for explosion SFX.

`T0006.2` rebuilt the BGM as simple chord harmony. Channels 0-2 now act as melody, harmony, and soft support with large/medium/small volume hierarchy. Channel 3 remains reserved for explosion SFX.

`T0006.3` lowered overall BGM volume and changed channel 2 from high soft support into a calm mid-register rhythmic pulse. Explosion SFX remains on channel 3 and should read as the primary audio subject.

`T0007.0` added a rare silent UFO ambient flyby to the official runtime. UFO scheduling and path helpers live in Pyxel-independent runtime code, rendering is Pyxel-bound, and `U` toggles the ambient layer. UFOs do not interact with fireworks and have no sound, beam, trail, particles, or gameplay behavior.

`T0007.1` changed the UFO visual from a flat sprite-like saucer into a small 3D wireframe saucer. Geometry construction remains Pyxel-independent in `runtime/ufo.py`, while Pyxel drawing remains isolated to `runtime/render.py`. Scheduling frequency, rarity, silence, `U` toggle behavior, and non-interaction constraints are unchanged.

`T0008.0` added two required firework variants without replacing existing presets. `Sphere Bloom` is the explicit canonical sphere-like bloom, while `Long Willow` is the stronger longer-falling willow / 枝垂れ variant.

`T0008.1` tuned second-phase additions without adding new systems. UFOs are modestly larger and choose deterministic low, middle, or high flyby height bands while remaining rare, silent, beamless, trailless, particleless, and non-interactive. `Long Willow` now mixes longer-trail falling branches with trail-light or no-long-trail falling embers.

`T0008.3` added delayed mini-burst garnish for eligible fireworks. Kiku, Sphere Bloom, Peony, and Multi-ring can spawn a small deterministic set of nearby child blooms after staggered delays. The garnish is not a new main firework kind, has no key binding, and leaves CITY, stars, UFO, audio, shell tail, and global glitter behavior unchanged.

`T0008.4` added `Smile` as a shaped burst with two eyes and a smiling mouth arc. It is included in runtime and preview cycle/random/salvo selection. Smile intentionally does not use delayed mini-burst garnish so the face shape remains readable.

`T0008.3.2` added deterministic per-burst color palette variants. Each firework kind has three predefined palette variants, and each launch selects one from its seed without changing geometry, timing, shell tail, trail behavior, CITY, stars, UFO, audio, or global glitter. Delayed mini-burst garnish inherits the selected parent palette.

`T0008.3.1` tuned `Long Willow` long branch trail decay. Only the long-trail branch subgroup keeps about 56 frames of trail history, uses softened downward velocity and gravity, and draws older rear trail sections sparsely broken so the willow lingers without becoming a solid curtain or falling through the box floor. Baseline Willow, shell tail, global glitter, palette selection, CITY, stars, UFO, and audio remain unchanged.

`T0010.0` added official-runtime mobile touch controls. The play field can be dragged or flicked to rotate the camera, and a top-right `MENU` opens a Pyxel-rendered control panel. `T0010.1` changed panel checkboxes to apply immediately behind the panel, removed the `APPLY` step, and added a BGM-only toggle that leaves explosion SFX active while overall audio is on. The panel uses scaled text for readability and includes touch zoom buttons. `T0010.2` added PC mouse-wheel zoom using the same camera zoom bounds as keyboard and touch controls. `T0010.3` shortened the mobile panel and aligned `ZOOM+`, `ZOOM-`, and `CLOSE` in one bottom row so zoom changes can be checked with more of the scene still visible. `T0010.4` moved BGM beside audio and added a top `COUNT` selector for `1` through `5` and random salvo start. `T0010.5` replaced the small `NEXT` label with a wider current-firework name selector. `T0010.6` connected the mobile `COUNT` selector to runtime salvo state so the selected count is used by `SALVO START` and active repeat salvos. `T0010.7` connected mobile `AUTO` launches to the selected `COUNT` value instead of forcing single-shell auto launches. `T0010.8` added a release helper to disable Pyxel Web's default virtual gamepad so the in-app touch panel is the public mobile control surface. `T0010.9` retries BGM startup on the first touch input for mobile Safari audio unlock behavior. `T0010.10` extends the public Web HTML patcher with a Safari WebAudio unlock handler that runs directly from touch/click/key events before `launchPyxel(...)`. `T0010.11` makes mobile `random` type mode reset `COUNT RND` to fixed `1`, so random firework type and random launch count remain explicit separate choices. Keyboard controls remain available.

`T0009.0` scrubbed local absolute paths and local machine references from tracked source, docs, goals, and handoff records. Public-facing docs should use repository-relative paths such as `docs/...`, `src/...`, and `scripts/...`; the release safety checker in `scripts/check_public_safety.py` is part of `scripts/check_all.py`.

Primary launch commands:

```bash
python main.py
python3 main.py
pyxel run main.py
.venv/bin/python main.py
.venv/bin/python scripts/run_runtime_app.py --profile iphone16_balanced
```

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

The first official runtime now uses this package-side shape:

```text
src/pyxel_goal_game/runtime/
  __init__.py
  app.py
  effects.py
  state.py
  input.py
  render.py
  audio.py
  show_controller.py
  camera_motion.py
  show_schedule.py
```

Responsibilities:

- `app.py`: Pyxel app loop boundary, initialization, and lifecycle.
- `effects.py`: active shell, particle, secondary burst, and glitter residue runtime state plus small effect builders.
- `state.py`: runtime state, active fireworks, scheduled salvos, active shells, active particles, glitter residue, toggles, selected profile, selected firework kind, selected scenery, and selected camera mode.
- `input.py`: maps keys to runtime actions without embedding generation logic.
- `render.py`: Pyxel-bound drawing, draw order, box, CITY, stars, shells, particles, glitter residue, and optional HUD.
- `audio.py`: Pyxel sound/music setup, BGM playback, explosion SFX playback, and audio cooldown/mute policy.
- `show_controller.py`: single launch, salvo launch, random firework selection, height variation, scheduled launches, and secondary burst triggering.
- `camera_motion.py`: auto rotate ON/OFF, speed modes, speed-dependent pitch sway, and manual rotation helpers if cleanly extractable.
- `show_schedule.py`: immutable launch schedule construction for single launches, salvos, random type selection, and height variation.

## Migration Order

Use small follow-up tasks:

1. `T0005.1`: Extract preview runtime state/controller scaffold.
2. `T0005.2`: Extract camera motion and auto-rotate comfort settings.
3. `T0005.3`: Extract show launch/salvo scheduling.
4. `T0005.4`: Add first official runtime app and entrypoint without touching `main.py`.
5. `T0005.5`: Review runtime parity and decide `main.py` launcher handoff.
6. `T0005.6`: Convert `main.py` to a thin official runtime launcher.

Each task should keep the preview working and should avoid changing visual tuning unless the task explicitly says it is a tuning task.

## Protected main.py Policy

`main.py` is now a thin launcher for the official package runtime.

Future changes must not move runtime logic back into `main.py`. Runtime behavior belongs in `src/pyxel_goal_game/runtime/`, and the preview remains available in `tools/preview_firework_box.py`.

## Risks And Guardrails

Risks:

- Importing from `tools/preview_firework_box.py` would make a temporary harness part of production architecture.
- Moving everything in one patch would mix state, input, rendering, scheduling, and visual tuning regressions.
- Moving runtime logic back into `main.py` would recreate a single-file prototype and bypass the package runtime boundary.
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
- Keeps `main.py` thin and free of runtime logic.
- Supports the `iphone16_balanced` visual target.
- Preserves the 3D cuboid observation box.
- Preserves the eleven first-generation firework presets.
- Preserves shell launch, shell tail, compact burst radius, deterministic wobble, pre-scale trail decisions, and glitter residue.
- Preserves CITY, boulevard, tower, ferris wheel, signs, windows, and 48-building density.
- Preserves interior star placement and visibility rules.
- Preserves auto-rotate comfort settings.
- Preserves deterministic behavior where the preview already has deterministic generation or scheduling.
- Passes compile, tests, ruff, check_all, and smoke coverage.
- Keeps the preview available as a regression viewer.
