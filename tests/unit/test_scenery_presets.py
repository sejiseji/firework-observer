from __future__ import annotations

from pathlib import Path

import pytest

from pyxel_goal_game.scenery_presets import (
    SCENERY_PRESET_NAMES,
    SceneryKind,
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

    assert len(city.lines) >= 72
    assert len({round(point.x, 4) for point in points}) > 10
    assert len({round(point.y, 4) for point in points}) > 5
    assert len({round(point.z, 4) for point in points}) > 6


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
    assert len(vertical_edges) >= 24
    assert len(top_edges) >= 24


def test_city_stays_low_in_observation_box() -> None:
    city = get_scenery_preset("city", profile=CLASSIC_PROFILE)
    y_values = tuple(point.y for point in city.all_points)

    assert max(y_values) - min(y_values) <= CLASSIC_PROFILE.box_height * 0.20


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
