# Prototype Reconciliation

## Purpose

The standalone `main.py` is the protected reference prototype for the current Firework Observer feel.

This document records what must be preserved before package-side gameplay migration. It is intentionally documentation-only: no prototype code, package gameplay code, screen profile implementation, scenery rendering, or firework preset implementation is changed by T0002.5.

## Reference Prototype Inventory

### File Structure

`main.py` contains these top-level pieces:

- constants: `WIDTH`, `HEIGHT`, `FPS`, `BOX_W`, `BOX_H`, `BOX_D`, `MAX_PARTICLES`
- `ProjectedPoint`
- `Camera3D`
- `FireworkBox`
- `Rocket`
- `Particle`
- `FireworkSystem`
- `App`
- helpers: `clamp`, `random_sphere_velocity`, `draw_background`

### Screen And Box

- Screen: `256x144`
- FPS: `60`
- Box dimensions: `120.0 x 80.0 x 120.0`
- Max particles: `400`
- Internal coordinate convention:
  - `x`: horizontal
  - `y`: up
  - `z`: depth
  - larger `y` means higher

### Camera3D

Defaults:

- `yaw = 0.6`
- `pitch = 0.3`
- `zoom = 1.0`
- `target_yaw = 0.6`
- `target_pitch = 0.3`
- `target_zoom = 1.0`
- `focal = 180.0`
- `camera_distance = 180.0`

Input response:

- left/right adjust target yaw by `0.035`
- up/down adjust target pitch by `0.025`
- `A` zooms in by `0.018`
- `S` zooms out by `0.018`
- `C` resets target yaw, pitch, and zoom to defaults
- `Q` quits

Clamps:

- target pitch: `-1.05` to `1.05`
- target zoom: `0.62` to `1.8`

Smoothing:

- yaw approaches target at `0.12`
- pitch approaches target at `0.12`
- zoom approaches target at `0.10`

Projection:

- Rotate around Y first, then X.
- Clamp projected depth with `max(1.0, rz2 + camera_distance)`.
- Scale uses `focal / depth * zoom`.
- Screen projection uses `sx = WIDTH // 2 + rx * scale`.
- Screen projection uses `sy = HEIGHT // 2 - ry * scale`.
- Drawing uses rounded projected integer coordinates through `ProjectedPoint.sx` and `ProjectedPoint.sy`.

### Box Rendering

The box is an 8-vertex, 12-edge wire cuboid:

- vertices are generated from half dimensions of the box
- no filled faces
- edge depth is the average projected depth of the two endpoints
- edges are sorted far to near
- `front` filtering lets draw calls render rear and front passes separately

Edge classification:

- `near = min(edge_depths)`
- `far = max(edge_depths)`
- `span = max(1.0, far - near)`
- front edge threshold: `depth < near + span * 0.42`

Colors:

- front edges: `13`
- rear edges: `5`
- far rear helper edges: `1` when `depth > near + span * 0.78`

### Rocket Behavior

Launch:

- `x = random.uniform(-25.0, 25.0)`
- `y = -BOX_H / 2`
- `z = random.uniform(-25.0, 25.0)`
- `vx = random.uniform(-0.045, 0.045)`
- `vy = random.uniform(1.25, 1.55)`
- `vz = random.uniform(-0.045, 0.045)`
- `target_y = random.uniform(5.0, BOX_H / 2 - 10.0)`

Update:

- previous position is stored every frame
- position adds velocity
- gravity-like deceleration subtracts `0.018` from `vy`
- explosion happens when `vy <= 0.0` or `y >= target_y`

Draw:

- rockets always trail from previous projected position to current projected position
- trail color: `9`
- tip color: `7`

### Particle Behavior

Particle state includes:

- current and previous 3D position
- 3D velocity
- `life` and `max_life`
- color, fade mid, fade dark, tip color
- drag and gravity
- partial trail settings
- projected depth

Update:

- previous position is stored before motion
- position adds velocity
- `vx *= drag`
- `vy = vy * drag + gravity`
- `vz *= drag`
- `life -= 1`
- dead when `life <= 0`

For the current kiku burst:

- particle count: `112`
- speed range: `0.90` to `1.65`
- life range: `55` to `85`
- palette: `10`, `9`, `7`
- fade mid: `9`
- fade dark: `2`
- tip color: `7`
- drag: `0.985`
- gravity: `-0.025`
- trail rate: `0.32`
- trail speed threshold: `1.05`
- trail early ratio: `0.48`
- strong trail speed threshold: `1.45`
- trail draw interval: every frame

Partial trail condition:

- `has_trail = speed >= 1.05 and random.random() < 0.32`
- draw trail only while `age < int(life * 0.48)`
- draw trail only when `pyxel.frame_count % trail_draw_every == 0`
- particles without active trails use `pset`
- strong trails add a bright tip when `trail_strength >= 2`

Color fade:

- `life / max_life > 0.55`: primary color
- `life / max_life > 0.25`: fade mid
- otherwise: fade dark

### Burst Shape

The current kiku burst uses spherical velocity generation:

- `theta = random.uniform(0.0, math.tau)`
- `u = random.uniform(-1.0, 1.0)`
- `r = sqrt(max(0.0, 1.0 - u * u))`
- `vx = cos(theta) * r * speed`
- `vy = u * speed`
- `vz = sin(theta) * r * speed`

### Render Order

The protected prototype renders in this order:

1. clear background
2. simple dark background horizon line at `HEIGHT // 2 + 30`, color `1`
3. rear box edges
4. rockets
5. depth-sorted particles
6. front box edges
7. UI

Future scenery should fit into the already documented order:

1. background
2. rear box edges
3. back scenery
4. rockets and particles
5. front scenery
6. front box edges
7. UI

### UI

UI is intentionally small and dim:

- `(4, 4)`: `Z:launch Kiku  ARROWS:rotate`
- `(4, 12)`: `A/S:zoom C:reset`
- `(4, HEIGHT - 8)`: particle and rocket counts
- UI color: `5`

## Package Architecture Comparison

The current package under `src/pyxel_goal_game/` is still a 2D template implementation:

- screen constants are `160x120`, not `256x144`
- `model.camera.Camera` has only `angle` and `distance`
- `model.particle.Particle` is 2D and stores `x`, `y`, `vx`, `vy`
- `systems.particle_system.ParticleSystem` creates 2D radial bursts
- 2D gravity currently increases `vy`
- renderer draws 2D particle trails for every particle with enough trail points
- input maps arrow keys to focus movement and space to trigger
- `ObserverScene` moves a 2D focus point and spawns bursts there

Closest package-side homes for prototype concepts:

| Prototype concept | Package-side destination |
| --- | --- |
| `Camera3D` | `model.camera`, `systems.camera_system`, `render.projection` |
| `ProjectedPoint` | `render.projection` or a render model module |
| `FireworkBox` geometry | model/render split, likely `model.world` plus `render.primitive_drawer` |
| `Rocket` | `model.firework` or a new model module |
| `Particle` 3D state | `model.particle` after a staged 2D-to-3D migration |
| `FireworkSystem` | `systems.firework_system` and `systems.particle_system` |
| input mapping | `input.controls` |
| render order | `scenes.observer` and render modules |
| UI | `render.hud_renderer` |

## What Must Remain Prototype-Only For Now

- `main.py` remains a reference-only prototype until an explicit migration task.
- The package should not directly import or execute code from `main.py`.
- The package should not be mass-rewritten to match `main.py` in one patch.
- The external `Firework.py` remains reference material only and must not be copied.

## Behavior That Must Be Preserved

Preserve these exactly or with explicitly documented tuning deltas:

- classic `256x144` profile availability
- `120x80x120` classic box proportions
- y-up 3D coordinates
- negative gravity for firework particles
- Camera3D default yaw/pitch/zoom and smoothing feel
- `focal = 180.0` and `camera_distance = 180.0` for the classic profile until deliberately retuned
- target-based camera input rather than direct physical coordinate rotation
- particle coordinates remain unchanged by camera input
- rear-box / particles / front-box render readability
- rockets always use trails
- particles use partial trails, not all-particle trails
- kiku burst density, speed, life, drag, gravity, and color fade as reference tuning
- max particle cap behavior
- dim, minimal UI

## Migration Strategy

1. Keep `main.py` protected and reference-only.
2. Add screen profile configuration scaffold first if continuing the current roadmap; preserve the classic profile.
3. Migrate Camera3D and projection behavior into package-side model/system/render boundaries.
4. Add package-side wire box geometry and rear/front render passes.
5. Add 3D rocket and particle model fields without changing firework preset breadth.
6. Preserve rocket launch and kiku burst behavior as the first package-side visual target.
7. Preserve partial trail behavior before adding more presets.
8. Introduce or refine `FireworkPreset`, `TrailPreset`, and later `SecondaryPreset` only after the protected behavior is mapped.
9. Add future scenery only as quiet 3D line geometry inside the box, never as screen-space background.

## Risks

- Reimplementing the prototype from scratch can easily lose the camera smoothing and depth readability.
- Migrating all systems in one patch would mix camera, box, particle physics, trails, and presets, making visual regressions hard to isolate.
- The current package has 2D gravity and screen-space particles; blindly extending it could invert y-up assumptions.
- Drawing all particle trails in the package would violate the prototype's partial trail philosophy.
- Adding screen profiles before preserving the classic profile would remove the main comparison baseline.
- Adding scenery as a 2D background would break the rotation expectation documented in the screen/scenery architecture.

## Suggested Follow-Up Tasks

- `T0002.8`: Add screen profile configuration scaffold while preserving `classic`.
- `T0002.9`: Add package-side Camera3D and projection scaffold with tests, no visible gameplay migration.
- `T0002.10`: Add package-side wire box model/render scaffold for the classic profile.
- `T0003.0`: Establish firework preset scaffold after profile/projection prerequisites are stable.
- `T0003.1`: Recreate kiku/radial behavior using the protected prototype values.

## Package Scaffold Status

`T0002.9` added `src/pyxel_goal_game/camera3d.py` as a Pyxel-independent projection scaffold.

- `Vec3` represents y-up 3D points.
- `ProjectedPoint` preserves float projection values and rounded `sx` / `sy` draw coordinates.
- `Camera3D.from_profile()` reads screen width, height, focal length, and camera distance from `ScreenProfile`.
- `Camera3D.transform()` follows the protected prototype yaw-then-pitch formula.
- `Camera3D.project()` follows the protected prototype perspective projection and depth guard.
- `Camera3D.step_toward_target()` preserves the prototype smoothing coefficients without binding keyboard input.

This scaffold is not yet wired into Pyxel rendering, box drawing, particles, rockets, or scenery.

`T0002.10` added `src/pyxel_goal_game/wire_box.py` as a Pyxel-independent observation box geometry scaffold.

- `WireBox.from_profile()` reads box dimensions from `ScreenProfile`.
- The generated box has 8 vertices centered on the origin and 12 edge index pairs.
- Edge groups record prototype-compatible initial geometry groups: `rear`, `front`, and `connector`.
- `WireBox.project_edges()` projects edges through `Camera3D` and records average depth for future render ordering.

This scaffold is not yet wired into Pyxel rendering and does not implement full renderer-level depth sorting.

`T0003.0` added `src/pyxel_goal_game/firework_presets.py` as a Pyxel-independent firework preset scaffold.

- `FireworkKind` and `FireworkShape` define staged preset identifiers.
- `TrailPreset`, `SecondaryPreset`, and `FireworkPreset` represent future preset data.
- Downward gravity remains negative in the data model.
- Partial trail policy is represented by `TrailPreset`.

This scaffold is not yet wired into runtime particles, rockets, rendering, or preset cycling.

`T0003.1` added deterministic Kiku/radial burst generation in `src/pyxel_goal_game/firework_bursts.py`.

- `KIKU_PRESET` stores the protected prototype Kiku values.
- `ParticleSpawnSpec` represents initial particle data without runtime mutation.
- `generate_kiku_burst()` generates a 3D spherical velocity distribution from a seed.
- Trail eligibility is deterministic and partial, using `TrailPreset`.

This generator is not yet wired into runtime particles, rockets, rendering, or preset cycling.

`T0003.2` added deterministic Ring burst generation in `src/pyxel_goal_game/firework_bursts.py`.

- `RING_PRESET` stores the documented ring values.
- `generate_ring_burst()` produces ring-plane initial velocity specs with small deterministic `z` thickness.
- `generate_burst()` now supports `FireworkShape.SPHERE` and `FireworkShape.RING`.

This generator is not yet wired into runtime particles, rockets, rendering, or preset cycling.

`T0003.7` added deterministic Senrin seed and secondary burst specification support in `src/pyxel_goal_game/firework_bursts.py`.

- `SENRIN_PRESET` stores primary seed values and references `SENRIN_SECONDARY_PRESET`.
- `ParticleSpawnSpec.secondary_burst` is optional and remains `None` for non-secondary presets.
- `SecondaryBurstSpec` records deterministic delayed secondary burst data without introducing production runtime particle execution.
- `generate_secondary_burst()` can turn a secondary spec into deterministic secondary `ParticleSpawnSpec` values for preview-only inspection.

This representation should guide future runtime migration: production particles may execute optional secondary burst specs later, but `main.py` and current package runtime behavior remain protected until an explicit migration task.
