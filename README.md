# Pyxel Goal-Oriented Codex Template

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
```

Other supported launch paths:

```bash
python3 main.py
pyxel run main.py
.venv/bin/python main.py --profile iphone16_balanced
.venv/bin/python scripts/run_runtime_app.py --profile iphone16_balanced
```

`main.py` is the default public entrypoint. `scripts/run_runtime_app.py` remains an explicit runtime launcher for development, and `tools/preview_firework_box.py` remains the manual preview harness.

Runtime audio is enabled by default. Press `M` to mute or restore the simple chord-harmony music-box BGM and restrained firework explosion SFX.

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
