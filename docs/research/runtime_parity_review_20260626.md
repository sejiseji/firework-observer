# Runtime Parity Review 2026-06-26

## Commands

Preview reference:

```bash
.venv/bin/python tools/preview_firework_box.py --profile iphone16_balanced
```

Official runtime:

```bash
.venv/bin/python scripts/run_runtime_app.py --profile iphone16_balanced
```

## Tested Profile

- `iphone16_balanced`
- screen: `236x512`
- box: `120x260x120`

## Review Result

Status: `PARITY OK`

- Official runtime launched successfully.
- No visual parity problems were found.
- No control problems were found.
- No stability problems were found.
- Preview remains available as the development harness.
- Official runtime is ready to become the default entry path.

## Checked Features

- Startup.
- Portrait `iphone16_balanced` profile.
- 3D observation box.
- CITY scenery.
- 48-building density.
- Central boulevard.
- Tower.
- Ferris wheel.
- Signs and windows.
- Interior stars.
- No exterior-facing stars.
- Auto rotate slow, normal, and fast modes.
- Pitch sway comfort.
- Single launch with `Z`.
- Firework kind cycle with `SPACE`.
- Random mode with `R`.
- Height variation with `H`.
- Fixed salvo modes with `1` through `5`.
- Random-count salvo with `0`.
- Shell tail.
- Glitter residue.
- All first-generation firework kinds:
  - Kiku
  - Ring
  - Spiral
  - Willow
  - Peony
  - Multi-ring
  - Senrin
  - Halo
- `R + H + 0` stress mode.

## Handoff Decision

Status: `READY`

`main.py` can become a thin launcher to the official runtime in a separate explicit task.

The next task is:

- `T0005.6`: Convert `main.py` to official runtime launcher.

## Guardrails For T0005.6

- Do not move runtime logic back into `main.py`.
- Keep `main.py` as a thin launcher only.
- Preserve `tools/preview_firework_box.py` as the development harness.
- Preserve package-side runtime ownership of app loop, input, render, effects, camera motion, state, and scheduling.
