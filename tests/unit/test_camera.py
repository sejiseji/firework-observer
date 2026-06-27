from __future__ import annotations

from pyxel_goal_game.model.camera import Camera
from pyxel_goal_game.systems.camera_system import rotate_camera


def test_rotate_camera_changes_angle() -> None:
    camera = Camera(angle=1.0)
    rotate_camera(camera, 0.5)
    assert camera.angle == 1.5
