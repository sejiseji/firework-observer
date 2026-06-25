from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Literal

from pyxel_goal_game.camera3d import Vec3
from pyxel_goal_game.screen_profiles import DEFAULT_SCREEN_PROFILE, ScreenProfile

SceneryPhase = Literal["back", "front"]


class SceneryKind(Enum):
    EMPTY = auto()
    MOUNTAINS = auto()
    CITY = auto()
    RIVERBANK = auto()


@dataclass(frozen=True)
class SceneryLine:
    start: Vec3
    end: Vec3
    color: int
    phase: SceneryPhase = "back"


@dataclass(frozen=True)
class SceneryPolyline:
    points: tuple[Vec3, ...]
    color: int
    phase: SceneryPhase = "back"


@dataclass(frozen=True)
class SceneryPreset:
    kind: SceneryKind
    label: str
    lines: tuple[SceneryLine, ...] = ()
    polylines: tuple[SceneryPolyline, ...] = ()

    @property
    def all_points(self) -> tuple[Vec3, ...]:
        line_points = tuple(
            point for line in self.lines for point in (line.start, line.end)
        )
        polyline_points = tuple(point for polyline in self.polylines for point in polyline.points)
        return line_points + polyline_points


SCENERY_PRESET_NAMES = ("empty", "mountains", "city", "riverbank")


def get_scenery_preset(
    name: str,
    profile: ScreenProfile = DEFAULT_SCREEN_PROFILE,
) -> SceneryPreset:
    if name == "empty":
        return empty_scenery()
    if name == "mountains":
        return mountain_scenery(profile)
    if name == "city":
        return city_scenery(profile)
    if name == "riverbank":
        return riverbank_scenery(profile)
    raise KeyError(name)


def empty_scenery() -> SceneryPreset:
    return SceneryPreset(kind=SceneryKind.EMPTY, label="Empty")


def mountain_scenery(profile: ScreenProfile) -> SceneryPreset:
    ridge = tuple(
        box_point(profile, x, y, 0.75)
        for x, y in (
            (-0.92, -0.78),
            (-0.66, -0.54),
            (-0.44, -0.72),
            (-0.10, -0.47),
            (0.18, -0.68),
            (0.54, -0.51),
            (0.92, -0.76),
        )
    )
    low_ridge = tuple(
        box_point(profile, x, y, 0.68)
        for x, y in (
            (-0.90, -0.83),
            (-0.58, -0.66),
            (-0.28, -0.80),
            (0.06, -0.63),
            (0.38, -0.77),
            (0.86, -0.68),
        )
    )
    return SceneryPreset(
        kind=SceneryKind.MOUNTAINS,
        label="Mountains",
        polylines=(
            SceneryPolyline(points=ridge, color=5),
            SceneryPolyline(points=low_ridge, color=1),
        ),
    )


def city_scenery(profile: ScreenProfile) -> SceneryPreset:
    buildings = (
        (-0.88, -0.74, 0.12),
        (-0.66, -0.62, 0.10),
        (-0.47, -0.78, 0.13),
        (-0.25, -0.58, 0.10),
        (-0.04, -0.70, 0.11),
        (0.18, -0.52, 0.12),
        (0.42, -0.74, 0.10),
        (0.63, -0.60, 0.13),
        (0.86, -0.76, 0.10),
    )
    lines: list[SceneryLine] = []
    base_y = -0.94
    z = 0.72
    for center_x, top_y, width in buildings:
        left = center_x - width / 2.0
        right = center_x + width / 2.0
        color = 5 if top_y < -0.65 else 1
        lines.extend(
            (
                SceneryLine(
                    box_point(profile, left, base_y, z),
                    box_point(profile, left, top_y, z),
                    color,
                ),
                SceneryLine(
                    box_point(profile, right, base_y, z),
                    box_point(profile, right, top_y, z),
                    color,
                ),
                SceneryLine(
                    box_point(profile, left, top_y, z),
                    box_point(profile, right, top_y, z),
                    color,
                ),
                SceneryLine(
                    box_point(profile, left, base_y, z),
                    box_point(profile, right, base_y, z),
                    1,
                ),
            )
        )
    return SceneryPreset(
        kind=SceneryKind.CITY,
        label="City",
        lines=tuple(lines),
    )


def riverbank_scenery(profile: ScreenProfile) -> SceneryPreset:
    left_bank = tuple(
        box_point(profile, x, -0.93, z)
        for x, z in (
            (-0.86, -0.52),
            (-0.60, -0.34),
            (-0.28, -0.18),
            (0.10, 0.02),
            (0.44, 0.28),
            (0.82, 0.54),
        )
    )
    right_bank = tuple(
        box_point(profile, x, -0.86, z)
        for x, z in (
            (-0.64, -0.64),
            (-0.36, -0.44),
            (-0.04, -0.22),
            (0.28, 0.02),
            (0.58, 0.22),
            (0.94, 0.42),
        )
    )
    far_bank = tuple(
        box_point(profile, x, -0.74, z)
        for x, z in (
            (-0.94, 0.58),
            (-0.56, 0.48),
            (-0.14, 0.54),
            (0.26, 0.46),
            (0.90, 0.62),
        )
    )
    return SceneryPreset(
        kind=SceneryKind.RIVERBANK,
        label="Riverbank",
        polylines=(
            SceneryPolyline(points=left_bank, color=5, phase="front"),
            SceneryPolyline(points=right_bank, color=1, phase="front"),
            SceneryPolyline(points=far_bank, color=12),
        ),
    )


def box_point(
    profile: ScreenProfile,
    x_ratio: float,
    y_ratio: float,
    z_ratio: float,
) -> Vec3:
    return Vec3(
        x=x_ratio * profile.box_width / 2.0,
        y=y_ratio * profile.box_height / 2.0,
        z=z_ratio * profile.box_depth / 2.0,
    )
