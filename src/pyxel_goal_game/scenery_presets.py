from __future__ import annotations

import math
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
        (-0.88, -0.46, 0.10, 0.12, 0.13),
        (-0.82, 0.40, 0.12, 0.15, 0.18),
        (-0.74, -0.30, 0.12, 0.13, 0.17),
        (-0.66, 0.18, 0.14, 0.18, 0.23),
        (-0.61, 0.66, 0.12, 0.13, 0.14),
        (-0.52, 0.44, 0.12, 0.16, 0.16),
        (-0.38, 0.02, 0.13, 0.16, 0.27),
        (-0.34, -0.42, 0.12, 0.13, 0.19),
        (-0.23, 0.30, 0.15, 0.18, 0.21),
        (-0.08, 0.08, 0.12, 0.14, 0.30),
        (-0.04, 0.62, 0.12, 0.13, 0.15),
        (0.04, -0.48, 0.11, 0.12, 0.14),
        (0.08, 0.40, 0.14, 0.16, 0.17),
        (0.22, 0.18, 0.15, 0.18, 0.25),
        (0.26, 0.68, 0.11, 0.12, 0.16),
        (0.39, 0.42, 0.13, 0.16, 0.20),
        (0.44, -0.42, 0.12, 0.13, 0.17),
        (0.50, 0.05, 0.16, 0.17, 0.24),
        (0.67, 0.28, 0.13, 0.15, 0.19),
        (0.70, 0.68, 0.12, 0.13, 0.14),
        (0.78, -0.30, 0.12, 0.13, 0.16),
        (0.88, 0.08, 0.10, 0.12, 0.13),
        (-0.72, -0.08, 0.11, 0.13, 0.15),
        (-0.55, -0.22, 0.14, 0.14, 0.18),
        (-0.16, -0.18, 0.13, 0.15, 0.16),
        (0.10, -0.14, 0.14, 0.15, 0.20),
        (0.32, -0.22, 0.12, 0.13, 0.15),
        (0.58, -0.12, 0.11, 0.12, 0.14),
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
    lines.extend(city_sign_lines(profile=profile, buildings=buildings, base_y=base_y))
    lines.extend(landmark_tower_lines(profile=profile, base_y=base_y))
    lines.extend(ferris_wheel_lines(profile=profile, base_y=base_y))
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


def city_sign_lines(
    *,
    profile: ScreenProfile,
    buildings: tuple[tuple[float, float, float, float, float], ...],
    base_y: float,
) -> tuple[SceneryLine, ...]:
    lines: list[SceneryLine] = []
    for building_index in (1, 4, 7, 10, 18, 22):
        lines.extend(
            wall_sign_lines(
                profile=profile,
                building=buildings[building_index],
                base_y=base_y,
                color=12 if building_index in (4, 10, 18) else 5,
            )
        )
    for building_index in (5, 9, 13, 20):
        lines.extend(
            projecting_sign_lines(
                profile=profile,
                building=buildings[building_index],
                base_y=base_y,
                color=10 if building_index in (9, 20) else 5,
            )
        )
    for building_index in (2, 8, 14, 24):
        lines.extend(
            rooftop_sign_lines(
                profile=profile,
                building=buildings[building_index],
                base_y=base_y,
                color=12 if building_index in (8, 24) else 5,
            )
        )
    return tuple(lines)


def wall_sign_lines(
    *,
    profile: ScreenProfile,
    building: tuple[float, float, float, float, float],
    base_y: float,
    color: int,
) -> tuple[SceneryLine, ...]:
    center_x, center_z, width, depth, height = building
    sign_width = width * 0.45
    sign_height = min(0.045, height * 0.24)
    y_mid = base_y + height * 0.58
    z = center_z + depth / 2.0 + 0.002
    x_left = center_x - sign_width / 2.0
    x_right = center_x + sign_width / 2.0
    y_bottom = y_mid - sign_height / 2.0
    y_top = y_mid + sign_height / 2.0
    corners = (
        box_point(profile, x_left, y_bottom, z),
        box_point(profile, x_right, y_bottom, z),
        box_point(profile, x_right, y_top, z),
        box_point(profile, x_left, y_top, z),
    )
    return rectangle_lines(corners, color)


def projecting_sign_lines(
    *,
    profile: ScreenProfile,
    building: tuple[float, float, float, float, float],
    base_y: float,
    color: int,
) -> tuple[SceneryLine, ...]:
    center_x, center_z, width, depth, height = building
    x = center_x + width / 2.0
    z_wall = center_z + depth * 0.18
    z_outer = z_wall + depth * 0.42
    y_bottom = base_y + height * 0.44
    y_top = y_bottom + min(0.055, height * 0.28)
    support = SceneryLine(
        box_point(profile, x, (y_bottom + y_top) / 2.0, z_wall),
        box_point(profile, x, (y_bottom + y_top) / 2.0, z_outer),
        5,
    )
    sign = rectangle_lines(
        (
            box_point(profile, x, y_bottom, z_outer),
            box_point(profile, x, y_top, z_outer),
            box_point(profile, x + width * 0.22, y_top, z_outer),
            box_point(profile, x + width * 0.22, y_bottom, z_outer),
        ),
        color,
    )
    return (support, *sign)


def rooftop_sign_lines(
    *,
    profile: ScreenProfile,
    building: tuple[float, float, float, float, float],
    base_y: float,
    color: int,
) -> tuple[SceneryLine, ...]:
    center_x, center_z, width, depth, height = building
    top_y = base_y + height
    sign_bottom = top_y + 0.012
    sign_top = min(-0.39, sign_bottom + 0.045)
    sign_width = width * 0.54
    z = center_z + depth * 0.18
    x_left = center_x - sign_width / 2.0
    x_right = center_x + sign_width / 2.0
    support_left_x = center_x - sign_width * 0.28
    support_right_x = center_x + sign_width * 0.28
    supports = (
        SceneryLine(
            box_point(profile, support_left_x, top_y, z),
            box_point(profile, support_left_x, sign_bottom, z),
            5,
        ),
        SceneryLine(
            box_point(profile, support_right_x, top_y, z),
            box_point(profile, support_right_x, sign_bottom, z),
            5,
        ),
    )
    sign = rectangle_lines(
        (
            box_point(profile, x_left, sign_bottom, z),
            box_point(profile, x_right, sign_bottom, z),
            box_point(profile, x_right, sign_top, z),
            box_point(profile, x_left, sign_top, z),
        ),
        color,
    )
    return (*supports, *sign)


def rectangle_lines(
    corners: tuple[Vec3, Vec3, Vec3, Vec3],
    color: int,
) -> tuple[SceneryLine, ...]:
    return tuple(
        SceneryLine(corners[index], corners[(index + 1) % 4], color)
        for index in range(4)
    )


def landmark_tower_lines(
    *,
    profile: ScreenProfile,
    base_y: float,
) -> tuple[SceneryLine, ...]:
    base = base_y
    lower_deck = -0.70
    deck = -0.58
    top = -0.46
    antenna = -0.38
    center_x = 0.76
    center_z = -0.03
    base_half_width = 0.135
    lower_deck_half_width = 0.080
    deck_half_width = 0.055
    top_half_width = 0.022
    depth = 0.105

    base_points = (
        box_point(profile, center_x - base_half_width, base, center_z - depth),
        box_point(profile, center_x + base_half_width, base, center_z - depth),
        box_point(profile, center_x + base_half_width, base, center_z + depth),
        box_point(profile, center_x - base_half_width, base, center_z + depth),
    )
    deck_points = (
        box_point(profile, center_x - deck_half_width, deck, center_z - depth * 0.55),
        box_point(profile, center_x + deck_half_width, deck, center_z - depth * 0.55),
        box_point(profile, center_x + deck_half_width, deck, center_z + depth * 0.55),
        box_point(profile, center_x - deck_half_width, deck, center_z + depth * 0.55),
    )
    lower_deck_points = (
        box_point(
            profile,
            center_x - lower_deck_half_width,
            lower_deck,
            center_z - depth * 0.72,
        ),
        box_point(
            profile,
            center_x + lower_deck_half_width,
            lower_deck,
            center_z - depth * 0.72,
        ),
        box_point(
            profile,
            center_x + lower_deck_half_width,
            lower_deck,
            center_z + depth * 0.72,
        ),
        box_point(
            profile,
            center_x - lower_deck_half_width,
            lower_deck,
            center_z + depth * 0.72,
        ),
    )
    top_points = (
        box_point(profile, center_x - top_half_width, top, center_z - depth * 0.20),
        box_point(profile, center_x + top_half_width, top, center_z - depth * 0.20),
        box_point(profile, center_x + top_half_width, top, center_z + depth * 0.20),
        box_point(profile, center_x - top_half_width, top, center_z + depth * 0.20),
    )
    center_deck = box_point(profile, center_x, deck, center_z)
    center_top = box_point(profile, center_x, top, center_z)
    antenna_top = box_point(profile, center_x, antenna, center_z)

    lines: list[SceneryLine] = []
    for index in range(4):
        lines.append(SceneryLine(base_points[index], lower_deck_points[index], 5))
        lines.append(SceneryLine(lower_deck_points[index], deck_points[index], 5))
        lines.append(SceneryLine(deck_points[index], top_points[index], 5))
        lines.append(SceneryLine(base_points[index], lower_deck_points[(index + 1) % 4], 1))
        lines.append(SceneryLine(lower_deck_points[index], deck_points[(index + 1) % 4], 1))
    for ring in (lower_deck_points, deck_points, top_points):
        for index in range(4):
            lines.append(SceneryLine(ring[index], ring[(index + 1) % 4], 5))
    lines.append(SceneryLine(center_deck, center_top, 5))
    lines.append(SceneryLine(center_top, antenna_top, 10))
    return tuple(lines)


def ferris_wheel_lines(
    *,
    profile: ScreenProfile,
    base_y: float,
) -> tuple[SceneryLine, ...]:
    center_x = -0.72
    center_y = -0.72
    center_z = -0.55
    radius = 0.13
    rim_segments = 12
    rim_points = tuple(
        box_point(
            profile,
            center_x + math.cos(index / rim_segments * math.tau) * radius,
            center_y + math.sin(index / rim_segments * math.tau) * radius,
            center_z,
        )
        for index in range(rim_segments)
    )
    hub = box_point(profile, center_x, center_y, center_z)
    lines: list[SceneryLine] = []

    for index in range(rim_segments):
        lines.append(SceneryLine(rim_points[index], rim_points[(index + 1) % rim_segments], 5))
    for index in range(0, rim_segments, 2):
        lines.append(SceneryLine(hub, rim_points[index], 1))

    support_feet = (
        box_point(profile, center_x - radius * 0.75, base_y, center_z - 0.035),
        box_point(profile, center_x + radius * 0.75, base_y, center_z - 0.035),
        box_point(profile, center_x - radius * 0.55, base_y, center_z + 0.040),
        box_point(profile, center_x + radius * 0.55, base_y, center_z + 0.040),
    )
    lower_hub = box_point(profile, center_x, center_y - radius * 0.18, center_z)
    for foot in support_feet:
        lines.append(SceneryLine(foot, lower_hub, 5))

    for index in (1, 4, 7, 10):
        rim_point = rim_points[index]
        cabin_drop = box_point(
            profile,
            (rim_point.x / (profile.box_width / 2.0)),
            (rim_point.y / (profile.box_height / 2.0)) - 0.035,
            center_z,
        )
        lines.append(SceneryLine(rim_point, cabin_drop, 1))

    return tuple(lines)


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
