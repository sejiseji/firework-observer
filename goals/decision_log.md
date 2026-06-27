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

## 2026-06-26 Relax ceiling star shallow-angle visibility

Decision:
Relax the top-face interior star visibility threshold further so ceiling stars remain visible when the eye line is closer to parallel with the ceiling plane.

Reason:
User review found that ceiling stars still disappeared too early at shallow viewing angles. The side-wall visibility behavior was not part of this issue and should stay unchanged.

Alternatives:
Increase star count, broaden all face thresholds, or draw top stars unconditionally.

Impact:
Only the top-face threshold changed. Side-wall thresholds, star placement, preview controls, CITY, firework generation, shell tail behavior, and production runtime remain unchanged.

## 2026-06-26 Balance CITY building outline brightness

Decision:
Change CITY building cuboid outline colors from height-based coloring to a deterministic bright-blue/dark-blue pattern with an even split and scattered distribution.

Reason:
The previous height-based coloring could create visible clusters of similar brightness. The user wanted the city to read as mixed bright and dark building groups, with overall brightness reduced and no large bright/dark blocks.

Alternatives:
Darken all buildings, randomize colors with a seed, or tune tower/sign/window colors at the same time.

Impact:
Only building cuboid outline color selection changed. The landmark tower, ferris wheel, signage, windows, preview controls, firework generation, shell tail behavior, CITY geometry placement, and production runtime remain unchanged.

## 2026-06-26 Increase CITY building count to 48

Decision:
Increase the active CITY building cuboid count to 48 while preserving the even bright-blue/dark-blue outline split and interleaved brightness distribution.

Reason:
The user wanted the same building color conditions but with a denser city mass. Increasing the building count strengthens the cutaway urban footprint while keeping the darker overall read from the balanced color pattern.

Alternatives:
Increase only window/sign density, add new landmarks, or broaden city coverage without changing the building count target.

Impact:
Only CITY building cuboid data changed. The landmark tower, ferris wheel, signage, windows, central boulevard, preview controls, firework generation, shell tail behavior, and production runtime remain unchanged.

## 2026-06-26 Reduce burst radius maximum width

Decision:
Apply an 80% radius speed scale to primary firework burst velocities while preserving the existing deterministic per-kind radius wobble.

Reason:
User review found the maximum explosion radius too wide. Scaling the effective burst velocity directly reduces the visual radius without changing preset constants, particle counts, or firework identities.

Alternatives:
Lower each preset `speed_range`, reduce only the wobble upper bound, or add preview-only camera scaling.

Impact:
Primary burst velocity magnitudes are reduced to 80% of their bounded generated speed. Trail decisions continue to use the pre-radius-scale speed so existing trail tendencies remain stable. Senrin secondary, preset constants, shell tail, CITY, preview controls, and production runtime remain unchanged.

## 2026-06-26 Keep ceiling stars at near-parallel angles

Decision:
Widen only the top-face interior star visibility threshold so ceiling stars remain visible even when the eye line is near parallel with the ceiling plane.

Reason:
User review found that ceiling stars should not disappear at the practical shallow-angle limit. Side-wall star visibility was not part of the issue.

Alternatives:
Draw top stars unconditionally, broaden all face thresholds, or increase star density.

Impact:
Only the top-face visibility threshold changed. Side-wall thresholds, star placement, CITY, fireworks, shell tail, preview controls, and production runtime remain unchanged.

## 2026-06-26 Document preview-to-runtime integration contract

Decision:
Freeze the current first-generation preview as the package runtime promotion target and document the extraction contract in `docs/architecture/PREVIEW_TO_RUNTIME_INTEGRATION.md`.

Reason:
The preview has stabilized enough to serve as the visual reference for runtime promotion. Continuing to grow stable behavior inside `tools/preview_firework_box.py` would make production migration harder, but directly rewriting `main.py` or importing the preview tool would create avoidable architecture risk.

Alternatives:
Keep all behavior in the preview, rewrite `main.py` immediately, or start runtime extraction without a contract.

Impact:
This is documentation-only. `main.py`, source behavior, preview behavior, tests, and runtime gameplay remain unchanged. Future T0005.x tasks should extract package-side runtime state, camera motion, show scheduling, rendering, entrypoint, and final `main.py` handoff in small steps.

## 2026-06-26 Add package-side runtime state/controller scaffold

Decision:
Create `src/pyxel_goal_game/runtime/` with Pyxel-independent state and show-controller scaffolding before migrating renderer or preview behavior.

Reason:
The first migration step needs a stable package-side place to represent selected profile, firework kind, toggles, salvo modes, auto-rotate speed mode, frame count, and seed base. Adding the scaffold first avoids importing `tools/preview_firework_box.py` from runtime and keeps later extraction tasks small.

Alternatives:
Move preview code directly, start with a renderer, or change `main.py` first.

Impact:
Runtime scaffold modules and tests were added. The scaffold does not open Pyxel, does not render, does not schedule real particles, and does not change preview behavior. `main.py`, production runtime gameplay, firework generation, CITY, shell tail, stars, and preview controls remain unchanged.

## 2026-06-26 Extract runtime camera motion settings

Decision:
Move settled auto-rotate speed and pitch sway comfort settings into Pyxel-independent `src/pyxel_goal_game/runtime/camera_motion.py`, and make the manual preview consume those package-side settings.

Reason:
Camera comfort is now stable enough to be part of the first-generation runtime contract. Keeping these values in the preview would duplicate or hide the official runtime target.

Alternatives:
Leave the values in `tools/preview_firework_box.py`, extract them later with renderer migration, or retune camera motion during extraction.

Impact:
Auto-rotate settings are now reusable package-side constants/helpers. Preview behavior, key bindings, HUD mode display, firework generation, shell tail, glitter, CITY, stars, and production runtime behavior remain unchanged.

## 2026-06-26 Extract runtime show scheduling

Decision:
Move single launch, fixed-count salvo, random-count salvo, random firework kind selection, and height variation schedule construction into Pyxel-independent `src/pyxel_goal_game/runtime/show_schedule.py`.

Reason:
Show scheduling is stable enough to promote from preview into package runtime, but shell simulation, particle spawning, and rendering should remain separate migration steps. This keeps the extraction focused on deciding when, where, which kind, and which seed to launch.

Alternatives:
Keep scheduling inside `tools/preview_firework_box.py`, move shell simulation at the same time, or wait until renderer migration.

Impact:
Preview now consumes package-side immutable launch schedules and converts them into existing preview shell objects. `main.py`, firework generation, shell tail, glitter residue, CITY, stars, camera motion, key bindings, and production runtime behavior remain unchanged.

## 2026-06-26 Add first official runtime app beside preview

Decision:
Add a package-side official runtime app and launcher without modifying protected `main.py` or importing from `tools/preview_firework_box.py`.

Reason:
State, camera motion, and show scheduling have already been promoted package-side. The next integration step needs a runnable official runtime path while preserving the manual preview as a regression viewer.

Alternatives:
Modify `main.py` immediately, keep the project runnable only through the preview tool, or import the preview tool from runtime.

Impact:
The official runtime now has package-side Pyxel app/input/render/effects boundaries and can be launched with `scripts/run_runtime_app.py`. The preview remains available, and `main.py` remains unchanged. Remaining work should review visual/runtime parity before any `main.py` handoff decision.

## 2026-06-26 Mark official runtime ready for main.py handoff

Decision:
Record official runtime parity as OK and mark `main.py` handoff readiness as `READY`.

Reason:
Manual review compared the preview and official runtime with `iphone16_balanced`. Startup, controls, CITY, interior stars, first-generation fireworks, shell tail, glitter residue, salvos, height variation, auto-rotate comfort, and `R + H + 0` stress mode showed no visual, control, or stability problems.

Alternatives:
Keep `main.py` protected indefinitely, or convert it before recording parity results.

Impact:
This is documentation-only. `main.py` remains unchanged in T0005.5. A separate explicit task, `T0005.6`, is now ready to convert `main.py` to a thin launcher for the official runtime.

## 2026-06-27 Convert main.py to official runtime launcher

Decision:
Convert `main.py` into a thin launcher that delegates to `pyxel_goal_game.runtime.app.main`.

Reason:
Runtime parity was recorded as OK and handoff readiness was marked READY in T0005.5. The official package runtime should now be the default project entry path, while runtime logic remains package-side.

Alternatives:
Keep `main.py` as the old standalone prototype, duplicate runtime logic into `main.py`, or remove `main.py`.

Impact:
`main.py` no longer contains the old single-file prototype implementation. It imports the official runtime app entrypoint and calls it. Runtime behavior remains owned by `src/pyxel_goal_game/runtime/`; the preview remains available as a development harness.

## 2026-06-27 Make main launcher robust for simple startup

Decision:
Treat `python main.py`, `python3 main.py`, and `pyxel run main.py` as first-class public launch paths. Keep `main.py` thin with only `src/` bootstrap and runtime delegation, and normalize Pyxel wrapper arguments in the runtime CLI layer.

Reason:
The default entrypoint should work from a source checkout or Pyxel's official runner without requiring users to know the internal runtime script or pass a profile argument. `pyxel run main.py` can pass `run main.py` through to the script, so the runtime parser must strip that wrapper prefix while still rejecting real invalid arguments.

Alternatives:
Keep `.venv/bin/python main.py --profile iphone16_balanced` as the only supported path, duplicate CLI parsing in `main.py`, or silently ignore arbitrary unknown arguments.

Impact:
`main.py` remains a thin launcher and does not import from `tools/`. The runtime CLI now defaults to `iphone16_balanced` and normalizes `run <entry>.py` prefixes. Runtime visuals, firework generation, CITY, stars, shell tail, glitter, controls, and preview behavior remain unchanged.

## 2026-06-27 Add runtime audio scaffold

Decision:
Add official runtime audio with quiet high-register music-box BGM, low restrained explosion SFX, channel separation, burst SFX cooldown, and `M` audio toggle.

Reason:
The first-generation visual runtime is stable, but the experience lacks audio presence. A simple runtime audio layer can add atmosphere without changing visual systems or preview behavior.

Alternatives:
Delay audio until after UFO work, add only explosion SFX, or implement audio inside `main.py` or the preview harness.

Impact:
Runtime audio is isolated in `src/pyxel_goal_game/runtime/audio.py`. BGM starts during runtime initialization, burst SFX triggers on actual burst events, and `M` toggles audio. Visual behavior, firework generation, CITY, stars, shell tail, glitter visuals, camera motion, preview harness, and UFO exclusion remain unchanged.

## 2026-06-27 Extend BGM with harmony

Decision:
Extend runtime BGM into a longer three-channel music-box arrangement: channel 0 melody, channel 1 high-register arpeggio accompaniment, channel 2 sparse shimmer accents, with channel 3 still reserved for explosion SFX.

Reason:
The initial BGM could read as a short single-note loop. Adding subtle accompaniment and a longer phrase improves atmosphere without changing visuals or crowding the low explosion sound.

Alternatives:
Use block chords, add low bass notes, consume channel 3 for BGM, or postpone audio tuning until after UFO work.

Impact:
Only runtime audio definitions and audio tests changed. The `M` toggle, explosion cooldown, SFX channel, runtime visuals, firework generation, CITY, stars, shell tail, glitter visuals, and main launcher remain unchanged.

## 2026-06-27 Rebuild BGM as simple chord harmony

Decision:
Replace the arpeggio/shimmer BGM arrangement with simple aligned chord harmony: channel 0 melody, channel 1 harmony, channel 2 soft support, and channel 3 reserved for explosion SFX.

Reason:
The previous secondary lines could read as independent melodies rather than harmony. Aligning the BGM channels rhythmically and using a clear large/medium/small volume hierarchy supports the melody without creating conflicting counter-lines.

Alternatives:
Keep tuning the arpeggio/shimmer arrangement, return to single-line BGM, use low bass support, or consume channel 3 for richer harmony.

Impact:
Only runtime audio definitions, audio tests, and project records changed. Visual behavior, firework generation, CITY, stars, shell tail, glitter visuals, key bindings, `M` toggle semantics, explosion SFX channel, and main launcher remain unchanged.

## 2026-06-27 Tune BGM support rhythm and volume

Decision:
Lower overall runtime BGM volume and change channel 2 from high soft support into a sparse mid-register rhythmic support pulse. Keep channel 3 reserved for explosion SFX.

Reason:
Even low-volume high notes can feel sharp or noisy. Moving support into a slower mid-register `tan` / `ta-tan` role and lowering melody/harmony volume makes the BGM sit behind the fireworks while preserving the music-box character.

Alternatives:
Raise explosion SFX, remove support entirely, keep high support notes, or delay audio tuning until after UFO work.

Impact:
Only runtime audio definitions, audio tests, and project records changed. Visual behavior, firework generation, CITY, stars, shell tail, glitter visuals, key bindings, `M` toggle semantics, explosion SFX channel, and main launcher remain unchanged.

## 2026-06-27 Add rare UFO ambient flyby

Decision:
Add a rare, silent UFO flyby as an official-runtime ambient layer, with deterministic package-side scheduling/path helpers and Pyxel-bound line/pixel rendering. Add `U` as a review toggle.

Reason:
The first-generation runtime has stable visuals and audio. A rare non-interactive upper-space flyby adds a small surprise without changing firework behavior, CITY, stars, audio, or gameplay rules.

Alternatives:
Postpone UFO until after new firework presets, make UFO preview-only, add UFO sound/beam/interactions immediately, or make UFO frequent for visibility.

Impact:
Runtime now has `runtime/ufo.py` pure helpers and app/render/input integration. UFOs are rare, silent, non-interactive, and visually secondary. Firework generation, CITY, stars, shell tail, glitter, camera motion, audio, main launcher, and tools preview imports remain unchanged.

## 2026-06-27 Add sphere bloom and long willow fireworks

Decision:
Add `Sphere Bloom` and `Long Willow` as first-class firework variants. Keep existing Kiku, Peony, and Willow behavior available.

Reason:
The project already had sphere-like Kiku/Peony and a baseline Willow, but the required sphere and willow categories needed clearer explicit variants. `Sphere Bloom` provides a clean canonical sphere. `Long Willow` provides a stronger, longer falling willow / 枝垂れ behavior.

Alternatives:
Retune Kiku, Peony, or Willow in place; add only one variant; or delay new firework variants until after more UFO tuning.

Impact:
Pure preset/generation data, runtime ordering, preview ordering, tests, and docs changed. CITY, stars, UFO behavior, audio, shell tail, glitter, camera motion, and main launcher remain unchanged.

## 2026-06-27 Render UFO as wireframe saucer

Decision:
Replace the UFO's flat sprite-like runtime drawing with a small 3D wireframe saucer built from Pyxel-independent `Vec3` geometry and rendered through the existing `Camera3D` projection.

Reason:
The previous UFO was easy to miss because it read as a small 2D mark while the rest of the scene uses 3D projected line geometry. A wireframe saucer matches the CITY, ferris wheel, box, and firework projection language without increasing frequency or adding effects.

Alternatives:
Increase UFO spawn frequency, make it larger/brighter, add sound/trails/beams, or leave it as a flat mark.

Impact:
Only UFO geometry/rendering and related tests/docs changed. UFO scheduling frequency, rarity, `U` toggle behavior, silence, no-beam/no-trail/no-particle constraints, firework generation, CITY, stars, audio, shell tail, glitter, and controls remain unchanged.

## 2026-06-27 Tune UFO height bands and Long Willow trails

Decision:
Modestly increase UFO wireframe size, choose UFO flyby altitude from deterministic low/middle/high bands, and tune `Long Willow` particles into mixed trail groups.

Reason:
UFO readability should improve through spatial clarity rather than frequency, brightness, sound, or effects. Long Willow should gain visual richness internally by mixing longer falling branches with lighter embers rather than adding another willow preset.

Alternatives:
Make UFO more frequent, add UFO sound/trails/beams, add another willow variant, or make all Long Willow particles use long trails.

Impact:
UFO scheduling cadence, rarity, `U` toggle behavior, no-sound/no-beam/no-trail/no-particle constraints, CITY, stars, audio, shell tail, global glitter, firework order, random/salvo scheduling, and baseline Willow remain unchanged.

## 2026-06-27 Add delayed mini-burst garnish

Decision:
Add delayed mini-burst garnish as an optional secondary show effect for Kiku, Sphere Bloom, Peony, and Multi-ring. The effect schedules a small deterministic set of nearby child blooms after staggered delays.

Reason:
The runtime already supports secondary particle spawning for Senrin, and a small delayed garnish adds show-like after-pop texture without adding a new main firework kind. Limiting the first pass to rounder / denser eligible parents avoids cluttering Willow, Long Willow, Ring, Halo, Senrin, and Spiral.

Alternatives:
Create a new mini-burst firework kind, attach garnish to every preset, make garnish always occur, add child-burst SFX/glitter, or postpone until after Smile.

Impact:
Runtime effects and app scheduling changed. Firework cycle/order, random/salvo scheduling, CITY, stars, UFO, audio, shell tail, global glitter behavior, launcher behavior, and existing main firework kinds remain unchanged.

## 2026-06-27 Add smile firework preset

Decision:
Add `Smile` as a first-class shaped firework preset. The burst uses two eye clusters and a smiling mouth arc embedded in a front-biased 3D plane.

Reason:
The current set already covers natural sphere, ring, spiral, willow, multi-ring, Senrin, and Halo patterns. A simple shaped Smile preset adds a readable playful show element while staying within the existing deterministic burst model.

Alternatives:
Implement Star or Heart first, add Smile as a garnish instead of a main preset, or attach delayed mini-burst garnish to Smile.

Impact:
Preset/generation dispatch, runtime and preview firework order, random/salvo selection, tests, and docs changed. Smile is excluded from delayed mini-burst garnish so after-pops do not obscure the face. `main.py`, launcher behavior, CITY, stars, UFO, audio, shell tail, global glitter, and existing firework behavior remain unchanged.

## 2026-06-27 Add per-burst color palette variants

Decision:
Add three predefined color palette variants for each current firework kind and select one deterministically from the launch seed.

Reason:
Fixed one-palette-per-kind coloring made random shows visually repetitive. Seed-selected palette variants add show variety without changing firework geometry, timing, shell tail, trail behavior, or runtime controls.

Alternatives:
Use one global palette bank for every kind, choose colors with global random state, recolor particles independently, or defer color work until after additional presets.

Impact:
Firework preset color data, burst color selection, runtime accent/garnish color selection, tests, and docs changed. Delayed mini-burst garnish inherits the selected parent palette. `main.py`, launcher behavior, CITY, stars, UFO, audio, shell tail, global glitter, Long Willow trail behavior, and firework geometry remain unchanged.

## 2026-06-27 Tune Long Willow long trail decay

Decision:
Add a Long Willow-only long-branch trail history. Long branch particles keep about 56 frames of trail samples, and older rear trail sections render sparsely broken.

Reason:
Long Willow needed longer lingering branch trails without making every ember heavy or turning the burst into a solid rain curtain. A dedicated history field keeps the effect scoped to Long Willow long-trail particles.

Alternatives:
Increase global trail lifetime, retune baseline Willow, add global glitter, or make all Long Willow particles use solid long trails.

Impact:
Particle trail metadata, runtime/preview particle history rendering, Long Willow tests, and docs changed. Baseline Willow, shell tail, global glitter, Long Willow palette variants, mini-burst garnish palette inheritance, CITY, stars, UFO, audio, firework geometry, and launcher behavior remain unchanged.

Follow-up:
Long Willow long-branch particles now use softened downward velocity and reduced gravity so their lingering trails fall more slowly and stay inside the observation box. The change remains scoped to the long-trail branch subgroup.

## 2026-06-27 Scrub local paths and add public safety check

Decision:
Remove local absolute paths, local machine references, and user-specific fragments from tracked source, docs, goals, and handoff records. Add a release safety checker and run it as part of `scripts/check_all.py`.

Reason:
The project is moving toward public release. Durable docs and handoff files can accidentally preserve private machine paths, so release hygiene needs both one-time cleanup and an automated guard.

Alternatives:
Manually review only before release, leave historical logs untouched, or rely on external repository scanning.

Impact:
Docs/goals/handoff records now use repository-relative paths or neutral placeholders. `scripts/check_public_safety.py` scans tracked files for local absolute path patterns, and `scripts/check_all.py` runs it before tests and lint. Runtime behavior and visuals remain unchanged.

## 2026-06-27 Add Japanese public README

Decision:
Add `README.ja.md` as a Japanese public-facing README, keep `README.md` as the main entry, and cross-link the two files.

Reason:
Firework Observer's intended mood and usage are easier to explain naturally in Japanese. A separate Japanese README keeps the public entry clear without replacing the current main README.

Alternatives:
Make `README.md` Japanese-primary and add `README.en.md`, or keep only an English README.

Impact:
README documentation and release checklist changed. Runtime behavior, launchers, firework generation, CITY, stars, UFO, audio, and safety checker behavior remain unchanged.

## 2026-06-27 Add mobile touch control panel

Decision:
Add touch-friendly official-runtime controls: drag/flick camera rotation on the play field and a top-right `MENU` button that opens a Pyxel-rendered mobile panel. Panel checkbox/settings changes are staged as a draft and reflected only by pressing `APPLY`.

Reason:
The public Pyxel Web build should be playable on smartphones without a keyboard. Keeping the controls behind a compact panel avoids covering the fireworks while still making key runtime toggles available.

Alternatives:
Add many always-visible touch buttons, require a hardware keyboard, or build a DOM overlay outside Pyxel.

Impact:
Only runtime input/render/app UI state, pure mobile UI helpers, tests, and docs changed. Firework generation, CITY, stars, UFO, audio behavior, shell tail, glitter, launcher behavior, and keyboard controls remain unchanged.

Follow-up:
Mobile panel text now uses scaled rendering for readability, and the panel includes `ZOOM+` / `ZOOM-` buttons so touch users can zoom without a keyboard. PC zoom remains available through `A` / `S`.

## 2026-06-28 Make mobile panel instant and add BGM toggle

Decision:
Change mobile panel checkboxes from staged draft controls to immediate toggles. Remove the `APPLY` step from the touch workflow, keep `CLOSE` as a simple dismiss action, and add a panel-only BGM toggle separate from the overall audio toggle.

Reason:
On a touch device, tapping a checkbox and seeing the game state change immediately behind the menu is more direct than staging changes and applying them later. BGM also needs a lighter control path: users may want quiet fireworks with explosion SFX intact.

Alternatives:
Keep `APPLY`, add a keyboard BGM shortcut, or make `M` cycle through audio states.

Impact:
Runtime mobile input, state/controller/audio behavior, panel rendering, tests, README, integration docs, visual checklist, goals, and handoff records changed. Firework generation, CITY, stars, UFO, shell tail, glitter, launcher behavior, and existing keyboard controls remain unchanged.

## 2026-06-28 Add PC mouse-wheel zoom

Decision:
Map `MOUSE_WHEEL_Y` to the runtime camera zoom target, using the same `MIN_ZOOM` / `MAX_ZOOM` bounds as keyboard and touch zoom controls.

Reason:
PC users naturally expect mouse-wheel scrolling to zoom the view. The feature complements existing `A` / `S` keyboard zoom and mobile `ZOOM+` / `ZOOM-` buttons without adding new visible UI.

Alternatives:
Keep zoom keyboard-only on PC, add separate zoom buttons for PC, or repurpose scroll for menu navigation.

Impact:
Runtime input handling, tests, README, integration docs, visual checklist, goals, and handoff records changed. Firework generation, CITY, stars, UFO, audio, mobile panel behavior, launcher behavior, and existing keyboard controls remain unchanged.

## 2026-06-28 Compact mobile panel height

Decision:
Shorten the mobile control panel and place `ZOOM+`, `ZOOM-`, and `CLOSE` as equal-width buttons on one bottom row.

Reason:
The panel was tall enough to cover almost the entire viewport, making it hard to judge zoom changes without closing the panel. Keeping some of the scene visible behind the panel makes touch zoom review more direct.

Alternatives:
Keep the full-height panel, add panel transparency, or move zoom controls outside the panel.

Impact:
Runtime mobile UI geometry, tests, README, integration docs, visual checklist, goals, and handoff records changed. Firework generation, CITY, stars, UFO, audio, input semantics, launcher behavior, and existing controls remain unchanged.

## 2026-06-28 Add mobile salvo count selector

Decision:
Move BGM onto the same mobile panel row as audio, and use the freed row for a top `COUNT` selector that cycles `1`, `2`, `3`, `4`, `5`, and `RND`. The existing mobile salvo action becomes `SALVO START` and starts the currently selected count.

Reason:
Audio and BGM are closely related toggles and fit naturally on one row. Touch users also need access to fixed-count salvos without keyboard number keys, but changing the count should not immediately fire while the user is cycling through choices.

Alternatives:
Keep BGM on its own row, make the count selector fire immediately, add six separate count buttons, or leave fixed-count salvos keyboard-only.

Impact:
Runtime mobile UI geometry, input handling, app mobile panel state, tests, README, integration docs, visual checklist, goals, and handoff records changed. Firework generation, CITY, stars, UFO, audio playback behavior, shell tail, glitter, launcher behavior, and keyboard controls remain unchanged.

## 2026-06-28 Show current firework kind on mobile selector

Decision:
Replace the small mobile `NEXT` label with a wider button labeled by the currently selected firework kind.

Reason:
Touch users could cycle firework kinds, but the panel did not make the current selection clear. Showing the selected kind directly makes the button both a status display and the cycle control.

Alternatives:
Keep `NEXT`, add a separate read-only label, or move firework selection into a larger list/menu.

Impact:
Runtime mobile UI geometry/rendering, mobile UI tests, README, integration docs, visual checklist, goals, and handoff records changed. Firework generation, CITY, stars, UFO, audio, shell tail, glitter, launcher behavior, and keyboard controls remain unchanged.

## 2026-06-28 Connect mobile count selector to salvo state

Decision:
Make the mobile `COUNT` selector update runtime salvo state, not only the panel-local label.

Reason:
The panel showed `COUNT` cycling, but `SALVO START` and active persistent salvos could continue using the old runtime count, making the UI look disconnected from the actual launched salvo size.

Alternatives:
Keep `COUNT` as a pending selection that only applies on `SALVO START`, or split the UI into separate apply/start controls.

Impact:
Runtime mobile salvo state handling and tests changed. Firework generation, CITY, stars, UFO, audio, shell tail, glitter, launcher behavior, panel layout, and keyboard controls remain unchanged.

## 2026-06-28 Connect mobile auto launch to selected count

Decision:
Make mobile-panel `AUTO` launches use the selected `COUNT` value instead of always scheduling a single-shell launch.

Reason:
The touch panel presents `AUTO` beside the `COUNT` selector, so users expect automatic launches to honor the selected count. Keeping `AUTO` as single-shell only made the panel feel disconnected.

Alternatives:
Keep `AUTO` as keyboard-equivalent single-shell auto launch, require `SALVO START` for multi-shell automatic repeats, or add a separate auto-salvo toggle.

Impact:
Runtime mobile auto-launch scheduling and tests changed. Firework generation, CITY, stars, UFO, audio, shell tail, glitter, launcher behavior, panel layout, and keyboard controls remain unchanged.
