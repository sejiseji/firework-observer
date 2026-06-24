from __future__ import annotations

from pyxel_goal_game.model.camera import Camera


def rotate_camera(camera: Camera, delta: float) -> None:
    camera.angle += delta
