# Architecture Compass

## Core principle

Keep Pyxel-specific side effects at the boundary.
Keep game logic as deterministic and testable as practical.

## Layers

```text
app / loop
  Pyxel initialization and run boundary

input / audio / render
  Pyxel API adapters

scenes
  scene orchestration

systems
  state update logic

model
  data structures and deterministic behavior

resources
  path and asset loading helpers
```

## Dependency direction

Preferred direction:

```text
app -> loop -> scenes -> systems -> model
render -> model
input -> commands
audio -> sound events
```

Avoid:

```text
model -> pyxel
systems -> pyxel drawing
deep modules importing app
```

## Why this matters

Codex performs better when responsibilities are explicit.
This structure reduces the chance that a small visual change becomes a broad rewrite.
