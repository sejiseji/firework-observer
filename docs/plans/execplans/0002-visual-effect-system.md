# ExecPlan 0002: Visual Effect System

## Goal

Add a small, bounded visual effect system suitable for particles, fireworks, trails, or similar expressive Pyxel effects.

## Background

Visual effects are high-risk for performance and architecture drift.
This plan keeps effects bounded and testable.

## Non-goals

- no unbounded particle history
- no physically exact simulation requirement
- no dependency on external rendering engines

## Implementation steps

1. Define particle model.
2. Define deterministic update system.
3. Add capped particle spawning.
4. Add rendering adapter.
5. Add snapshot-style tests for lifecycle behavior.
6. Add smoke capture script if visuals change.

## Validation commands

```bash
uv run pytest
uv run ruff check .
uv run python scripts/capture_smoke.py
```

## Acceptance criteria

- particle count is bounded,
- particle lifecycle is tested,
- visual effect appears in game,
- performance budget is not knowingly violated.

## User feedback required

Ask whether the visual direction should be:

- smoother,
- more pixel-art-like,
- more abstract,
- more physically convincing.
