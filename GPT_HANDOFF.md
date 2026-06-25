# GPT Handoff

Use this file to share the current project situation with another GPT session.

## Project

- Repository: `fireworksbox`
- Current date: 2026-06-23
- Project type: Pyxel game prototype
- Working title: `Firework Observer`
- Goal: Build a calm, smooth Pyxel prototype where the player observes expressive fireworks in a small cutout space.

## Current State

The `pyxel_goal_codex_template_v2.zip` template has been expanded into this repository.

The project now includes:

- `AGENTS.md`: Codex working rules and required project context.
- `PROJECT_INIT.md`: Initialization guide.
- `project_brief.json`: Current game brief, copied from the template example.
- `docs/product/`: durable product direction.
- `docs/architecture/`: architecture constraints.
- `goals/`: task queue, goal state, logs, and acceptance checklists.
- `src/pyxel_goal_game/`: package-based Pyxel template implementation.
- `tests/`: unit, simulation, golden, and smoke tests.
- `.agents/skills/`: local skill documents for Codex-style task workflows.
- `docs/research/external_firework_reference.md`: notes from reviewing an external firework implementation as reference material only.
- `docs/prompts/goal_driven_mode.md`: master prompt for one-goal-at-a-time Codex development.
- `docs/architecture/SCREEN_PROFILES.md`: planning for classic and larger portrait Pyxel internal profiles.
- `docs/architecture/SCENERY_OBJECTS.md`: planning for future quiet 3D line scenery inside the observation box.
- `docs/architecture/PROTOTYPE_RECONCILIATION.md`: inventory of protected `main.py` behavior and package migration strategy.

An existing standalone `main.py` is still present and was not overwritten. It appears to contain a separate single-file Pyxel firework box prototype.

Important: the current good-feeling firework box behavior may live in this standalone `main.py`, not yet in `src/pyxel_goal_game/`. Treat `main.py` as a protected reference prototype for now.

## Product Direction

Important source files:

- `docs/product/GAME_BRIEF.md`
- `docs/product/NORTH_STAR.md`
- `docs/product/GAME_DESIGN.md`
- `docs/product/PLAYER_EXPERIENCE.md`
- `docs/product/NON_GOALS.md`
- `goals/GOAL_STATE.md`
- `goals/task_queue.json`

Current product direction:

- Mood: calm and beautiful.
- Pace: meditative.
- Challenge: none.
- Main verbs: observe, rotate camera, trigger fireworks, adjust viewpoint.
- Technical goal: deterministic simulation where practical.
- Architecture: model/system/render separation.
- Pyxel API boundary: app, loop, render, input, and audio only.

Details that should be preserved or reviewed before feature migration:

- Cutout rectangular observation space.
- 256x144 screen.
- Transparent cuboid / box-like 3D space.
- 3D coordinates use `x`, `y`, and `z`; larger `y` means higher.
- Partial trails: rockets always have trails, particles only partially have trails.
- Firework preset direction includes chrysanthemum, peony, ring, willow, spiral, and small-shell cluster styles.
- Render ordering should preserve depth readability: rear box edges, particles, then front box edges.
- The classic `256x144` profile remains the baseline, with planned larger portrait profiles documented as `236x512` and `393x852`.
- Future scenery must be 3D line geometry inside the observation box, projected through the same camera pipeline as fireworks.
- Do not solve scenery as a 2D screen-space background.

## Task Progress

`T0001: Initialize docs from project brief` is complete.

Completed work:

- Created `project_brief.json` from `project_brief.example.json`.
- Ran `python3 scripts/init_from_brief.py project_brief.json --apply`.
- Generated/updated product docs, goal state, roadmap, and task queue.
- Recorded completion in `goals/done_log.md`.
- Reviewed `/Users/toytoytoy330/Desktop/AllMyFiles/Pyxel/01_kamito/Firework.py` as external reference material and documented adaptable preset ideas in `docs/research/external_firework_reference.md`.
- Completed `T0002`: pyxel, pytest, ruff, and uv are installed; imports, compile checks, pytest, ruff, and check_all pass.
- Completed lint validation cleanup: existing ruff findings were fixed without changing gameplay behavior.
- Completed `T0002.7` out of order as a documentation-only planning task: screen profiles and in-box scenery architecture are recorded. Do not redo it unless validation shows the task queue or docs are inconsistent.
- Completed `T0002.5`: standalone `main.py` behavior is inventoried and mapped to package architecture in `docs/architecture/PROTOTYPE_RECONCILIATION.md`.
- Completed `T0002.8`: package-side `ScreenProfile` scaffold exists in `src/pyxel_goal_game/screen_profiles.py`; `classic` is the default profile, with `iphone16_balanced` and `iphone16_large` available as data.
- Completed `T0002.9`: package-side Pyxel-independent `Camera3D` projection scaffold exists in `src/pyxel_goal_game/camera3d.py` with tests for classic center projection, y-up projection, profile-dependent centers, depth guard, determinism, and smoothing.
- Completed `T0002.10`: package-side Pyxel-independent `WireBox` scaffold exists in `src/pyxel_goal_game/wire_box.py` with tests for profile dimensions, 8 vertices, 12 edges, origin centering, edge groups, and `Camera3D` projection.
- Completed `T0003.0`: package-side Pyxel-independent firework preset scaffold exists in `src/pyxel_goal_game/firework_presets.py` with `FireworkKind`, `FireworkShape`, `TrailPreset`, `SecondaryPreset`, and `FireworkPreset`.
- Completed `T0003.1`: deterministic Kiku/radial burst generation exists in `src/pyxel_goal_game/firework_bursts.py`, producing immutable `ParticleSpawnSpec` values from `KIKU_PRESET`.
- Completed `T0003.2`: deterministic Ring burst generation exists in `src/pyxel_goal_game/firework_bursts.py`, producing mostly planar ring velocity specs from `RING_PRESET`.
- Completed `T0003.3`: deterministic Spiral burst generation exists in `src/pyxel_goal_game/firework_bursts.py`, producing 3D twisted `ParticleSpawnSpec` values from `SPIRAL_PRESET`.
- Completed `T0003.4`: deterministic Willow burst generation exists in `src/pyxel_goal_game/firework_bursts.py`, producing falling-tail `ParticleSpawnSpec` values from `WILLOW_PRESET`.
- Completed `T0003.5`: deterministic Peony burst generation exists in `src/pyxel_goal_game/firework_bursts.py`, producing short bright sphere `ParticleSpawnSpec` values from `PEONY_PRESET`.

Current next task:

- `T0003.6: Implement multi-ring or halo preset`

Remaining queued tasks:

- `T0003.6: Implement multi-ring or halo preset`
- `T0003.7: Implement senrin / secondary burst preset`
- `T0003.8: Add preset cycling and visual tuning checklist`
- `T0004: Recreate protected prototype viewpoint controls in package`
- `T0005: Add trail tuning checklist`
- `T0006.0: Add scenery preset data scaffold`
- `T0006.1: Add EMPTY and MOUNTAINS scenery presets`
- `T0006.2: Add CITY skyline scenery preset`
- `T0006.3: Add FOREST scenery preset`
- `T0006.4: Add RIVERBANK scenery preset`
- `T0006.5: Add scenery preset cycling UI`

Completed out-of-order research task:

- `T0002.6: Review external firework reference files`

## Validation Status

Passed:

```bash
python3 -c 'import sys; sys.path.insert(0, "src"); import pyxel_goal_game; import pyxel_goal_game.model.firework; import pyxel_goal_game.systems.particle_system; print("package import ok")'
.venv/bin/python -c 'import sys; sys.path.insert(0, "src"); import pyxel; import pytest; import pyxel_goal_game.__main__; print("pyxel/pytest/entry imports ok with src path")'
python3 -m compileall src tests scripts tools
.venv/bin/python -m pytest
.venv/bin/python -m ruff check .
uv --version
python3 scripts/check_all.py
```

Setup notes:

- Project `.venv` uses Python 3.12.13.
- `uv.lock` was generated by `uv sync --extra dev`.
- `uv` is installed as a user-level pipx app at `/Users/toytoytoy330/.local/bin/uv`.
- The current package uses `src` layout; direct ad hoc imports should include `src` on `PYTHONPATH` unless running through pytest/uv project context.
- `main.py` received only an import-formatting lint fix during cleanup; no prototype logic changed.

## Suggested Next GPT Prompt

```text
Read AGENTS.md, PROJECT_INIT.md, GPT_HANDOFF.md,
docs/product/GAME_BRIEF.md, docs/product/NORTH_STAR.md,
docs/product/GAME_DESIGN.md, docs/product/PLAYER_EXPERIENCE.md,
docs/product/NON_GOALS.md,
docs/research/external_firework_reference.md,
docs/prompts/goal_driven_mode.md,
goals/GOAL_STATE.md, goals/task_queue.json, and goals/decision_log.md.

Start from T0002.5 only.
Do not implement new gameplay features yet.
Do not implement firework presets yet.
Execute only one goal, then stop.

Important:
- There is an existing standalone main.py prototype that may contain the current good-feeling firework box behavior.
- Treat main.py as a protected reference prototype for now.
- Inspect main.py and document good-feeling behavior to preserve.
- Document a migration or preservation strategy before package-side gameplay work.
- Do not start T0003.0 or any firework preset task.
- Do not copy or integrate external Firework.py code.
- docs/research/external_firework_reference.md is reference material only.
- Do not broaden the design beyond the recorded brief.
- Do not change visual behavior during this task.
```

## Last T0002 Prompt Used

```text
Start from T0002 only.
Do not implement new gameplay features.
Do not implement firework presets yet.
Do not modify standalone main.py.
Do not refactor src/ for visual behavior yet.
Do not start T0002.5.
Do not start T0003.0 or any firework preset task.

Goal:
Verify package imports, test environment, lint environment, and check_all behavior.

Before editing:
- Run git status.
- Identify the current branch and currently changed files.
- State which files, if any, you expect to modify.

Validation:
- Run every available validation command:
  - python3 -m compileall src tests scripts tools
  - python3 -m pytest
  - python3 -m ruff check .
  - python3 scripts/check_all.py
- If pytest, ruff, or uv are missing, document the exact setup gap and recommended install command.
- Do not silently install global dependencies unless explicitly instructed.

After the task:
- Update goals/done_log.md.
- Report git diff --stat.
- Confirm whether main.py was unchanged.
- Confirm whether gameplay behavior was unchanged.
- Stop after T0002.
```

## Notes For Future Work

- Treat `docs/` and `goals/` as durable project memory.
- Keep task patches small and focused.
- Do not hide product decisions in chat history.
- `T0003.2.5` added a manual Kiku/Ring visual preview at `tools/preview_firework_box.py`.
- Run the preview with `.venv/bin/python tools/preview_firework_box.py`; use `--profile iphone16_balanced` to inspect the larger balanced profile without changing defaults.
- Preview controls: `Z` launches one burst, `1`-`5` schedule fixed-position salvos, `SPACE` switches Kiku/Ring/Spiral/Willow/Peony in sequential mode, `R` enters random burst mode, `SPACE` exits random mode, arrow keys rotate, `A`/`S` zoom, `C` resets camera, `X` toggles auto-rotate, `V` toggles auto-launch, and `D` toggles debug HUD.
- The preview is a development tool only. It does not migrate `main.py`, production runtime particles, scenery, or future firework presets.
- `T0003.2.7` tuned iPhone-style profiles to use portrait viewport / portrait firework volume: `iphone16_balanced` is now screen `236x512`, box `120x260x120`, camera distance `340.0`; `iphone16_large` is screen `393x852`, box `200x440x200`, camera distance `560.0`.
- `T0003.2.8` added deterministic Ring orientation bank support in `firework_bursts.py`; the manual preview now builds a 24-orientation bank from seed `20260623` for Ring bursts.
- `T0003.3` added `SPIRAL_PRESET` and deterministic 3D Spiral burst generation; the manual preview now cycles Kiku, Ring, and Spiral.
- `T0003.4` added `WILLOW_PRESET` and deterministic Willow burst generation; the manual preview now cycles Kiku, Ring, Spiral, and Willow.
- `T0003.5` added `PEONY_PRESET` and deterministic Peony burst generation; the manual preview now cycles Kiku, Ring, Spiral, Willow, and Peony.
- `T0003.5.5` added preview-only random burst selection mode; `R` enters random mode and `SPACE` returns to sequential cycling.
- `T0003.5.6` added Pyxel-independent fixed-position salvo plans and preview number-key scheduling for 1-5 burst compositions.
- `classic` remains unchanged and remains the default profile.
- If the user changes the game direction, update `project_brief.json` and regenerate or manually update the related docs.
- Review whether the standalone `main.py` should be migrated into `src/pyxel_goal_game/` or kept only as a reference prototype.
- Before implementing `T0003.0`, inspect `main.py`, identify behavior to preserve, and document the migration strategy in `T0002.5`.
- Use `docs/architecture/PROTOTYPE_RECONCILIATION.md` as the source of truth for preserving protected prototype behavior during migration.
- Use `docs/prompts/goal_driven_mode.md` for future Codex sessions so each run completes only one eligible task.
- `T0004` should mean recreating the protected `main.py` viewpoint/camera feel on the package side, not inventing unrelated camera behavior.
