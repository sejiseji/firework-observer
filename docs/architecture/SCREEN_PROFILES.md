# Screen Profiles

## Purpose

Firework Observer should support larger landscape screen profiles without losing the protected classic prototype feel.

Screen size affects the observation box, camera projection, UI placement, max particle count, scenery proportions, and render cost. These values must be treated as profile-dependent rather than scattered constants.

## Resolution Policy

- Preserve the existing `256x144` classic profile as the baseline.
- Prefer a balanced iPhone16-landscape-like internal profile of `512x236`.
- Keep `852x393` as an optional larger profile.
- Do not use native `2556x1179` as the default Pyxel internal resolution.
- Treat Pyxel internal resolution and display scale as separate concerns.

The internal Pyxel resolution defines simulation-to-screen composition and drawing cost. Display scaling can enlarge the window or browser canvas without requiring native phone-pixel rendering.

## Initial Profiles

| Profile | Screen | Box | Focal | Camera Distance | Max Particles |
| --- | --- | --- | --- | --- | --- |
| `classic` | `256x144` | `120x80x120` | `180.0` | `180.0` | `400` |
| `iphone16_balanced` | `512x236` | `220x120x220` | `260.0` | `300.0` | `600` |
| `iphone16_large` | `852x393` | `360x190x360` | `430.0` | `500.0` | `900` |

These values are starting points for visual tuning, not final proof that every effect reads well.

## Profile-Dependent Values

The following must become profile-dependent before larger-screen gameplay tuning:

- screen width and height
- observation box width, height, and depth
- camera focal length
- camera distance
- UI anchor positions and spacing
- max particle count
- scenery coordinate scale
- trail density and particle budget, if larger profiles become too busy or too expensive

## Coordinate Strategy

Use box-relative or normalized coordinates for generated visuals.

Examples:

```python
x = box.w * ratio_x
y = box.h * ratio_y
z = box.d * ratio_z
```

Avoid hard-coded coordinates that only look correct in `256x144`.

This applies to fireworks, scenery, and any future visual guide lines inside the observation box.

## Risks

- Wider profiles increase particle and line rendering cost.
- Larger profiles may require max particle and trail-density tuning.
- UI tied to `256x144` positions will look cramped or misplaced in larger profiles.
- Box dimensions and camera values tuned independently can break the feeling that fireworks are inside the box.
- Native phone-pixel internal rendering would be expensive and inconsistent with Pyxel-style pixel composition.

## Future Task Boundary

`T0002.8` should introduce a screen profile configuration scaffold while preserving the classic behavior. It should not add scenery rendering or new firework presets.

## Implementation Status

`T0002.8` added the package-side scaffold in `src/pyxel_goal_game/screen_profiles.py`.

- `ScreenProfile` is an immutable dataclass.
- `classic` is the default profile.
- `iphone16_balanced` and `iphone16_large` exist as selectable data.
- `GameSettings` now holds a profile and exposes width and height from that profile.
- `ObserverScene` uses profile width, height, and max particle count.
- HUD bottom text anchors to the active profile height instead of the old fixed `120px` template coordinate.
- `Camera3D.from_profile()` can now read profile width, height, focal length, and camera distance for pure projection tests.
- `WireBox.from_profile()` can now read profile box width, height, and depth for pure geometry tests.

This task did not implement scenery rendering, new firework presets, or `main.py` migration.
