# Decision Log

Use this for lightweight decisions that do not need a full ADR.

## Format

```md
## YYYY-MM-DD Decision title

Decision:
Reason:
Alternatives:
Impact:
```

## 2026-06-23 Protect standalone main.py as reference prototype

Decision:
Treat the standalone `main.py` as a protected reference prototype until its behavior is inspected and a migration strategy is documented.

Reason:
The current good-feeling firework box behavior may exist in `main.py`, while the long-term project structure lives under `src/pyxel_goal_game/`.

Alternatives:
Continue developing `main.py` as the main implementation, or immediately migrate it into the package structure.

Impact:
T0002 must not modify `main.py`. Before T0003 gameplay work, complete `T0002.5` to reconcile the standalone prototype with the package architecture.

## 2026-06-23 Use one-goal-at-a-time staged firework implementation

Decision:
Codex should execute only the next eligible incomplete task from `goals/task_queue.json`, complete validation and logs, then stop. Firework preset work is split into `T0003.0` through `T0003.8` instead of one broad T0003 task.

Reason:
Adding many firework types in one pass risks losing the current good-feeling prototype behavior, mixing environment issues with implementation issues, and making visual regressions hard to isolate.

Alternatives:
Implement several presets in one broad patch, or keep a single vague "implement first deterministic burst preset" task.

Impact:
Future sessions should use `docs/prompts/goal_driven_mode.md`. Presets must be added one at a time after T0002 and T0002.5 are complete.

## 2026-06-23 Treat T0004 as prototype viewpoint migration

Decision:
`T0004` should mean recreating the protected `main.py` viewpoint/camera behavior on the package side, not inventing a new camera feature.

Reason:
The current viewing feel is part of the good prototype behavior that may live in `main.py`. A generic camera task could drift away from that feel.

Alternatives:
Leave T0004 as a vague camera adjustment task, or implement new camera behavior before reconciling `main.py`.

Impact:
T0004 depends on T0002.5 migration notes and should preserve the 256x144 transparent box viewing feel.

## 2026-06-24 Link screen profiles with in-box scenery architecture

Decision:
Document screen profiles and future scenery architecture together before firework preset implementation.

Reason:
Larger landscape profiles change the observation box size, camera focal length, camera distance, UI placement, max particle count, scenery proportions, and render order. Future scenery must exist as static 3D line geometry inside the same observation box as fireworks, so it needs the same box-relative coordinate and projection assumptions.

Alternatives:
Treat screen size as an isolated constant change, or draw scenery as a 2D screen-space background behind the box.

Impact:
`T0002.7` records screen and scenery planning before `T0003.0`. Future work should add `T0002.8` for screen profile configuration and `T0006.*` for staged scenery data and rendering. Scenery must not bypass the `Camera3D` projection pipeline.

## 2026-06-24 Preserve main.py behavior through staged package migration

Decision:
Treat `main.py` as the protected reference for camera feel, box projection, kiku burst tuning, and partial trail behavior. Do not migrate it by direct copy or broad rewrite; migrate package-side behavior in small documented slices.

Reason:
The package implementation is currently a 2D template, while `main.py` contains the working 3D observation box prototype. Direct replacement would mix screen sizing, camera projection, box rendering, rocket physics, particle physics, trails, and UI, making regressions hard to review.

Alternatives:
Overwrite package gameplay from `main.py`, keep developing only `main.py`, or reimplement the package behavior from memory without preserving the exact prototype constants.

Impact:
Future work should use `docs/architecture/PROTOTYPE_RECONCILIATION.md` as the migration reference. The next recommended task remains `T0002.8` unless the roadmap is adjusted to insert a package-side Camera3D scaffold first.

## 2026-06-24 Add ScreenProfile scaffold with classic default

Decision:
Add `ScreenProfile` as package-side immutable configuration data and make `classic` the default profile for package settings.

Reason:
Screen size, observation box dimensions, camera focal length, camera distance, and max particle count must be managed together before larger-profile tuning. Keeping `classic` as the default preserves the protected baseline while allowing `iphone16_balanced` and `iphone16_large` to exist as data for future tasks.

Alternatives:
Keep hard-coded screen constants only, switch immediately to a larger profile, or delay profiles until after firework preset work.

Impact:
Future camera, box, particle budget, and UI work should read from `ScreenProfile` rather than adding new fixed constants. This task intentionally does not add scenery rendering, new firework presets, or `main.py` migration.

## 2026-06-24 Add Pyxel-independent Camera3D projection scaffold

Decision:
Add package-side `Camera3D`, `Vec3`, and `ProjectedPoint` as pure projection data and math in `src/pyxel_goal_game/camera3d.py`.

Reason:
All future box, firework, and scenery rendering must share the same y-up 3D projection pipeline. Keeping the scaffold Pyxel-independent makes it testable and prevents camera math from being coupled to drawing or input handling.

Alternatives:
Embed projection math directly in render modules, extend the existing 2D `Camera`, or wait until firework preset work to introduce projection.

Impact:
Future package-side box geometry, particle rendering, and scenery rendering should use this projection scaffold. This task does not bind keyboard input, migrate particles or rockets, add scenery, or change the default profile.

## 2026-06-24 Add Pyxel-independent WireBox geometry scaffold

Decision:
Add package-side `WireBox`, `Edge3D`, and `ProjectedEdge` as pure geometry/projection data in `src/pyxel_goal_game/wire_box.py`.

Reason:
The transparent observation cuboid is a core visual anchor. It should share `ScreenProfile` dimensions and `Camera3D` projection before firework or scenery rendering is migrated.

Alternatives:
Hard-code box vertices in a renderer, delay box geometry until visual rendering, or couple the box directly to Pyxel draw calls.

Impact:
Future render tasks can draw the box from projected edge data without duplicating geometry or projection math. This task does not add Pyxel drawing, firework presets, scenery rendering, rocket migration, or particle migration.

## 2026-06-24 Add Pyxel-independent firework preset scaffold

Decision:
Add package-side `FireworkKind`, `FireworkShape`, `TrailPreset`, `SecondaryPreset`, and `FireworkPreset` in `src/pyxel_goal_game/firework_presets.py` as pure data/config.

Reason:
Future firework types should be added one at a time from explicit preset data rather than ad hoc runtime branches. Keeping the scaffold Pyxel-independent makes conventions testable before generation, rendering, or preset cycling is connected.

Alternatives:
Extend the existing 2D template `model.firework.FireworkPreset`, implement Kiku generation immediately, or copy concepts directly from the external `Firework.py`.

Impact:
`T0003.1` can implement deterministic radial/Kiku generation against this scaffold. This task intentionally does not change runtime gameplay, add visible presets, migrate rockets/particles, or connect Pyxel rendering.

## 2026-06-24 Add deterministic Kiku burst generation as spawn specs

Decision:
Implement Kiku as `KIKU_PRESET` plus deterministic `ParticleSpawnSpec` generation in a Pyxel-independent `firework_bursts.py` module.

Reason:
The first firework behavior should be testable before it is connected to runtime particles or rendering. Generating immutable initial spawn specs preserves the protected y-up, negative-gravity, and partial-trail conventions while keeping runtime migration separate.

Alternatives:
Connect Kiku directly to the current runtime particle system, copy the standalone `main.py` implementation directly, or implement several preset shapes at once.

Impact:
`T0003.2` can add Ring generation using the same pure generation pattern. Runtime particle conversion and Pyxel rendering remain future work.

## 2026-06-24 Add deterministic Ring burst generation as spawn specs

Decision:
Implement Ring as `RING_PRESET` plus deterministic `ParticleSpawnSpec` generation in the existing Pyxel-independent `firework_bursts.py` module.

Reason:
Ring is the first planar structure that benefits strongly from the 3D observation box. Adding it as pure initial velocity specs keeps it testable while preserving the staged boundary before runtime rendering.

Alternatives:
Wait until rendering integration, implement a tilted or multi-ring variant immediately, or copy ring logic from the external reference file.

Impact:
`T0003.3` can add Spiral generation using the same generation pattern. Runtime particle conversion, Pyxel rendering, preset cycling, and scenery remain future work.

## 2026-06-24 Add manual Kiku/Ring Pyxel preview before Spiral

Decision:
Add `tools/preview_firework_box.py` as a manual development preview harness that uses package-side `ScreenProfile`, `Camera3D`, `WireBox`, `generate_kiku_burst`, and `generate_ring_burst`.

Reason:
Kiku and Ring should be visually inspected before adding Spiral so trail density, box readability, camera feel, and ring planarity can be evaluated with the current pure generation data. Keeping the preview in `tools/` avoids mixing temporary visual inspection code into production runtime.

Alternatives:
Connect Kiku/Ring directly to the main runtime, continue adding Spiral without visual inspection, or modify the protected standalone `main.py`.

Impact:
The preview is manual-only and opens Pyxel only when executed directly. It does not change runtime gameplay, `main.py`, default profile selection, firework preset generation, or scenery behavior. After visual inspection, `T0003.3` remains the next preset task.

## 2026-06-24 Tune iPhone profiles to portrait firework volume

Decision:
Make iPhone-style internal observation boxes tall portrait firework volumes. `classic` remains unchanged and remains the default.

Reason:
Firework composition depends on vertical launch space, altitude variation, gravity, and falling trails. The internal box should read as a vertical firework chamber rather than a wide slab.

Alternatives:
Keep iPhone boxes horizontally oriented or delay profile tuning until after Spiral.

Impact:
`iphone16_balanced` now uses `120x260x120` with camera distance `340.0`, and `iphone16_large` uses `200x440x200` with camera distance `560.0`.

## 2026-06-24 Tune iPhone profiles to portrait Pyxel viewport

Decision:
Change iPhone-style Pyxel screens from landscape to portrait while preserving the tall internal firework volume. `classic` remains unchanged and remains the default.

Reason:
The manual preview confirmed that making only the box vertical is insufficient when the Pyxel canvas remains wide. Firework viewing benefits from vertical screen space as well as vertical internal volume.

Alternatives:
Keep the wide canvas with a tall central box, add side UI first, or wait until Spiral before changing viewport dimensions.

Impact:
`iphone16_balanced` now uses screen `236x512` with box `120x260x120`; `iphone16_large` now uses screen `393x852` with box `200x440x200`. Future Spiral, Willow, and scenery tuning should assume portrait viewport / portrait firework volume for iPhone-style profiles.

## 2026-06-25 Add deterministic Ring orientation bank

Decision:
Add Pyxel-independent `RingOrientation`, `RingOrientationBank`, and `build_ring_orientation_bank()` to the pure burst generation module. The manual preview builds a 24-orientation bank from explicit seed `20260623` and passes it to Ring generation.

Reason:
Ring orientation should be reproducible and visually varied without relying on global random state. A stratified bank keeps near-vertical, oblique, and near-horizontal Ring planes available, which gives better controlled variation than fresh unconstrained random orientations.

Alternatives:
Keep all Rings in the original XY plane, generate a fresh fully random orientation for every Ring burst, or defer orientation variation until runtime integration.

Impact:
`generate_ring_burst()` accepts an optional `orientation_bank`. If provided, the Ring orientation is selected deterministically from the bank by burst seed. If omitted, a deterministic direct orientation is generated from the seed. Kiku generation, runtime gameplay, `main.py`, and production rendering remain unchanged.

## 2026-06-25 Add deterministic Spiral burst generation

Decision:
Add `SPIRAL_PRESET` and `generate_spiral_burst()` as Pyxel-independent preset data and burst generation. The manual preview now cycles Kiku, Ring, and Spiral.

Reason:
Spiral is the first preset focused on readable 3D twist rather than a spherical shell or oriented plane. Implementing it as deterministic `ParticleSpawnSpec` generation keeps it testable before runtime particle migration.

Alternatives:
Connect Spiral directly to production gameplay, derive it from the external 2D reference code, or delay Spiral until after Willow.

Impact:
`generate_burst()` now supports `FireworkShape.SPIRAL`. The generated velocities form a normalized 3D spiral direction so speed magnitudes remain within preset range. Kiku, Ring, RingOrientationBank, production runtime, `main.py`, and scenery remain unchanged.

## 2026-06-25 Add deterministic Willow burst generation

Decision:
Add `WILLOW_PRESET` and `generate_willow_burst()` as Pyxel-independent preset data and burst generation. The manual preview now cycles Kiku, Ring, Spiral, and Willow.

Reason:
Willow is the first preset focused on long afterglow, stronger downward gravity, and selected longer trails. It should be represented as deterministic spawn specs before runtime migration so falling-tail behavior can be tuned from data.

Alternatives:
Tune Willow directly in the preview runtime, implement Peony first, or defer falling-tail behavior until rocket/particle migration.

Impact:
`generate_burst()` now supports `FireworkShape.WILLOW`. Willow uses loose radial horizontal velocity, varied initial vertical velocity, stronger negative gravity, and longer partial trail settings. Kiku, Ring, Spiral, production runtime, `main.py`, profiles, and scenery remain unchanged.

## 2026-06-25 Add deterministic Peony burst generation

Decision:
Add `PEONY_PRESET` and `generate_peony_burst()` as Pyxel-independent preset data and burst generation. The manual preview now cycles Kiku, Ring, Spiral, Willow, and Peony.

Reason:
Peony should contrast with Willow by being a short-lived, bright, round bloom with restrained trails. Keeping it as deterministic spawn specs preserves testability and avoids mixing visual tuning with production runtime migration.

Alternatives:
Tune Kiku to double as Peony, connect Peony directly to production gameplay, or delay short bright blooms until after Multi-ring/Halo.

Impact:
`generate_burst()` already supports Peony through `FireworkShape.SPHERE`. Peony reuses the sphere generator with lower particle count, shorter life, brighter palette, and lower trail rate. Kiku, Ring, Spiral, Willow, production runtime, `main.py`, profiles, and scenery remain unchanged.

## 2026-06-25 Add random burst selection mode to preview

Decision:
Add preview-only random burst selection mode to `tools/preview_firework_box.py`. Pressing `R` enters random mode, `Z` and auto-launch choose a deterministic random implemented burst type, and `SPACE` exits random mode back to sequential cycling.

Reason:
Kiku, Ring, Spiral, Willow, and Peony now exist in the manual preview. Random selection makes comparative visual inspection faster without changing production runtime behavior or pure generation modules.

Alternatives:
Wait for production preset cycling, add random selection to runtime, or keep only manual sequential cycling.

Impact:
The preview owns a local seeded RNG and avoids global random state. `main.py`, production gameplay, firework generation outputs, profiles, and scenery remain unchanged. The next implementation task remains `T0003.6`.

## 2026-06-25 Add fixed-position salvo launch plans to preview

Decision:
Add Pyxel-independent fixed-position salvo plan data and connect number keys `1` through `5` in the manual preview to schedule consecutive profile-scaled burst launches.

Reason:
The preview can now inspect individual and random burst types. Before adding Multi-ring or Halo, fixed multi-shot salvos make it possible to inspect density, height variation, and composition inside the portrait observation box.

Alternatives:
Implement salvo behavior directly in production runtime, keep only manual single-shot launch, or wait until after Multi-ring/Halo to assess multi-burst density.

Impact:
`src/pyxel_goal_game/salvo_patterns.py` provides pure `SalvoPlan` data based on `ScreenProfile` box dimensions. The preview schedules bursts at fixed box-relative positions with 12-frame spacing. `main.py`, production gameplay, pure firework generation outputs, profiles, and scenery remain unchanged.

## 2026-06-25 Add deterministic Multi-ring burst generation

Decision:
Add `MULTI_RING_PRESET` and `generate_multi_ring_burst()` as Pyxel-independent preset data and burst generation. The manual preview now includes Multi-ring in sequential cycling, random mode, and fixed-position salvos.

Reason:
Multi-ring should provide a layered ring structure without immediately moving into Halo or Senrin complexity. Implementing it as deterministic spawn specs keeps it testable and makes preview density checks possible before production runtime migration.

Alternatives:
Implement Halo first, make Multi-ring a production-only runtime effect, or increase the existing Ring particle count instead of adding layered behavior.

Impact:
`generate_burst()` now supports `FireworkShape.MULTI_RING`. Multi-ring uses three deterministic ring layers sharing a coherent orientation with clamped speed bands and restrained partial trails. Kiku, Ring, Spiral, Willow, Peony, production runtime, `main.py`, profiles, and scenery remain unchanged.

## 2026-06-25 Add deterministic Senrin secondary burst specs

Decision:
Add `SENRIN_PRESET`, `SENRIN_SECONDARY_PRESET`, optional `ParticleSpawnSpec.secondary_burst`, and deterministic secondary burst generation. The manual preview executes secondary bursts locally for Senrin inspection.

Reason:
Senrin needs delayed small secondary bursts, but production runtime migration is still out of scope. Representing secondary behavior as deterministic data keeps the pure generation model testable and lets the preview show the visual idea without changing gameplay runtime.

Alternatives:
Implement runtime secondary particles immediately, fake Senrin as a dense single-stage sphere, or defer Senrin until after production particle migration.

Impact:
`generate_burst()` now supports `FireworkShape.SENRIN_SEED`. Non-secondary presets keep `secondary_burst=None`. Preview sequential, random, and salvo modes include Senrin and execute secondary bursts locally. `main.py`, production gameplay, profiles, scenery, and existing preset outputs remain unchanged.

## 2026-06-25 Add persistent preview salvo controls

Decision:
Change preview number keys `1` through `5` from one-off salvo scheduling to persistent fixed-count salvo loops, assign `0` to persistent random-count salvo mode, add `H` height variation, and draw preview-only launch-to-burst rocket trajectories.

Reason:
The preview now needs to inspect repeated show-like compositions, not only individual salvos. `0` is more useful as a random-count control than as stop, while `1` provides the default one-shot loop. Keeping this preview-only avoids changing production runtime behavior.

Alternatives:
Keep one-off number-key salvos, use `0` as a stop command, or move repeated salvo behavior into production runtime.

Impact:
`R` randomizes burst type independently from `0` randomizing salvo count. `V` auto-launch and persistent salvo mode are mutually exclusive. `Z` remains a single immediate launch. `main.py`, production gameplay, pure firework generation outputs, profiles, and scenery remain unchanged.

## 2026-06-25 Add visual tuning checklist

Decision:
Add `docs/research/visual_tuning_checklist.md` before further preset expansion or runtime integration.

Reason:
The preview now supports seven deterministic firework types plus random type, random count, height variation, persistent salvos, auto launch, and auto rotate. Parameter tuning should be judged against a documented checklist instead of ad hoc visual impressions.

Alternatives:
Proceed directly to Halo, tune Senrin or Multi-ring immediately, or begin runtime integration before locking evaluation criteria.

Impact:
The checklist records profile policy, commands, controls, per-preset visual criteria, stress sequences, density-risk thresholds, and follow-up tuning candidates. No preset parameters, pure generation behavior, production runtime behavior, scenery, or `main.py` were changed.

## 2026-06-25 Fix preview rocket tail and pacing

Decision:
Change manual preview rockets from full launch-to-burst path lines to short recent-motion tails, make rockets fly for a longer distance-aware duration before exploding, and vary each rocket's speed deterministically.

Reason:
The previous preview made rockets look like a growing straight line from launch to burst, and explosions happened too quickly and too uniformly. The preview should show a readable launch phase without pretending to be the production runtime particle system.

Alternatives:
Keep full trajectory lines, only lengthen the previous trajectory animation, or implement a full runtime rocket physics model.

Impact:
The preview now schedules rockets that launch, move, keep a short 3D history tail, and then spawn the selected burst at arrival. `Z`, auto-launch, persistent fixed-count salvos, random-count salvos, random type mode, and height variation all use this preview rocket path. `main.py`, production gameplay, pure burst generation outputs, preset parameters, profiles, and scenery remain unchanged.

## 2026-06-25 Review external Firework.py candidate presets

Decision:
Add `docs/research/external_firework_candidates_20260625.md` to record future preset candidates from the external `Firework.py` file without copying or integrating its code.

Reason:
The external file contains useful visual and mathematical ideas such as Halo, Elliptical, Fibonacci, Counter Ring, Star, Heart, Sierpinski, and Magic Square bursts. These should be translated into Firework Observer's deterministic 3D `Vec3` / `ParticleSpawnSpec` model rather than imported as 2D complex-plane functions.

Alternatives:
Implement Halo immediately, ignore the external file, or expand the existing older reference notes only.

Impact:
The new research document recommends Halo as the next safest preset if density is stable, followed by Orbit/Elliptical, Golden Bloom/Fibonacci, Counter Ring, and later shape-plane presets. `main.py`, production gameplay, preset parameters, pure generation behavior, preview behavior, and scenery remain unchanged.

## 2026-06-25 Add preview VFX accents

Decision:
Add preview-only burst-type rocket tail colors and short-lived center-outward burst accent rays.

Reason:
The preview already supports rocket launches and seven burst types. Coloring rocket tails by scheduled burst type improves launch readability, and a few early accent rays make explosion starts clearer without changing deterministic pure burst generation.

Alternatives:
Change `ParticleSpawnSpec`, add accent rays to all particles, add production runtime VFX immediately, or wait until Halo.

Impact:
Rocket styles are frozen when rockets are scheduled, so random mode and salvos show the color of the actual selected type. Accent rays are assigned to a deterministic limited subset of preview particles at burst spawn time. Senrin secondary bursts keep no added accent rays. `main.py`, production gameplay, pure generation outputs, preset parameters, Halo, and scenery remain unchanged.

## 2026-06-25 Restore preview rocket fireball shape

Decision:
Keep the new type-colored rocket palette, but restore the rocket head from a single point to a small clustered fireball shape.

Reason:
The type-colored rocket tails are useful, but the launch fireball shape became visually too cheap as a single pixel. A compact pixel cluster keeps the improved color identity while making the launch head read as a fireball again.

Alternatives:
Revert all rocket VFX color work, enlarge the entire rocket tail, or add a heavier animated sprite.

Impact:
Only `tools/preview_firework_box.py` rocket head drawing changed. `main.py`, production gameplay, preset parameters, pure generation behavior, Halo, and scenery remain unchanged.

## 2026-06-25 Replace fireball stick tail with ember trail

Decision:
Draw the launch fireball's trailing effect as separated ember pixels instead of connected line segments.

Reason:
Connected line segments made the launch fireball look like it had a rigid booster or stick attached. The object is a launched firework shell, so its trail should read as residual sparks behind the fireball, not attached propulsion hardware.

Alternatives:
Remove the trail entirely, shorten the connected line further, or keep the line and only change colors.

Impact:
The preview keeps the current type-colored palette and compact fireball head, but the trail is now disconnected recent ember points with a small gap behind the head. `main.py`, production gameplay, preset parameters, pure generation behavior, Halo, and scenery remain unchanged.

## 2026-06-25 Restore pre-color-change launch shape

Decision:
Restore the manual preview launch shape to the version used before burst-type rocket colors were added, while keeping the burst-type color palette.

Reason:
The type-specific colors are useful, but the later compact fireball and ember-trail shapes did not match the preferred launch appearance. The requested target is the earlier launch silhouette, not a full rollback of color styling.

Alternatives:
Revert all preview VFX color work, keep the ember trail, or make another new launch sprite.

Impact:
The preview launch now uses the earlier connected recent-history trail and single head point, mapped through each burst type's palette. `main.py`, production gameplay, preset parameters, pure generation behavior, Halo, and scenery remain unchanged.

## 2026-06-25 Draw launch fireball as filled teardrop

Decision:
Render the preview launch object as a filled, direction-aware teardrop fireball instead of a line, ember trail, or booster-like attachment.

Reason:
The launched object should read as a firework shell/fireball, not a rocket with a physical booster or stick attached. The requested shape is a narrow filled loop/teardrop silhouette, with burst-type colors applied to the filled form.

Alternatives:
Use the earlier connected history line, keep detached ember pixels, draw a compact round cluster, or add a sprite asset.

Impact:
Only manual preview launch drawing changed. Type-specific colors remain. The fireball shape is generated from current projected motion direction and filled with Pyxel triangles plus a bright nose. `main.py`, production gameplay, preset parameters, pure generation behavior, Halo, and scenery remain unchanged.

## 2026-06-25 Restore simple firework shell gradient tail

Decision:
Use one shared preview-only rising firework shell tail for all burst types: a short recent-motion gradient of white, white, white, yellow, yellow, brown, brown.

Reason:
The rising object is a firework shell, not a rocket. Type-colored launch geometry and filled teardrop shapes were overcomplicating the visual and making the object read incorrectly. The stable base expression should be a small shell/fireball with a short gradient tail.

Alternatives:
Keep type-colored shell tails, keep the filled teardrop shape, draw a full trajectory guide, or remove the shell tail entirely.

Impact:
The preview no longer varies rising shell tail shape or color by burst type. It draws only recent history samples with the fixed white/yellow/brown gradient and keeps burst accent rays separate. `main.py`, production gameplay, preset parameters, pure generation behavior, Halo, and scenery remain unchanged.

## 2026-06-25 Add preview in-box scenery scaffold

Decision:
Add preview-selectable scenery as static, low-detail 3D line geometry inside the observation box, starting with `EMPTY`, `MOUNTAINS`, `CITY`, and `RIVERBANK`.

Reason:
Scenery should establish a place under the fireworks without becoming a 2D screen-space background. Keeping it as `Vec3` line/polyline data lets it rotate and project through the same `Camera3D` pipeline as the box and fireworks.

Alternatives:
Draw a flat background, wait for production runtime integration, or implement all future scenery kinds at once.

Impact:
`src/pyxel_goal_game/scenery_presets.py` now provides Pyxel-independent scenery data. The manual preview can cycle scenery with `G` and toggle it with `B`. `main.py`, production gameplay, firework preset parameters, pure firework generation behavior, Halo, and external Firework.py integration remain unchanged.

## 2026-06-25 Refocus scenery to city-only urban kit

Decision:
Refocus active preview scenery on `EMPTY` and `CITY`, and rebuild `CITY` as a low-detail 3D urban kit made from cuboid building blocks and sparse lit windows.

Reason:
City scenery has the clearest relationship to fireworks and the strongest sense of human presence. Mountains and riverbank are useful reference ideas, but growing them in parallel would dilute the next visual direction. The city should read as small 3D geometry on the box floor, not as a flat side-wall skyline.

Alternatives:
Continue cycling all scenery presets, add forest/coast/dike next, or keep the previous flat skyline style.

Impact:
`SCENERY_PRESET_NAMES` now exposes only `empty` and `city` to the preview cycle. The city data remains Pyxel-independent and uses profile-scaled `Vec3` line geometry. `main.py`, production gameplay, firework preset parameters, pure firework generation behavior, Halo, and external Firework.py integration remain unchanged.

## 2026-06-26 Ground city building wireframes

Decision:
Omit the four bottom-face perimeter edges from CITY building cuboids, while preserving vertical edges, top edges, and sparse windows. Also slightly reduced the current city block scale and height.

Reason:
Full bottom cuboid edges made the city read like loose miniature boxes placed on the floor. Omitting only the bottom perimeter makes buildings feel grounded into the cut floor plane, which better matches the observation-box direction.

Alternatives:
Keep full 12-edge cuboids, remove more building structure, or delay city readability tuning until landmarks are added.

Impact:
Only Pyxel-independent scenery data changed. `main.py`, production gameplay, firework preset parameters, pure firework generation behavior, preview controls, Halo, and external Firework.py integration remain unchanged.

## 2026-06-26 Add subtle burst radius variation

Decision:
Add small deterministic per-particle burst radius variation as bounded velocity magnitude wobble in pure burst generation.

Reason:
Perfectly uniform burst radii make explosions feel too mechanically even. A small bounded wobble adds naturalness while preserving each preset's identity and existing y-up physics.

Alternatives:
Change particle positions, add preview-only visual noise, tune preset speed ranges directly, or defer until after Halo.

Impact:
Pure burst generation now varies effective velocity magnitudes slightly within each preset's existing speed range. Shell tail rendering, CITY scenery, preview controls, `main.py`, production runtime, preset parameter constants, Halo, and external Firework.py integration remain unchanged.

## 2026-06-26 Add CITY landmark and utility lines

Decision:
Extend the CITY scenery with one low-detail 3D landmark tower, a few utility poles, and slightly sagging overhead wire polylines.

Reason:
The city should feel like a lived-in urban stage beneath the fireworks, not only a set of anonymous building blocks. A small tower and utility lines add scale and human presence with limited line cost.

Alternatives:
Add Halo first, add more building blocks, reintroduce natural scenery presets, or defer city details until production runtime integration.

Impact:
Only Pyxel-independent CITY scenery data changed. `main.py`, production runtime, firework presets, pure firework generation, shell tail behavior, preview controls, Halo, and external Firework.py integration remain unchanged.

## 2026-06-26 Implement Halo as a light wobbling ring

Decision:
Add `HALO_PRESET` as a deterministic, Pyxel-independent, single-plane wobbling light-ring burst and include it in preview sequential, random, and salvo selection.

Reason:
The current city stage is acceptable, and Halo is the next lowest-risk external-reference-inspired preset. It extends the Ring/Multi-ring family while staying lighter, softer, and less dense than Multi-ring.

Alternatives:
Tune density before adding another preset, implement Orbit/Elliptical first, or add Halo as preview-only VFX instead of pure burst generation.

Impact:
Pure firework generation now supports `FireworkShape.HALO`. Preview can launch Halo through `SPACE`, `R`, `1`-`5`, and `0` random-count salvos. CITY scenery, shell tail behavior, existing preset constants, `main.py`, and production runtime remain unchanged.

## 2026-06-26 Densify CITY and replace utility lines with signage

Decision:
Refine active CITY into a denser cutaway urban mass, remove utility poles and overhead wires, enlarge and ground the landmark tower, and add low-detail building-attached signage.

Reason:
The pole/wire layer added human detail, but it pulled the scene toward separate street objects rather than a cutaway urban rooftop mass. Dense buildings and signs better support the city-as-stage direction while keeping fireworks dominant.

Alternatives:
Keep utility poles and wires, add more natural scenery, add UFO ambient behavior first, or leave CITY sparse until runtime integration.

Impact:
Only Pyxel-independent CITY scenery data changed. `main.py`, production runtime, firework generation, firework presets, shell tail behavior, preview controls, Halo, and active scenery selection remain unchanged.

## 2026-06-26 Add ferris wheel and fuller CITY footprint

Decision:
Spread active CITY buildings across more of the lower observation-box footprint and add one low-detail ferris wheel as a quiet urban/leisure landmark.

Reason:
The city should feel like a dense cutaway urban stage across the bottom of the cuboid, not a cluster of buildings near the center. A small off-center ferris wheel adds recognizable place character while keeping fireworks dominant.

Alternatives:
Add UFO ambient behavior, add interior stars, tune firework presets, or broaden scenery back to mountains/riverbank/forest/coast.

Impact:
Only Pyxel-independent CITY scenery data changed. `main.py`, production runtime, firework generation, firework presets, shell tail behavior, preview controls, auto-rotate speed control, and active `EMPTY`/`CITY` scenery selection remain unchanged.

## 2026-06-26 Add interior box stars

Decision:
Add subtle twinkling stars as a preview-only ambience layer attached to the observation box's interior top face and upper side faces, with a `T` toggle.

Reason:
The next ambient layer should reinforce the feeling of looking into a cutout box without becoming a 2D background or free-floating particle effect. Stars must render only when their interior face is visible, so they do not look painted on exterior box walls.

Alternatives:
Add UFO ambient behavior first, add screen-space stars, place stars freely in 3D space, or postpone ambient layers until runtime integration.

Impact:
Added Pyxel-independent star field and visibility helpers plus preview rendering/toggle support. `main.py`, production runtime, firework generation, burst radius variation, firework presets, shell tail behavior, CITY geometry, UFO, and existing preview controls remain unchanged.

## 2026-06-26 Tune burst compactness and CITY layout

Decision:
Tighten deterministic burst radius wobble, enlarge the CITY ferris wheel, and move CITY building blocks away from the center to preserve a boulevard-like open corridor.

Reason:
The existing burst wobble added useful naturalness but could feel slightly too wide at the upper radius. The ferris wheel needed to read more clearly as a circular landmark, and the dense CITY mass needed a central avenue to improve launch readability and city staging.

Alternatives:
Leave the existing wobble unchanged, add more city detail, implement UFO ambient behavior, or change preview controls.

Impact:
Pure burst generation keeps deterministic radius variation but with smaller factors. CITY remains Pyxel-independent line geometry, with utility poles/wires still absent. `main.py`, production runtime, preview controls, shell tail, interior stars, UFO, and firework preset constants remain unchanged.

## 2026-06-26 Tune preview auto-rotate comfort

Decision:
Reduce preview auto-rotate normal and fast speeds, and scale pitch sway by the selected speed mode.

Reason:
Long visual review needs a comfortable auto-rotate mode. The previous pitch sway used the same amplitude for all speed modes and could feel nauseating, especially when the viewer wanted slow observation.

Alternatives:
Remove pitch sway entirely, change key bindings, or leave auto-rotate speed-only.

Impact:
Preview `X` and `Q` controls are preserved. `slow`, `normal`, and `fast` remain ordered, with `normal` and `fast` calmer than before and slower modes using less vertical sway. `main.py`, production runtime, firework generation, burst radius variation, shell tail, CITY, ferris wheel, boulevard, interior stars, UFO, and firework preset constants remain unchanged.

## 2026-06-26 Tune stars, glitter residue, and CITY edges

Decision:
Relax only the top-face interior star visibility threshold, add sparse preview-only burst glitter residue, make the CITY ferris wheel read more circular, and add peripheral CITY buildings near side floor regions.

Reason:
User review found that ceiling stars disappeared too early while side-wall star visibility was already acceptable. Firework bursts needed a small residual sparkle without becoming denser core bursts. CITY needed stronger side coverage and a more circular ferris wheel while preserving the central boulevard and launch readability.

Alternatives:
Broaden all star face thresholds, add glitter to pure burst generation, add more central buildings, or postpone CITY tuning until a later pass.

Impact:
Top-face stars are more permissive while side-face thresholds remain unchanged. Glitter residue is preview-only and short-lived. CITY stays Pyxel-independent, with utility poles and overhead wires still absent. `main.py`, production runtime, preview controls, shell tail behavior, burst compactness, auto-rotate comfort, UFO, and firework preset constants remain unchanged.
