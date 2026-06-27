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

## 2026-06-25 Replace fireball stick tail with ember trail

- Summary: Changed the launch fireball trail from connected line segments to separated ember pixels so it no longer reads as a rigid attached booster or stick.
- Files changed: `tools/preview_firework_box.py`, `goals/decision_log.md`, and `goals/done_log.md`.
- Behavior:
  - Type-colored palette remains unchanged.
  - Fireball head remains a compact pixel cluster.
  - Trailing effect now uses disconnected ember points from older history positions.
  - The newest history near the fireball head is skipped to leave a small visual gap.
- Tests:
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest` passed: 132 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 132 passed.
- Manual preview command: `.venv/bin/python tools/preview_firework_box.py --profile iphone16_balanced`
- Preservation: `main.py` was unchanged. Production runtime, preset parameters, pure generation behavior, Halo, and scenery were unchanged.

## 2026-06-25 Restore pre-color-change preview launch shape

- Summary: Restored the manual preview launch shape to the pre type-color-change form: connected recent-history trail segments plus a single bright head point, while preserving burst-type color palettes.
- Files changed: `tools/preview_firework_box.py`, `goals/decision_log.md`, and `goals/done_log.md`.
- Behavior:
  - Type-colored palettes remain unchanged.
  - The ember-point trail and compact 5-pixel head were removed.
  - Launch drawing now follows the older shape, with old/mid/head colors mapped from each burst type's palette.
  - Burst accent rays and particle generation are unchanged.
- Tests:
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest` passed: 132 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 132 passed.
- Manual preview command: `.venv/bin/python tools/preview_firework_box.py --profile iphone16_balanced`
- Preservation: `main.py` was unchanged. Production runtime, preset parameters, pure generation behavior, Halo, and scenery were unchanged.

## 2026-06-25 Draw preview launch fireball as filled teardrop

- Summary: Replaced line/ember-style launch drawing with a filled, direction-aware teardrop fireball shape using the existing burst-type palettes.
- Files changed: `tools/preview_firework_box.py`, `goals/decision_log.md`, and `goals/done_log.md`.
- Behavior:
  - The launch object is drawn as the firework shell/fireball itself, not as a rocket with an attached booster or stick.
  - The shape is filled with Pyxel triangles and capped with a bright nose color.
  - Type-colored palettes remain unchanged.
  - Burst accent rays and particle generation are unchanged.
- Tests:
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest` passed: 132 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 132 passed.
- Manual preview command: `.venv/bin/python tools/preview_firework_box.py --profile iphone16_balanced`
- Preservation: `main.py` was unchanged. Production runtime, preset parameters, pure generation behavior, Halo, and scenery were unchanged.

## 2026-06-25 T0003.8.7 Restore simple gradient firework shell tail

- Summary: Replaced the filled teardrop/type-colored launch visual with one shared short firework shell tail using the fixed white, white, white, yellow, yellow, brown, brown gradient.
- Files changed: `tools/preview_firework_box.py`, `docs/research/visual_tuning_checklist.md`, `goals/decision_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, `goals/done_log.md`, and `GPT_HANDOFF.md`.
- Behavior:
  - The rising object is documented and drawn as a firework shell/fireball, not a rocket or trajectory guide.
  - The tail uses only recent history samples.
  - Tail color is shared across all burst types.
  - Burst accent rays and particle generation are unchanged.
- Tests:
  - `.venv/bin/python -m json.tool goals/task_queue.json` passed.
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest` passed: 132 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 132 passed.
- Manual preview command: `.venv/bin/python tools/preview_firework_box.py --profile iphone16_balanced`
- Preservation: `main.py` was unchanged. Production runtime, preset parameters, pure generation behavior, Halo, and scenery were unchanged.

## 2026-06-25 T0004.0 Add preview scenery preset scaffold and switching

- Summary: Added preview-selectable low-detail 3D scenery inside the observation box.
- Files changed: `src/pyxel_goal_game/scenery_presets.py`, `tests/unit/test_scenery_presets.py`, `tools/preview_firework_box.py`, `docs/architecture/SCENERY_OBJECTS.md`, `docs/research/visual_tuning_checklist.md`, `goals/decision_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, `goals/done_log.md`, and `GPT_HANDOFF.md`.
- Behavior:
  - Added Pyxel-independent scenery data for `EMPTY`, `MOUNTAINS`, `CITY`, and `RIVERBANK`.
  - Scenery uses box-relative y-up 3D coordinates converted to `Vec3`.
  - Preview renders scenery through `Camera3D.project()`.
  - `G` cycles scenery presets.
  - `B` toggles scenery visibility.
  - Scenery is rendered as quiet line/polyline geometry, not as a 2D background.
- Tests:
  - `.venv/bin/python -m json.tool goals/task_queue.json` passed.
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest` passed: 151 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 151 passed.
  - `uv run python scripts/capture_smoke.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `uv run python scripts/capture_smoke.py` passed when run with approved `uv` cache access; it wrote `reports/visual_smoke/smoke_20260625_230244.txt`.
- Manual preview command: `.venv/bin/python tools/preview_firework_box.py --profile iphone16_balanced`
- Preservation: `main.py` was unchanged. Production runtime, firework preset parameters, pure firework generation behavior, Halo, and external Firework.py integration were unchanged.

## 2026-06-25 T0004.1 Refocus scenery to city-only 3D urban kit

- Summary: Refocused active preview scenery on `EMPTY` and `CITY`, and rebuilt `CITY` as low-detail 3D cuboid buildings with sparse windows.
- Files changed: `src/pyxel_goal_game/scenery_presets.py`, `tests/unit/test_scenery_presets.py`, `docs/architecture/SCENERY_OBJECTS.md`, `docs/research/visual_tuning_checklist.md`, `goals/decision_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, `goals/done_log.md`, and `GPT_HANDOFF.md`.
- Behavior:
  - Preview `G` cycle now effectively toggles `Empty` / `City`.
  - `CITY` is no longer a flat skyline; it is built from 3D wireframe cuboid building blocks.
  - Buildings use profile-scaled box-relative coordinates near the lower part of the observation box.
  - Sparse front/side windows are included, with a small subset brighter.
  - `MOUNTAINS` and `RIVERBANK` remain reference/dev functions but are not active preview cycle targets.
- Tests:
  - `.venv/bin/python -m json.tool goals/task_queue.json` passed.
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest` passed: 148 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 148 passed.
  - `uv run python scripts/capture_smoke.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `uv run python scripts/capture_smoke.py` passed when run with approved `uv` cache access; it wrote `reports/visual_smoke/smoke_20260625_232113.txt`.
- Manual preview command: `.venv/bin/python tools/preview_firework_box.py --profile iphone16_balanced`
- Preservation: `main.py` was unchanged. Production runtime, firework preset parameters, pure firework generation behavior, Halo, and external Firework.py integration were unchanged.

## 2026-06-26 T0004.1.1 Ground city building wireframes

- Summary: Adjusted CITY building wireframes so buildings rise from the cut floor plane instead of reading as loose miniature boxes.
- Files changed: `src/pyxel_goal_game/scenery_presets.py`, `tests/unit/test_scenery_presets.py`, `docs/architecture/SCENERY_OBJECTS.md`, `docs/research/visual_tuning_checklist.md`, `goals/decision_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, `goals/done_log.md`, and `GPT_HANDOFF.md`.
- Behavior:
  - CITY building blocks are slightly smaller and lower.
  - Building cuboids omit their bottom-face perimeter edges.
  - Vertical edges, top edges, and sparse windows remain.
  - City scenery remains Pyxel-independent 3D line geometry.
- Tests:
  - `.venv/bin/python -m json.tool goals/task_queue.json` passed.
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest` passed: 150 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 150 passed.
  - `uv run python scripts/capture_smoke.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `uv run python scripts/capture_smoke.py` passed when run with approved `uv` cache access; it wrote `reports/visual_smoke/smoke_20260626_062740.txt`.
- Manual preview command: `.venv/bin/python tools/preview_firework_box.py --profile iphone16_balanced`
- Preservation: `main.py` was unchanged. Production runtime, firework preset parameters, pure firework generation behavior, Halo, and external Firework.py integration were unchanged.

## 2026-06-26 T0003.8.9 Add subtle burst radius variation

- Summary: Added bounded deterministic burst radius variation through per-particle velocity magnitude wobble in pure burst generation.
- Files changed: `src/pyxel_goal_game/firework_bursts.py`, `tests/unit/test_firework_bursts.py`, `docs/research/visual_tuning_checklist.md`, `goals/decision_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, `goals/done_log.md`, and `GPT_HANDOFF.md`.
- Behavior:
  - Kiku, Peony, Ring, Spiral, Willow, Multi-ring, and Senrin primary bursts now have subtle bounded radius variation.
  - Speeds remain clamped to each preset's existing speed range.
  - Senrin secondary generation was left unchanged.
  - Firework shell tail rendering, CITY scenery, preview controls, and preset constants were unchanged.
- Tests:
  - `.venv/bin/python -m json.tool goals/task_queue.json` passed.
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest` passed: 157 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 157 passed.
  - `uv run python scripts/capture_smoke.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `uv run python scripts/capture_smoke.py` passed when run with approved `uv` cache access; it wrote `reports/visual_smoke/smoke_20260626_071945.txt`.
- Manual preview command: `.venv/bin/python tools/preview_firework_box.py --profile iphone16_balanced`
- Preservation: `main.py` was unchanged. Production runtime, firework shell tail rendering, CITY scenery, preview controls, preset constants, Halo, and external Firework.py integration were unchanged.

## 2026-06-26 T0004.2 Add city landmark, utility poles, and wires

- Summary: Added CITY-only low-detail urban details: one 3D landmark tower, utility poles, and sagging overhead wire polylines.
- Files changed: `src/pyxel_goal_game/scenery_presets.py`, `tests/unit/test_scenery_presets.py`, `docs/architecture/SCENERY_OBJECTS.md`, `docs/research/visual_tuning_checklist.md`, `goals/decision_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, `goals/done_log.md`, and `GPT_HANDOFF.md`.
- Behavior:
  - CITY now includes one quiet 3D landmark tower below the main bloom region.
  - CITY now includes a few front-phase utility poles.
  - CITY now includes slightly sagging overhead wire polylines.
  - EMPTY / CITY remain the active scenery presets.
  - City scenery remains Pyxel-independent 3D line/polyline geometry.
- Tests:
  - `.venv/bin/python -m json.tool goals/task_queue.json` passed.
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest` passed: 158 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 158 passed.
  - `uv run python scripts/capture_smoke.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `uv run python scripts/capture_smoke.py` passed when run with approved `uv` cache access; it wrote `reports/visual_smoke/smoke_20260626_080011.txt`.
- Manual preview command: `.venv/bin/python tools/preview_firework_box.py --profile iphone16_balanced`
- Preservation: `main.py` was unchanged. Production runtime, firework presets, pure firework generation, shell tail behavior, preview controls, Halo, and external Firework.py integration were unchanged.

## 2026-06-26 T0003.9 Implement Halo preset

- Summary: Added deterministic Halo generation as a light, soft, wobbling ring-like burst.
- Files changed: `src/pyxel_goal_game/firework_presets.py`, `src/pyxel_goal_game/firework_bursts.py`, `tools/preview_firework_box.py`, `tests/unit/test_firework_bursts.py`, `docs/research/visual_tuning_checklist.md`, `goals/decision_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, `goals/done_log.md`, and `GPT_HANDOFF.md`.
- Behavior:
  - Added `HALO_TRAIL_PRESET` and `HALO_PRESET`.
  - Added deterministic `generate_halo_burst(origin, seed)`.
  - `generate_burst()` now supports `FireworkShape.HALO`.
  - Preview sequential, random, fixed-count salvo, and random-count salvo modes include Halo.
  - Halo reuses deterministic ring orientation behavior but stays single-layer, lighter than Multi-ring, and sparse in trails.
- Tests:
  - `.venv/bin/python -m json.tool goals/task_queue.json` passed.
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest` passed: 167 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 167 passed.
  - `uv run python scripts/capture_smoke.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `uv run python scripts/capture_smoke.py` passed when run with approved `uv` cache access; it wrote `reports/visual_smoke/smoke_20260626_174429.txt`.
- Manual preview command: `.venv/bin/python tools/preview_firework_box.py --profile iphone16_balanced`
- Preservation: `main.py` unchanged. Production runtime, CITY scenery, shell tail behavior, and existing firework preset parameters unchanged.

## 2026-06-26 T0004.2.1 Densify city blocks and replace utility poles with signage

- Summary: Refined active CITY into a denser cutaway urban mass by adding more grounded building blocks, enlarging and grounding the landmark tower, removing utility poles/wires, and adding low-detail building signage.
- Files changed: `src/pyxel_goal_game/scenery_presets.py`, `tests/unit/test_scenery_presets.py`, `docs/architecture/SCENERY_OBJECTS.md`, `docs/research/visual_tuning_checklist.md`, `goals/decision_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, `goals/done_log.md`, and `GPT_HANDOFF.md`.
- Behavior:
  - CITY now has a denser building footprint in the lower observation volume.
  - CITY building bottom-face perimeter edges remain omitted.
  - The landmark tower is larger and reaches the floor baseline.
  - Utility poles and overhead wire polylines were removed from active CITY.
  - CITY now includes wall-mounted, projecting, and rooftop signs.
  - EMPTY / CITY remain the active scenery presets.
- Tests:
  - `.venv/bin/python -m json.tool goals/task_queue.json` passed.
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest` passed: 170 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 170 passed.
  - `uv run python scripts/capture_smoke.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `uv run python scripts/capture_smoke.py` passed when run with approved `uv` cache access; it wrote `reports/visual_smoke/smoke_20260626_190406.txt`.
- Manual preview command: `.venv/bin/python tools/preview_firework_box.py --profile iphone16_balanced`
- Preservation: `main.py` unchanged. Production runtime, firework generation, firework presets, shell tail behavior, preview controls, and Halo unchanged.

## 2026-06-26 Preview auto-rotation speed cycling

- Summary: Added preview-only auto-rotation speed cycling with `Q`.
- Files changed: `tools/preview_firework_box.py`, `goals/done_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, and `GPT_HANDOFF.md`.
- Behavior:
  - `X` still toggles auto-rotate ON/OFF.
  - `Q` cycles auto-rotate speed through `slow`, `normal`, and `fast`.
  - Default speed remains close to the previous auto-rotate behavior.
  - Debug HUD shows the current rotation speed label.
- Tests:
  - `python3 -m compileall tools/preview_firework_box.py` passed.
  - `.venv/bin/python -m pytest` passed: 170 tests passed.
  - `.venv/bin/python -m ruff check tools/preview_firework_box.py` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 170 passed.
  - `uv run python scripts/capture_smoke.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `uv run python scripts/capture_smoke.py` passed when run with approved `uv` cache access; it wrote `reports/visual_smoke/smoke_20260626_202712.txt`.
- Preservation: `main.py` unchanged. Production runtime, firework generation, scenery, shell tail behavior, and preview launch controls unchanged.

## 2026-06-26 T0004.2.3 Add ferris wheel and full-footprint city coverage

- Summary: Expanded active CITY building coverage across more of the lower observation-box footprint and added one low-detail ferris wheel.
- Files changed: `src/pyxel_goal_game/scenery_presets.py`, `tests/unit/test_scenery_presets.py`, `docs/architecture/SCENERY_OBJECTS.md`, `docs/research/visual_tuning_checklist.md`, `goals/decision_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, `goals/done_log.md`, and `GPT_HANDOFF.md`.
- Behavior:
  - CITY now includes additional small, medium, and modest mid-rise cuboid buildings spread toward the left, right, front, and rear lower floor area.
  - CITY building bottom-face perimeter edges remain omitted.
  - CITY now includes one static low-detail ferris wheel with rim segments, spokes, and support legs.
  - Utility poles and overhead wires remain absent from active CITY.
  - EMPTY / CITY remain the active scenery presets.
- Tests:
  - `.venv/bin/python -m json.tool goals/task_queue.json` passed.
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest` passed: 172 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 172 passed.
  - `uv run python scripts/capture_smoke.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `uv run python scripts/capture_smoke.py` passed when run with approved `uv` cache access; it wrote `reports/visual_smoke/smoke_20260626_204005.txt`.
- Manual preview command: `.venv/bin/python tools/preview_firework_box.py --profile iphone16_balanced`
- Preservation: `main.py` unchanged. Production runtime, firework generation, firework presets, shell tail behavior, preview controls, and auto-rotate speed control unchanged.

## 2026-06-26 T0004.2.4 Add interior twinkling box stars with toggle

- Summary: Added preview-only twinkling stars attached to the observation box's interior top and upper side faces, with `T` toggling and conservative interior-face visibility.
- Files changed: `src/pyxel_goal_game/ambient_box_stars.py`, `tools/preview_firework_box.py`, `tests/unit/test_ambient_box_stars.py`, `docs/architecture/SCENERY_OBJECTS.md`, `docs/research/visual_tuning_checklist.md`, `goals/decision_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, `goals/done_log.md`, and `GPT_HANDOFF.md`.
- Behavior:
  - Stars are generated as deterministic Pyxel-independent `Vec3` points attached to the box interior.
  - Stars are limited to the interior top face and upper side-face bands.
  - Stars are not placed on the floor, lower side walls, or open central volume.
  - Preview renders stars only when their attached interior face is visible.
  - `T` toggles stars ON/OFF in preview.
- Tests:
  - `.venv/bin/python -m json.tool goals/task_queue.json` passed.
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest` passed: 182 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 182 passed.
  - `uv run python scripts/capture_smoke.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `uv run python scripts/capture_smoke.py` passed when run with approved `uv` cache access; it wrote `reports/visual_smoke/smoke_20260626_204637.txt`.
- Manual preview command: `.venv/bin/python tools/preview_firework_box.py --profile iphone16_balanced`
- Preservation: `main.py` unchanged. Production runtime, firework generation, burst radius variation, firework presets, shell tail behavior, CITY geometry, UFO, and existing preview controls unchanged.

## 2026-06-26 T0004.2.5 Tune burst compactness and city landmark layout

- Summary: Tightened deterministic burst radius wobble, enlarged the CITY ferris wheel, and adjusted building placement to preserve a central boulevard-like open corridor.
- Files changed: `src/pyxel_goal_game/firework_bursts.py`, `src/pyxel_goal_game/scenery_presets.py`, `tests/unit/test_firework_bursts.py`, `tests/unit/test_scenery_presets.py`, `docs/architecture/SCENERY_OBJECTS.md`, `docs/research/visual_tuning_checklist.md`, `goals/decision_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, `goals/done_log.md`, and `GPT_HANDOFF.md`.
- Behavior:
  - Burst radius variation remains deterministic but uses tighter per-kind wobble factors.
  - Particle counts and preset constants remain unchanged.
  - Senrin secondary generation remains unchanged.
  - The CITY ferris wheel is larger and has more rim/spoke segments.
  - CITY building blocks avoid the central corridor while preserving broader lower-footprint coverage.
  - Utility poles and overhead wires remain absent from active CITY.
- Tests:
  - `.venv/bin/python -m json.tool goals/task_queue.json` passed.
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest` passed: 183 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 183 passed.
  - `uv run python scripts/capture_smoke.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `uv run python scripts/capture_smoke.py` passed when run with approved `uv` cache access; it wrote `reports/visual_smoke/smoke_20260626_212142.txt`.
- Manual preview command: `.venv/bin/python tools/preview_firework_box.py --profile iphone16_balanced`
- Preservation: `main.py` unchanged. Production runtime, preview controls, shell tail behavior, interior stars, UFO, and firework preset constants unchanged.

## 2026-06-26 T0004.2.6 Tune preview auto rotate comfort

- Summary: Reduced preview auto-rotate normal and fast speeds and scaled vertical pitch sway by speed mode.
- Files changed: `tools/preview_firework_box.py`, `tests/unit/test_preview_auto_rotate.py`, `docs/research/visual_tuning_checklist.md`, `goals/decision_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, `goals/done_log.md`, and `GPT_HANDOFF.md`.
- Behavior:
  - `X` still toggles auto-rotate ON/OFF.
  - `Q` still cycles `slow`, `normal`, and `fast`.
  - Auto-rotate speeds are now `slow=0.0035`, `normal=0.0065`, and `fast=0.0100`.
  - Pitch sway now scales by mode, with slow using the smallest vertical sway.
  - Debug HUD still shows `rot slow/normal/fast`.
- Tests:
  - `.venv/bin/python -m json.tool goals/task_queue.json` passed.
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest` passed: 188 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` then failed under approved `uv` cache access because `uv run pytest` did not include the repo root on `sys.path` for `tests/unit/test_preview_auto_rotate.py`; the test was updated to insert the repo root explicitly.
  - `python3 scripts/check_all.py` passed after the import-path test fix; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 188 passed.
  - `uv run python scripts/capture_smoke.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `uv run python scripts/capture_smoke.py` passed when run with approved `uv` cache access; it wrote `reports/visual_smoke/smoke_20260626_212808.txt`.
- Manual preview command: `.venv/bin/python tools/preview_firework_box.py --profile iphone16_balanced`
- Preservation: `main.py` unchanged. Production runtime, firework generation, burst radius variation, shell tail behavior, CITY geometry, ferris wheel geometry, boulevard layout, interior stars, UFO, and firework preset constants unchanged.

## 2026-06-26 T0004.2.8 Tune ceiling stars, glitter residue, ferris wheel roundness, and city edge coverage

- Summary: Relaxed top-face interior star visibility, added sparse preview-only glitter residue after bursts, made the CITY ferris wheel read more circular, and added peripheral CITY buildings while preserving the central boulevard.
- Files changed: `src/pyxel_goal_game/ambient_box_stars.py`, `src/pyxel_goal_game/scenery_presets.py`, `tools/preview_firework_box.py`, `tests/unit/test_ambient_box_stars.py`, `tests/unit/test_scenery_presets.py`, `tests/unit/test_preview_auto_rotate.py`, `docs/architecture/SCENERY_OBJECTS.md`, `docs/research/visual_tuning_checklist.md`, `goals/decision_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, `goals/done_log.md`, and `GPT_HANDOFF.md`.
- Behavior:
  - Top-face stars remain visible at shallower interior viewing angles.
  - Side-wall star visibility remains on the previous stricter threshold.
  - Burst glitter residue is preview-only, bounded, short-lived, and sparse.
  - CITY ferris wheel geometry is more circular and remains grounded/inside bounds.
  - Extra CITY buildings cover sparse side/peripheral regions while preserving the boulevard and launch readability.
  - Utility poles and overhead wires remain absent.
- Tests:
  - Targeted pytest for ambient stars, scenery presets, and preview auto-rotate/glitter tests passed: 44 tests passed.
  - Targeted ruff check for changed pure/preview/test files passed.
  - `.venv/bin/python -m json.tool goals/task_queue.json` passed.
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest` passed: 192 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 192 passed.
  - `uv run python scripts/capture_smoke.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `uv run python scripts/capture_smoke.py` passed when run with approved `uv` cache access; it wrote `reports/visual_smoke/smoke_20260626_215154.txt`.
- Manual preview command: `.venv/bin/python tools/preview_firework_box.py --profile iphone16_balanced`
- Preservation: `main.py` unchanged. Production runtime, preview controls, shell tail behavior, burst compactness, auto-rotate comfort, UFO, and firework preset constants unchanged.

## 2026-06-26 T0004.2.8.1 Relax ceiling star shallow-angle visibility

- Summary: Relaxed only the top-face interior star visibility threshold further so ceiling stars stay visible when the eye line is closer to parallel with the ceiling plane.
- Files changed: `src/pyxel_goal_game/ambient_box_stars.py`, `tests/unit/test_ambient_box_stars.py`, `docs/architecture/SCENERY_OBJECTS.md`, `docs/research/visual_tuning_checklist.md`, `goals/decision_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, `goals/done_log.md`, and `GPT_HANDOFF.md`.
- Behavior:
  - Top-face stars remain visible at smaller eye-line-to-ceiling angles.
  - Side-wall star visibility thresholds remain unchanged.
  - Star placement, CITY, fireworks, shell tail, preview controls, and production runtime remain unchanged.
- Tests:
  - `.venv/bin/python -m json.tool goals/task_queue.json` passed.
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest` passed: 192 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 192 passed.
  - `uv run python scripts/capture_smoke.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `uv run python scripts/capture_smoke.py` passed when run with approved `uv` cache access; it wrote `reports/visual_smoke/smoke_20260626_220014.txt`.
- Manual preview command: `.venv/bin/python tools/preview_firework_box.py --profile iphone16_balanced`
- Preservation: `main.py` unchanged. Production runtime, firework generation, shell tail behavior, CITY, glitter residue, auto-rotate comfort, UFO, and preview controls unchanged.

## 2026-06-26 T0004.2.9 Balance city building outline brightness

- Summary: Changed CITY building cuboid outline colors from height-based selection to an even, interleaved bright-blue/dark-blue pattern.
- Files changed: `src/pyxel_goal_game/scenery_presets.py`, `tests/unit/test_scenery_presets.py`, `docs/architecture/SCENERY_OBJECTS.md`, `docs/research/visual_tuning_checklist.md`, `goals/decision_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, `goals/done_log.md`, and `GPT_HANDOFF.md`.
- Behavior:
  - CITY building cuboid outlines are split evenly between bright blue and dark blue.
  - Bright and dark buildings are interleaved so they do not form large same-brightness clusters.
  - Landmark tower, ferris wheel, signage, windows, CITY geometry, preview controls, fireworks, and shell tail remain unchanged.
- Tests:
  - `.venv/bin/python -m json.tool goals/task_queue.json` passed.
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest` passed: 193 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 193 passed.
  - `uv run python scripts/capture_smoke.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `uv run python scripts/capture_smoke.py` passed when run with approved `uv` cache access; it wrote `reports/visual_smoke/smoke_20260626_220645.txt`.
- Manual preview command: `.venv/bin/python tools/preview_firework_box.py --profile iphone16_balanced`
- Preservation: `main.py` unchanged. Production runtime, firework generation, shell tail behavior, CITY geometry, tower, ferris wheel, signage, windows, UFO, and preview controls unchanged.

## 2026-06-26 T0004.2.10 Increase city building count to 48

- Summary: Increased active CITY building cuboids to 48 while preserving the balanced bright-blue/dark-blue building outline distribution.
- Files changed: `src/pyxel_goal_game/scenery_presets.py`, `tests/unit/test_scenery_presets.py`, `docs/architecture/SCENERY_OBJECTS.md`, `docs/research/visual_tuning_checklist.md`, `goals/decision_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, `goals/done_log.md`, and `GPT_HANDOFF.md`.
- Behavior:
  - CITY now uses 48 building cuboids.
  - Building outlines remain evenly split between bright blue and dark blue.
  - Bright/dark building groups remain interleaved.
  - Central boulevard, tower, ferris wheel, signage, windows, preview controls, fireworks, and shell tail remain unchanged.
- Tests:
  - `.venv/bin/python -m json.tool goals/task_queue.json` passed.
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest` passed: 193 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 193 passed.
  - `uv run python scripts/capture_smoke.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `uv run python scripts/capture_smoke.py` passed when run with approved `uv` cache access; it wrote `reports/visual_smoke/smoke_20260626_221128.txt`.
- Manual preview command: `.venv/bin/python tools/preview_firework_box.py --profile iphone16_balanced`
- Preservation: `main.py` unchanged. Production runtime, firework generation, shell tail behavior, tower, ferris wheel, signage, windows, UFO, and preview controls unchanged.

## 2026-06-26 T0003.8.11 Reduce burst radius maximum width

- Summary: Reduced primary firework burst radius by applying an 80% radius speed scale after deterministic wobble and clamping.
- Files changed: `src/pyxel_goal_game/firework_bursts.py`, `tests/unit/test_firework_bursts.py`, `docs/research/visual_tuning_checklist.md`, `goals/decision_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, `goals/done_log.md`, and `GPT_HANDOFF.md`.
- Behavior:
  - Primary burst velocity magnitudes are reduced to 80% of the previous bounded generated speed.
  - Deterministic per-kind wobble remains.
  - Trail decisions use pre-radius-scale speed so trail tendencies remain stable.
  - Senrin secondary, preset constants, shell tail, CITY, preview controls, and production runtime remain unchanged.
- Tests:
  - `.venv/bin/python -m json.tool goals/task_queue.json` passed.
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest` passed: 193 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 193 passed.
  - `uv run python scripts/capture_smoke.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `uv run python scripts/capture_smoke.py` passed when run with approved `uv` cache access; it wrote `reports/visual_smoke/smoke_20260626_221728.txt`.
- Manual preview command: `.venv/bin/python tools/preview_firework_box.py --profile iphone16_balanced`
- Preservation: `main.py` unchanged. Production runtime, firework preset constants, Senrin secondary, shell tail behavior, CITY, UFO, and preview controls unchanged.

## 2026-06-26 T0004.2.8.2 Keep ceiling stars visible at near-parallel angles

- Summary: Widened only the top-face interior star visibility threshold so ceiling stars stay visible at near-parallel eye-line-to-ceiling angles.
- Files changed: `src/pyxel_goal_game/ambient_box_stars.py`, `tests/unit/test_ambient_box_stars.py`, `docs/architecture/SCENERY_OBJECTS.md`, `docs/research/visual_tuning_checklist.md`, `goals/decision_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, `goals/done_log.md`, and `GPT_HANDOFF.md`.
- Behavior:
  - Top-face stars remain visible at the practical shallow-angle limit.
  - Side-wall visibility thresholds remain unchanged.
  - Star placement, CITY, fireworks, shell tail, preview controls, and production runtime remain unchanged.
- Tests:
  - `.venv/bin/python -m json.tool goals/task_queue.json` passed.
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest` passed: 193 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 193 passed.
  - `uv run python scripts/capture_smoke.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `uv run python scripts/capture_smoke.py` passed when run with approved `uv` cache access; it wrote `reports/visual_smoke/smoke_20260626_222047.txt`.
- Manual preview command: `.venv/bin/python tools/preview_firework_box.py --profile iphone16_balanced`
- Preservation: `main.py` unchanged. Production runtime, firework generation, shell tail behavior, CITY, UFO, and preview controls unchanged.

## 2026-06-26 T0005.0 Preview-to-runtime integration contract

- Summary: Added `docs/architecture/PREVIEW_TO_RUNTIME_INTEGRATION.md` to define how the first-generation preview should be promoted into package runtime without importing from `tools/` or modifying protected `main.py`.
- Files changed: `docs/architecture/PREVIEW_TO_RUNTIME_INTEGRATION.md`, `docs/architecture/PROTOTYPE_RECONCILIATION.md`, `docs/research/visual_tuning_checklist.md`, `goals/decision_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, `goals/done_log.md`, and `GPT_HANDOFF.md`.
- Behavior:
  - Documentation-only.
  - First-generation preview behavior is now the runtime promotion reference.
  - Follow-up runtime extraction tasks are documented as `T0005.1` through `T0005.6`.
  - Runtime must not import `tools/preview_firework_box.py`.
  - `main.py` remains protected until a separate explicit handoff task.
- Tests:
  - `.venv/bin/python -m json.tool goals/task_queue.json` passed.
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest` passed: 193 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 193 passed.
  - Visual smoke was not run because this was a docs-only integration planning task.
- Preservation: `main.py` unchanged. Source behavior, preview behavior, tests, firework generation, CITY, shell tail, stars, and production runtime unchanged.

## 2026-06-26 T0005.1 Add runtime state/controller scaffold

- Summary: Added the first package-side `pyxel_goal_game.runtime` scaffold with Pyxel-independent runtime state data and pure controller helpers for preview-equivalent state transitions.
- Files changed: `src/pyxel_goal_game/runtime/__init__.py`, `src/pyxel_goal_game/runtime/state.py`, `src/pyxel_goal_game/runtime/show_controller.py`, `tests/unit/test_runtime_state.py`, `tests/unit/test_runtime_show_controller.py`, `docs/architecture/PREVIEW_TO_RUNTIME_INTEGRATION.md`, `goals/decision_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, `goals/done_log.md`, and `GPT_HANDOFF.md`.
- Behavior:
  - Runtime state can represent selected profile, selected firework kind, active scenery, first-generation toggles, salvo count mode, auto-rotate speed mode, frame count, and seed base.
  - Show-controller helpers cover firework cycling, random mode, auto launch, height variation, stars, scenery visibility, auto rotate, rotate speed cycling, fixed salvos, random-count salvos, frame ticking, and seed advancement.
  - The scaffold is import-safe and does not import Pyxel or tools.
  - Preview is not yet migrated to use the scaffold.
- Tests:
  - Targeted runtime scaffold pytest passed: 16 tests passed.
  - Targeted runtime scaffold ruff check passed.
  - `.venv/bin/python -m json.tool goals/task_queue.json` passed.
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest` passed: 209 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 209 passed.
  - Visual smoke was not run because this scaffold task does not change visual behavior.
- Preservation: `main.py` unchanged. `tools/preview_firework_box.py` behavior unchanged. Firework generation, shell tail behavior, glitter residue, CITY geometry, interior stars, preview controls, and production runtime unchanged.

## 2026-06-26 T0005.2 Extract camera motion and auto-rotate comfort settings

- Summary: Added Pyxel-independent `runtime/camera_motion.py` with settled auto-rotate speed and pitch sway comfort settings, and updated the manual preview to consume those package-side settings.
- Files changed: `src/pyxel_goal_game/runtime/camera_motion.py`, `src/pyxel_goal_game/runtime/__init__.py`, `tools/preview_firework_box.py`, `tests/unit/test_runtime_camera_motion.py`, `tests/unit/test_preview_auto_rotate.py`, `docs/architecture/PREVIEW_TO_RUNTIME_INTEGRATION.md`, `docs/research/visual_tuning_checklist.md`, `goals/decision_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, `goals/done_log.md`, and `GPT_HANDOFF.md`.
- Behavior:
  - Auto-rotate speeds remain `slow=0.0035`, `normal=0.0065`, and `fast=0.0100`.
  - Pitch sway scales remain `slow=0.25`, `normal=0.55`, and `fast=0.80`.
  - Preview `X`, `Q`, and HUD mode label behavior are preserved.
  - Rendering and input ownership are not migrated yet.
- Tests:
  - Targeted camera motion and preview auto-rotate pytest passed: 15 tests passed.
  - `.venv/bin/python -m json.tool goals/task_queue.json` passed.
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest` passed: 217 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 217 passed.
  - Visual smoke was not run because preview behavior was intended to remain equivalent.
- Preservation: `main.py` unchanged. Firework generation, firework preset constants, burst radius scaling, shell tail, glitter residue, CITY, interior stars, UFO, and production runtime unchanged.

## 2026-06-26 T0005.3 Extract show launch and salvo scheduling

- Summary: Added Pyxel-independent runtime show scheduling helpers and updated the manual preview to consume immutable launch schedules for single launches, fixed salvos, random-count salvos, random firework kind selection, and height variation.
- Files changed: `src/pyxel_goal_game/runtime/show_schedule.py`, `src/pyxel_goal_game/runtime/__init__.py`, `tools/preview_firework_box.py`, `tests/unit/test_runtime_show_schedule.py`, `docs/architecture/PREVIEW_TO_RUNTIME_INTEGRATION.md`, `docs/research/visual_tuning_checklist.md`, `goals/decision_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, `goals/done_log.md`, and `GPT_HANDOFF.md`.
- Behavior:
  - Runtime schedule data records start frame, frame offsets, launch origin, burst origin, firework kind, and seed.
  - Single launch, fixed salvo, and random-count salvo schedule construction now live package-side.
  - Preview still owns shell simulation, particle spawning, rendering, shell tail, and glitter residue.
  - Preview key bindings and visual intent are preserved.
- Tests:
  - Targeted runtime schedule and salvo pytest passed: 33 tests passed.
  - `.venv/bin/python -m json.tool goals/task_queue.json` passed.
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest` passed: 233 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 233 passed.
  - `uv run python scripts/capture_smoke.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `uv run python scripts/capture_smoke.py` passed when run with approved `uv` cache access; it wrote `reports/visual_smoke/smoke_20260626_235351.txt`.
- Preservation: `main.py` unchanged. Firework generation, firework preset constants, burst radius scaling, shell tail, glitter residue, CITY, interior stars, camera motion, UFO, and production runtime unchanged.

## 2026-06-26 T0005.4 Add first official runtime app and entrypoint

- Summary: Added the first official package-side Firework Observer runtime app and launcher without modifying protected `main.py` or importing from `tools/preview_firework_box.py`.
- Files changed: `src/pyxel_goal_game/runtime/app.py`, `src/pyxel_goal_game/runtime/input.py`, `src/pyxel_goal_game/runtime/render.py`, `src/pyxel_goal_game/runtime/effects.py`, `scripts/run_runtime_app.py`, runtime import/input tests, integration docs, visual checklist, goals logs, roadmap, task queue, and `GPT_HANDOFF.md`.
- Behavior:
  - Official runtime launches separately with `.venv/bin/python scripts/run_runtime_app.py --profile iphone16_balanced`.
  - Runtime owns the Pyxel app loop, input mapping, rendering, active shell simulation, particle updates, secondary bursts, and glitter residue.
  - Runtime uses package-side state/controller, camera motion, and show scheduling modules.
  - Preview remains available as a development harness and regression viewer.
  - `main.py` remains protected and unchanged.
- Tests:
  - Validation results are recorded in the final task report.
- Preservation: Firework generation, preset constants, burst radius scaling, shell tail visual intent, glitter residue visual intent, CITY geometry, interior star behavior, camera motion settings, show scheduling semantics, UFO exclusion, and preview availability are preserved.

## 2026-06-26 T0005.5 Record runtime parity review and main.py handoff readiness

- Summary: Recorded manual runtime parity review results and marked `main.py` handoff readiness as `READY`.
- Files changed: `docs/research/runtime_parity_review_20260626.md`, `docs/architecture/PREVIEW_TO_RUNTIME_INTEGRATION.md`, `docs/research/visual_tuning_checklist.md`, `goals/decision_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, `goals/done_log.md`, and `GPT_HANDOFF.md`.
- Behavior:
  - Documentation-only.
  - Official runtime parity is recorded as OK.
  - Runtime stability is recorded as OK.
  - Preview remains the development harness.
  - `T0005.6` is now the next task to convert `main.py` into a thin official runtime launcher.
- Tests:
  - `.venv/bin/python -m json.tool goals/task_queue.json` passed.
  - `python3 -m compileall src tests scripts tools` passed.
  - `.venv/bin/python -m pytest` passed: 238 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 238 passed.
  - Visual smoke was not run because this was a documentation-only parity recording task.
- Preservation: `main.py` unchanged. Runtime behavior, preview behavior, firework generation, CITY, stars, shell tail, glitter residue, and controls unchanged.

## 2026-06-27 T0005.6 Convert main.py to official runtime launcher

- Summary: Converted `main.py` into a thin launcher for the official package runtime.
- Files changed: `main.py`, `tests/unit/test_main_launcher.py`, `docs/architecture/PREVIEW_TO_RUNTIME_INTEGRATION.md`, `docs/research/runtime_parity_review_20260626.md`, `docs/research/visual_tuning_checklist.md`, `goals/decision_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, `goals/done_log.md`, and `GPT_HANDOFF.md`.
- Behavior:
  - `.venv/bin/python main.py` is now the default project entry path for the official runtime.
  - `main.py` delegates to `pyxel_goal_game.runtime.app.main`.
  - `main.py` does not import `tools/preview_firework_box.py`.
  - `main.py` contains no copied runtime logic.
  - `tools/preview_firework_box.py` remains available as a development harness.
- Tests:
  - `.venv/bin/python main.py --help` passed.
  - `.venv/bin/python scripts/run_runtime_app.py --help` passed.
  - `.venv/bin/python -m json.tool goals/task_queue.json` passed.
  - `python3 -m compileall src tests scripts tools main.py` passed.
  - `.venv/bin/python -m pytest` passed: 239 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 239 passed.
  - `uv run python scripts/capture_smoke.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `uv run python scripts/capture_smoke.py` passed when run with approved `uv` cache access; it wrote `reports/visual_smoke/smoke_20260627_080123.txt`.
- Preservation: Firework generation, preset constants, burst radius scaling, shell tail, glitter residue, CITY, interior stars, camera motion, show scheduling, preview behavior, and UFO exclusion unchanged.

## 2026-06-27 T0005.6.1 Make main.py a robust simple launcher

- Summary: Made the default launcher robust for source-checkout and Pyxel-run startup. `main.py` keeps only the minimal `src/` bootstrap and official runtime delegation, while runtime CLI parsing normalizes Pyxel wrapper arguments such as `run main.py`.
- Files changed: `src/pyxel_goal_game/runtime/app.py`, `tests/unit/test_runtime_app_cli.py`, `README.md`, `docs/architecture/PREVIEW_TO_RUNTIME_INTEGRATION.md`, `docs/research/runtime_parity_review_20260626.md`, `docs/research/visual_tuning_checklist.md`, `goals/decision_log.md`, `goals/roadmap.md`, `goals/task_queue.json`, `goals/done_log.md`, and `GPT_HANDOFF.md`.
- Behavior:
  - `python main.py`, `python3 main.py`, `.venv/bin/python main.py`, and `pyxel run main.py` are documented as first-class launch paths.
  - `pyxel run main.py` style argv is normalized before argparse sees runtime options.
  - Default runtime profile is now `iphone16_balanced`.
  - Real invalid arguments still fail through argparse.
- Tests:
  - `.venv/bin/python -m json.tool goals/task_queue.json` passed.
  - `python3 -m compileall src tests scripts tools main.py` passed.
  - `.venv/bin/python -m pytest` passed: 248 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `.venv/bin/python main.py --help` passed.
  - `.venv/bin/python scripts/run_runtime_app.py --help` passed.
  - `python3 main.py --help` passed.
  - `python main.py --help` could not run because this shell has no `python` command (`zsh:1: command not found: python`).
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 248 passed.
  - `uv run python scripts/capture_smoke.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `uv run python scripts/capture_smoke.py` passed when run with approved `uv` cache access; it wrote `reports/visual_smoke/smoke_20260627_100216.txt`.
  - `.venv/bin/pyxel run main.py` was launched briefly and terminated after confirming it did not immediately fail with the prior `unrecognized arguments: run main.py` argparse error.
- Preservation: Runtime visual behavior, firework generation, preset constants, CITY, stars, shell tail, glitter residue, key bindings, preview harness, and UFO exclusion unchanged.

## 2026-06-27 T0006.0 Add runtime audio scaffold with music-box BGM and explosion SFX

- Summary: Added the first official runtime audio layer with high-register music-box BGM, low restrained explosion SFX, burst SFX cooldown, and `M` mute toggle.
- Files changed: `src/pyxel_goal_game/runtime/audio.py`, runtime state/controller/input/app/render modules, runtime audio tests, README, integration docs, visual checklist, goals logs, roadmap, task queue, and `GPT_HANDOFF.md`.
- Behavior:
  - Runtime audio starts by default when the official runtime initializes.
  - BGM uses quiet high-register music-box-style sound/music definitions.
  - Explosion SFX plays on actual burst events, not shell launch.
  - Explosion SFX uses a short frame cooldown to avoid excessive salvo stacking.
  - `M` toggles audio off and on.
  - Debug HUD reports audio enabled/disabled state.
- Tests:
  - `.venv/bin/python -m json.tool goals/task_queue.json` passed.
  - `python3 -m compileall src tests scripts tools main.py` passed.
  - `.venv/bin/python -m pytest` passed: 254 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `.venv/bin/python main.py --help` passed.
  - `.venv/bin/python scripts/run_runtime_app.py --help` passed.
  - Direct Pyxel audio setup smoke passed with `.venv/bin/python` and `RuntimeAudio`.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 254 passed.
  - `uv run python scripts/capture_smoke.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `uv run python scripts/capture_smoke.py` passed when run with approved `uv` cache access; it wrote `reports/visual_smoke/smoke_20260627_131819.txt`.
  - `.venv/bin/python main.py --profile iphone16_balanced` launched briefly with audio initialization and no immediate crash.
- Preservation: Visual behavior, firework generation, preset constants, CITY geometry, stars, shell tail, glitter visuals, camera motion, show scheduling, preview harness, robust main launcher, and UFO exclusion unchanged.

## 2026-06-27 T0006.1 Add BGM harmony and extend loop length

- Summary: Extended runtime BGM from a short, simple line into a longer multi-channel music-box arrangement with melody, arpeggio accompaniment, and sparse shimmer accents.
- Files changed: `src/pyxel_goal_game/runtime/audio.py`, `tests/unit/test_runtime_audio.py`, README, integration docs, visual checklist, goals logs, roadmap, task queue, and `GPT_HANDOFF.md`.
- Behavior:
  - BGM now uses three music channels for melody, high-register arpeggio, and sparse shimmer accents.
  - Channel 3 remains reserved for explosion SFX.
  - BGM loop phrase is longer and less repetitive.
  - Explosion SFX, cooldown, and `M` toggle behavior are preserved.
- Tests:
  - `.venv/bin/python -m json.tool goals/task_queue.json` passed.
  - `python3 -m compileall src tests scripts tools main.py` passed.
  - `.venv/bin/python -m pytest` passed: 255 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `.venv/bin/python main.py --help` passed.
  - Direct Pyxel audio setup smoke passed with `.venv/bin/python` and `RuntimeAudio`.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 255 passed.
  - `uv run python scripts/capture_smoke.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `uv run python scripts/capture_smoke.py` passed when run with approved `uv` cache access; it wrote `reports/visual_smoke/smoke_20260627_161125.txt`.
  - `.venv/bin/python main.py --profile iphone16_balanced` launched briefly with extended BGM initialization and no immediate crash.
- Preservation: Visual behavior, firework generation, preset constants, CITY geometry, stars, shell tail, glitter visuals, camera motion, show scheduling, preview harness, robust main launcher, and UFO exclusion unchanged.

## 2026-06-27 T0006.2 Rebuild BGM as simple chord harmony

- Summary: Rebuilt runtime BGM from independent arpeggio/shimmer-style secondary lines into aligned simple chord harmony.
- Files changed: `src/pyxel_goal_game/runtime/audio.py`, `tests/unit/test_runtime_audio.py`, README, integration docs, visual checklist, goals logs, roadmap, task queue, and `GPT_HANDOFF.md`.
- Behavior:
  - Channel 0 remains the dominant melody.
  - Channel 1 now acts as medium-volume harmony.
  - Channel 2 now acts as low-volume soft support.
  - Channel 3 remains reserved for low restrained explosion SFX.
  - The BGM loop remains longer than the original short loop, but no longer uses busy arpeggio/counter-line motion.
  - `M` mute toggle, SFX cooldown, and visual behavior are preserved.
- Tests:
  - `.venv/bin/python -m json.tool goals/task_queue.json` passed.
  - `.venv/bin/python -m pytest tests/unit/test_runtime_audio.py` passed: 7 tests passed.
  - `python3 -m compileall src tests scripts tools main.py` passed.
  - `.venv/bin/python -m pytest` passed: 255 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `.venv/bin/python main.py --help` passed.
  - Direct Pyxel audio setup smoke passed with `.venv/bin/python` and `RuntimeAudio`.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 255 passed.
  - `uv run python scripts/capture_smoke.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `uv run python scripts/capture_smoke.py` passed when run with approved `uv` cache access; it wrote `reports/visual_smoke/smoke_20260627_162233.txt`.
  - `.venv/bin/python main.py --profile iphone16_balanced` launched briefly with chord-harmony BGM initialization and no immediate crash.
- Preservation: Visual behavior, firework generation, preset constants, CITY geometry, stars, shell tail, glitter visuals, camera motion, show scheduling, preview harness, robust main launcher, and UFO exclusion unchanged.

## 2026-06-27 T0006.3 Tune BGM support rhythm and lower overall volume

- Summary: Lowered runtime BGM volume and changed channel 2 from high soft support into sparse mid-register rhythmic support so explosion SFX reads as the primary audio subject.
- Files changed: `src/pyxel_goal_game/runtime/audio.py`, `tests/unit/test_runtime_audio.py`, README, integration docs, visual checklist, goals logs, roadmap, task queue, and `GPT_HANDOFF.md`.
- Behavior:
  - Channel 0 melody volume changed from `5` to `4`.
  - Channel 1 harmony volume changed from `3` to `2`.
  - Channel 2 remains volume `1`, but now uses sparse octave-3 support pulses instead of high support tones.
  - Channel 3 remains reserved for low restrained explosion SFX.
  - `M` mute toggle, SFX cooldown, and visual behavior are preserved.
- Tests:
  - `.venv/bin/python -m json.tool goals/task_queue.json` passed.
  - `.venv/bin/python -m pytest tests/unit/test_runtime_audio.py` passed: 8 tests passed.
  - `python3 -m compileall src tests scripts tools main.py` passed.
  - `.venv/bin/python -m pytest` passed: 256 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `.venv/bin/python main.py --help` passed.
  - Direct Pyxel audio setup smoke passed with `.venv/bin/python` and `RuntimeAudio`.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 256 passed.
  - `uv run python scripts/capture_smoke.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `uv run python scripts/capture_smoke.py` passed when run with approved `uv` cache access; it wrote `reports/visual_smoke/smoke_20260627_163441.txt`.
  - `.venv/bin/python main.py --profile iphone16_balanced` launched briefly with calmer BGM support initialization and no immediate crash.
- Preservation: Visual behavior, firework generation, preset constants, CITY geometry, stars, shell tail, glitter visuals, camera motion, show scheduling, preview harness, robust main launcher, and UFO exclusion unchanged.

## 2026-06-27 T0007.0 Add rare UFO ambient flyby to official runtime

- Summary: Added a rare silent UFO ambient flyby to the official runtime as a non-interactive upper-space visual surprise.
- Files changed: `src/pyxel_goal_game/runtime/ufo.py`, runtime state/controller/app/input/render modules, runtime UFO/input/state/controller tests, README, integration docs, visual checklist, goals logs, roadmap, task queue, and `GPT_HANDOFF.md`.
- Behavior:
  - UFO scheduling/path helpers are Pyxel-independent and deterministic.
  - At most one UFO flyby is active at a time.
  - UFOs are delayed, rare, and use cooldown/check windows.
  - UFOs render as small low-detail line/pixel saucers in the 3D scene.
  - `U` toggles UFO ambient on/off for review.
  - UFOs have no beam, trail, sound, particles, collision, scoring, or gameplay interaction.
- Tests:
  - `.venv/bin/python -m json.tool goals/task_queue.json` passed.
  - `.venv/bin/python -m pytest tests/unit/test_runtime_ufo.py tests/unit/test_runtime_state.py tests/unit/test_runtime_show_controller.py tests/unit/test_runtime_input.py tests/unit/test_runtime_app_imports.py` passed: 28 tests passed.
  - `python3 -m compileall src tests scripts tools main.py` passed.
  - `.venv/bin/python -m pytest` passed: 263 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `.venv/bin/python main.py --help` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 263 passed.
  - `uv run python scripts/capture_smoke.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `uv run python scripts/capture_smoke.py` passed when run with approved `uv` cache access; it wrote `reports/visual_smoke/smoke_20260627_170034.txt`.
  - `.venv/bin/python main.py --profile iphone16_balanced` launched briefly with UFO ambient integration and no immediate crash.
- Preservation: Firework generation, preset constants, CITY geometry, stars, shell tail, glitter visuals, camera motion, show scheduling, audio behavior, preview harness, and robust main launcher unchanged.

## 2026-06-27 T0008.0 Add required sphere and willow firework variants

- Summary: Added `Sphere Bloom` as the explicit canonical sphere-like firework and `Long Willow` as the explicit longer falling willow / 枝垂れ variant.
- Files changed: `src/pyxel_goal_game/firework_presets.py`, `src/pyxel_goal_game/firework_bursts.py`, runtime ordering/effects modules, preview ordering/effects, firework/runtime tests, README, product docs, research docs, visual checklist, goals logs, roadmap, task queue, and `GPT_HANDOFF.md`.
- Behavior:
  - Runtime and preview cycle order is now Kiku, Sphere Bloom, Ring, Spiral, Willow, Long Willow, Peony, Multi-ring, Senrin, and Halo.
  - Random mode and salvo scheduling include both new variants through the shared runtime order.
  - `Sphere Bloom` uses deterministic native 3D spherical generation with a clean moderate particle count and restrained trails.
  - `Long Willow` uses deterministic willow generation with longer life, stronger fall, and stronger trail emphasis than baseline Willow.
  - Existing Kiku, Peony, and Willow remain available.
- Tests:
  - `.venv/bin/python -m json.tool goals/task_queue.json` passed.
  - Targeted firework/runtime/preview tests passed before full validation: 149 passed.
  - `python3 -m compileall src tests scripts tools main.py` passed.
  - `.venv/bin/python -m pytest` passed: 270 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `.venv/bin/python main.py --help` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 270 passed.
  - `uv run python scripts/capture_smoke.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `uv run python scripts/capture_smoke.py` passed when run with approved `uv` cache access; it wrote `reports/visual_smoke/smoke_20260627_171343.txt`.
  - `.venv/bin/python main.py --profile iphone16_balanced` launched briefly with Sphere Bloom / Long Willow integration and no immediate crash.
- Preservation: `main.py` unchanged. CITY, stars, UFO behavior, audio, shell tail, glitter visuals, camera motion, and robust launcher behavior unchanged.

## 2026-06-27 T0007.1 Replace UFO sprite with 3D wireframe saucer

- Summary: Replaced the official-runtime UFO's flat sprite-like drawing with a small 3D wireframe saucer built from Pyxel-independent `Vec3` geometry.
- Files changed: `src/pyxel_goal_game/runtime/ufo.py`, `src/pyxel_goal_game/runtime/render.py`, `tests/unit/test_runtime_ufo.py`, README, integration docs, visual checklist, goals logs, roadmap, task queue, and `GPT_HANDOFF.md`.
- Behavior:
  - UFO wireframe includes an elliptical rim, dome, shallow lower body, and three small light points.
  - UFO geometry follows the flyby position and travel direction and is projected through `Camera3D`.
  - UFO scheduling frequency, initial delay, cooldown, rarity, and `U` toggle behavior are unchanged.
  - UFO remains silent, beamless, trailless, particle-free, and non-interactive.
- Tests:
  - `.venv/bin/python -m json.tool goals/task_queue.json` passed.
  - Targeted UFO/runtime tests passed before full validation: 24 passed.
  - `python3 -m compileall src tests scripts tools main.py` passed.
  - `.venv/bin/python -m pytest` passed: 272 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `.venv/bin/python main.py --help` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 272 passed.
  - `uv run python scripts/capture_smoke.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `uv run python scripts/capture_smoke.py` passed when run with approved `uv` cache access; it wrote `reports/visual_smoke/smoke_20260627_174453.txt`.
  - `.venv/bin/python main.py --profile iphone16_balanced` launched briefly with wireframe UFO integration and no immediate crash.
- Preservation: Firework generation, CITY, stars, audio, shell tail, glitter visuals, camera motion, controls, and robust launcher behavior unchanged.

## 2026-06-27 T0008.1 Tune UFO visibility and Long Willow trail mixture

- Summary: Tuned UFO visibility with modestly larger wireframe geometry and deterministic low/middle/high flyby height bands, and tuned Long Willow to mix longer-trail branches with lighter falling embers.
- Files changed: `src/pyxel_goal_game/runtime/ufo.py`, `src/pyxel_goal_game/firework_bursts.py`, UFO/firework tests, README, integration docs, visual checklist, goals logs, roadmap, task queue, and `GPT_HANDOFF.md`.
- Behavior:
  - UFO radius range increased modestly while keeping the same rare scheduling cadence.
  - UFO flybys now record a deterministic `UfoHeightBand` and choose low, middle, or high upper-space pass bands.
  - Low UFO passes remain above CITY.
  - Long Willow keeps the same particle count but now mixes long-trail branches, short-trail embers, and no-trail embers.
  - Baseline Willow remains the lighter willow variant.
- Tests:
  - `.venv/bin/python -m json.tool goals/task_queue.json` passed.
  - Targeted UFO/firework tests passed before full validation: 113 passed.
  - `python3 -m compileall src tests scripts tools main.py` passed.
  - `.venv/bin/python -m pytest` passed: 274 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `.venv/bin/python main.py --help` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 274 passed.
  - `uv run python scripts/capture_smoke.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `uv run python scripts/capture_smoke.py` passed when run with approved `uv` cache access; it wrote `reports/visual_smoke/smoke_20260627_180003.txt`.
  - `.venv/bin/python main.py --profile iphone16_balanced` launched briefly with UFO height bands and Long Willow trail mixture and no immediate crash.
- Preservation: `main.py`, launcher behavior, CITY, stars, audio, shell tail, global glitter, UFO silence/no-beam/no-trail/no-particle constraints, firework order, random/salvo scheduling, and baseline Willow behavior unchanged.

## 2026-06-27 T0008.3 Add delayed mini-burst garnish

- Summary: Added optional delayed mini-burst garnish for eligible main fireworks.
- Files changed: `src/pyxel_goal_game/runtime/effects.py`, `src/pyxel_goal_game/runtime/app.py`, `tests/unit/test_runtime_effects.py`, README, product docs, integration docs, visual checklist, goals logs, roadmap, task queue, and `GPT_HANDOFF.md`.
- Behavior:
  - Eligible parents are Kiku, Sphere Bloom, Peony, and Multi-ring.
  - Excluded parents remain Willow, Long Willow, Ring, Halo, Senrin, and Spiral.
  - Garnish uses deterministic local random by parent kind and seed.
  - Each garnish event schedules 2 to 5 small child sphere-like bursts near the parent origin with staggered delays.
  - No new key binding or main firework kind was added.
- Tests:
  - `.venv/bin/python -m json.tool goals/task_queue.json` passed.
  - Targeted runtime effects/import tests passed before full validation: 8 passed.
  - `python3 -m compileall src tests scripts tools main.py` passed.
  - `.venv/bin/python -m pytest` passed: 279 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `.venv/bin/python main.py --help` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 279 passed.
  - `uv run python scripts/capture_smoke.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `uv run python scripts/capture_smoke.py` passed when run with approved `uv` cache access; it wrote `reports/visual_smoke/smoke_20260627_185835.txt`.
  - `.venv/bin/python main.py --profile iphone16_balanced` launched briefly with delayed mini-burst garnish and no immediate crash.
- Preservation: `main.py`, launcher behavior, CITY, stars, UFO, audio, shell tail, global glitter behavior, firework order, random/salvo scheduling, and existing main firework kinds unchanged.

## 2026-06-27 T0008.4 Add smile firework preset

- Summary: Added Smile as a first-class shaped firework preset.
- Files changed: `src/pyxel_goal_game/firework_presets.py`, `src/pyxel_goal_game/firework_bursts.py`, runtime/preview firework ordering, tests, README, product docs, integration docs, visual checklist, external candidate notes, goals logs, roadmap, task queue, and `GPT_HANDOFF.md`.
- Behavior:
  - `FireworkKind.SMILE` and `SMILE_PRESET` now exist.
  - Smile uses two small eye clusters and a smiling mouth arc in a front-biased 3D plane.
  - Runtime and preview cycle order is Kiku, Sphere Bloom, Smile, Ring, Spiral, Willow, Long Willow, Peony, Multi-ring, Senrin, and Halo.
  - Random mode and salvos can select Smile.
  - Smile is excluded from delayed mini-burst garnish so the face shape remains readable.
- Tests:
  - Targeted firework/runtime tests passed before full validation: 161 passed.
  - `python3 -m compileall src tests scripts tools main.py` passed.
  - `.venv/bin/python -m pytest` passed: 285 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `.venv/bin/python main.py --help` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 285 passed.
  - `uv run python scripts/capture_smoke.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `uv run python scripts/capture_smoke.py` passed when run with approved `uv` cache access; it wrote `reports/visual_smoke/smoke_20260627_191737.txt`.
  - `.venv/bin/python main.py --profile iphone16_balanced` launched briefly with Smile preset integration and no immediate crash.
- Preservation: `main.py`, launcher behavior, CITY, stars, UFO, audio, shell tail, global glitter behavior, delayed mini-burst garnish behavior for existing eligible kinds, and existing firework variants unchanged.

## 2026-06-27 T0008.3.2 Add per-burst color palette variants

- Summary: Added deterministic per-burst color palette variants for every current firework kind.
- Files changed: `src/pyxel_goal_game/firework_presets.py`, `src/pyxel_goal_game/firework_bursts.py`, `src/pyxel_goal_game/runtime/effects.py`, relevant tests, README, product docs, integration docs, visual checklist, goals logs, roadmap, task queue, and `GPT_HANDOFF.md`.
- Behavior:
  - Each firework kind has exactly three predefined palette variants.
  - Each launch selects one palette from the launch seed.
  - Burst particle colors use the selected palette without consuming the generation RNG.
  - Senrin secondary colors stay coherent with the selected Senrin palette.
  - Delayed mini-burst garnish inherits the selected parent palette.
  - Color variation does not change geometry, timing, shell tail, global glitter, Long Willow trail grouping, or controls.
- Tests:
  - Targeted firework/runtime tests passed before full validation: 150 passed.
  - `python3 -m compileall src tests scripts tools main.py` passed.
  - `.venv/bin/python -m pytest` passed: 290 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `.venv/bin/python main.py --help` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 290 passed.
  - `uv run python scripts/capture_smoke.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `uv run python scripts/capture_smoke.py` passed when run with approved `uv` cache access; it wrote `reports/visual_smoke/smoke_20260627_193029.txt`.
  - `.venv/bin/python main.py --profile iphone16_balanced` launched briefly with palette variants and no immediate crash.
- Preservation: `main.py`, launcher behavior, CITY, stars, UFO, audio, shell tail, global glitter behavior, Long Willow trail behavior, Smile behavior, and existing firework geometry unchanged.

## 2026-06-27 T0008.3.1 Tune Long Willow long trail decay

- Summary: Added Long Willow-only long branch trail history and sparse rear decay.
- Files changed: `src/pyxel_goal_game/firework_bursts.py`, `src/pyxel_goal_game/runtime/effects.py`, `src/pyxel_goal_game/runtime/render.py`, `tools/preview_firework_box.py`, relevant tests, README, integration docs, visual checklist, goals logs, roadmap, task queue, and `GPT_HANDOFF.md`.
- Behavior:
  - Only Long Willow long-trail branch particles receive long trail history.
  - Long branch particles keep about 56 frames of trail history, matching roughly 0.93 seconds at 60fps.
  - Older rear sections are sparsely broken by deterministic phase/step settings.
  - Baseline Willow has no long trail history.
  - Palette variants and palette inheritance remain unchanged.
- Tests:
  - Targeted firework/runtime/preview tests passed before full validation: 125 passed.
  - `python3 -m compileall src tests scripts tools main.py` passed.
  - `.venv/bin/python -m pytest` passed: 292 tests passed.
  - `.venv/bin/python -m ruff check .` passed.
  - `.venv/bin/python main.py --help` passed.
  - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 292 passed.
  - `uv run python scripts/capture_smoke.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
  - `uv run python scripts/capture_smoke.py` passed when run with approved `uv` cache access; it wrote `reports/visual_smoke/smoke_20260627_194247.txt`.
  - `.venv/bin/python main.py --profile iphone16_balanced` launched briefly with Long Willow trail decay and no immediate crash.
  - Follow-up shortening: Long branch trail history was reduced from 84 frames to 56 frames.
  - Follow-up fall-speed tuning: Long branch particles use softened downward velocity and reduced gravity so they fall more gently and avoid punching through the box floor.
  - Follow-up validation:
    - Targeted Long Willow/runtime tests passed: 117 passed.
    - `python3 -m compileall src tests scripts tools main.py` passed.
    - `.venv/bin/python -m pytest` passed: 292 tests passed.
    - `.venv/bin/python -m ruff check .` passed.
    - `.venv/bin/python main.py --help` passed.
    - `python3 scripts/check_all.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
    - `python3 scripts/check_all.py` passed when run with approved `uv` cache access; it ran `uv run pytest` and `uv run ruff check .`, and pytest reported 292 passed.
    - `uv run python scripts/capture_smoke.py` first failed in sandbox because `uv` could not access `/Users/toytoytoy330/.cache/uv`.
    - `uv run python scripts/capture_smoke.py` passed when run with approved `uv` cache access; it wrote `reports/visual_smoke/smoke_20260627_194909.txt`.
    - `.venv/bin/python main.py --profile iphone16_balanced` launched briefly with shorter Long Willow trail decay and no immediate crash.
- Preservation: `main.py`, launcher behavior, baseline Willow, shell tail, global glitter, CITY, stars, UFO, audio, Long Willow palette variants, mini-burst garnish palette inheritance, and firework geometry unchanged.
