from __future__ import annotations

from dataclasses import dataclass, replace
from math import sin
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
