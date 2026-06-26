from __future__ import annotations

from pathlib import Path

import pytest

from pyxel_goal_game.scenery_presets import (
    SCENERY_PRESET_NAMES,
    SceneryKind,
    ferris_wheel_lines,
    get_scenery_preset,
)
from pyxel_goal_game.screen_profiles import (
    CLASSIC_PROFILE,
    IPHONE16_BALANCED_PROFILE,
    ScreenProfile,
)


def assert_points_inside_box(profile: ScreenProfile, name: str) -> None:
    preset = get_scenery_preset(name, profile=profile)
    half_width = profile.box_width / 2.0
    half_height = profile.box_height / 2.0
    half_depth = profile.box_depth / 2.0

    for point in preset.all_points:
        assert -half_width <= point.x <= half_width
        assert -half_height <= point.y <= half_height
        assert -half_depth <= point.z <= half_depth


def test_empty_scenery_has_no_geometry() -> None:
    preset = get_scenery_preset("empty", profile=CLASSIC_PROFILE)

    assert preset.kind is SceneryKind.EMPTY
    assert preset.label == "Empty"
    assert preset.lines == ()
    assert preset.polylines == ()
    assert preset.all_points == ()


def test_active_preview_scenery_is_city_focused() -> None:
    assert SCENERY_PRESET_NAMES == ("empty", "city")


@pytest.mark.parametrize("name", ["mountains", "city", "riverbank"])
def test_initial_scenery_presets_contain_geometry(name: str) -> None:
    preset = get_scenery_preset(name, profile=CLASSIC_PROFILE)

    assert preset.kind is not SceneryKind.EMPTY
    assert preset.lines or preset.polylines
    assert preset.all_points


@pytest.mark.parametrize("name", SCENERY_PRESET_NAMES)
@pytest.mark.parametrize("profile", [CLASSIC_PROFILE, IPHONE16_BALANCED_PROFILE])
def test_scenery_points_stay_inside_box(profile: ScreenProfile, name: str) -> None:
    assert_points_inside_box(profile, name)


def test_scenery_is_profile_scaled() -> None:
    classic = get_scenery_preset("mountains", profile=CLASSIC_PROFILE)
    balanced = get_scenery_preset("mountains", profile=IPHONE16_BALANCED_PROFILE)

    classic_y_values = tuple(point.y for point in classic.all_points)
    balanced_y_values = tuple(point.y for point in balanced.all_points)

    assert max(balanced_y_values) < max(classic_y_values)
    assert min(balanced_y_values) < min(classic_y_values)


def test_city_uses_3d_building_geometry() -> None:
    city = get_scenery_preset("city", profile=CLASSIC_PROFILE)
    points = city.all_points

    assert len(city.lines) >= 360
    assert len({round(point.x, 4) for point in points}) > 10
    assert len({round(point.y, 4) for point in points}) > 5
    assert len({round(point.z, 4) for point in points}) > 6


def test_city_extends_across_fuller_lower_footprint() -> None:
    city = get_scenery_preset("city", profile=CLASSIC_PROFILE)
    points = city.all_points
    half_width = CLASSIC_PROFILE.box_width / 2.0
    half_depth = CLASSIC_PROFILE.box_depth / 2.0

    assert min(point.x for point in points) < -half_width * 0.88
    assert max(point.x for point in points) > half_width * 0.88
    assert min(point.z for point in points) < -half_depth * 0.50
    assert max(point.z for point in points) > half_depth * 0.55


def test_city_has_peripheral_side_building_coverage() -> None:
    city = get_scenery_preset("city", profile=CLASSIC_PROFILE)
    base_y = min(point.y for point in city.all_points)
    grounded_verticals = [
        line
        for line in city.lines
        if line.start.x == line.end.x
        and line.start.z == line.end.z
        and line.start.y != line.end.y
        and (line.start.y == base_y or line.end.y == base_y)
    ]
    half_width = CLASSIC_PROFILE.box_width / 2.0
    half_depth = CLASSIC_PROFILE.box_depth / 2.0

    assert sum(1 for line in grounded_verticals if line.start.x < -half_width * 0.75) >= 8
    assert sum(1 for line in grounded_verticals if line.start.x > half_width * 0.75) >= 8
    assert any(abs(line.start.z) > half_depth * 0.60 for line in grounded_verticals)


def test_city_preserves_central_boulevard_corridor() -> None:
    city = get_scenery_preset("city", profile=CLASSIC_PROFILE)
    base_y = min(point.y for point in city.all_points)
    grounded_verticals = [
        line
        for line in city.lines
        if line.start.x == line.end.x
        and line.start.z == line.end.z
        and line.start.y != line.end.y
        and (line.start.y == base_y or line.end.y == base_y)
    ]

    assert all(abs(line.start.x) >= CLASSIC_PROFILE.box_width * 0.06 for line in grounded_verticals)


def test_city_buildings_omit_bottom_face_edges() -> None:
    city = get_scenery_preset("city", profile=CLASSIC_PROFILE)
    base_y = min(point.y for point in city.all_points)
    bottom_edges = [
        line
        for line in city.lines
        if line.start.y == base_y and line.end.y == base_y
    ]
    vertical_edges = [
        line
        for line in city.lines
        if line.start.x == line.end.x
        and line.start.z == line.end.z
        and line.start.y != line.end.y
        and (line.start.y == base_y or line.end.y == base_y)
    ]
    top_edges = [
        line
        for line in city.lines
        if line.start.y == line.end.y and line.start.y > base_y
    ]

    assert bottom_edges == []
    assert len(vertical_edges) >= 60
    assert len(top_edges) >= 40


def test_city_buildings_are_grounded() -> None:
    city = get_scenery_preset("city", profile=CLASSIC_PROFILE)
    base_y = min(point.y for point in city.all_points)
    grounded_verticals = [
        line
        for line in city.lines
        if line.start.x == line.end.x
        and line.start.z == line.end.z
        and line.start.y != line.end.y
        and (line.start.y == base_y or line.end.y == base_y)
    ]

    assert len(grounded_verticals) >= 60


def test_city_stays_low_in_observation_box() -> None:
    city = get_scenery_preset("city", profile=CLASSIC_PROFILE)
    y_values = tuple(point.y for point in city.all_points)

    assert max(y_values) - min(y_values) <= CLASSIC_PROFILE.box_height * 0.30


def test_city_includes_quiet_urban_landmarks() -> None:
    city = get_scenery_preset("city", profile=CLASSIC_PROFILE)

    assert any(line.color == 10 for line in city.lines)
    assert max(point.y for point in city.all_points) > -CLASSIC_PROFILE.box_height * 0.21


def test_city_includes_low_detail_ferris_wheel() -> None:
    wheel_lines = ferris_wheel_lines(profile=CLASSIC_PROFILE, base_y=-0.96)
    wheel_points = tuple(point for line in wheel_lines for point in (line.start, line.end))
    base_y = min(point.y for point in wheel_points)
    x_extent = max(point.x for point in wheel_points) - min(point.x for point in wheel_points)
    y_extent = max(point.y for point in wheel_points) - min(point.y for point in wheel_points)
    grounded_supports = [
        line
        for line in wheel_lines
        if line.start.y == base_y or line.end.y == base_y
    ]
    hub_like_points = [
        point
        for point in wheel_points
        if abs(point.x - (-0.72 * CLASSIC_PROFILE.box_width / 2.0)) < 0.001
        and abs(point.y - (-0.69 * CLASSIC_PROFILE.box_height / 2.0)) < 0.001
    ]

    assert len(wheel_lines) >= 36
    assert len(grounded_supports) >= 4
    assert len(hub_like_points) >= 10
    normalized_x_extent = x_extent / CLASSIC_PROFILE.box_width
    normalized_y_extent = y_extent / CLASSIC_PROFILE.box_height

    assert normalized_x_extent > 0.15
    assert normalized_y_extent > 0.18
    assert 0.82 <= x_extent / y_extent <= 1.18
    assert len({round(point.x, 4) for point in wheel_points}) >= 10
    assert len({round(point.y, 4) for point in wheel_points}) >= 10


def test_city_removes_active_utility_poles_and_wires() -> None:
    city = get_scenery_preset("city", profile=CLASSIC_PROFILE)

    assert city.polylines == ()
    assert all(line.phase == "back" for line in city.lines)


def test_city_includes_sparse_signage() -> None:
    city = get_scenery_preset("city", profile=CLASSIC_PROFILE)
    colors = [line.color for line in city.lines]

    assert 12 in colors
    assert colors.count(12) < len(colors) // 10


def test_city_has_sparse_lit_windows() -> None:
    city = get_scenery_preset("city", profile=CLASSIC_PROFILE)
    colors = [line.color for line in city.lines]

    assert 7 in colors
    assert 10 in colors
    assert colors.count(7) + colors.count(10) < len(colors) // 3


@pytest.mark.parametrize("name", SCENERY_PRESET_NAMES)
def test_scenery_generation_is_deterministic(name: str) -> None:
    assert get_scenery_preset(name, profile=CLASSIC_PROFILE) == get_scenery_preset(
        name,
        profile=CLASSIC_PROFILE,
    )


def test_scenery_module_does_not_import_pyxel() -> None:
    source_lines = Path("src/pyxel_goal_game/scenery_presets.py").read_text().splitlines()

    assert "import pyxel" not in source_lines
    assert "from pyxel import" not in source_lines


def test_unknown_scenery_name_raises_key_error() -> None:
    with pytest.raises(KeyError):
        get_scenery_preset("unknown", profile=CLASSIC_PROFILE)
