# Goal State

## Current phase

Initialized prototype planning.

## Current goal

freely observing fireworks from changing angles

## Current playable target

player changes viewpoint and triggers/selects fireworks

## What Codex should optimize for

1. Follow `docs/product/GAME_BRIEF.md`.
2. Make small, testable changes.
3. Preserve architecture boundaries.
4. Record assumptions and risks.
5. Feed user answers back into durable docs.

## Current risks

- Codex may infer product direction beyond the brief.
- Visual quality may require subjective review.
- Performance can degrade if particles/trails are uncapped.
- Product decisions may remain hidden in chat unless documented.

## Current mitigation

- Use task queue.
- Use acceptance checklists.
- Use deterministic simulation where practical.
- Record feedback in docs and goals.
