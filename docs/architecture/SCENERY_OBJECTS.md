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

- Skyline made from coarse vertical and horizontal line segments.
- No filled polygons initially.
- Keep building density sparse enough that fireworks remain readable.

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
