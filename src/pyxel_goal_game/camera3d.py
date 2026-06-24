from __future__ import annotations

import math
from dataclasses import dataclass

from pyxel_goal_game.screen_profiles import DEFAULT_SCREEN_PROFILE, ScreenProfile


@dataclass(frozen=True)
class Vec3:
    x: float
    y: float
    z: float


@dataclass(frozen=True)
class ProjectedPoint:
    x: float
    y: float
    depth: float

    @property
    def sx(self) -> int:
        return int(round(self.x))

    @property
    def sy(self) -> int:
        return int(round(self.y))


@dataclass
class Camera3D:
    width: int = DEFAULT_SCREEN_PROFILE.width
    height: int = DEFAULT_SCREEN_PROFILE.height
    focal: float = DEFAULT_SCREEN_PROFILE.focal
    camera_distance: float = DEFAULT_SCREEN_PROFILE.camera_distance
    yaw: float = 0.6
    pitch: float = 0.3
    zoom: float = 1.0
    target_yaw: float = 0.6
    target_pitch: float = 0.3
    target_zoom: float = 1.0
    yaw_smoothing: float = 0.12
    pitch_smoothing: float = 0.12
    zoom_smoothing: float = 0.10

    @classmethod
    def from_profile(cls, profile: ScreenProfile = DEFAULT_SCREEN_PROFILE) -> Camera3D:
        return cls(
            width=profile.width,
            height=profile.height,
            focal=profile.focal,
            camera_distance=profile.camera_distance,
        )

    def transform(self, point: Vec3) -> Vec3:
        cos_yaw = math.cos(self.yaw)
        sin_yaw = math.sin(self.yaw)
        cos_pitch = math.cos(self.pitch)
        sin_pitch = math.sin(self.pitch)

        rx = point.x * cos_yaw - point.z * sin_yaw
        rz = point.x * sin_yaw + point.z * cos_yaw

        ry = point.y * cos_pitch - rz * sin_pitch
        rz2 = point.y * sin_pitch + rz * cos_pitch
        return Vec3(rx, ry, rz2)

    def project(self, point: Vec3) -> ProjectedPoint:
        transformed = self.transform(point)
        depth = max(1.0, transformed.z + self.camera_distance)
        scale = self.focal / depth * self.zoom
        sx = self.width // 2 + transformed.x * scale
        sy = self.height // 2 - transformed.y * scale
        return ProjectedPoint(sx, sy, depth)

    def step_toward_target(self) -> None:
        self.yaw += (self.target_yaw - self.yaw) * self.yaw_smoothing
        self.pitch += (self.target_pitch - self.pitch) * self.pitch_smoothing
        self.zoom += (self.target_zoom - self.zoom) * self.zoom_smoothing
