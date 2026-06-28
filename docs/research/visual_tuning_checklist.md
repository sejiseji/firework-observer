# Visual Tuning Checklist

## Purpose

This checklist defines how to evaluate the current Firework Box preview before changing preset parameters or adding more effects.

Use it to judge Kiku, Sphere Bloom, Smile, Ring, Spiral, Willow, Long Willow, Peony, Multi-ring, Senrin, and Halo in the manual preview and official runtime. Do not treat this document as permission to change preset values, production runtime behavior, scenery, or `main.py`.

Before public release, run `python3 scripts/check_public_safety.py` and keep documentation paths repository-relative.

## Profile Policy

- `classic` remains the compatibility and test baseline.
- `iphone16_balanced` is the primary visual tuning target.
- `iphone16_large` is an optional stress check after `iphone16_balanced` is readable.

Current key profile values:

| Profile | Screen | Box | Role |
| --- | --- | --- | --- |
| `classic` | `256x144` | `120x80x120` | Protected comparison baseline |
| `iphone16_balanced` | `236x512` | `120x260x120` | Primary visual tuning target |
| `iphone16_large` | `393x852` | `200x440x200` | Optional larger stress check |

## Preview Commands

```bash
.venv/bin/python tools/preview_firework_box.py
.venv/bin/python tools/preview_firework_box.py --profile iphone16_balanced
```

Use `iphone16_balanced` for most visual judgement. Use `classic` to confirm compatibility and compact-screen readability.

## Preview Controls

| Input | Behavior |
| --- | --- |
| `SPACE` | Cycle firework type in sequential mode, or exit random type mode |
| `R` | Enter random burst type mode |
| `Z` | Launch one immediate burst |
| `V` | Toggle auto launch |
| `1` | Start persistent one-shot salvo loop |
| `2`-`5` | Start persistent fixed-count salvo loop |
| `0` | Start persistent random-count salvo loop |
| `H` | Toggle salvo burst height variation |
| `G` | Cycle scenery preset |
| `B` | Toggle scenery visibility |
| `T` | Toggle interior box stars |
| `X` | Toggle auto rotate |
| `D` | Toggle debug HUD |
| `A` / `S` | Zoom in / out |
| Arrow keys | Rotate camera |

Interaction rules:

- `R` randomizes burst type.
- `0` randomizes salvo count.
- `H` randomizes explosion height within the box.
- Rising firework shells should show a short fixed gradient tail behind the fireball, not full launch-to-current path lines.
- The canonical shell tail color sequence is white, white, white, yellow, yellow, brown, brown.
- Shell tail geometry and colors are shared across burst types. Do not vary this shape by firework type.
- Avoid rocket-like terminology and behavior for the rising shell visual.
- Burst accent rays should appear only briefly and only on a limited subset of particles.
- Each firework kind should retain its identity across its three deterministic color palette variants.
- Repeated launches with different seeds may change color, but geometry, timing, shell tail, trail behavior, and glitter behavior should not change because of palette selection.
- Delayed mini-burst garnish should inherit the selected parent palette.
- `R` and `0` are independent.
- `R + 0` randomizes both type and count.
- `R + 0 + H` is the main fireworks-show stress mode.
- `V` auto launch and persistent salvo loops are mutually exclusive.
- `Z` remains a single immediate launch and does not change persistent salvo state.
- `G` cycles low-detail in-box 3D scenery presets.
- `B` hides or shows scenery without changing firework behavior.
- `T` hides or shows subtle stars attached to the top and upper interior side faces.
- Scenery must rotate with the box. It is not a 2D screen-space background.
- Interior stars must not render on exterior-facing box surfaces.

## Per-Firework Checks

### Kiku

- Reads as the baseline sphere.
- Density is full but not opaque.
- Trails show motion without turning every particle into a line.
- The shared white/yellow/brown shell tail and a few center accent rays make the opening readable.
- Occasional delayed mini-burst garnish stays near the main burst and remains sparse.
- Works as the reference preset for comparison with Peony and Senrin.

### Sphere Bloom

- Reads as the clean canonical sphere-like firework.
- Feels smoother and more uniform than Kiku.
- Stays distinct from Peony by being calmer and less pink/red.
- Sparse trails do not make it noisy.
- Occasional delayed mini-burst garnish reads as a small after-pop, not a second full explosion.
- Salvos do not make it too dense.

### Smile

- Reads as a smile face in `iphone16_balanced`.
- Both eyes are visible.
- The mouth arc is visible and reads as a smile, not a random curve.
- The shaped plane avoids extreme edge-on angles.
- It stays playful but does not dominate the show.
- Delayed mini-burst garnish does not apply to Smile, so after-pops do not obscure the face.

### Ring

- Orientation varies across launches.
- No obvious fixed-direction bias appears during repeated random launches.
- The ring plane is readable when rotating the camera.
- The shared shell tail and accent rays do not obscure the ring plane.
- It remains distinct from Multi-ring.

### Spiral

- Reads as a 3D twisted structure, not a flat circle.
- Rotation reveals depth and twist.
- It does not overextend vertically in `iphone16_balanced`.
- Accent rays reinforce the twist without over-drawing it.
- It remains distinct from Ring.

### Willow

- Tails visibly fall under gravity.
- The portrait volume gives the falling trails enough space.
- Trail density is high enough for afterglow but not high enough to cover later salvos.
- The shared shell tail and accent rays do not compete with Willow's falling particle trails.
- It remains distinct from Kiku and Peony.

### Long Willow

- Reads immediately as the stronger willow / 枝垂れ variant.
- Falls longer and more gracefully than baseline Willow.
- Does not become a full-screen rain curtain.
- Includes both longer-trail falling branches and trail-light / no-long-trail embers.
- Long branches leave roughly 0.93 seconds of falling trail history.
- Long branches fall gently enough to stay inside the observation box instead of punching through the floor.
- Older rear trail sections become sparse and broken instead of remaining solid.
- The mixed trail structure adds depth without making the burst noisy.
- Salvos remain readable and do not hide later bursts.
- CITY and shell tails remain readable below it.

### Peony

- Looks shorter and brighter than Kiku.
- Trails are restrained and points remain the main visual.
- Brief accent rays make the first bloom feel bright.
- Occasional delayed mini-burst garnish remains small enough that Peony still reads short and bright.
- It is not too similar to Kiku.
- It does not read like Willow or Ring.

### Multi-ring

- Multiple layers are readable as nested rings.
- It is clearly different from a single Ring.
- A 5-shot salvo does not fully obscure the box.
- Accent rays do not hide layer separation.
- Occasional delayed mini-burst garnish does not hide layer separation.
- Random mode density remains acceptable when Multi-ring appears with other presets.

### Senrin

- Primary particles scatter first, then delayed secondary bursts appear.
- Secondary bursts are visible but not too dense.
- Secondary trails remain sparse.
- Primary accent rays are limited, and secondary bursts do not gain dense extra rays.
- A 5-shot salvo does not overwhelm the preview.
- Random-count salvos remain readable when Senrin appears.

### Halo

- Reads as a soft uneven light ring, not a dense sphere.
- It is lighter and more atmospheric than Multi-ring.
- The subtle radial wobble is visible without turning into a noisy cloud.
- Sparse trails do not cover CITY or later salvos.
- It remains distinct from Ring and Multi-ring.

## Check Sequences

1. Single type check:
   - Use `SPACE` to select each type.
   - Press `Z`.
   - Confirm the type is visually distinct.

2. Height variation check:
   - Press `H`.
   - Press `Z` several times and use `1`-`5` loops.
   - Confirm burst heights vary without leaving the box.

3. Firework shell tail check:
   - Use `1`-`5` salvo loops.
   - Confirm firework shells rise before bursts.
   - Confirm tails are short and follow recent motion only.
   - Confirm the tail near the shell is white, the middle is yellow, and the oldest tail is brown.
   - Confirm salvos have visible flight-time variation.
   - Confirm random burst type mode does not change the shell tail shape unexpectedly.

4. Burst accent check:
   - Press `Z` for each type.
   - Confirm only a few center-outward rays appear.
   - Confirm accent rays disappear quickly.
   - Confirm Senrin secondary bursts do not become over-dense.

5. Glitter residue check:
   - Press `Z` for each type.
   - Confirm a few tiny glitter points remain briefly after the burst starts.
   - Confirm residue expires quickly and does not read as a second explosion.
   - Confirm Senrin remains sparse, especially around secondary bursts.

6. Random variety check:
   - Press `R`.
   - Press `Z` repeatedly.
   - Confirm random type selection gives varied, recognizable bursts.

7. Auto random check:
   - Press `R`.
   - Press `V`.
   - Confirm auto launch uses random types and remains readable.

8. Fixed salvo check:
   - Select each type.
   - Press `1`, `2`, `3`, `4`, and `5`.
   - Confirm fixed-count loops are readable for each type.

9. Random-count check:
   - Press `0`.
   - Confirm repeated salvos choose changing shot counts from 1 to 5.

10. Fireworks-show stress check:
   - Press `R`.
   - Press `H`.
   - Press `0`.
   - Observe combined type, count, and height variation.

11. Burst radius variation check:
   - Select Kiku, Sphere Bloom, Smile, Ring, Spiral, Willow, Long Willow, Peony, Multi-ring, Senrin, and Halo.
   - Press `Z` for each type.
   - Confirm burst radii are subtly uneven but compact enough that bursts do not feel over-expanded.
   - Confirm maximum burst radius reads about 80% of the previous wide spread.
   - Confirm Ring and Multi-ring do not collapse into cloudy spheres.
   - Confirm Senrin secondary bursts remain sparse and controlled.
   - Confirm Halo remains a soft light ring and does not become a second Multi-ring.

12. Color palette variant check:
   - Launch the same firework kind repeatedly.
   - Confirm color palettes can vary between launches.
   - Confirm each kind still reads as itself after palette changes.
   - Confirm delayed mini-burst garnish uses the same palette family as its parent.
   - Confirm `R + H + 0` feels less repetitive without becoming visually noisy.

13. Scenery readability check:
   - Press `G` to cycle `Empty` and `City`.
   - Press `B` to confirm scenery can be hidden.
   - Rotate the camera and confirm scenery projects with the box.
   - Confirm scenery stays in the lower part of the observation volume.
   - Confirm City reads as small 3D cuboid buildings, not a flat wall skyline.
   - Confirm City reads as a dense cutaway urban mass, not sparse isolated objects.
   - Confirm City has the intended denser 48-building footprint without closing the central boulevard.
   - Confirm sparse lit windows are visible without outshining fireworks.
   - Confirm bright and dark blue building outlines are roughly balanced and scattered, not grouped into large bright/dark clusters.
   - Confirm the landmark tower is larger than surrounding buildings but clearly grounded.
   - Confirm building-attached signs are visible but not noisy.
   - Confirm City buildings spread across most of the lower footprint, not only the center cluster.
   - Confirm the ferris wheel is recognizable, grounded, circular enough, and quieter than fireworks.
   - Confirm the ferris wheel reads closer to round than vertically narrow from side views.
   - Confirm the ferris wheel does not block core launch readability.
   - Confirm the central boulevard-like corridor remains visible through the city mass.
   - Confirm peripheral side floor regions have building coverage without filling the boulevard.
   - Confirm utility poles and sagging overhead wires are absent from active CITY.
   - Confirm `R + H + 0` remains readable with scenery enabled.

13. Interior star check:
   - Press `T` to toggle stars ON/OFF.
   - Rotate the camera.
   - Confirm top-face stars remain visible when the ceiling is clearly visible, even at near-limit shallow eye-line-to-ceiling angles.
   - Confirm stars appear on the interior top face and upper side-wall bands.
   - Confirm side-wall star visibility behaves as before and does not become too broad.
   - Confirm stars do not appear on the floor, lower side walls, or open central volume.
   - Confirm exterior-facing box surfaces do not show stars.
   - Confirm stars twinkle subtly and remain quieter than fireworks.
   - Confirm `R + H + 0` remains readable with stars ON.

14. Auto-rotate comfort check:
   - Press `X` to enable auto-rotate.
   - Press `Q` to cycle `slow`, `normal`, and `fast`.
   - Confirm `slow` is comfortable for long observation.
   - Confirm `normal` is calmer than the previous fast-feeling preview rotation.
   - Confirm `fast` remains faster than normal but is no longer excessive.
   - Confirm slower modes have smaller vertical sway than faster modes.
   - Confirm CITY, ferris wheel, boulevard, interior stars, and fireworks remain readable during rotation.

## Density Risk Thresholds

If 5-shot Senrin overwhelms the preview:

- Lower `SENRIN_SECONDARY_PRESET.rate`.
- Lower `SENRIN_SECONDARY_PRESET.count_range`.
- Lower secondary trail rate.
- Shorten secondary life range.

If 5-shot Multi-ring overwhelms the preview:

- Lower `MULTI_RING_PRESET.particle_count`.
- Lower Multi-ring trail rate.
- Shorten Multi-ring life range.
- Reduce layer counts.

If 5-shot Halo overwhelms the preview:

- Lower `HALO_PRESET.particle_count`.
- Lower Halo trail rate.
- Shorten Halo life range.
- Reduce Halo radius wobble.

If Willow trails cover later salvos:

- Lower Willow trail rate.
- Lower Willow trail early ratio.
- Shorten Willow life range.
- Increase the preview persistent salvo repeat interval.

If Peony and Kiku look too similar:

- Shorten Peony life range.
- Lower Peony trail rate.
- Brighten or adjust Peony palette.
- Adjust Peony speed range.

If firework shell tails dominate:

- Shorten shell tail history length.
- Use only the fixed white/yellow/brown gradient.
- Do not introduce type-specific shell tail colors before the base shell visual is stable.

If burst accent rays dominate:

- Lower per-type accent counts.
- Shorten accent ray lifetime.
- Darken accent ray colors.
- Disable accent rays for Senrin or Multi-ring first.

If glitter residue dominates:

- Lower residue count before changing main burst particle counts.
- Shorten residue lifetime.
- Darken residue colors or reduce bright twinkle frames.
- Keep Senrin residue minimal and do not add residue to Senrin secondary bursts unless explicitly tuned.

If burst radius variation dominates:

- Reduce sphere-like burst variation first.
- Reduce ring-like burst variation if rings lose planar readability.
- Keep Senrin secondary variation at none or near zero until density is stable.
- Prefer smaller bounded speed wobble over random position offsets.
- Preserve some deterministic variation; do not return all bursts to perfectly uniform radii.

If scenery dominates:

- Reduce line count.
- Use darker colors.
- Move scenery lower in the box.
- Prefer fewer back-phase lines before adding front-phase details.
- Reduce bright window count before removing building outlines.
- For CITY, keep building bottom-face perimeter edges omitted so buildings feel grounded into the cut floor plane instead of separate boxes.
- For CITY, preserve vertical and top edges plus sparse windows; do not weaken the buildings by removing all structure.
- For CITY, preserve the dense cutaway mass impression while keeping upper bloom space open.
- If CITY tower or signs dominate, reduce their line count or darken them before removing building windows.
- If the CITY ferris wheel dominates, reduce its rim/spoke line count or darken it before shrinking the broader building footprint.
- If CITY density hurts launch readability, restore small corridors around launch paths before removing the off-center landmark elements.
- If the central boulevard disappears, move building blocks outward before lowering overall CITY density.
- If the ferris wheel reads vertically narrow, tune its normalized x/y extent before adding cabin detail.
- If interior stars dominate, lower star count, darken twinkle colors, or hide edge-on faces more aggressively.
- If stars look painted on the outside of the box, tighten the interior-face visibility threshold before changing star placement.
- If ceiling stars disappear while the top interior face is clearly visible, relax only the top-face visibility threshold and leave side-wall thresholds unchanged.

If auto-rotate causes discomfort:

- Prefer lowering normal and fast rotation speeds before changing manual controls.
- Reduce pitch/vertical sway in slower modes.
- Keep `slow < normal < fast`.
- Keep `X` as auto-rotate ON/OFF and `Q` as speed cycling.
- Runtime parity should use package-side `runtime/camera_motion.py` values for preview and official runtime camera comfort.

## Depth And Box Readability

For every check:

- The transparent box should remain readable.
- Particles should appear inside the 3D volume.
- Rotating the camera should reveal shape differences.
- Trails should not erase the front box edges.
- Firework shell tails and accent rays should not erase front box edges.
- Scenery should remain quieter than fireworks and should not occupy the upper bloom space.
- Dense salvos should not hide the current firework type.

## Frame Pacing And Particle Budget

Watch the debug HUD in stress modes:

- `R + H + 0` is the primary density stress mode.
- Senrin and Multi-ring are the highest-risk presets for particle count.
- Willow is the highest-risk preset for long-lived trails.
- If stress mode becomes unreadable, prefer reducing density before adding new firework types.

## Follow-Up Task Candidates

- `T0003.8.1`: Tune Senrin density for portrait preview.
- `T0003.8.2`: Tune Multi-ring density for salvo preview.
- `T0003.8.3`: Tune Willow trail density.
- `T0003.8.4`: Tune Peony/Kiku distinction.
- `T0003.8.5`: Tune firework shell tail readability.
- `T0003.8.6`: Tune persistent salvo repeat interval.
- `T0003.8.8`: Tune burst accent ray density.
- `T0003.8.10`: Tune burst radius variation if identities become less readable.
- `T0004.2`: Add city landmark tower, utility poles, and overhead wires.
- `T0004.3`: Tune city scenery readability against fireworks.
- `T0003.9`: Add Halo preset if density is stable.

Runtime integration planning should wait until visual tuning is stable enough that the preview no longer needs large parameter corrections.

## Runtime Parity Checks

Use `docs/architecture/PREVIEW_TO_RUNTIME_INTEGRATION.md` as the contract for promoting the preview into package runtime.

When comparing an official runtime against the preview, use:

```bash
.venv/bin/python tools/preview_firework_box.py --profile iphone16_balanced
.venv/bin/python scripts/run_runtime_app.py --profile iphone16_balanced
```

Parity checks:

- `iphone16_balanced` should remain the primary visual target.
- `classic` should remain the default compatibility baseline.
- The runtime should preserve the same 3D cuboid observation-box feel.
- Kiku, Sphere Bloom, Smile, Ring, Spiral, Willow, Long Willow, Peony, Multi-ring, Senrin, and Halo should remain available.
- Shell launch, short shell tail, compact burst radius, deterministic wobble, pre-scale trail decisions, and glitter residue should match the preview direction.
- CITY should preserve 48 building cuboids, central boulevard, tower, ferris wheel, signs, sparse windows, and interleaved two-blue building outlines.
- Interior stars should remain attached to top and upper side faces, never exterior-facing surfaces.
- Top-face stars should remain visible at shallow interior viewing angles.
- Side-face star visibility should remain stricter than top-face visibility.
- Auto rotate should preserve slow/normal/fast modes and reduced speed-dependent pitch sway.
- `R + H + 0` remains the primary stress review for type, height, and random-count salvo density.

Runtime migration failures should be treated as parity bugs before adding new visual features.

Scheduling parity checks:

- `Z` should still schedule one shell launch.
- `1` should still start persistent one-shot salvo mode.
- `2` through `5` should still start fixed-count salvo modes.
- `0` should still start random-count salvo mode.
- `R` should still freeze the chosen firework kind per scheduled slot.
- `H` should still freeze burst height variation per scheduled slot.
- Salvo slot positions and offsets should continue to come from the package-side salvo pattern data.

Official runtime manual checks:

- The official runtime should launch without touching protected `main.py`.
- The preview should remain available after the official runtime is added.
- `SPACE`, `R`, `Z`, `V`, `1`-`5`, `0`, `H`, `X`, `Q`, `T`, `G`, `B`, `D`, `A`/`S`, and arrow keys should remain usable.
- CITY, interior stars, shell tails, compact bursts, glitter residue, salvos, and auto-rotate comfort should be recognizable against the preview reference.
- Any visual mismatch should be recorded as a runtime parity issue before adding UFO, new presets, or additional scenery.

The first runtime parity review is recorded in:

- `docs/research/runtime_parity_review_20260626.md`

Result:

- Official runtime parity: OK.
- Runtime stability: OK.
- `main.py` handoff readiness: READY.

Default public entry paths after T0005.6.1:

- `python main.py`
- `python3 main.py`
- `pyxel run main.py`

The explicit runtime launcher remains available:

- `.venv/bin/python main.py --profile iphone16_balanced`
- `.venv/bin/python scripts/run_runtime_app.py --profile iphone16_balanced`

## Runtime Audio Checks

T0006.0 adds official runtime audio. Check it from the default runtime path, not the manual preview harness.

Command:

```bash
.venv/bin/python main.py --profile iphone16_balanced
```

Checks:

- BGM starts on launch.
- BGM reads as quiet, fragile music-box ambience and does not command attention.
- BGM uses simple chord harmony: channel 0 melody, channel 1 harmony, channel 2 calm mid-register support.
- Melody remains clear, but the BGM sits behind the fireworks.
- Harmony/support do not read as independent counter-lines.
- Support feels like a slow `tan` / `ta-tan` pulse, not high shimmer.
- BGM volume hierarchy is clear and restrained: melody medium-low, harmony lower, support soft.
- BGM loop still does not feel like a short single-note loop.
- `M` toggles audio off and back on.
- `Z` plays a low, restrained explosion SFX at burst timing, not at shell launch.
- `1`-`5` salvos and `R + H + 0` do not stack explosion sounds into noise.
- Explosion SFX remains separated on channel 3 and is the primary audio subject.
- Visual behavior remains unchanged.
- UFO has no sound.

## Runtime UFO Ambient Checks

T0007.0 adds a rare official-runtime UFO ambient flyby. T0007.1 renders it as a small 3D wireframe saucer instead of a flat sprite-like mark. T0008.1 modestly increases UFO size and varies flyby height across deterministic low, middle, and high bands. It is not part of firework generation and should not affect gameplay or audio.

Command:

```bash
.venv/bin/python main.py --profile iphone16_balanced
```

Checks:

- UFO ambient is enabled by default.
- `U` toggles UFO ambient on and off.
- UFO appears only rarely during normal observation.
- UFO passes calmly through the upper observation space.
- UFO is a small 3D wireframe saucer, readable but not dominant.
- UFO height varies across low, middle, and high bands.
- Low UFO passes remain clearly above CITY.
- Camera rotation helps the UFO feel placed inside the observation box.
- UFO has no beam, trail, particles, collision, sound, or gameplay interaction.
- Fireworks, CITY, stars, BGM, explosion SFX, shell tail, and glitter remain unchanged.
- `R + H + 0` remains readable if a UFO appears.

## Mobile Touch Control Checks

Use the official runtime or Pyxel Web build on a touch-capable device.

```bash
.venv/bin/python main.py --profile iphone16_balanced
```

Checks:

- Dragging or flicking the play field rotates the camera by default.
- On PC, mouse wheel changes camera zoom within the same safe range as `A` / `S`.
- The top-right `MENU` button opens and closes the mobile control panel.
- The public Pyxel Web build should not show Pyxel's default virtual d-pad/buttons.
- On iPhone, confirm Silent Mode is off before judging runtime audio.
- Panel checkboxes immediately reflect random, height, auto launch, auto rotate, stars, UFO, audio/BGM, and city settings behind the panel.
- Mobile `random` should randomize only firework type and should not change the current `COUNT`, including `COUNT RND`.
- `COUNT` cycles salvo count selection through `1`, `2`, `3`, `4`, `5`, and `RND`.
- `COUNT` updates the runtime salvo count state, so `SALVO START` and active salvo repeats use the selected count.
- `AUTO` uses the selected `COUNT` value for automatic launches instead of forcing single-shell launches.
- `BGM` can be turned off while `audio` remains on, and explosion SFX still plays.
- `speed` immediately cycles the auto-rotate speed.
- `CLOSE` dismisses the panel without changing already-applied settings.
- `LAUNCH` starts a single shell.
- The wide firework-kind button displays the current firework name and cycles the selected kind.
- `SALVO START` starts the currently selected `COUNT` salvo mode.
- `ZOOM+` and `ZOOM-` change the camera zoom on touch devices.
- `ZOOM+`, `ZOOM-`, and `CLOSE` share one compact bottom row so some of the scene remains visible behind the panel.
- Mobile panel text is larger than the normal HUD text and remains readable on a phone.
- Touch controls do not break keyboard or mouse-wheel controls.
- The menu and panel remain readable on the `iphone16_balanced` profile.
- Fireworks, CITY, stars, UFO, audio, shell tail, and glitter remain visually unchanged.
