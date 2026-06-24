# Goal-Driven Codex Mode

Use this prompt when asking Codex or another GPT session to continue development.

```text
Read AGENTS.md, PROJECT_INIT.md, GPT_HANDOFF.md,
docs/product/GAME_BRIEF.md, docs/product/NORTH_STAR.md,
docs/product/GAME_DESIGN.md, docs/product/PLAYER_EXPERIENCE.md,
docs/product/NON_GOALS.md,
docs/architecture/SCREEN_PROFILES.md,
docs/architecture/SCENERY_OBJECTS.md,
docs/research/external_firework_reference.md,
goals/GOAL_STATE.md, goals/task_queue.json, and goals/decision_log.md.

Work in GOAL-DRIVEN mode.

Rules:
- Execute only the next eligible incomplete task from goals/task_queue.json.
- Do not skip ahead.
- Do not implement more than one task in this run.
- Do not broaden the design beyond the recorded brief.
- Keep the patch small and reviewable.
- Preserve current good-feeling behavior.
- Treat standalone main.py as a protected reference prototype unless the active task explicitly says otherwise.
- Do not modify main.py during T0002 or T0003.* unless a later task explicitly authorizes it.
- Do not copy external Firework.py code directly.
- docs/research/external_firework_reference.md is reference material only.
- Prefer data-driven FireworkPreset / TrailPreset / SecondaryPreset additions.
- Respect the coordinate convention: internal y is up, gravity is negative.
- Preserve partial trail philosophy: rockets always trail, particles only partially trail.
- Preserve render readability: rear box edges -> fireworks/particles -> front box edges.
- Treat screen profiles as linked to box dimensions, camera projection, UI placement, particle budget, and scenery scale.
- Do not solve scenery by drawing in screen coordinates; scenery must exist inside the same 3D observation box as fireworks and use the same projection pipeline.

Do not:
- implement multiple firework presets in one task
- rewrite the renderer while adding a preset
- tune unrelated camera behavior while adding a preset
- change main.py unless the active task explicitly permits it
- copy old Firework.py code directly
- add sound, screenshots, scoring, characters, maps, or gameplay objectives
- convert the project into a full 3D engine
- add screen-space 2D scenery backgrounds
- remove existing docs/goals workflow

For the selected task:
1. Restate the task goal.
2. List files you expect to touch.
3. Before editing, run `git status`, identify the current branch, and list currently changed files.
4. Identify risks before editing.
5. Implement the smallest useful change.
6. Add or update tests/checks where practical.
7. Run available validation commands.
8. If a tool is missing, record the exact missing dependency and suggested install command.
9. After the task, report `git diff --stat`.
10. Update goals/done_log.md and any relevant goal files.
11. Stop after this task. Do not start the next task.

Report format:

Goal:
- ...

Files changed:
- ...

Behavior preserved:
- ...

Implemented:
- ...

Validation:
- command: ...
  result: ...

Git:
- branch: ...
- pre-task status: ...
- diff stat: ...

Risks / follow-up:
- ...

Next recommended task:
- ...
```

## T0002 Environment Verification Prompt

Use this exact focus for `T0002`.

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

## Staged Firework Preset Implementation

Use this only after `T0002` and `T0002.5` are complete.

```text
We are now entering staged firework preset implementation.

Goal:
Implement fireworks one preset at a time using the existing goal/task system.

Do not implement all presets at once.

Implementation order:
1. radial/kiku
2. ring
3. spiral
4. willow
5. peony
6. multi_ring or halo
7. senrin / secondary burst

For each preset task:
- Add only the preset required by the task.
- Add deterministic generation logic only if the existing generator cannot express the shape.
- Keep Pyxel drawing outside pure simulation/model code.
- Add or update unit tests for deterministic particle generation.
- Do not change visual tuning unrelated to the current preset.
- Do not copy external Firework.py code.
- Use external_firework_reference.md only to infer visual ideas.
- Update docs or tuning checklist with expected visual behavior.
- Stop after the current preset task.

Acceptance criteria for each preset:
- Same seed produces same particle initial states.
- Particle count is bounded.
- Trails remain partial, not all-particle trails.
- The preset respects y-up coordinates.
- The preset can be selected or invoked without breaking existing presets.
- Existing tests and compile checks still pass, or failures are documented as environment gaps.
```
