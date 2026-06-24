# ExecPlan 0001: Initial Playable Loop

## Goal

Create the smallest playable Pyxel loop with a visible scene, simple input, and clean exit behavior.

## Background

This template starts with a minimal architecture that separates Pyxel boundary code from testable logic.

## Non-goals

- no complex game progression
- no final art
- no broad framework
- no save system

## Implementation steps

1. Keep `App` as the Pyxel boundary.
2. Use `GameLoop` for update/draw dispatch.
3. Render a simple focus marker and sample particles.
4. Support arrow keys and Space.
5. Add tests for pure model/system logic.

## Validation commands

```bash
uv run pytest
uv run ruff check .
uv run python -m pyxel_goal_game
```

## Acceptance criteria

- game starts,
- input changes visible state,
- sample effect can be triggered,
- tests pass,
- no Pyxel run loop appears outside app/loop.

## User feedback required

After the first prototype, ask the user:

- Is the basic response speed acceptable?
- Should the next priority be visual polish, controls, or game rules?

## Progress log

- [ ] Initial loop implemented
- [ ] Smoke run confirmed
- [ ] User feedback recorded

## Decision log

- Use simple scene orchestration before adding any framework.
