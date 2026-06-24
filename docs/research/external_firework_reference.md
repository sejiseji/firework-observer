# External Firework Reference Notes

Source reviewed:

- `/Users/toytoytoy330/Desktop/AllMyFiles/Pyxel/01_kamito/Firework.py`

Review date: 2026-06-23

## Purpose

This document records reusable visual ideas from the external firework file.
The external file is reference material only. Do not import it directly, copy its
implementation into `src/`, or refactor the protected standalone `main.py` as
part of this research task.

## Summary Of The Old System

The old file is a 2D Pyxel-style firework generator built around complex numbers.
Most burst functions accept a complex center point and return a list of complex
particle positions. A `Firework` object launches upward in screen coordinates,
chooses one burst function at random, creates static burst points at peak height,
then repeatedly expands the burst around its center while life decreases.

Important traits:

- Burst shapes are mostly position sets, not velocity-based particles.
- The code uses 2D screen-space assumptions.
- Randomness is direct global `random` usage, not deterministic seed injection.
- Many functions are useful as shape inspiration, but not as drop-in simulation.
- Several number-sequence shapes generate interesting point distributions but do
  not map cleanly to the current 3D box without reinterpretation.

## Candidate Firework Types To Adapt

Strong candidates:

- Radial burst: base chrysanthemum / peony style.
- Spiral burst: good source for a spiral preset.
- Ring burst and ring burst2: useful for ring and counter-spiral ring presets.
- Multi-ring burst: useful for layered shells.
- Halo burst: useful for a soft ring with slight radius modulation.
- Radiating sphere projection: useful idea for a 3D spherical shell, but should
  be rebuilt directly in the current `x/y/z` model rather than projected from 2D.
- Elliptical burst: useful for flattened perspective shells or angled-plane
  presets.
- Star burst: useful as a constrained planar novelty preset.
- Heart shape: useful as a planar novelty preset with slight `z` thickness.
- Sierpinski triangle: useful as an experimental geometric preset.
- Magic square: useful as a grid/spark-cluster preset, likely low priority.

Secondary candidates:

- Fibonacci burst and fibonacci_burst_multiple: useful for organic point spacing
  or layered distribution.
- Triangular burst: useful as a simple multi-radius burst.
- Spiral recursive burst: interesting, but likely too visually busy unless capped
  aggressively.
- Moser / happy number distributions: possible novelty patterns, but less aligned
  with the calm observer direction.

Low priority or avoid:

- Lucas, Pascal, Harshad, Pell, and Sylvester variants in the old file appear to
  rotate or scale the absolute center in ways that can drift the burst instead of
  generating clean relative offsets.
- Bezier curve burst is not currently useful as written; it returns repeated
  scaled center points rather than a clear curve distribution.
- Any shape requiring high particle counts should be delayed until frame pacing
  and trail budgets are proven stable.

## Parts That Should Not Be Copied Directly

- Direct use of global randomness. Current work should prefer injected/randomized
  seeds for replayable tests.
- Screen-space `x/y` behavior. Current Firework Box uses internal 3D coordinates.
- Static point expansion as the only motion model. Current package direction is
  better served by velocity-based particles with life, drag, gravity, and trail
  controls.
- Large particle counts such as 150-250 without explicit performance review.
- Function-by-function `if` chains for preset selection. Current code should move
  toward explicit preset data and small shape builders.
- Full trails on every particle. The current brief requires partial particle
  trails, with rocket trails always present.

## Coordinate-System Risks

The old file is 2D and screen-oriented:

- `x` increases to the right.
- `y` increases downward on screen.
- Launching upward is implemented by subtracting from `y`.
- Many burst functions return complex values where `real` is screen `x` and
  `imag` is screen `y`.

The current Firework Box direction is internal 3D:

- `x` is horizontal.
- `y` is height, and larger `y` means higher.
- `z` is depth.
- Projection and draw order must preserve the transparent box effect.

Migration rule:

- Treat old complex offsets as planar inspiration only.
- Convert old `complex(dx, dy)` into Firework Box offsets deliberately, usually
  `(x=dx, y=-dy, z=small_thickness_or_shape_depth)` if the old value is in screen
  coordinates.
- For true 3D shells, rebuild coordinates in `x/y/z` instead of using the old
  2D projection function.

## Trail And Draw-Order Risks

The old file stores and expands position sets; it does not encode current trail
policy. When adapting:

- Rockets should always trail.
- Only selected particles should trail.
- Trail eligibility should come from a `TrailPreset` or equivalent deterministic
  rule, not ad hoc per-particle randomness.
- Draw order must remain: rear box edges, particles/trails, front box edges.
- Dense ring, recursive, and sphere patterns may make the transparent cuboid hard
  to read unless particle count and trail rate are capped.

## Suggested Preset Candidates

These are conceptual targets, not implementation code.

### Classic Chrysanthemum

- Source idea: `radial_burst`
- Shape: evenly distributed spherical or near-spherical shell.
- Particle count: 96-128
- Speed range: medium
- Life range: 55-85
- Gravity: mild downward, negative in Firework Box `y`
- Trail: low to medium partial trail rate
- Notes: safest first preset after the prototype reconciliation task.

### Spiral Ring

- Source idea: `spiral_burst`, `ring_burst`, `ring_burst2`
- Shape: planar or shallow-depth spiral ring.
- Particle count: 96-160, capped by frame pacing
- Speed range: medium
- Life range: 60-90
- Trail: medium rate, biased toward faster particles
- Notes: strong match for the requested spiral direction.

### Layered Halo

- Source idea: `multi_ring_burst`, `halo_burst`
- Shape: two to four radius bands, slight radius variation.
- Particle count: 72-120
- Speed range: low to medium
- Life range: 70-100
- Trail: low rate
- Notes: good calm visual toy effect; likely works well in the transparent box.

### Willow

- Source idea: not directly present, but can reuse radial or fibonacci spacing.
- Shape: initial shell followed by downward-curving particles.
- Particle count: 80-128
- Speed range: medium initial, stronger drag
- Life range: 90-130
- Gravity: more visible negative `y`
- Trail: medium rate, longer selected trails
- Notes: should be implemented carefully after basic drag/gravity tuning.

### Planar Heart Or Star

- Source idea: `heart_shape`, `star_burst`
- Shape: fixed plane with slight `z` thickness.
- Particle count: 40-101
- Speed range: low or shape-locked
- Life range: 60-90
- Trail: very low rate
- Notes: novelty preset; should be delayed until planar-shape projection is
  intentionally supported.

### Geometric Cluster

- Source idea: `sierpinski_triangle_burst`, `magic_square_firework`
- Shape: recursive triangle or grid cluster.
- Particle count: capped under 128
- Speed range: low
- Life range: 50-80
- Trail: very low or none
- Notes: useful for experiments, but lower priority than classic fireworks.

## Recommended Implementation Order

1. Finish `T0002`: verify package imports, test tools, lint tools, and
   `check_all` behavior.
2. Finish `T0002.5`: inspect protected standalone `main.py`, list good-feeling
   behavior, and document migration strategy.
3. Extend preset design only after the reference prototype is reconciled.
4. Implement one safe preset first, preferably Classic Chrysanthemum or Layered
   Halo.
5. Add Spiral Ring once particle caps and partial trails are stable.
6. Add Willow after drag/gravity and selected trail behavior are explicit.
7. Delay planar novelty presets until camera/projection behavior is reviewed.

## Acceptance Notes

For this research task:

- `main.py` was not modified.
- `src/` was not modified.
- The external code was not copied into the package.
- Candidate firework types were listed.
- Coordinate-system, draw-order, and trail-density risks were recorded.
