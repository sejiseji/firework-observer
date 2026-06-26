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


PEONY_TRAIL_PRESET = TrailPreset(
    rate=0.18,
    speed_threshold=1.10,
    early_ratio=0.32,
    strong_speed=1.30,
)

PEONY_PRESET = FireworkPreset(
    kind=FireworkKind.PEONY,
    label="Peony",
    shape=FireworkShape.SPHERE,
    particle_count=96,
    speed_range=(0.80, 1.35),
    life_range=(42, 68),
    palette=(14, 8, 10),
    fade_mid=8,
    fade_dark=2,
    tip_color=7,
    drag=0.982,
    gravity=-0.022,
    trail=PEONY_TRAIL_PRESET,
)


RING_TRAIL_PRESET = TrailPreset(
    rate=0.38,
    speed_threshold=0.90,
    early_ratio=0.46,
    strong_speed=1.25,
)

RING_PRESET = FireworkPreset(
    kind=FireworkKind.RING,
    label="Ring",
    shape=FireworkShape.RING,
    particle_count=104,
    speed_range=(1.05, 1.45),
    life_range=(58, 82),
    palette=(12, 6, 7),
    fade_mid=6,
    fade_dark=1,
    tip_color=7,
    drag=0.987,
    gravity=-0.018,
    trail=RING_TRAIL_PRESET,
)


MULTI_RING_TRAIL_PRESET = TrailPreset(
    rate=0.30,
    speed_threshold=0.85,
    early_ratio=0.44,
    strong_speed=1.25,
)

MULTI_RING_PRESET = FireworkPreset(
    kind=FireworkKind.MULTI_RING,
    label="Multi-ring",
    shape=FireworkShape.MULTI_RING,
    particle_count=120,
    speed_range=(0.85, 1.55),
    life_range=(58, 90),
    palette=(12, 6, 7, 10),
    fade_mid=6,
    fade_dark=1,
    tip_color=7,
    drag=0.987,
    gravity=-0.017,
    trail=MULTI_RING_TRAIL_PRESET,
)


HALO_TRAIL_PRESET = TrailPreset(
    rate=0.16,
    speed_threshold=0.70,
    early_ratio=0.35,
    strong_speed=1.05,
    draw_every=2,
)

HALO_PRESET = FireworkPreset(
    kind=FireworkKind.HALO,
    label="Halo",
    shape=FireworkShape.HALO,
    particle_count=96,
    speed_range=(0.70, 1.22),
    life_range=(64, 96),
    palette=(7, 10, 12),
    fade_mid=6,
    fade_dark=1,
    tip_color=7,
    drag=0.990,
    gravity=-0.012,
    trail=HALO_TRAIL_PRESET,
)


SPIRAL_TRAIL_PRESET = TrailPreset(
    rate=0.45,
    speed_threshold=0.70,
    early_ratio=0.55,
    strong_speed=1.10,
)

SPIRAL_PRESET = FireworkPreset(
    kind=FireworkKind.SPIRAL,
    label="Spiral",
    shape=FireworkShape.SPIRAL,
    particle_count=120,
    speed_range=(0.75, 1.35),
    life_range=(62, 94),
    palette=(11, 10, 7),
    fade_mid=3,
    fade_dark=1,
    tip_color=7,
    drag=0.986,
    gravity=-0.019,
    trail=SPIRAL_TRAIL_PRESET,
)


WILLOW_TRAIL_PRESET = TrailPreset(
    rate=0.68,
    speed_threshold=0.45,
    early_ratio=0.72,
    strong_speed=0.85,
)

WILLOW_PRESET = FireworkPreset(
    kind=FireworkKind.WILLOW,
    label="Willow",
    shape=FireworkShape.WILLOW,
    particle_count=88,
    speed_range=(0.55, 1.10),
    life_range=(85, 125),
    palette=(10, 9, 4),
    fade_mid=4,
    fade_dark=2,
    tip_color=10,
    drag=0.976,
    gravity=-0.040,
    trail=WILLOW_TRAIL_PRESET,
)


SENRIN_TRAIL_PRESET = TrailPreset(
    rate=0.26,
    speed_threshold=0.50,
    early_ratio=0.42,
    strong_speed=0.80,
)

SENRIN_SECONDARY_TRAIL_PRESET = TrailPreset(
    rate=0.06,
    speed_threshold=0.55,
    early_ratio=0.25,
    strong_speed=0.65,
    draw_every=2,
)

SENRIN_SECONDARY_PRESET = SecondaryPreset(
    rate=0.78,
    count_range=(8, 14),
    delay_range=(14, 28),
    speed_range=(0.28, 0.68),
    life_range=(28, 48),
    palette=(7, 10, 9, 14),
    fade_mid=9,
    fade_dark=2,
    tip_color=7,
    drag=0.982,
    gravity=-0.025,
    trail=SENRIN_SECONDARY_TRAIL_PRESET,
)

SENRIN_PRESET = FireworkPreset(
    kind=FireworkKind.SENRIN,
    label="Senrin",
    shape=FireworkShape.SENRIN_SEED,
    particle_count=42,
    speed_range=(0.55, 0.95),
    life_range=(32, 52),
    palette=(7, 10, 14),
    fade_mid=10,
    fade_dark=5,
    tip_color=7,
    drag=0.990,
    gravity=-0.012,
    trail=SENRIN_TRAIL_PRESET,
    secondary=SENRIN_SECONDARY_PRESET,
)
