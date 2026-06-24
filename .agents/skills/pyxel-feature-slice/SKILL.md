# Pyxel Feature Slice Skill

Use this when implementing one gameplay or rendering feature.

## Procedure

1. Read `goals/GOAL_STATE.md`.
2. Read the relevant product and architecture documents.
3. Identify the smallest coherent behavior change.
4. Implement model/system logic first.
5. Add or update tests.
6. Touch rendering last.
7. Run validation commands.
8. Summarize behavior, files changed, tests, and risks.

## Avoid

- broad rewrites
- hidden global state
- changing player experience beyond the task
- mixing asset pipeline changes with gameplay logic unless required
