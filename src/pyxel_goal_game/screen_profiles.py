from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ScreenProfile:
    name: str
    width: int
    height: int
    box_width: float
    box_height: float
    box_depth: float
    focal: float
    camera_distance: float
    max_particles: int


CLASSIC_PROFILE = ScreenProfile(
    name="classic",
    width=256,
    height=144,
    box_width=120.0,
    box_height=80.0,
    box_depth=120.0,
    focal=180.0,
    camera_distance=180.0,
    max_particles=400,
)

IPHONE16_BALANCED_PROFILE = ScreenProfile(
    name="iphone16_balanced",
    width=236,
    height=512,
    box_width=120.0,
    box_height=260.0,
    box_depth=120.0,
    focal=260.0,
    camera_distance=340.0,
    max_particles=600,
)

IPHONE16_LARGE_PROFILE = ScreenProfile(
    name="iphone16_large",
    width=393,
    height=852,
    box_width=200.0,
    box_height=440.0,
    box_depth=200.0,
    focal=430.0,
    camera_distance=560.0,
    max_particles=900,
)

SCREEN_PROFILES = {
    CLASSIC_PROFILE.name: CLASSIC_PROFILE,
    IPHONE16_BALANCED_PROFILE.name: IPHONE16_BALANCED_PROFILE,
    IPHONE16_LARGE_PROFILE.name: IPHONE16_LARGE_PROFILE,
}

DEFAULT_SCREEN_PROFILE_NAME = CLASSIC_PROFILE.name
DEFAULT_SCREEN_PROFILE = SCREEN_PROFILES[DEFAULT_SCREEN_PROFILE_NAME]


def get_screen_profile(name: str = DEFAULT_SCREEN_PROFILE_NAME) -> ScreenProfile:
    return SCREEN_PROFILES[name]
