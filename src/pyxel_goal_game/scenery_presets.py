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
    lines.extend(landmark_tower_lines(profile=profile, base_y=base_y))
    lines.extend(utility_pole_lines(profile=profile, base_y=base_y))
    polylines = utility_wire_polylines(profile=profile, base_y=base_y)
    return SceneryPreset(
        kind=SceneryKind.CITY,
        label="City",
        lines=tuple(lines),
        polylines=polylines,
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


def landmark_tower_lines(
    *,
    profile: ScreenProfile,
    base_y: float,
) -> tuple[SceneryLine, ...]:
    base = -0.88
    deck = -0.60
    top = -0.49
    antenna = -0.42
    center_x = 0.74
    center_z = 0.02
    base_half_width = 0.105
    deck_half_width = 0.052
    top_half_width = 0.020
    depth = 0.09

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
        lines.append(SceneryLine(base_points[index], deck_points[index], 5))
        lines.append(SceneryLine(deck_points[index], top_points[index], 5))
        lines.append(SceneryLine(base_points[index], deck_points[(index + 1) % 4], 1))
    for ring in (deck_points, top_points):
        for index in range(4):
            lines.append(SceneryLine(ring[index], ring[(index + 1) % 4], 5))
    lines.append(SceneryLine(center_deck, center_top, 5))
    lines.append(SceneryLine(center_top, antenna_top, 10))
    return tuple(lines)


def utility_pole_lines(
    *,
    profile: ScreenProfile,
    base_y: float,
) -> tuple[SceneryLine, ...]:
    poles = (
        (-0.82, -0.18, 0.18),
        (-0.36, -0.08, 0.22),
        (0.16, -0.16, 0.19),
    )
    lines: list[SceneryLine] = []
    for x, z, height in poles:
        bottom = box_point(profile, x, base_y + 0.02, z)
        top = box_point(profile, x, base_y + height, z)
        crossbar_left = box_point(profile, x - 0.055, base_y + height - 0.035, z)
        crossbar_right = box_point(profile, x + 0.055, base_y + height - 0.035, z)
        brace_left = box_point(profile, x - 0.030, base_y + height - 0.075, z)
        brace_right = box_point(profile, x + 0.030, base_y + height - 0.075, z)
        lines.extend(
            (
                SceneryLine(bottom, top, 5, phase="front"),
                SceneryLine(crossbar_left, crossbar_right, 5, phase="front"),
                SceneryLine(brace_left, top, 1, phase="front"),
                SceneryLine(top, brace_right, 1, phase="front"),
            )
        )
    return tuple(lines)


def utility_wire_polylines(
    *,
    profile: ScreenProfile,
    base_y: float,
) -> tuple[SceneryPolyline, ...]:
    wire_sets = (
        ((-0.82, -0.18, 0.18), (-0.36, -0.08, 0.22)),
        ((-0.36, -0.08, 0.22), (0.16, -0.16, 0.19)),
    )
    polylines: list[SceneryPolyline] = []
    for start, end in wire_sets:
        start_x, start_z, start_height = start
        end_x, end_z, end_height = end
        start_y = base_y + start_height - 0.045
        end_y = base_y + end_height - 0.045
        mid_x = (start_x + end_x) / 2.0
        mid_z = (start_z + end_z) / 2.0
        mid_y = min(start_y, end_y) - 0.025
        polylines.append(
            SceneryPolyline(
                points=(
                    box_point(profile, start_x, start_y, start_z),
                    box_point(profile, mid_x, mid_y, mid_z),
                    box_point(profile, end_x, end_y, end_z),
                ),
                color=1,
                phase="front",
            )
        )
    return tuple(polylines)


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
