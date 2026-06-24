# Pyxel Asset Pipeline Skill

Use this when adding, generating, baking, or exporting assets.

## Rules

- Raw assets go in `assets/raw/`.
- Generated intermediate assets go in `assets/generated/`.
- Pyxel resource files go in `assets/pyxel/`.
- Exports go in `assets/exports/`.
- Never overwrite source assets without an explicit task.

## Done condition

- Asset origin is clear.
- Bake/export command is documented.
- Runtime path is resolved through `src/pyxel_goal_game/resources/paths.py`.
