# ADR 0003: Deterministic Simulation First

## Status

Accepted

## Context

Particles and effects can become hard to test if they rely on uncontrolled randomness.

## Decision

Use deterministic seeds or explicit random sources for simulation logic when practical.

## Consequences

- Visual behavior can be replayed.
- Tests can verify lifecycle behavior.
- Final visuals may still include controlled randomness.
