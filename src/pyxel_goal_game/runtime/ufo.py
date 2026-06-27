from __future__ import annotations

from dataclasses import dataclass, replace
from math import cos, sin, tau
from random import Random

from pyxel_goal_game.camera3d import Vec3
from pyxel_goal_game.screen_profiles import ScreenProfile

UFO_INITIAL_DELAY_FRAMES = 900
UFO_CHECK_INTERVAL_FRAMES = 420
UFO_COOLDOWN_FRAMES = 1200
UFO_SPAWN_CHANCE = 0.18
UFO_MIN_DURATION_FRAMES = 300
UFO_MAX_DURATION_FRAMES = 420
UFO_DEFAULT_SEED = 20260627
UFO_RIM_SEGMENTS = 12


@dataclass(frozen=True)
class UfoEdge:
    start: Vec3
    end: Vec3


@dataclass(frozen=True)
class UfoWireframe:
    edges: tuple[UfoEdge, ...]
    lights: tuple[Vec3, ...]


@dataclass(frozen=True)
class UfoFlyby:
    start_frame: int
    duration_frames: int
    start: Vec3
    end: Vec3
    radius: float
    seed: int

    @property
    def end_frame(self) -> int:
        return self.start_frame + self.duration_frames

    def is_active(self, frame: int) -> bool:
        return self.start_frame <= frame < self.end_frame

    def position_at(self, frame: int) -> Vec3:
        progress = min(1.0, max(0.0, (frame - self.start_frame) / self.duration_frames))
        ease = progress * progress * (3.0 - 2.0 * progress)
        return Vec3(
            x=self.start.x + (self.end.x - self.start.x) * ease,
            y=self.start.y
            + (self.end.y - self.start.y) * ease
            + sin(progress * 3.141592653589793) * self.radius * 0.25,
            z=self.start.z + (self.end.z - self.start.z) * ease,
        )

    def wireframe_at(self, frame: int) -> UfoWireframe:
        return build_ufo_wireframe(
            center=self.position_at(frame),
            radius=self.radius,
            travel_start=self.start,
            travel_end=self.end,
        )


@dataclass(frozen=True)
class UfoState:
    active: UfoFlyby | None
    next_check_frame: int
    enabled: bool = True


def initial_ufo_state(*, start_frame: int = 0, enabled: bool = True) -> UfoState:
    return UfoState(
        active=None,
        next_check_frame=start_frame + UFO_INITIAL_DELAY_FRAMES,
        enabled=enabled,
    )


def toggle_ufo_enabled(state: UfoState, *, frame: int) -> UfoState:
    enabled = not state.enabled
    return UfoState(
        active=state.active if enabled else None,
        next_check_frame=frame + UFO_CHECK_INTERVAL_FRAMES,
        enabled=enabled,
    )


def update_ufo_state(
    state: UfoState,
    *,
    frame: int,
    profile: ScreenProfile,
    seed: int = UFO_DEFAULT_SEED,
) -> UfoState:
    if not state.enabled:
        return replace(state, active=None)
    if state.active is not None:
        if state.active.is_active(frame):
            return state
        return UfoState(
            active=None,
            next_check_frame=frame + UFO_COOLDOWN_FRAMES,
            enabled=True,
        )
    if frame < state.next_check_frame:
        return state

    rng = Random(seed + frame * 131)
    if rng.random() >= UFO_SPAWN_CHANCE:
        return replace(state, next_check_frame=frame + UFO_CHECK_INTERVAL_FRAMES)
    return UfoState(
        active=build_ufo_flyby(profile=profile, start_frame=frame, seed=seed + frame),
        next_check_frame=frame + UFO_COOLDOWN_FRAMES,
        enabled=True,
    )


def build_ufo_flyby(
    *,
    profile: ScreenProfile,
    start_frame: int,
    seed: int,
) -> UfoFlyby:
    rng = Random(seed)
    half_width = profile.box_width / 2
    half_height = profile.box_height / 2
    half_depth = profile.box_depth / 2
    left_to_right = rng.random() < 0.5
    x_margin = half_width * 0.92
    start_x = -x_margin if left_to_right else x_margin
    end_x = x_margin if left_to_right else -x_margin
    y_base = half_height * rng.uniform(0.28, 0.48)
    end_y = y_base + half_height * rng.uniform(-0.05, 0.05)
    z_base = half_depth * rng.uniform(-0.35, 0.35)
    end_z = z_base + half_depth * rng.uniform(-0.15, 0.15)
    duration = rng.randint(UFO_MIN_DURATION_FRAMES, UFO_MAX_DURATION_FRAMES)
    radius = max(2.0, min(profile.box_width, profile.box_depth) * rng.uniform(0.025, 0.04))
    return UfoFlyby(
        start_frame=start_frame,
        duration_frames=duration,
        start=Vec3(start_x, y_base, z_base),
        end=Vec3(end_x, end_y, end_z),
        radius=radius,
        seed=seed,
    )


def build_ufo_wireframe(
    *,
    center: Vec3,
    radius: float,
    travel_start: Vec3,
    travel_end: Vec3,
) -> UfoWireframe:
    forward_x = travel_end.x - travel_start.x
    forward_z = travel_end.z - travel_start.z
    forward_length = (forward_x * forward_x + forward_z * forward_z) ** 0.5
    if forward_length <= 0.0001:
        forward_x = 1.0
        forward_z = 0.0
    else:
        forward_x /= forward_length
        forward_z /= forward_length
    side_x = -forward_z
    side_z = forward_x

    def local_point(x: float, y: float, z: float) -> Vec3:
        return Vec3(
            center.x + side_x * x + forward_x * z,
            center.y + y,
            center.z + side_z * x + forward_z * z,
        )

    rim_width = radius * 1.25
    rim_depth = radius * 0.55
    rim_points = tuple(
        local_point(
            cos(index / UFO_RIM_SEGMENTS * tau) * rim_width,
            0.0,
            sin(index / UFO_RIM_SEGMENTS * tau) * rim_depth,
        )
        for index in range(UFO_RIM_SEGMENTS)
    )

    edges: list[UfoEdge] = [
        UfoEdge(rim_points[index], rim_points[(index + 1) % UFO_RIM_SEGMENTS])
        for index in range(UFO_RIM_SEGMENTS)
    ]

    dome_top = local_point(0.0, radius * 0.48, 0.0)
    dome_left = local_point(-radius * 0.45, radius * 0.10, -radius * 0.08)
    dome_right = local_point(radius * 0.45, radius * 0.10, -radius * 0.08)
    dome_back = local_point(0.0, radius * 0.12, radius * 0.26)
    lower = local_point(0.0, -radius * 0.30, 0.0)
    lower_left = local_point(-radius * 0.52, -radius * 0.08, 0.0)
    lower_right = local_point(radius * 0.52, -radius * 0.08, 0.0)
    lower_front = local_point(0.0, -radius * 0.08, -radius * 0.28)
    lower_back = local_point(0.0, -radius * 0.08, radius * 0.28)

    edges.extend(
        (
            UfoEdge(dome_left, dome_top),
            UfoEdge(dome_top, dome_right),
            UfoEdge(dome_top, dome_back),
            UfoEdge(dome_left, dome_right),
            UfoEdge(lower_left, lower),
            UfoEdge(lower_right, lower),
            UfoEdge(lower_front, lower),
            UfoEdge(lower_back, lower),
            UfoEdge(lower_left, lower_right),
            UfoEdge(lower_front, lower_back),
        )
    )

    lights = (
        local_point(-radius * 0.55, -radius * 0.10, -radius * 0.20),
        local_point(0.0, -radius * 0.13, -radius * 0.30),
        local_point(radius * 0.55, -radius * 0.10, -radius * 0.20),
    )
    return UfoWireframe(edges=tuple(edges), lights=lights)
