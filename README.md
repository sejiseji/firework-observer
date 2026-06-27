# Pyxel Goal-Oriented Codex Template

Japanese: [README.ja.md](README.ja.md)

A project template for semi-automatic Pyxel game development with Codex.

This repository is designed to make development stable by keeping the following information explicit:

- product goal
- non-goals
- architecture policy
- task queue
- acceptance criteria
- review checklist
- Codex handoff rules
- user feedback loop

## Quick start

```bash
uv sync
python main.py
uv run pytest
uv run ruff check .
python3 scripts/check_public_safety.py
```

Other supported launch paths:

```bash
python3 main.py
pyxel run main.py
.venv/bin/python main.py --profile iphone16_balanced
.venv/bin/python scripts/run_runtime_app.py --profile iphone16_balanced
```

`main.py` is the default public entrypoint. `scripts/run_runtime_app.py` remains an explicit runtime launcher for development, and `tools/preview_firework_box.py` remains the manual preview harness.

Before publishing, run `python3 scripts/check_public_safety.py`. Documentation and source files should use repository-relative paths such as `docs/...`, `src/...`, and `scripts/...`, not local machine paths.

Runtime audio is enabled by default. Press `M` to mute or restore the quiet chord-harmony music-box BGM and restrained firework explosion SFX.

A rare silent 3D wireframe UFO ambient flyby is enabled by default in the official runtime. UFOs use deterministic low, middle, or high pass heights. Press `U` to toggle it during review.

The current firework cycle includes Kiku, Sphere Bloom, Smile, Ring, Spiral, Willow, Long Willow, Peony, Multi-ring, Senrin, and Halo.
Each firework kind has three deterministic per-burst color palette variants, selected from the launch seed.
Kiku, Sphere Bloom, Peony, and Multi-ring can occasionally produce small delayed mini-burst garnish near the main bloom.
Smile is a shaped face burst and does not use delayed mini-burst garnish so the eyes and mouth remain readable.
Long Willow uses sparse decaying long-branch trails while baseline Willow remains lighter.

If you do not use `uv`, install dependencies manually from `pyproject.toml`.

## Main idea

Codex should not be expected to infer the whole project direction from short prompts.

Instead:

1. Human defines the goal in `docs/product/` and `goals/`.
2. Codex reads `AGENTS.md`, `GOAL_STATE.md`, and related architecture docs.
3. Codex implements one small coherent task.
4. Tests and checklists validate the result.
5. User feedback is recorded and fed back into the next task.


## Initialize from a game brief

This template includes a hearing sheet and initialization script.

1. Read `docs/product/QUESTIONNAIRE.md`.
2. Copy `project_brief.example.json` to `project_brief.json`.
3. Fill what you can.
4. Run:

```bash
python scripts/init_from_brief.py project_brief.json --apply
```

5. Give Codex the first task from `goals/task_queue.json`.

See `PROJECT_INIT.md` for details.
