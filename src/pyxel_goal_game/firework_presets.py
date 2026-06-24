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


KIKU_TRAIL_PRESET = TrailPreset(
    rate=0.32,
    speed_threshold=1.05,
    early_ratio=0.48,
    strong_speed=1.45,
)

KIKU_PRESET = FireworkPreset(
    kind=FireworkKind.KIKU,
    label="Kiku",
    shape=FireworkShape.SPHERE,
    particle_count=112,
    speed_range=(0.90, 1.65),
    life_range=(55, 85),
    palette=(10, 9, 7),
    fade_mid=9,
    fade_dark=2,
    tip_color=7,
    drag=0.985,
    gravity=-0.025,
    trail=KIKU_TRAIL_PRESET,
)
