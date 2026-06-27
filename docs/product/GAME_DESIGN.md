# Game Design

## Working title

Firework Observer

## Genre

- Main: observation / toy / visual experience
- Sub: firework simulator

## Core loop

1. Player starts by: player opens a small observation space
2. Player repeatedly: player changes viewpoint and triggers/selects fireworks
3. The game responds by: fireworks launch, burst, trail, and fade
4. The player progresses by: visual discovery rather than score progression
5. The loop ends when: player exits when satisfied

## Win / lose

- Win condition: none
- Lose condition: none

## Controls

- arrow_keys: adjust viewpoint or focus
- space: launch firework
- z_x: change firework preset later

## Current firework set

The official runtime includes these first-class firework variants:

- Kiku
- Sphere Bloom
- Smile
- Ring
- Spiral
- Willow
- Long Willow
- Peony
- Multi-ring
- Senrin
- Halo

`Sphere Bloom` is the explicit canonical sphere-like bloom. `Smile` is a shaped burst with two eyes and a smiling mouth arc. `Long Willow` is the explicit longer falling willow / 枝垂れ variant. Existing Kiku, Peony, and Willow remain distinct and available.

Some eligible main fireworks can also produce delayed mini-burst garnish: small deterministic child blooms near the original burst after short staggered delays. This is a secondary show effect, not a separate main firework kind.
`Smile` does not use delayed mini-burst garnish so the face shape stays readable.

## Future observation space expansion

Screen profile and scenery work should be designed together because the observation box scale, projection camera, UI placement, particle budget, and scenery proportions are linked.

- The classic `256x144` profile remains the baseline.
- A balanced larger profile should target `236x512`.
- A larger optional profile may target `393x852`.
- Larger profiles should use a portrait/tall screen and internal firework volume so launch height, altitude differences, and falling trails remain expressive.
- Future in-box scenery should be quiet 3D line geometry that rotates with the box.
- Do not solve scenery by drawing 2D screen-space backgrounds.

## Design notes for Codex

- Preserve the recorded core loop unless explicitly asked to change it.
- Prefer one polished interaction over many unfinished mechanics.
- If product direction is ambiguous, record an assumption or ask for user feedback depending on risk.
