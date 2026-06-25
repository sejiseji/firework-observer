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


SCENERY_PRESET_NAMES = ("empty", "city")


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
        (-0.70, 0.34, 0.14, 0.16, 0.20),
        (-0.49, 0.18, 0.13, 0.15, 0.28),
        (-0.25, 0.44, 0.16, 0.18, 0.18),
        (0.00, 0.26, 0.14, 0.17, 0.33),
        (0.28, 0.09, 0.17, 0.18, 0.23),
        (0.57, 0.33, 0.18, 0.15, 0.19),
    )
    lines: list[SceneryLine] = []
    base_y = -0.96
    for index, (center_x, center_z, width, depth, height) in enumerate(buildings):
        top_y = base_y + height
        color = 5 if height < 0.30 else 1
        lines.extend(
            building_cuboid_lines(
                profile=profile,
                center_x=center_x,
                center_z=center_z,
                width=width,
                depth=depth,
                base_y=base_y,
                top_y=top_y,
                color=color,
            )
        )
        lines.extend(
            building_window_lines(
                profile=profile,
                building_index=index,
                center_x=center_x,
                center_z=center_z,
                width=width,
                depth=depth,
                base_y=base_y,
                top_y=top_y,
            )
        )
    return SceneryPreset(
        kind=SceneryKind.CITY,
        label="City",
        lines=tuple(lines),
    )


def building_cuboid_lines(
    *,
    profile: ScreenProfile,
    center_x: float,
    center_z: float,
    width: float,
    depth: float,
    base_y: float,
    top_y: float,
    color: int,
) -> tuple[SceneryLine, ...]:
    left = center_x - width / 2.0
    right = center_x + width / 2.0
    rear = center_z - depth / 2.0
    front = center_z + depth / 2.0
    vertices = (
        box_point(profile, left, base_y, rear),
        box_point(profile, right, base_y, rear),
        box_point(profile, right, top_y, rear),
        box_point(profile, left, top_y, rear),
        box_point(profile, left, base_y, front),
        box_point(profile, right, base_y, front),
        box_point(profile, right, top_y, front),
        box_point(profile, left, top_y, front),
    )
    edges = (
        (0, 3),
        (1, 2),
        (4, 7),
        (5, 6),
        (2, 3),
        (3, 7),
        (6, 7),
        (2, 6),
    )
    return tuple(SceneryLine(vertices[start], vertices[end], color) for start, end in edges)


def building_window_lines(
    *,
    profile: ScreenProfile,
    building_index: int,
    center_x: float,
    center_z: float,
    width: float,
    depth: float,
    base_y: float,
    top_y: float,
) -> tuple[SceneryLine, ...]:
    lines: list[SceneryLine] = []
    left = center_x - width / 2.0
    right = center_x + width / 2.0
    front = center_z + depth / 2.0
    rear = center_z - depth / 2.0
    row_count = max(1, int((top_y - base_y) / 0.08))
    column_count = 2 if width < 0.18 else 3
    for row in range(row_count):
        y = base_y + 0.07 + row * 0.075
        if y >= top_y - 0.03:
            continue
        for column in range(column_count):
            x = left + (column + 1) * width / (column_count + 1)
            color = lit_window_color(building_index, row, column)
            half_window = width * 0.065
            lines.append(
                SceneryLine(
                    box_point(profile, x - half_window, y, front),
                    box_point(profile, x + half_window, y, front),
                    color,
                )
            )
            if column == column_count - 1 and row % 2 == 0:
                side_z = rear + depth * 0.35
                lines.append(
                    SceneryLine(
                        box_point(profile, right, y, side_z - depth * 0.06),
                        box_point(profile, right, y, side_z + depth * 0.06),
                        5,
                    )
                )
    return tuple(lines)


def lit_window_color(building_index: int, row: int, column: int) -> int:
    if (building_index * 5 + row * 3 + column) % 11 == 0:
        return 7
    if (building_index * 7 + row + column * 2) % 5 == 0:
        return 10
    return 1


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
