from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FireworkPreset:
    name: str
    particle_count: int
    speed: float
    color: int
    trail_length: int


DEFAULT_FIREWORK_PRESET = FireworkPreset(
    name="sample-burst",
    particle_count=24,
    speed=1.2,
    color=10,
    trail_length=8,
)
