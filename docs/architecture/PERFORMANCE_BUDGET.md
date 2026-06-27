# Performance Budget

## Initial target

- Pyxel default-friendly resolution
- stable interactive frame rate
- particle counts capped by design
- no unbounded trail history

## Default budgets

These are starting points, not permanent limits.

- active particles: 256
- trail samples per particle: 8
- expensive math in inner loops: avoid unless measured
- allocations per frame: keep low

## When performance drops

Prefer this order:

1. cap counts,
2. reduce history,
3. cache or precompute,
4. simplify visuals,
5. only then restructure architecture.
