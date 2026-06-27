# ADR 0001: Use src Layout

## Status

Accepted

## Context

The project needs reliable imports and tests during repeated Codex edits.

## Decision

Use `src/pyxel_goal_game/` for package source and `tests/` for tests.

## Consequences

- Imports are less likely to accidentally depend on the working directory.
- Test configuration is explicit.
- Scripts should import from the installed package path.
