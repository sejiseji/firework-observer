# Visual Tuning Checklist

## Purpose

This checklist defines how to evaluate the current Firework Box preview before changing preset parameters or adding more effects.

Use it to judge Kiku, Ring, Spiral, Willow, Peony, Multi-ring, Senrin, and Halo in the manual preview. Do not treat this document as permission to change preset values, production runtime behavior, scenery, or `main.py`.

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
- Works as the reference preset for comparison with Peony and Senrin.

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

### Peony

- Looks shorter and brighter than Kiku.
- Trails are restrained and points remain the main visual.
- Brief accent rays make the first bloom feel bright.
- It is not too similar to Kiku.
- It does not read like Willow or Ring.

### Multi-ring

- Multiple layers are readable as nested rings.
- It is clearly different from a single Ring.
- A 5-shot salvo does not fully obscure the box.
- Accent rays do not hide layer separation.
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
   - Select Kiku, Peony, Ring, Spiral, Willow, Multi-ring, Senrin, and Halo.
   - Press `Z` for each type.
   - Confirm burst radii are subtly uneven but compact enough that bursts do not feel over-expanded.
   - Confirm maximum burst radius reads about 80% of the previous wide spread.
   - Confirm Ring and Multi-ring do not collapse into cloudy spheres.
   - Confirm Senrin secondary bursts remain sparse and controlled.
   - Confirm Halo remains a soft light ring and does not become a second Multi-ring.

12. Scenery readability check:
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
```

Parity checks:

- `iphone16_balanced` should remain the primary visual target.
- `classic` should remain the default compatibility baseline.
- The runtime should preserve the same 3D cuboid observation-box feel.
- Kiku, Ring, Spiral, Willow, Peony, Multi-ring, Senrin, and Halo should remain available.
- Shell launch, short shell tail, compact burst radius, deterministic wobble, pre-scale trail decisions, and glitter residue should match the preview direction.
- CITY should preserve 48 building cuboids, central boulevard, tower, ferris wheel, signs, sparse windows, and interleaved two-blue building outlines.
- Interior stars should remain attached to top and upper side faces, never exterior-facing surfaces.
- Top-face stars should remain visible at shallow interior viewing angles.
- Side-face star visibility should remain stricter than top-face visibility.
- Auto rotate should preserve slow/normal/fast modes and reduced speed-dependent pitch sway.
- `R + H + 0` remains the primary stress review for type, height, and random-count salvo density.

Runtime migration failures should be treated as parity bugs before adding new visual features.
