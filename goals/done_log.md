# Done Log

Record completed tasks here.

## Format

```md
## YYYY-MM-DD T0001 Task title

- Summary:
- Tests:
- User-visible behavior:
- Risks:
- Follow-up:
```

## 2026-06-23 T0001 Initialize docs from project brief

- Summary: Created `project_brief.json` from `project_brief.example.json` and generated the initial project docs, goal state, roadmap, and task queue.
- Tests: `python3 -m compileall src tests scripts tools` passed. `python3 -m pytest`, `python3 -m ruff check .`, and `python3 scripts/check_all.py` could not run because local dev tools are not installed (`pytest`, `ruff`, and `uv` missing).
- User-visible behavior: No gameplay behavior changed.
- Risks: The brief is based on the template example and should be reviewed by the user before product direction is treated as final.
- Follow-up: Complete T0002 by installing or configuring the project dev environment, then run tests and lint.

## 2026-06-23 T0002.6 Review external firework reference files

- Summary: Reviewed `/Users/toytoytoy330/Desktop/AllMyFiles/Pyxel/01_kamito/Firework.py` as reference material and created `docs/research/external_firework_reference.md`.
- Tests: Not applicable; documentation-only research task.
- User-visible behavior: No gameplay behavior changed.
- Risks: The external file is 2D screen-space code and should not be imported directly into the 3D Firework Box package.
- Follow-up: Finish T0002 and T0002.5 before implementing preset candidates from the research notes.

## 2026-06-23 T0002 Verify package imports and tests

- Summary: Set up local validation dependencies and verified package import, compile, pytest, ruff, uv, and check_all status. Dependency availability is now fixed; remaining validation failure is existing lint debt.
- Pre-task git state: branch `main`; repository has no commits yet; current project files are untracked.
- Files intentionally changed: `goals/task_queue.json`, `goals/done_log.md`, `GPT_HANDOFF.md`, and generated `uv.lock`.
- Setup:
  - Created project `.venv`.
  - Installed `pyxel`, `pytest`, and `ruff` into `.venv` via project dependency sync.
  - Installed `uv` as a user-level CLI with `pipx`, available at `/Users/toytoytoy330/.local/bin/uv`.
  - `uv sync --extra dev` selected Python 3.12.13 and generated `uv.lock`.
- Tests:
  - `python3 -c 'import sys; sys.path.insert(0, "src"); import pyxel_goal_game; import pyxel_goal_game.model.firework; import pyxel_goal_game.systems.particle_system; print("package import ok")'` passed.
  - `.venv/bin/python -c 'import sys; sys.path.insert(0, "src"); import pyxel; import pytest; import pyxel_goal_game.__main__; print("pyxel/pytest/entry imports ok with src path")'` passed.
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest` passed: 9 tests passed.
  - `.venv/bin/python -m ruff check .` ran and failed on 13 existing lint findings.
  - `python3 scripts/check_all.py` now finds `uv`; when run with uv cache access, pytest passes and ruff fails on the same 13 lint findings.
- Remaining lint findings:
  - `main.py`: import sorting.
  - `scripts/build_pyxapp.py`: unused `subprocess`.
  - `scripts/capture_smoke.py`: import sorting and one long line.
  - `scripts/check_all.py`: import sorting and unused `sys`.
  - `scripts/init_from_brief.py`: two long lines.
  - `scripts/new_task.py`: import sorting.
  - `src/pyxel_goal_game/model/world.py`: quoted return annotation.
  - `src/pyxel_goal_game/resources/paths.py`: import sorting.
  - `tools/codex/make_task_packet.py`: import sorting.
  - `tools/codex/validate_handoff.py`: import sorting.
- User-visible behavior: No gameplay behavior changed.
- Preservation: `main.py` was not edited, refactored, formatted, migrated, or overwritten. No new firework presets were implemented.
- Risks: `ruff check .` and `check_all.py` still fail until lint findings are fixed. `main.py` has one ruff import-sorting finding but remains protected until T0002.5 decides how to treat it.
- Follow-up: Start `T0002.5` next to inspect the protected standalone `main.py` and document package migration strategy.

## 2026-06-23 Lint validation cleanup

- Summary: Fixed existing ruff findings so the local validation suite is green.
- Files changed: `main.py`, `scripts/build_pyxapp.py`, `scripts/capture_smoke.py`, `scripts/check_all.py`, `scripts/init_from_brief.py`, `scripts/new_task.py`, `src/pyxel_goal_game/model/world.py`, `src/pyxel_goal_game/resources/paths.py`, `tools/codex/make_task_packet.py`, and `tools/codex/validate_handoff.py`.
- Tests:
  - `.venv/bin/python -m ruff check .` passed.
  - `.venv/bin/python -m pytest` passed: 9 tests passed.
  - `python3 -m compileall src tests scripts tools` passed.
  - `python3 scripts/check_all.py` passed.
- User-visible behavior: No gameplay behavior changed.
- Preservation: `main.py` received only an import-formatting lint fix; no prototype logic was changed, migrated, or refactored.
- Risks: The next task should still treat `main.py` as a protected reference prototype and start with `T0002.5`.
- Follow-up: Start `T0002.5` next.

## 2026-06-24 T0002.7 Document screen profiles and in-box scenery architecture

- Summary: Completed `T0002.7` out of order as a documentation-only planning task. Added screen profile strategy and in-box scenery architecture before screen profile or scenery implementation.
- Files changed: `docs/architecture/SCREEN_PROFILES.md`, `docs/architecture/SCENERY_OBJECTS.md`, `docs/product/GAME_BRIEF.md`, `docs/product/GAME_DESIGN.md`, `docs/prompts/goal_driven_mode.md`, `goals/decision_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, and `GPT_HANDOFF.md`.
- Tests: `.venv/bin/python -m json.tool goals/task_queue.json` passed.
- User-visible behavior: No gameplay behavior changed.
- Preservation: `main.py` was unchanged. `src` gameplay behavior was unchanged. No new firework presets were implemented. No scenery rendering was implemented.
- Risks: Future scenery must remain 3D line geometry inside the observation box; drawing scenery as a 2D screen-space background would violate the recorded design.
- Follow-up: Keep `T0002.5` as the next reconciliation task before package-side gameplay migration. Start `T0002.8` only after `T0002.5` is complete.

## 2026-06-24 T0002 Validation reconciliation after baseline commit

- Summary: Re-ran T0002 validation against baseline commit `f9f7e0e` because roadmap and task queue mark T0002 complete. Confirmed the project validation path is consistent when using the project-managed `uv` environment.
- Pre-task git state: branch `main`; worktree clean; baseline commit `f9f7e0e Initialize Firework Observer planning docs` exists.
- Task state: `goals/task_queue.json` records T0002 in `done`; `goals/roadmap.md` marks package import/test verification complete.
- Tests:
  - `python3 -m compileall src tests scripts tools` passed.
  - `python3 -m pytest` failed because `/opt/homebrew/opt/python@3.14/bin/python3.14` does not have `pytest` installed.
  - `python3 -m ruff check .` failed because `/opt/homebrew/opt/python@3.14/bin/python3.14` does not have `ruff` installed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when rerun with approved cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 9 passed.
- Missing dependency note: global `python3` is Python 3.14 and lacks `pytest` and `ruff`. Use the project-managed path via `python3 scripts/check_all.py`, or install/sync the dev environment with `uv sync --extra dev`.
- User-visible behavior: No gameplay behavior changed.
- Preservation: `main.py` was unchanged. `src` gameplay behavior was unchanged. No screen profiles, scenery rendering, or firework presets were implemented.
- Follow-up: Start `T0002.5` next.

## 2026-06-24 T0002.5 Reconcile standalone prototype with package architecture

- Summary: Inspected protected `main.py`, inventoried the current good-feeling prototype behavior, compared it with the package architecture, and documented a staged migration strategy in `docs/architecture/PROTOTYPE_RECONCILIATION.md`.
- Pre-task git state: branch `main`; worktree clean; latest commit `b35b31b Record T0002 validation reconciliation`.
- Files changed: `docs/architecture/PROTOTYPE_RECONCILIATION.md`, `goals/decision_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, `goals/done_log.md`, and `GPT_HANDOFF.md`.
- Tests:
  - `python3 -m compileall src tests scripts tools` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 9 passed.
- User-visible behavior: No gameplay behavior changed.
- Preservation: `main.py` was unchanged. `src` gameplay behavior was unchanged. No screen profile implementation, scenery rendering, or firework preset implementation was added.
- Risks: The package is still a 2D template and should not be rewritten wholesale from `main.py`. Future migration should preserve Camera3D, box projection, y-up negative gravity, partial trails, and render order in small slices.
- Follow-up: Start `T0002.8` next unless the user chooses to prioritize the newly added `T0002.9` Camera3D scaffold first.

## 2026-06-24 T0002.8 Add screen profile configuration scaffold

- Summary: Added package-side `ScreenProfile` configuration data with `classic`, `iphone16_balanced`, and `iphone16_large` profiles. `classic` remains the default profile. `GameSettings` now exposes dimensions from its selected profile, and `ObserverScene` uses profile dimensions and max particle count.
- Pre-task git state: branch `main`; worktree clean; latest commit `317eaa7 Document prototype reconciliation strategy`.
- Files changed: `src/pyxel_goal_game/screen_profiles.py`, `src/pyxel_goal_game/constants.py`, `src/pyxel_goal_game/settings.py`, `src/pyxel_goal_game/model/world.py`, `src/pyxel_goal_game/render/hud_renderer.py`, `src/pyxel_goal_game/scenes/observer.py`, `src/pyxel_goal_game/loop.py`, `tests/unit/test_screen_profiles.py`, `docs/architecture/SCREEN_PROFILES.md`, `goals/decision_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, `goals/done_log.md`, and `GPT_HANDOFF.md`.
- Tests:
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest` passed: 14 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 14 passed.
- User-visible behavior: Package default screen settings now resolve through the `classic` profile values, and the HUD bottom line anchors to the active profile height. No firework preset, scenery, or `main.py` behavior was changed.
- Preservation: `main.py` was unchanged. No scenery rendering, new firework presets, or external Firework.py code was added.
- Follow-up: Start `T0002.9` next to add package-side Camera3D/projection scaffold without visible gameplay migration.

## 2026-06-24 T0002.9 Add package-side Camera3D and projection scaffold

- Summary: Added Pyxel-independent package-side `Camera3D`, `Vec3`, and `ProjectedPoint` projection scaffold using `ScreenProfile` width, height, focal length, and camera distance. The scaffold preserves the protected prototype yaw-then-pitch transform, y-up screen projection, depth guard, and smoothing coefficients without binding keyboard input or rendering.
- Pre-task git state: branch `main`; worktree clean; latest commit `646b0dc Add screen profile scaffold`.
- Files changed: `src/pyxel_goal_game/camera3d.py`, `tests/unit/test_camera3d.py`, `docs/architecture/PROTOTYPE_RECONCILIATION.md`, `docs/architecture/SCREEN_PROFILES.md`, `goals/decision_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, `goals/done_log.md`, and `GPT_HANDOFF.md`.
- Tests:
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest tests/unit/test_camera3d.py` passed: 6 tests passed.
  - `.venv/bin/python -m pytest` passed: 20 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 20 passed.
- User-visible behavior: No visible gameplay behavior changed.
- Preservation: `main.py` was unchanged. Default profile remains `classic`. No firework presets, scenery rendering, rocket migration, particle migration, or external Firework.py code was added.
- Follow-up: Start `T0002.10` next to add package-side wire box scaffold.

## 2026-06-24 T0002.10 Add package-side wire box scaffold

- Summary: Added Pyxel-independent package-side `WireBox`, `Edge3D`, and `ProjectedEdge` geometry scaffold using `ScreenProfile` box dimensions and `Camera3D` projection. The scaffold generates 8 origin-centered vertices, 12 prototype-compatible edges, edge groups, and projected edges with average depth for future render ordering.
- Pre-task git state: branch `main`; worktree clean; latest commit `987086d Add Camera3D projection scaffold`.
- Files changed: `src/pyxel_goal_game/wire_box.py`, `tests/unit/test_wire_box.py`, `docs/architecture/PROTOTYPE_RECONCILIATION.md`, `docs/architecture/SCREEN_PROFILES.md`, `docs/architecture/SCENERY_OBJECTS.md`, `goals/decision_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, `goals/done_log.md`, and `GPT_HANDOFF.md`.
- Tests:
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest tests/unit/test_wire_box.py` passed: 7 tests passed.
  - `.venv/bin/python -m pytest` passed: 27 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 27 passed.
- User-visible behavior: No visible gameplay behavior changed.
- Preservation: `main.py` was unchanged. Default profile remains `classic`. No firework presets, scenery rendering, rocket migration, particle migration, or external Firework.py code was added.
- Follow-up: Start `T0003.0` next unless the user chooses to insert a render-only classic box integration task first.

## 2026-06-24 T0003.0 Establish firework preset scaffold

- Summary: Added Pyxel-independent firework preset scaffold with `FireworkKind`, `FireworkShape`, `TrailPreset`, `SecondaryPreset`, and `FireworkPreset`. The scaffold can represent future Kiku, Peony, Ring, Willow, Spiral, Multi-ring, Halo, and Senrin presets without runtime generation or rendering.
- Pre-task git state: branch `main`; worktree clean; latest commit `87ceefa Add wire box geometry scaffold`.
- Files changed: `src/pyxel_goal_game/firework_presets.py`, `tests/unit/test_firework_presets.py`, `docs/architecture/PROTOTYPE_RECONCILIATION.md`, `goals/decision_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, `goals/done_log.md`, and `GPT_HANDOFF.md`.
- Tests:
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest tests/unit/test_firework_presets.py` passed: 7 tests passed.
  - `.venv/bin/python -m pytest` passed: 34 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 34 passed.
- User-visible behavior: No visible gameplay behavior changed.
- Preservation: `main.py` was unchanged. Default profile remains `classic`. No runtime firework behavior, scenery rendering, rocket migration, particle migration, or external Firework.py code was added.
- Follow-up: Start `T0003.1` next to implement deterministic radial/Kiku generation.

## 2026-06-24 T0003.1 Implement deterministic radial / kiku preset

- Summary: Added `KIKU_PRESET` with protected prototype values and a Pyxel-independent deterministic Kiku burst generator that returns immutable `ParticleSpawnSpec` values. The generator creates a 3D spherical velocity distribution from a seed and represents partial trail eligibility from `TrailPreset`.
- Pre-task git state: branch `main`; worktree clean; latest commit `aca566e Add firework preset scaffold`.
- Files changed: `src/pyxel_goal_game/firework_presets.py`, `src/pyxel_goal_game/firework_bursts.py`, `tests/unit/test_firework_bursts.py`, `docs/architecture/PROTOTYPE_RECONCILIATION.md`, `goals/decision_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, `goals/done_log.md`, and `GPT_HANDOFF.md`.
- Tests:
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest tests/unit/test_firework_bursts.py tests/unit/test_firework_presets.py` passed: 16 tests passed.
  - `.venv/bin/python -m pytest` passed: 43 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 43 passed.
- User-visible behavior: No visible gameplay behavior changed.
- Preservation: `main.py` was unchanged. Default profile remains `classic`. No runtime Rocket or Particle migration, Pyxel rendering connection, Ring/Spiral/Willow/Peony/Multi-ring/Halo/Senrin implementation, scenery rendering, or external Firework.py code was added.
- Follow-up: Start `T0003.2` next to implement the Ring preset using the same pure generation pattern.

## 2026-06-24 T0003.2 Implement ring preset

- Summary: Added `RING_PRESET` and deterministic Ring burst generation. The generator returns immutable `ParticleSpawnSpec` values with XY-plane ring velocities, small deterministic z thickness, negative gravity, and partial trail fields from `TrailPreset`.
- Pre-task git state: branch `main`; worktree clean; latest commit `0149420 Add deterministic Kiku burst generation`.
- Files changed: `src/pyxel_goal_game/firework_presets.py`, `src/pyxel_goal_game/firework_bursts.py`, `tests/unit/test_firework_bursts.py`, `docs/architecture/PROTOTYPE_RECONCILIATION.md`, `goals/decision_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, `goals/done_log.md`, and `GPT_HANDOFF.md`.
- Tests:
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest tests/unit/test_firework_bursts.py tests/unit/test_firework_presets.py` passed: 25 tests passed.
  - `.venv/bin/python -m pytest` passed: 52 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 52 passed.
- User-visible behavior: No visible gameplay behavior changed.
- Preservation: `main.py` was unchanged. Default profile remains `classic`. No runtime Rocket or Particle migration, Pyxel rendering connection, Spiral/Willow/Peony/Multi-ring/Halo/Senrin implementation, scenery rendering, or external Firework.py code was added.
- Follow-up: Start `T0003.3` next to implement the Spiral preset using the same pure generation pattern.

## 2026-06-24 T0003.2.5 Add manual Pyxel preview for Kiku and Ring bursts

- Summary: Added `tools/preview_firework_box.py`, a manual Pyxel preview harness that uses package-side `ScreenProfile`, `Camera3D`, `WireBox`, `generate_kiku_burst`, and `generate_ring_burst` to inspect Kiku/Ring visual feel before Spiral work.
- Pre-task git state: branch `main`; worktree clean; latest commit `5952c1e Add deterministic Ring burst generation`.
- Files changed: `tools/preview_firework_box.py`, `goals/decision_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, `goals/done_log.md`, and `GPT_HANDOFF.md`.
- Manual run command: `.venv/bin/python tools/preview_firework_box.py`
- Optional profile run command: `.venv/bin/python tools/preview_firework_box.py --profile iphone16_balanced`
- Preview controls: `Z` launches, `SPACE` switches Kiku/Ring, arrow keys rotate, `A`/`S` zoom, `C` resets camera, `X` toggles auto-rotate, `V` toggles auto-launch, and `D` toggles debug HUD.
- Tests:
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest` passed: 52 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 52 passed.
- User-visible behavior: No production gameplay behavior changed. The preview opens a Pyxel window only when run manually.
- Preservation: `main.py` was unchanged. Default profile remains `classic`. No Spiral/Willow/Peony/Multi-ring/Halo/Senrin implementation, scenery rendering, production runtime migration, or external Firework.py code was added.
- Follow-up: Run the manual preview, record visual tuning notes if needed, then start `T0003.3` to implement Spiral.

## 2026-06-24 T0003.2.6 Tune iPhone screen profiles to portrait firework volume

- Summary: Adjusted iPhone-style screen profiles so the internal observation box becomes a tall firework volume. `classic` remains unchanged and remains the default.
- Pre-task git state: branch `main`; worktree clean; latest commit `55fbc18 Add manual Kiku Ring preview harness`.
- Files changed: `src/pyxel_goal_game/screen_profiles.py`, `tests/unit/test_screen_profiles.py`, `tests/unit/test_wire_box.py`, `tests/unit/test_camera3d.py`, `docs/architecture/SCREEN_PROFILES.md`, `docs/product/GAME_DESIGN.md`, `goals/decision_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, `goals/done_log.md`, and `GPT_HANDOFF.md`.
- Profile changes:
  - `classic`: unchanged at screen `256x144`, box `120x80x120`, focal `180.0`, camera distance `180.0`, max particles `400`.
  - Superseded by `T0003.2.7`, which makes the iPhone-style Pyxel screens portrait as well as the box.
- Manual preview command: `.venv/bin/python tools/preview_firework_box.py --profile iphone16_balanced`
- Tests:
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest` passed: 54 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 54 passed.
- User-visible behavior: No production gameplay behavior changed. The tuned profile values affect only code that explicitly selects those larger profiles.
- Preservation: `main.py` was unchanged. Default profile remains `classic`. No new firework types, scenery rendering, production runtime migration, or external Firework.py code was added.
- Follow-up: Use the manual preview to inspect `iphone16_balanced`, then start `T0003.3` to implement Spiral against the updated profile assumptions.

## 2026-06-24 T0003.2.7 Tune iPhone screen profiles to portrait Pyxel viewport

- Summary: Changed iPhone-style Pyxel screen profiles from landscape to portrait while preserving the tall internal firework volume. `classic` remains unchanged and remains the default.
- Pre-task git state: branch `main`; worktree clean; latest commit `7a3a09c Tune iPhone profiles for portrait firework volume`.
- Files changed: `src/pyxel_goal_game/screen_profiles.py`, `tests/unit/test_screen_profiles.py`, `tests/unit/test_camera3d.py`, `docs/architecture/SCREEN_PROFILES.md`, `docs/product/GAME_BRIEF.md`, `docs/product/GAME_DESIGN.md`, `goals/decision_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, `goals/done_log.md`, and `GPT_HANDOFF.md`.
- Profile changes:
  - `classic`: unchanged at screen `256x144`, box `120x80x120`, focal `180.0`, camera distance `180.0`, max particles `400`.
  - `iphone16_balanced`: screen `236x512`, box `120x260x120`, focal `260.0`, camera distance `340.0`, max particles `600`.
  - `iphone16_large`: screen `393x852`, box `200x440x200`, focal `430.0`, camera distance `560.0`, max particles `900`.
- Manual preview command: `.venv/bin/python tools/preview_firework_box.py --profile iphone16_balanced`
- Tests:
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest` passed: 54 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 54 passed.
- User-visible behavior: No production gameplay behavior changed. The tuned profile values affect only code that explicitly selects those larger profiles.
- Preservation: `main.py` was unchanged. Default profile remains `classic`. No new firework types, scenery rendering, production runtime migration, or external Firework.py code was added.
- Follow-up: Use the manual preview to inspect `iphone16_balanced`, then start `T0003.3` to implement Spiral against the updated portrait profile assumptions.

## 2026-06-25 T0003.2.8 Add deterministic Ring orientation bank

- Summary: Added Pyxel-independent `RingOrientation` and `RingOrientationBank` support. Ring generation can now use a deterministic stratified orientation bank, and the manual preview builds a 24-orientation bank for Ring bursts.
- Pre-task git state: branch `main`; worktree clean; latest commit `0cc438c Tune iPhone profiles for portrait viewport`.
- Files changed: `src/pyxel_goal_game/firework_bursts.py`, `tests/unit/test_firework_bursts.py`, `tools/preview_firework_box.py`, `goals/decision_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, `goals/done_log.md`, and `GPT_HANDOFF.md`.
- Behavior:
  - `build_ring_orientation_bank(seed=20260623, count=24)` creates deterministic near-vertical, oblique, and near-horizontal Ring orientations.
  - `generate_ring_burst(..., orientation_bank=bank)` selects orientation deterministically by burst seed.
  - If no bank is provided, Ring orientation is still generated deterministically from the burst seed.
  - Preview Ring launches use the bank; Kiku launches are unchanged.
- Tests:
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest` passed: 63 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 63 passed.
- User-visible behavior: Production gameplay remains unchanged. Manual preview Ring bursts can now vary orientation deterministically.
- Preservation: `main.py` was unchanged. Default profile remains `classic`. No Spiral/Willow/Peony/Multi-ring/Halo/Senrin implementation, scenery rendering, production runtime migration, or external Firework.py code was added.
- Follow-up: Use the manual preview to inspect Ring orientation variety, then start `T0003.3` to implement Spiral.

## 2026-06-25 T0003.3 Implement spiral preset

- Summary: Added `SPIRAL_PRESET` and deterministic Pyxel-independent Spiral burst generation. The generator returns immutable `ParticleSpawnSpec` values with normalized 3D spiral velocities, negative gravity, and partial trail fields from `TrailPreset`.
- Pre-task git state: branch `main`; worktree clean; latest commit `863c332 Add deterministic Ring orientation bank`.
- Files changed: `src/pyxel_goal_game/firework_presets.py`, `src/pyxel_goal_game/firework_bursts.py`, `tests/unit/test_firework_bursts.py`, `tools/preview_firework_box.py`, `goals/decision_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, `goals/done_log.md`, and `GPT_HANDOFF.md`.
- Behavior:
  - `generate_spiral_burst(origin=..., seed=...)` creates deterministic 3D spiral spawn specs.
  - `generate_burst()` now supports `FireworkShape.SPIRAL`.
  - Preview `SPACE` cycles Kiku, Ring, and Spiral.
  - Spiral velocities include x/y/z variation while preserving speed magnitudes within `SPIRAL_PRESET.speed_range`.
- Tests:
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest` passed: 72 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 72 passed.
- User-visible behavior: Production gameplay remains unchanged. Manual preview can now inspect Spiral.
- Preservation: `main.py` was unchanged. Default profile remains `classic`. `iphone16_balanced` remains screen `236x512` and box `120x260x120`. No Willow/Peony/Multi-ring/Halo/Senrin implementation, scenery rendering, production runtime migration, or external Firework.py code was added.
- Follow-up: Use the manual preview to inspect Spiral in the portrait profile, then start `T0003.4` to implement Willow.

## 2026-06-25 T0003.4 Implement willow preset

- Summary: Added `WILLOW_PRESET` and deterministic Pyxel-independent Willow burst generation. The generator returns immutable `ParticleSpawnSpec` values with loose radial spread, varied vertical velocity, stronger negative gravity, and longer partial trail fields from `TrailPreset`.
- Pre-task git state: branch `main`; worktree clean; latest commit `f06e9de Add deterministic Spiral burst generation`.
- Files changed: `src/pyxel_goal_game/firework_presets.py`, `src/pyxel_goal_game/firework_bursts.py`, `tests/unit/test_firework_bursts.py`, `tools/preview_firework_box.py`, `goals/decision_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, `goals/done_log.md`, and `GPT_HANDOFF.md`.
- Behavior:
  - `generate_willow_burst(origin=..., seed=...)` creates deterministic willow spawn specs.
  - `generate_burst()` now supports `FireworkShape.WILLOW`.
  - Preview `SPACE` cycles Kiku, Ring, Spiral, and Willow.
  - Willow uses stronger negative gravity and longer partial trail settings than earlier presets.
- Tests:
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest` passed: 82 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 82 passed.
- User-visible behavior: Production gameplay remains unchanged. Manual preview can now inspect Willow.
- Preservation: `main.py` was unchanged. Default profile remains `classic`. `iphone16_balanced` remains screen `236x512` and box `120x260x120`. No Peony/Multi-ring/Halo/Senrin implementation, scenery rendering, production runtime migration, or external Firework.py code was added.
- Follow-up: Use the manual preview to inspect Willow trail density in the portrait profile, then start `T0003.5` to implement Peony.

## 2026-06-25 T0003.5 Implement peony preset

- Summary: Added `PEONY_PRESET` and deterministic Pyxel-independent Peony burst generation. Peony reuses the sphere burst path with shorter life, bright palette values, fewer particles than Kiku, and restrained partial trail fields from `TrailPreset`.
- Pre-task git state: branch `main`; worktree clean; latest commit `a1f82aa Add deterministic Willow burst generation`.
- Files changed: `src/pyxel_goal_game/firework_presets.py`, `src/pyxel_goal_game/firework_bursts.py`, `tests/unit/test_firework_bursts.py`, `tools/preview_firework_box.py`, `goals/decision_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, `goals/done_log.md`, and `GPT_HANDOFF.md`.
- Behavior:
  - `generate_peony_burst(origin=..., seed=...)` creates deterministic Peony spawn specs.
  - `generate_burst()` supports Peony through the existing `FireworkShape.SPHERE` path.
  - Preview `SPACE` cycles Kiku, Ring, Spiral, Willow, and Peony.
  - Peony uses shorter life and lower trail tendency than Kiku/Willow.
- Tests:
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest` passed: 91 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 91 passed.
- User-visible behavior: Production gameplay remains unchanged. Manual preview can now inspect Peony.
- Preservation: `main.py` was unchanged. Default profile remains `classic`. `iphone16_balanced` remains screen `236x512` and box `120x260x120`. No Multi-ring/Halo/Senrin implementation, scenery rendering, production runtime migration, or external Firework.py code was added.
- Follow-up: Use the manual preview to inspect Peony brightness and trail restraint, then start `T0003.6` to implement Multi-ring or Halo.

## 2026-06-25 T0003.5.5 Add random burst selection mode to preview

- Summary: Added preview-only random burst selection mode to `tools/preview_firework_box.py`. `R` enters random mode, `Z` launches a deterministic random implemented burst type, auto-launch also chooses random burst types in random mode, and `SPACE` exits random mode back to sequential cycling.
- Pre-task git state: branch `main`; worktree clean; latest commit `4c121d3 Add deterministic Peony burst generation`.
- Files changed: `tools/preview_firework_box.py`, `goals/decision_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, `goals/done_log.md`, and `GPT_HANDOFF.md`.
- Behavior:
  - Sequential mode keeps existing `SPACE` next-type behavior.
  - Random mode uses a preview-local seeded RNG and does not use global random state.
  - Returning from random mode sets the sequential index to the last launched burst type.
  - HUD shows `SEQ` or `RANDOM` and the selected or last launched burst label.
- Tests:
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest` passed: 91 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 91 passed.
- Manual preview command: `.venv/bin/python tools/preview_firework_box.py --profile iphone16_balanced`
- User-visible behavior: Production gameplay remains unchanged. Manual preview can now randomize existing burst types for visual inspection.
- Preservation: `main.py` was unchanged. Default profile remains `classic`. No Multi-ring/Halo/Senrin implementation, scenery rendering, production runtime migration, pure generation behavior changes, or external Firework.py code was added.
- Follow-up: Use random preview mode for visual comparison, then start `T0003.6` to implement Multi-ring or Halo.

## 2026-06-25 T0003.5.6 Add fixed-position salvo launch plans to preview

- Summary: Added Pyxel-independent fixed-position salvo plan data and connected number keys `1` through `5` in the manual preview to schedule consecutive profile-scaled burst launches.
- Pre-task git state: branch `main`; worktree clean; latest commit `b11f70b Add preview random burst mode`.
- Files changed: `src/pyxel_goal_game/salvo_patterns.py`, `tests/unit/test_salvo_patterns.py`, `tools/preview_firework_box.py`, `goals/decision_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, `goals/done_log.md`, and `GPT_HANDOFF.md`.
- Behavior:
  - Number keys `1` through `5` schedule fixed-position salvo plans.
  - Salvo positions are box-relative and scale from each `ScreenProfile` box dimension.
  - Sequential mode uses the current selected burst type for every salvo slot.
  - Random mode chooses fixed random burst types when the salvo is scheduled.
  - Scheduled slots launch with 12-frame spacing and retain their chosen type.
  - `Z` single-launch behavior remains available.
- Tests:
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest` passed: 108 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 108 passed.
- Manual preview command: `.venv/bin/python tools/preview_firework_box.py --profile iphone16_balanced`
- User-visible behavior: Production gameplay remains unchanged. Manual preview can now inspect 1-5 burst compositions.
- Preservation: `main.py` was unchanged. Default profile remains `classic`. No Multi-ring/Halo/Senrin implementation, scenery rendering, production runtime migration, firework generation behavior changes, or external Firework.py code was added.
- Follow-up: Use salvo preview mode to assess multi-burst density, then start `T0003.6` to implement Multi-ring or Halo.

## 2026-06-25 T0003.6 Implement multi-ring preset

- Summary: Added `MULTI_RING_PRESET` and deterministic Pyxel-independent Multi-ring burst generation. Multi-ring creates 3 ring layers with counts 32/40/48, clamped speed multipliers, shared deterministic orientation, and restrained partial trails.
- Pre-task git state: branch `main`; worktree clean; latest commit `350d0ca Add preview salvo launch plans`.
- Files changed: `src/pyxel_goal_game/firework_presets.py`, `src/pyxel_goal_game/firework_bursts.py`, `tests/unit/test_firework_bursts.py`, `tools/preview_firework_box.py`, `goals/decision_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, `goals/done_log.md`, and `GPT_HANDOFF.md`.
- Behavior:
  - `generate_multi_ring_burst(origin=..., seed=...)` creates deterministic Multi-ring spawn specs.
  - `generate_burst()` now supports `FireworkShape.MULTI_RING`.
  - Multi-ring supports optional `RingOrientationBank`, matching Ring generation style.
  - Preview `SPACE` cycles Kiku, Ring, Spiral, Willow, Peony, and Multi-ring.
  - Preview random mode and 1-5 salvo scheduling include Multi-ring.
- Tests:
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest` passed: 119 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 119 passed.
- Manual preview command: `.venv/bin/python tools/preview_firework_box.py --profile iphone16_balanced`
- User-visible behavior: Production gameplay remains unchanged. Manual preview can now inspect Multi-ring alone, in random mode, and in 1-5 salvos.
- Preservation: `main.py` was unchanged. Default profile remains `classic`. `iphone16_balanced` remains screen `236x512` and box `120x260x120`. No Halo/Senrin implementation, scenery rendering, production runtime migration, or external Firework.py code was added.
- Follow-up: Use the manual preview to inspect 5-shot Multi-ring density, then start `T0003.7` or insert a small density-tuning task if needed.

## 2026-06-25 T0003.7 Implement senrin / secondary burst preset

- Summary: Added `SENRIN_PRESET`, `SENRIN_SECONDARY_PRESET`, optional `SecondaryBurstSpec` data on primary spawn specs, deterministic secondary burst generation, and preview-only secondary burst execution.
- Pre-task git state: branch `main`; worktree clean; latest commit `7b68c1b Add deterministic Multi-ring burst generation`.
- Files changed: `src/pyxel_goal_game/firework_presets.py`, `src/pyxel_goal_game/firework_bursts.py`, `tests/unit/test_firework_bursts.py`, `tools/preview_firework_box.py`, `docs/architecture/PROTOTYPE_RECONCILIATION.md`, `goals/decision_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, `goals/done_log.md`, and `GPT_HANDOFF.md`.
- Behavior:
  - `generate_senrin_burst(origin=..., seed=...)` creates deterministic primary seed spawn specs.
  - Some primary specs carry deterministic `secondary_burst` data.
  - `generate_secondary_burst(origin=..., spec=...)` creates deterministic secondary particles.
  - Preview `SPACE` cycles Kiku, Ring, Spiral, Willow, Peony, Multi-ring, and Senrin.
  - Preview random mode and 1-5 salvo scheduling include Senrin.
  - Preview executes secondary bursts locally when primary particles reach their delay.
- Tests:
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest` passed: 132 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 132 passed.
- Manual preview command: `.venv/bin/python tools/preview_firework_box.py --profile iphone16_balanced`
- User-visible behavior: Production gameplay remains unchanged. Manual preview can now inspect Senrin primary and secondary burst behavior.
- Preservation: `main.py` was unchanged. Default profile remains `classic`. `iphone16_balanced` remains screen `236x512` and box `120x260x120`. No Halo implementation, scenery rendering, production runtime migration, or external Firework.py code was added.
- Follow-up: Use the manual preview to inspect Senrin secondary density, then continue to `T0003.8` or insert a tuning task if needed.

## 2026-06-25 T0003.7.5 Add persistent preview salvo controls

- Summary: Changed manual preview number keys into persistent salvo loops, added `0` as random-count salvo mode, added `H` height variation, and drew preview-only launch-to-burst rocket trajectories for salvos.
- Pre-task git state: branch `main`; worktree clean; latest commit `3af6273 Add deterministic Senrin secondary bursts`.
- Files changed: `tools/preview_firework_box.py`, `goals/decision_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, `goals/done_log.md`, and `GPT_HANDOFF.md`.
- Behavior:
  - `1` starts persistent fixed one-shot salvo mode.
  - `2` through `5` start persistent fixed-count salvo modes.
  - `0` starts persistent random-count salvo mode, choosing a fresh count from 1 to 5 for each repeated salvo.
  - `R` randomizes burst type independently from `0` randomizing salvo count.
  - `H` toggles box-relative height variation for salvo burst positions.
  - `V` auto-launch and persistent salvo mode are mutually exclusive.
  - `Z` remains a single immediate launch and does not toggle persistent salvo mode.
  - Salvo launches draw preview-only launch-to-burst rocket trajectories.
- Tests:
  - `.venv/bin/python -m json.tool goals/task_queue.json` passed.
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest` passed: 132 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 132 passed.
- Manual preview command: `.venv/bin/python tools/preview_firework_box.py --profile iphone16_balanced`
- User-visible behavior: Production gameplay remains unchanged. Manual preview can now run repeated fixed-count or random-count salvo compositions.
- Preservation: `main.py` was unchanged. Default profile remains `classic`. No Halo implementation, scenery rendering, production runtime migration, pure firework generation changes, or external Firework.py code was added.
- Follow-up: Continue to `T0003.8` for preset cycling and visual tuning checklist work.

## 2026-06-25 T0003.8 Add preset cycling and visual tuning checklist

- Summary: Added `docs/research/visual_tuning_checklist.md` to define the manual visual review procedure for all implemented firework presets and preview controls.
- Pre-task git state: branch `main`; worktree clean; latest commit `a257131 Add persistent preview salvo controls`.
- Files changed: `docs/research/visual_tuning_checklist.md`, `goals/decision_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, `goals/done_log.md`, and `GPT_HANDOFF.md`.
- Checklist coverage:
  - Profile policy: `classic` as compatibility baseline, `iphone16_balanced` as primary visual tuning target, and `iphone16_large` as optional stress check.
  - Preview commands and controls.
  - Kiku, Ring, Spiral, Willow, Peony, Multi-ring, and Senrin visual criteria.
  - `R` random type mode, `0` random-count salvo mode, `H` height variation, persistent `1`-`5` salvo loops, rocket tail readability, and the `R + H + 0` stress sequence.
  - Density risks for Senrin, Multi-ring, and Willow.
  - Follow-up tuning candidates before Halo or runtime integration.
- Tests:
  - `.venv/bin/python -m json.tool goals/task_queue.json` passed.
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest` passed: 132 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 132 passed.
- User-visible behavior: None. This was a documentation/checklist task.
- Preservation: `main.py` was unchanged. Production runtime, preset parameters, pure generation behavior, Halo, and scenery were unchanged.
- Follow-up: Run the manual visual review with `.venv/bin/python tools/preview_firework_box.py --profile iphone16_balanced`, then choose density tuning, Halo planning, or runtime integration planning based on the checklist results.

## 2026-06-25 T0003.7.6 Fix preview rocket tail, flight pacing, and launch speed variation

- Summary: Corrected preview rocket launch visuals so rockets launch before bursting, draw only short recent-motion tails, use longer distance-aware flight timing, and vary launch speed per rocket.
- Pre-task git state: branch `main`; worktree clean; latest commit `cc6027d Add visual tuning checklist`.
- Files changed: `tools/preview_firework_box.py`, `docs/research/visual_tuning_checklist.md`, `goals/decision_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, `goals/done_log.md`, and `GPT_HANDOFF.md`.
- Behavior:
  - `Z` now schedules a preview rocket and bursts after arrival instead of exploding immediately.
  - Salvo slot delay now means rocket launch start delay.
  - Rockets keep a short 3D history tail and no longer draw a full launch-to-current path line.
  - Rocket flight duration depends on vertical distance, deterministic speed factor, and small jitter, clamped to 96 through 180 frames.
  - Persistent salvo repeat interval was increased to 210 frames to fit longer launches.
  - Random type mode, random-count salvo mode, height variation, auto launch, and persistent salvos continue to use preview-only rocket scheduling.
- Tests:
  - `.venv/bin/python -m json.tool goals/task_queue.json` passed.
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest` passed: 132 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 132 passed.
- Manual preview command: `.venv/bin/python tools/preview_firework_box.py --profile iphone16_balanced`
- User-visible behavior: Production gameplay remains unchanged. Manual preview rocket launches are slower, less uniform, and draw short tails.
- Preservation: `main.py` was unchanged. Production runtime, preset parameters, pure generation behavior, Halo, scenery, and profile values were unchanged.
- Follow-up: Use the manual visual checklist and inspect `R + H + 0` stress mode before choosing density tuning, Halo planning, or runtime integration planning.

## 2026-06-25 T0003.8.5 Review external Firework.py for future preset candidates

- Summary: Reviewed `/Users/toytoytoy330/Desktop/AllMyFiles/Pyxel/01_kamito/Firework.py` as reference material only and documented future preset candidates in `docs/research/external_firework_candidates_20260625.md`.
- Pre-task git state: branch `main`; worktree clean; latest commit `2c57a7b Fix preview rocket launch pacing`.
- Files changed: `docs/research/external_firework_candidates_20260625.md`, `goals/decision_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, `goals/done_log.md`, and `GPT_HANDOFF.md`.
- Analysis covered:
  - Halo
  - Elliptical / Orbit
  - Golden Bloom / Fibonacci
  - Counter Ring
  - Star
  - Heart
  - Sierpinski
  - Magic Square / Grid
  - Radiating Sphere Projection
- Key decision: Treat external functions as 2D mathematical/visual reference only. Future presets should be translated into deterministic 3D `Vec3` / `ParticleSpawnSpec` generation.
- Recommended order: Halo, Orbit/Elliptical, Golden Bloom/Fibonacci, Counter Ring, shape-plane scaffold, Star, Heart, then geometry bursts.
- Tests:
  - `.venv/bin/python -m json.tool goals/task_queue.json` passed.
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest` passed: 132 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 132 passed.
- User-visible behavior: None. This was a documentation-only research task.
- Preservation: `main.py` was unchanged. Production runtime, preset parameters, pure generation behavior, preview behavior, Halo implementation, and scenery were unchanged. No external code was copied.
- Follow-up: Run visual density review first. If stable, implement Halo next; otherwise tune Senrin, Multi-ring, or Willow density before adding presets.

## 2026-06-25 T0003.8.6 Add type-colored rocket tails and burst accent rays

- Summary: Added preview-only VFX accents: rockets now use burst-type tail colors, and selected explosion particles draw short-lived center-outward accent rays.
- Pre-task git state: branch `main`; worktree clean; latest commit `5fc3709 Document external firework preset candidates`.
- Files changed: `tools/preview_firework_box.py`, `docs/research/visual_tuning_checklist.md`, `goals/decision_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, `goals/done_log.md`, and `GPT_HANDOFF.md`.
- Behavior:
  - Rocket tail colors are frozen by scheduled burst type.
  - `Z`, random mode, auto launch, fixed-count salvos, and random-count salvos all use type-colored rocket tails.
  - A deterministic limited subset of primary burst particles draws short-lived accent rays from the burst origin.
  - Senrin secondary bursts do not get added accent rays.
  - Existing particle trail behavior remains unchanged.
- Tests:
  - `.venv/bin/python -m json.tool goals/task_queue.json` passed.
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest` passed: 132 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 132 passed.
- Manual preview command: `.venv/bin/python tools/preview_firework_box.py --profile iphone16_balanced`
- User-visible behavior: Production gameplay remains unchanged. Manual preview launches and burst starts are more readable and type-aware.
- Preservation: `main.py` was unchanged. Production runtime, preset parameters, pure generation behavior, Halo, scenery, and external Firework.py integration were unchanged.
- Follow-up: Use `R + H + 0` to check accent density. If stable, proceed to Halo; if not, tune accent ray density or high-risk presets first.

## 2026-06-25 Restore preview rocket fireball shape

- Summary: Kept type-colored rocket palettes but changed the preview rocket head from a single pixel back to a compact fireball cluster.
- Files changed: `tools/preview_firework_box.py`, `goals/decision_log.md`, and `goals/done_log.md`.
- Behavior:
  - Rocket tails remain type-colored.
  - Rocket heads now draw as a small 5-pixel cluster using the same type color set.
  - Tail length, rocket pacing, accent rays, and burst generation are unchanged.
- Tests:
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest` passed: 132 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 132 passed.
- Manual preview command: `.venv/bin/python tools/preview_firework_box.py --profile iphone16_balanced`
- Preservation: `main.py` was unchanged. Production runtime, preset parameters, pure generation behavior, Halo, and scenery were unchanged.
