from __future__ import annotations

from math import isclose

from pyxel_goal_game.camera3d import Camera3D, Vec3
from pyxel_goal_game.screen_profiles import (
    CLASSIC_PROFILE,
    IPHONE16_BALANCED_PROFILE,
)


def test_classic_origin_projects_to_screen_center() -> None:
    camera = Camera3D.from_profile(CLASSIC_PROFILE)
    projected = camera.project(Vec3(0.0, 0.0, 0.0))

    assert projected.x == 128
    assert projected.y == 72
    assert projected.sx == 128
    assert projected.sy == 72
    assert projected.depth == 180.0


def test_larger_y_projects_higher_on_screen() -> None:
    camera = Camera3D.from_profile(CLASSIC_PROFILE)
    low = camera.project(Vec3(0.0, 0.0, 0.0))
    high = camera.project(Vec3(0.0, 10.0, 0.0))

    assert high.y < low.y


def test_profile_controls_projection_center_and_camera_values() -> None:
    camera = Camera3D.from_profile(IPHONE16_BALANCED_PROFILE)
    projected = camera.project(Vec3(0.0, 0.0, 0.0))

    assert camera.width == 236
    assert camera.height == 512
    assert camera.focal == 260.0
    assert camera.camera_distance == 340.0
    assert projected.x == 118
    assert projected.y == 256
    assert projected.depth == 340.0


def test_projection_is_deterministic() -> None:
    camera = Camera3D.from_profile(CLASSIC_PROFILE)
    point = Vec3(12.0, 5.0, -8.0)

    assert camera.project(point) == camera.project(point)


def test_depth_guard_matches_prototype_behavior() -> None:
    camera = Camera3D.from_profile(CLASSIC_PROFILE)
    camera.camera_distance = 0.0
    camera.yaw = 0.0
    camera.pitch = 0.0

    projected = camera.project(Vec3(0.0, 0.0, -20.0))

    assert projected.depth == 1.0


def test_step_toward_target_uses_prototype_smoothing() -> None:
    camera = Camera3D.from_profile(CLASSIC_PROFILE)
    camera.target_yaw = 1.6
    camera.target_pitch = 1.3
    camera.target_zoom = 2.0

    camera.step_toward_target()

    assert isclose(camera.yaw, 0.72)
    assert isclose(camera.pitch, 0.42)
    assert isclose(camera.zoom, 1.1)
