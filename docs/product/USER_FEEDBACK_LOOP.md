# User Feedback Loop

## Purpose

This project assumes Codex may not safely resolve vague product direction on its own.

When a task contains ambiguity, do not silently decide product direction unless the answer is already recorded in:

- `docs/product/`
- `docs/architecture/`
- `goals/`
- `docs/adr/`

## Feedback states

Use these states in task reports:

- `clear`: enough information exists to implement
- `assumption-made`: implementation proceeded with an explicit assumption
- `needs-user-decision`: product direction is blocked
- `needs-playtest`: subjective feel must be checked by the user

## How to record feedback

- Stable product direction: update `docs/product/`
- Architecture decision: add or update `docs/adr/`
- Short-term task feedback: update `goals/task_queue.json`
- Completion notes: update `goals/done_log.md`
- Small decision: update `goals/decision_log.md`

## Rule for Codex

If a user answers a product question, convert that answer into a durable document update.
Do not leave important direction only in chat history.
