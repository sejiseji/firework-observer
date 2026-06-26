# Scenery Objects

## Purpose

Future scenery must be static, low-detail 3D line geometry inside the same observation box as the fireworks.

Scenery must not be drawn as a 2D screen-space background. It must rotate and project through the same `Camera3D` / projection pipeline as the box, rockets, and particles.

## Coordinate Convention

Scenery uses the same internal 3D coordinate convention as fireworks:

- `x`: horizontal
- `y`: up
- `z`: depth
- larger `y` means higher

Coordinates should be box-relative where practical so scenery scales across screen profiles.

## Visual Constraints

- Scenery must remain quieter than fireworks.
- Use dark, low-contrast Pyxel palette colors first.
- Prefer sparse line geometry over dense detail.
- Avoid filled polygons initially.
- Keep model definitions free of direct Pyxel calls.

## Future Scene Kinds

- `EMPTY`
- `MOUNTAINS`
- `CITY`
- `FOREST`
- `RIVERBANK`
- `MIXED`

## Future Primitive Candidates

- `Vec3`
- `Line3D`
- `Polyline3D`
- optional future `WireCuboid3D`

These primitives should be data-only model objects. Rendering code should project and draw them later.

## Preset Direction

### Mountains

- Low-detail polyline near the rear side of the box.
- Dark colors.
- Few points.
- Should read as distant structure, not as the main subject.

### City

- City is the primary scenery direction for the current preview.
- It should read as a small 3D urban kit on the floor of the observation box, not a flat skyline stuck to a side wall.
- Use low-detail wireframe cuboid buildings with varied widths, heights, and depths.
- Add sparse windows to visible building faces.
- A small subset of windows may be brighter to imply human presence.
- Keep building density and brightness sparse enough that fireworks remain readable.

### Forest

- Simple trunks and sparse branch lines.
- Dark, low-contrast lines.
- Avoid leaf clusters until the line budget is proven safe.

### Riverbank

- Floor-plane polylines near the bottom of the box.
- Possible future water or reflection expansion.
- No reflection implementation in the initial scenery tasks.

## Render Order

Recommended first implementation order:

1. Background
2. Rear box edges
3. Back scenery
4. Rockets and particles
5. Front scenery
6. Front box edges
7. UI

## Initial Depth Strategy

Use phase-based rendering first:

- back
- front

Do not implement full line-level depth sorting in the first scenery pass. Full sorting can be future work if phase-based rendering cannot preserve depth readability.

## Risks

- Scenery clutter can compete with fireworks.
- Bright scenery colors can reduce firework readability.
- Screen-space backgrounds would break camera rotation expectations.
- Too many line segments can make the box visually noisy.
- Direct Pyxel calls inside scenery model definitions would violate model/render separation.
- Wider screen profiles increase particle and line rendering cost.

## Future Task Boundary

`T0006.*` tasks should add scenery in stages:

- data scaffold first
- `EMPTY` and `MOUNTAINS`
- `CITY`
- `FOREST`
- `RIVERBANK`
- preset cycling UI

No scenery rendering should be implemented as part of the documentation task.

## Shared Box Geometry

Package-side box geometry now exists as `WireBox` in `src/pyxel_goal_game/wire_box.py`.
Future scenery presets should use the same `ScreenProfile` box dimensions and y-up coordinate convention rather than defining their own screen-space bounds.

## Implemented Preview Scaffold

`T0004.0` added a preview-first scenery scaffold:

- Data module: `src/pyxel_goal_game/scenery_presets.py`
- Preview integration: `tools/preview_firework_box.py`
- Controls:
  - `G`: cycle scenery preset
  - `B`: toggle scenery visibility

Implemented initial presets in `T0004.0`:

- `EMPTY`
- `MOUNTAINS`
- `CITY`
- `RIVERBANK`

The data module is Pyxel-independent. It generates static 3D line and polyline geometry from `ScreenProfile` box dimensions, using box-relative ratios converted into `Vec3` points.

The manual preview projects scenery through the same `Camera3D` pipeline as the box and firework particles. Scenery remains inside the observation box and is rendered as low-detail line geometry, not as a 2D screen-space background.

Current preview render order:

1. Background
2. Rear/far box edges
3. Back scenery
4. Rising firework shells and particles
5. Front scenery
6. Front/near box edges
7. HUD

This is still a preview/development layer. Production runtime scenery integration remains a later task.

## City-Focused Refinement

`T0004.1` refocused active preview scenery around `EMPTY` and `CITY`.

Active preview scenery cycle:

- `EMPTY`
- `CITY`

The previous `MOUNTAINS` and `RIVERBANK` data remain reference/dev candidates, but they are no longer the practical focus of preview cycling.

The current `CITY` preset is a low-detail 3D urban kit:

- Dense wireframe cuboid buildings
- Low-rise and mid-rise block variation
- Profile-scaled box-relative placement near the bottom of the observation volume
- Sparse front and side-face windows
- A small number of brighter lit windows
- Building-attached signs, projecting signs, and rooftop signs

The CITY direction is a dense cutaway urban mass, not a sparse set of isolated objects on the floor.

## City Grounding Rule

`T0004.1.1` adjusted the city cuboid layer so buildings read as rising from the cut floor plane instead of sitting on the floor as separate miniature boxes.

CITY building cuboids should:

- Omit the four bottom-face perimeter edges
- Keep the four vertical edges
- Keep the four top-face edges
- Keep sparse windows on visible faces
- Stay slightly smaller and lower than the initial `T0004.1` block sizes

This rule is intentional. Do not restore full 12-edge cuboids for CITY buildings unless a later task explicitly changes the city staging direction.

## City Landmark And Signage

`T0004.2` added a small set of CITY-only urban details:

- One low-detail 3D landmark tower inspired by Tokyo Tower
- A few utility poles
- Slightly sagging overhead wire polylines

These details are still preview scenery data, not production runtime scenery. They remain static `Vec3` line/polyline geometry inside the observation box.

The tower should stay below the main firework bloom region. Utility poles and wires should remain visually quiet and should not become a dense line network. Future city work should tune readability before adding more urban detail.

`T0004.2.1` revised the active CITY direction:

- Increased building density so the lower city footprint reads as a cutaway urban mass
- Enlarged and grounded the landmark tower by extending its legs to the floor baseline
- Removed active utility poles and overhead wires
- Added low-detail signage attached to buildings

Active CITY signage should remain simple geometry:

- Wall-mounted sign frames on visible building faces
- A few projecting side signs
- A few rooftop signs on short supports
- No dense text rendering
- No loud neon effects

The utility pole and wire idea is intentionally not part of the active CITY preset after `T0004.2.1`. The city should feel like a dense urban section cut out of the floor plane, with building mass and signs carrying the sense of human activity.

`T0004.2.3` extended the active CITY footprint and added a quiet leisure landmark:

- More small, medium, and modest mid-rise cuboid buildings spread toward the left, right, front, and rear lower floor area
- One low-detail ferris wheel placed off-center in the lower city region
- Ferris wheel geometry is static line data: rim segments, hub, spokes, and support legs
- Building bottom-face perimeter edges remain omitted
- Utility poles and overhead wires remain removed from active CITY

CITY should now read as a fuller cutaway urban stage across the lower footprint of the observation box. Preserve launch readability and upper bloom space: the city can occupy most of the bottom, but it must remain visually quieter than fireworks.

`T0004.2.5` tuned CITY layout readability:

- Buildings avoid a central x-axis corridor so the city reads as having a broad boulevard through the cutaway mass
- The broader lower-footprint coverage is preserved on both sides of the corridor
- The ferris wheel was enlarged and tuned to read more circular
- The ferris wheel remains grounded, static, subdued, and below the main firework bloom area
- Utility poles and overhead wires remain removed from active CITY

`T0004.2.8` added another CITY readability pass:

- Additional small and medium buildings fill sparse peripheral floor regions near the side edges
- The central boulevard remains open and launch readability remains protected
- The ferris wheel uses a more circular world-space rim while staying grounded and inside the box

Future CITY tuning should preserve the central boulevard unless a later task explicitly changes the stage layout.

## Interior Box Stars

`T0004.2.4` added a preview-only interior star ambience layer.

Stars are environmental points attached to the observation box interior, not fireworks, free-floating particles, or a 2D background. They should appear only on:

- The interior top face
- The upper bands of interior side faces

Stars should not appear on:

- The floor
- Lower side-wall bands
- Open central volume
- Exterior-facing box surfaces

Each star belongs to a box face and uses an interior-face visibility test. If the camera angle sees the exterior side of a face, that face's stars should not render. This is required so stars read as inside the observation box instead of painted on the outside.

`T0004.2.8` made only the top-face visibility threshold more permissive so ceiling stars stay visible at shallower angles when the ceiling is clearly visible. Side-face star visibility remains on the previous stricter threshold.

`T0004.2.8.1` relaxed the top-face threshold further so ceiling stars remain visible even when the eye line is closer to parallel with the ceiling plane. Side-face thresholds still remain unchanged.

The current preview toggle is:

- `T`: show/hide interior stars

Star generation and visibility helpers live in Pyxel-independent code. Preview rendering projects visible stars through `Camera3D`.

## Burst Glitter Residue

`T0004.2.8` added a preview-only glitter residue layer after burst spawn.

The residue is intentionally not part of pure firework generation. It is a small, short-lived visual polish layer in the preview renderer:

- A bounded number of tiny glitter points spawn near the burst center
- Glitter drifts lightly and expires quickly
- The effect is sparse and should not read as a second explosion
- Senrin uses minimal residue, and Senrin secondary bursts do not gain extra density

Future tuning should reduce residue count, lifetime, or brightness before changing core burst particle counts.
