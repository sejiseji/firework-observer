# Visual Tuning Checklist

## Purpose

This checklist defines how to evaluate the current Firework Box preview before changing preset parameters or adding more effects.

Use it to judge Kiku, Ring, Spiral, Willow, Peony, Multi-ring, and Senrin in the manual preview. Do not treat this document as permission to change preset values, production runtime behavior, scenery, or `main.py`.

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

5. Random variety check:
   - Press `R`.
   - Press `Z` repeatedly.
   - Confirm random type selection gives varied, recognizable bursts.

6. Auto random check:
   - Press `R`.
   - Press `V`.
   - Confirm auto launch uses random types and remains readable.

7. Fixed salvo check:
   - Select each type.
   - Press `1`, `2`, `3`, `4`, and `5`.
   - Confirm fixed-count loops are readable for each type.

8. Random-count check:
   - Press `0`.
   - Confirm repeated salvos choose changing shot counts from 1 to 5.

9. Fireworks-show stress check:
   - Press `R`.
   - Press `H`.
   - Press `0`.
   - Observe combined type, count, and height variation.

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

## Depth And Box Readability

For every check:

- The transparent box should remain readable.
- Particles should appear inside the 3D volume.
- Rotating the camera should reveal shape differences.
- Trails should not erase the front box edges.
- Firework shell tails and accent rays should not erase front box edges.
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
- `T0003.9`: Add Halo preset if density is stable.

Runtime integration planning should wait until visual tuning is stable enough that the preview no longer needs large parameter corrections.
