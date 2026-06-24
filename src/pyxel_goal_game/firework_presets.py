from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class FireworkKind(Enum):
    KIKU = auto()
    PEONY = auto()
    RING = auto()
    WILLOW = auto()
    SPIRAL = auto()
    MULTI_RING = auto()
    HALO = auto()
    SENRIN = auto()


class FireworkShape(Enum):
    SPHERE = auto()
    RING = auto()
    WILLOW = auto()
    SPIRAL = auto()
    MULTI_RING = auto()
    HALO = auto()
    SENRIN_SEED = auto()


@dataclass(frozen=True)
class TrailPreset:
    rate: float
    speed_threshold: float
    early_ratio: float
    strong_speed: float
    draw_every: int = 1

    def __post_init__(self) -> None:
        if self.draw_every < 1:
            msg = "draw_every must be at least 1"
            raise ValueError(msg)


@dataclass(frozen=True)
class SecondaryPreset:
    rate: float
    count_range: tuple[int, int]
    delay_range: tuple[int, int]
    speed_range: tuple[float, float]
    life_range: tuple[int, int]
    palette: tuple[int, ...]
    fade_mid: int
    fade_dark: int
    tip_color: int
    drag: float
    gravity: float
    trail: TrailPreset


@dataclass(frozen=True)
class FireworkPreset:
    kind: FireworkKind
    label: str
    shape: FireworkShape
    particle_count: int
    speed_range: tuple[float, float]
    life_range: tuple[int, int]
    palette: tuple[int, ...]
    fade_mid: int
    fade_dark: int
    tip_color: int
    drag: float
    gravity: float
    trail: TrailPreset
    secondary: SecondaryPreset | None = None


FUTURE_FIREWORK_KINDS = (
    FireworkKind.KIKU,
    FireworkKind.PEONY,
    FireworkKind.RING,
    FireworkKind.WILLOW,
    FireworkKind.SPIRAL,
    FireworkKind.MULTI_RING,
    FireworkKind.HALO,
    FireworkKind.SENRIN,
)
