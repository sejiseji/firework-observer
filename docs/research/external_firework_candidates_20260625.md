# External Firework Candidates 2026-06-25

## Purpose

This document reviews `/Users/toytoytoy330/Desktop/AllMyFiles/Pyxel/01_kamito/Firework.py` as visual and mathematical reference material for future Firework Observer presets.

Do not copy code from that file into this project. The old file is a 2D complex-plane Pyxel sketch. Firework Observer should translate useful ideas into deterministic 3D `Vec3` / `ParticleSpawnSpec` generation.

## Source System Summary

The external file generates burst shapes mostly as lists of complex 2D positions. It uses direct randomness, screen-space assumptions, and post-burst point expansion.

Firework Observer currently uses:

- y-up internal 3D coordinates.
- deterministic seed-based generation.
- `ParticleSpawnSpec` as initial velocity and visual data.
- `Camera3D` projection through the observation box.
- partial trails controlled by preset data.

Translation rule:

```text
external 2D shape idea
-> deterministic 3D orientation / basis
-> Vec3 velocity directions
-> ParticleSpawnSpec sequence
```

## Recommended Order

| Order | Candidate | Category | Risk | Recommendation |
| --- | --- | --- | --- | --- |
| 1 | Halo | ring-based | Low | Best next implementation candidate |
| 2 | Elliptical / Orbit | ring-based | Low | Strong fit for 3D observation |
| 3 | Golden Bloom / Fibonacci | sphere/spiral-based | Medium | Good mathematical preset |
| 4 | Counter Ring | ring/spiral hybrid | Medium | Useful Ring/Spiral bridge |
| 5 | Star | plane shape | Medium | Clear shape preset, best after shape-plane scaffold |
| 6 | Heart | plane shape | Medium | Strong novelty, more symbolic |
| 7 | Sierpinski | geometry/fractal | High | Interesting but density-sensitive |
| 8 | Magic Square / Grid | geometry burst | High | More geometric specimen than firework |

## Candidate Details

### Halo

- Source idea: `halo_burst`
- External behavior: particles keep a ring-like distance with a small sinusoidal radial modulation.
- Firework Observer translation:
  - Reuse Ring orientation concepts.
  - Generate one softly modulated ring or shallow halo shell.
  - Use low to moderate particle count.
  - Keep trail rate lower than Ring and Multi-ring.
- Suggested category: ring-based.
- Orientation bank: yes, use `RingOrientationBank`.
- Density risk: low to medium.
- Preview-first: yes.
- Notes:
  - Differentiate from Multi-ring by making it a soft outer glow, not several crisp rings.
  - Implemented in `T0003.9` as a light, soft, wobbling single-ring burst.

### Elliptical / Orbit

- Source idea: `elliptical_burst`
- External behavior: planar ellipse with random rotation.
- Firework Observer translation:
  - Use a 3D oriented plane.
  - Use one in-plane basis vector as the major axis and the other as the minor axis.
  - Generate velocity directions from an ellipse instead of a circle.
  - Add small normal thickness so it does not become a purely flat screen shape.
- Suggested category: ring-based.
- Orientation bank: yes, either reuse Ring orientation or create an ellipse/orbit bank.
- Density risk: low.
- Preview-first: yes.
- Suggested names: `Orbit`, `Ellipse`, `Oval Ring`.
- Notes:
  - Strong match for rotating the observation box, because the ellipse changes character by camera angle.

### Golden Bloom / Fibonacci

- Source ideas: `fibonacci_burst`, `fibonacci_burst_multiple`
- External behavior: particles use golden-ratio angular spacing.
- Firework Observer translation:
  - Use golden-angle indexing for direction generation.
  - Vary speed or radius by particle index.
  - Add small z or y layering so it reads as a 3D bloom instead of a flat disc.
  - Keep deterministic seed control for roll, scale, and palette choices.
- Suggested category: sphere/spiral-based.
- Orientation bank: optional.
- Density risk: medium.
- Preview-first: yes.
- Suggested names: `Golden Bloom`, `Phyllotaxis`, `Fibonacci Bloom`.
- Notes:
  - This can sit between Kiku and Spiral: organic distribution, less symbolic than Star or Heart.

### Counter Ring

- Source idea: `ring_burst2`
- External behavior: alternating particles reverse angular direction, creating opposing spiral/ring structure.
- Firework Observer translation:
  - Use one orientation plane.
  - Split particles into two direction groups.
  - Group A advances theta normally; Group B uses reversed theta or offset roll.
  - Add slight speed differences so the two strands braid without becoming a dense cloud.
- Suggested category: ring/spiral hybrid.
- Orientation bank: yes.
- Density risk: medium.
- Preview-first: yes.
- Suggested names: `Counter Ring`, `Braided Ring`, `Twin Spiral Ring`.
- Notes:
  - Good bridge between Ring and Spiral.
  - Keep trail rate restrained; braided trails can become visually loud.

### Star

- Source idea: `star_burst`
- External behavior: five outer points and five inner points form a star.
- Firework Observer translation:
  - Use a future plane-shape scaffold.
  - Generate 2D star control points in local plane coordinates.
  - Convert local shape points into 3D velocity directions.
  - Add slight normal thickness and small per-point jitter.
- Suggested category: plane shape.
- Orientation bank: yes, likely a `ShapePlaneOrientationBank`.
- Density risk: medium.
- Preview-first: yes.
- Notes:
  - Clear from the front, compressed from the side.
  - Should be treated as a special shape preset, not a core natural firework.

### Heart

- Source idea: `heart_shape`
- External behavior: standard parametric heart curve in 2D.
- Firework Observer translation:
  - Use the same future plane-shape scaffold as Star.
  - Sample the heart curve into local plane offsets.
  - Convert offsets into velocity directions and clamp maximum speeds.
  - Use very low trail rate so the icon shape stays legible.
- Suggested category: plane shape.
- Orientation bank: yes.
- Density risk: medium.
- Preview-first: yes.
- Notes:
  - Strong novelty preset.
  - More symbolic than the current Firework Box direction; delay until core presets are stable.

### Sierpinski

- Source idea: `sierpinski_triangle_burst`
- External behavior: recursive triangle subdivision.
- Firework Observer translation:
  - Generate bounded local triangle points.
  - Use a low recursion depth and strict particle cap.
  - Convert points into velocity directions in a 3D plane.
  - Use almost no trails.
- Suggested category: geometry/fractal.
- Orientation bank: yes, shape-plane based.
- Density risk: high.
- Preview-first: yes.
- Notes:
  - Reads as a geometric specimen more than a natural firework.
  - Delay until shape-plane rendering and density budget are proven.

### Magic Square / Grid

- Source idea: `magic_square_firework`
- External behavior: rotated grid of points.
- Firework Observer translation:
  - Treat as a grid burst or temporary geometric mark inside the box.
  - Use low particle count and minimal trails.
  - Consider this for a future geometry burst pack rather than the main firework set.
- Suggested category: geometry burst.
- Orientation bank: optional, but a plane orientation is needed.
- Density risk: high if grid is large.
- Preview-first: yes.
- Notes:
  - Could look like a box-contained pattern experiment rather than fireworks.

### Radiating Sphere Projection

- Source idea: `radiating_sphere_projection_burst`
- External behavior: distributes points on a sphere, rotates them, then projects to 2D.
- Firework Observer translation:
  - Do not port the 2D projection.
  - Use direct `Vec3` sphere directions in the existing coordinate system.
  - This mostly overlaps Kiku and possible future 3D shell variants.
- Suggested category: sphere-based.
- Orientation bank: no, direct sphere direction generation is enough.
- Density risk: medium to high if particle count follows the external values.
- Preview-first: yes.
- Notes:
  - Useful as confirmation that true 3D sphere generation belongs natively in Firework Observer, not as imported 2D projection math.
  - `T0008.0` addressed the required canonical sphere role with `Sphere Bloom`, implemented as native deterministic `Vec3` sphere generation rather than external 2D projection logic.

### Required Willow Variant Follow-Up

- Source idea: stronger willow / falling-tail family.
- Firework Observer translation:
  - Keep the existing baseline Willow intact.
  - Add a separate longer-falling willow variant with stronger downward gravity, longer lifetime, and more visible trail emphasis.
- Status:
  - `T0008.0` added `Long Willow` for this role.
- Notes:
  - Future tuning should compare baseline Willow and Long Willow side by side instead of merging their identities.

## Implementation Guidance

### Do Not Copy

- Do not import `Firework.py`.
- Do not copy its functions.
- Do not preserve complex-number screen-space coordinate handling.
- Do not use global random state.
- Do not copy its particle counts directly.

### Translate Instead

- Plane candidates should use a deterministic 3D plane basis.
- Ring candidates should reuse or extend `RingOrientationBank`.
- Shape candidates should wait for a shared shape-plane scaffold.
- Geometry candidates should be preview-first and low density.
- Every generated particle should still be a `ParticleSpawnSpec`.

### Orientation Strategy

Use the existing `RingOrientationBank` for:

- Halo
- Orbit / Elliptical
- Counter Ring

Add a future `ShapePlaneOrientationBank` only when implementing:

- Star
- Heart
- Sierpinski
- Magic Square / Grid

## Recommended Follow-Up Tasks

1. `T0008.1`: Visual review and tune Sphere Bloom / Long Willow if needed.
2. `T0008.2`: Implement Orbit / Elliptical preset.
3. `T0008.3`: Implement Golden Bloom / Fibonacci preset.
4. `T0008.4`: Implement Counter Ring preset.
5. `T0008.5`: Add shape-plane burst scaffold.
6. `T0008.6`: Implement Star preset.
7. `T0008.7`: Implement Heart preset.
8. `T0008.8`: Evaluate Sierpinski / Magic Square geometry bursts.

Before starting those, run the existing visual tuning checklist against `iphone16_balanced`. If Senrin, Multi-ring, or Willow are already too dense, tune density first.

## Current Recommendation

Do manual visual review first:

```bash
.venv/bin/python tools/preview_firework_box.py --profile iphone16_balanced
```

Sphere Bloom and Long Willow now cover the required sphere and willow roles. Review them in the official runtime first; if density is stable, proceed to Orbit / Elliptical or another clearly distinct preset. If density is not stable, tune Sphere Bloom, Long Willow, Senrin, Multi-ring, or Willow before adding more presets.
