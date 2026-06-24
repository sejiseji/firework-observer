# Game Brief

## Status

Initialized from `project_brief.json`.

## Identity

- Working title: Firework Observer
- One-line pitch: A smooth Pyxel prototype where the player observes expressive fireworks in a small cutout space.
- Main genre: observation / toy / visual experience
- Sub genre: firework simulator
- Target platform: local prototype, later browser demo
- Target audience: people who enjoy calm visual toys and compact Pyxel experiments
- Session length: 3-10 minutes
- Release intent: prototype

## North star

- First feeling: smooth, beautiful, surprisingly rich for Pyxel
- Memory after play: the fireworks felt alive and pleasant to observe
- Single most important experience: freely observing fireworks from changing angles
- Must not lose: smooth visual feel and small maintainable implementation
- Success definition: a playable prototype with satisfying fireworks, stable frame pacing, and clear Codex task continuity

## Player experience

- Mood: calm and beautiful
- Pace: meditative
- Difficulty: no challenge
- Pressure: none
- Desired aftertaste: relaxing and visually satisfying

## Main verbs

- observe
- rotate camera
- trigger fireworks
- adjust viewpoint

## Technical boundaries

- Target FPS: 60
- Max active particles: 256
- Max trail length: 8
- Architecture: model/system/render separation
- Deterministic simulation: True
- Pyxel API boundary: app, loop, render, input, audio only

## Specific visual and spatial requirements

- Screen size: 256x144.
- Space: a cutout rectangular observation space with a transparent cuboid / box feel.
- Coordinates: use 3D `x`, `y`, and `z`; larger `y` means higher in the firework space.
- Trails: rockets always have trails; particles should use partial trails rather than every particle trailing.
- Preset direction: chrysanthemum, peony, ring, willow, spiral, and small-shell cluster styles.
- Depth readability: draw rear box edges, then particles, then front box edges.

## Future screen and scenery direction

- Preserve `256x144` as the classic baseline profile.
- Plan larger Pyxel internal profiles separately from display scaling; do not default to native phone-pixel resolution.
- Recommended future profile: `512x236` for an iPhone16-landscape-like balanced view.
- Optional larger profile: `852x393`.
- Box dimensions, camera focal length, camera distance, UI placement, and max particle count should become profile-dependent.
- Future scenery should be selectable static low-detail 3D line geometry inside the observation box.
- Scenery must project through the same camera pipeline as fireworks, not a 2D screen-space background.

See:

- `docs/architecture/SCREEN_PROFILES.md`
- `docs/architecture/SCENERY_OBJECTS.md`

## Current reference prototype

The standalone `main.py` may contain the current good-feeling firework box behavior.
Treat it as a protected reference prototype until a migration strategy is documented.
Do not overwrite, refactor, or migrate it during environment verification.

## Codex operation

- Patch size: small
- Allow refactor: only when task explicitly asks
- Allow dependency addition: no, unless approved
- Update docs: True
- Stop on product ambiguity: record assumption or ask user depending on risk
