# Project Initialization Guide

This template is not meant to be used as a blank Python scaffold only.
It is meant to be initialized from a game concept brief.

## Recommended flow

1. Copy `project_brief.example.json` to `project_brief.json`.
2. Fill in the fields you can answer.
3. For unknown fields, write `"unknown"` or leave arrays empty.
4. Run:

```bash
python scripts/init_from_brief.py project_brief.json --apply
```

5. Review generated/updated documents:

- `docs/product/NORTH_STAR.md`
- `docs/product/GAME_DESIGN.md`
- `docs/product/PLAYER_EXPERIENCE.md`
- `docs/product/NON_GOALS.md`
- `goals/GOAL_STATE.md`
- `goals/roadmap.md`
- `goals/task_queue.json`

6. Give Codex this instruction:

```text
Read AGENTS.md, PROJECT_INIT.md, docs/product/GAME_BRIEF.md, goals/GOAL_STATE.md,
and goals/task_queue.json. Start from the first todo task only.
Do not broaden the design beyond the recorded brief.
```

## Important

Codex should not invent the whole game from a short genre label.

A genre such as "firework observation", "platformer", or "puzzle" is only a starting hint.
The durable source of truth should be `project_brief.json` and the generated project docs.

## When the user cannot answer everything

Proceed with explicit assumptions.

Record assumptions in:

- `docs/product/GAME_BRIEF.md`
- `goals/decision_log.md`
- `goals/task_queue.json`

Do not hide product decisions in chat history.
