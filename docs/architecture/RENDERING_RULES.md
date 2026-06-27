# Rendering Rules

## Priorities

1. Stable frame pacing
2. Clear visual hierarchy
3. Small readable draw functions
4. Controlled use of particles/trails
5. Cheap approximations over expensive exactness

## Particle/trail guidance

- Store only the history needed for the visible effect.
- Cap particle counts.
- Use deterministic seeds for tests.
- Use simple projection math before complex 3D illusions.
- Prefer lookup tables when repeated trigonometry becomes hot.
