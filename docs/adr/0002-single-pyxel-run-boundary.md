# ADR 0002: Single Pyxel Run Boundary

## Status

Accepted

## Context

Pyxel applications are driven by a run loop.
If the run loop spreads across the codebase, tests and Codex edits become fragile.

## Decision

Keep `pyxel.init()` and `pyxel.run()` in the app/loop boundary.

## Consequences

- Models and systems are easier to test.
- Rendering remains isolated.
- Some adapters are needed between pure state and Pyxel APIs.
