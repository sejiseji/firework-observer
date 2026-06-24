# Initialize Project From Hearing

Use this prompt with Codex after filling `project_brief.json`.

```text
Read:

- AGENTS.md
- PROJECT_INIT.md
- project_brief.json
- docs/product/QUESTIONNAIRE.md

Then initialize the project documentation.

Update only:

- docs/product/GAME_BRIEF.md
- docs/product/NORTH_STAR.md
- docs/product/GAME_DESIGN.md
- docs/product/PLAYER_EXPERIENCE.md
- docs/product/NON_GOALS.md
- goals/GOAL_STATE.md
- goals/roadmap.md
- goals/task_queue.json
- docs/adr/ only if a durable architecture decision is necessary

Do not implement gameplay yet.

Done when:
- project direction is explicit,
- non-goals are explicit,
- first 5 small Codex tasks are listed,
- unknowns are recorded as assumptions or user questions.
```
