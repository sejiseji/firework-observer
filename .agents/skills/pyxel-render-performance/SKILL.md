# Pyxel Render Performance Skill

Use this when changing particles, trails, camera projection, palette animation, or dense drawing.

## Budget-first checks

- What is the target resolution?
- How many objects are drawn per frame?
- Can computation be cached?
- Can trails be represented by sparse samples?
- Can a lookup table replace repeated math?
- Is visual smoothness more important than exact physical correctness?

## Validation

Run:

```bash
uv run pytest
uv run python scripts/capture_smoke.py
```

Record observations in `reports/performance/` if behavior changes.
