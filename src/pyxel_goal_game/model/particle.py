from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Particle:
    x: float
    y: float
    vx: float
    vy: float
    life: int
    color: int = 10
    trail: list[tuple[float, float]] = field(default_factory=list)

    @property
    def alive(self) -> bool:
        return self.life > 0
