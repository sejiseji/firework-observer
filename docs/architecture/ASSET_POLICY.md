# Asset Policy

## Directories

- `assets/raw/`: editable originals
- `assets/generated/`: generated intermediate files
- `assets/pyxel/`: `.pyxres` files
- `assets/exports/`: exported builds or asset bundles

## Runtime loading

Use:

- `src/pyxel_goal_game/resources/paths.py`
- `src/pyxel_goal_game/resources/loader.py`

Do not hardcode fragile relative paths throughout the codebase.
