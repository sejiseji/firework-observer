from __future__ import annotations

import pytest

from pyxel_goal_game.screen_profiles import (
    DEFAULT_SCREEN_PROFILE,
    SCREEN_PROFILES,
    get_screen_profile,
)
from pyxel_goal_game.settings import GameSettings


def test_classic_profile_is_default() -> None:
    assert DEFAULT_SCREEN_PROFILE.name == "classic"
    assert GameSettings().profile is DEFAULT_SCREEN_PROFILE
    assert GameSettings().width == 256
    assert GameSettings().height == 144


@pytest.mark.parametrize(
    ("name", "screen", "box", "focal", "camera_distance", "max_particles"),
    [
        ("classic", (256, 144), (120.0, 80.0, 120.0), 180.0, 180.0, 400),
        (
            "iphone16_balanced",
            (512, 236),
            (120.0, 260.0, 120.0),
            260.0,
            340.0,
            600,
        ),
        ("iphone16_large", (852, 393), (200.0, 440.0, 200.0), 430.0, 560.0, 900),
    ],
)
def test_profiles_match_documented_values(
    name: str,
    screen: tuple[int, int],
    box: tuple[float, float, float],
    focal: float,
    camera_distance: float,
    max_particles: int,
) -> None:
    profile = get_screen_profile(name)
    assert profile.width == screen[0]
    assert profile.height == screen[1]
    assert (profile.box_width, profile.box_height, profile.box_depth) == box
    assert profile.focal == focal
    assert profile.camera_distance == camera_distance
    assert profile.max_particles == max_particles


def test_profiles_are_registered_by_name() -> None:
    assert set(SCREEN_PROFILES) == {"classic", "iphone16_balanced", "iphone16_large"}


@pytest.mark.parametrize("name", ["iphone16_balanced", "iphone16_large"])
def test_iphone_profiles_use_portrait_firework_volume(name: str) -> None:
    profile = get_screen_profile(name)
    screen_ratio = profile.width / profile.height
    box_ratio = profile.box_height / profile.box_width

    assert profile.box_height > profile.box_width
    assert profile.box_height > profile.box_depth
    assert box_ratio == pytest.approx(screen_ratio, rel=0.04)
