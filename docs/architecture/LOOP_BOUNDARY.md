# Loop Boundary

## Rule

Only the app/loop layer should own the direct Pyxel run loop.

## Current entry points

- `src/pyxel_goal_game/__main__.py`
- `src/pyxel_goal_game/app.py`
- `src/pyxel_goal_game/loop.py`

## Update/draw separation

- `update()` mutates game state.
- `draw()` reads state and renders it.
- Pure logic should be tested outside Pyxel when possible.

## Codex warning

Do not call `pyxel.run()` in tests, systems, models, or tools.
