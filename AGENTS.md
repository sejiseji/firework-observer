# AGENTS.md

## Project purpose

This is a Pyxel game project optimized for goal-oriented semi-automatic development with Codex.

The repository is intentionally documentation-heavy because Codex should not rely on vague long-term inference.
Durable goals, constraints, and decisions are stored as project files.

Before non-trivial implementation, read:

- `docs/product/GAME_BRIEF.md`
- `docs/product/NORTH_STAR.md`
- `docs/product/GAME_DESIGN.md`
- `docs/product/NON_GOALS.md`
- `docs/architecture/ARCHITECTURE_COMPASS.md`
- `goals/GOAL_STATE.md`
- `goals/task_queue.json`

## Working rules

- Implement one coherent behavioral change per task.
- Prefer small patches over broad rewrites.
- Do not redesign architecture unless the task explicitly asks for it.
- Keep `pyxel.run()` behind the app/loop boundary.
- Keep deterministic game logic outside direct Pyxel API calls where practical.
- Prefer pure Python models and systems that can be tested without opening a Pyxel window.
- Treat `docs/` and `goals/` as durable project memory.
- Treat `.codex/` as tool configuration, not the product source of truth.
- Record important design decisions in `docs/adr/`.

## Expected task format

When starting a task, identify:

- Goal
- Relevant docs
- Files likely to change
- Constraints
- Validation commands
- Done condition

## Validation

Run these before reporting completion when relevant:

```bash
uv run pytest
uv run ruff check .
```

For rendering or gameplay feel changes, also run or update:

```bash
uv run python scripts/capture_smoke.py
```

If a command cannot be run, report exactly why.

## Done means

A task is done only when:

- the requested behavior is implemented,
- relevant tests pass or the failure is clearly explained,
- risky decisions are documented,
- user-visible changes are summarized,
- follow-up tasks are added to `goals/task_queue.json` when needed.
