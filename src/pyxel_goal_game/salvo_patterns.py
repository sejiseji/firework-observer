from __future__ import annotations

from dataclasses import dataclass

from pyxel_goal_game.camera3d import Vec3
from pyxel_goal_game.screen_profiles import ScreenProfile

SALVO_LAUNCH_Y_RATIO = -0.92
DEFAULT_SALVO_INTERVAL_FRAMES = 12

SALVO_BURST_RATIOS = {
    1: ((0.00, 0.55, 0.00),),
    2: (
        (-0.38, 0.42, -0.10),
        (0.38, 0.60, 0.10),
    ),
    3: (
        (-0.55, 0.38, 0.08),
        (0.00, 0.68, 0.00),
        (0.55, 0.45, -0.08),
    ),
    4: (
        (-0.58, 0.32, 0.10),
        (-0.25, 0.58, -0.10),
        (0.25, 0.50, 0.12),
        (0.58, 0.36, -0.12),
    ),
    5: (
        (-0.65, 0.30, 0.12),
        (-0.35, 0.50, -0.10),
        (0.00, 0.72, 0.00),
        (0.35, 0.50, 0.10),
        (0.65, 0.30, -0.12),
    ),
}


@dataclass(frozen=True)
class SalvoSlot:
    launch_position: Vec3
    burst_position: Vec3
    delay_frames: int
    seed_offset: int


@dataclass(frozen=True)
class SalvoPlan:
    slots: tuple[SalvoSlot, ...]
    interval_frames: int


def build_salvo_plan(
    *,
    count: int,
    profile: ScreenProfile,
    interval_frames: int = DEFAULT_SALVO_INTERVAL_FRAMES,
) -> SalvoPlan:
    if count not in SALVO_BURST_RATIOS:
        msg = "count must be between 1 and 5"
        raise ValueError(msg)
    if interval_frames < 1:
        msg = "interval_frames must be at least 1"
        raise ValueError(msg)

    half_width = profile.box_width / 2
    half_height = profile.box_height / 2
    half_depth = profile.box_depth / 2
    slots = tuple(
        SalvoSlot(
            launch_position=Vec3(
                x=x_ratio * half_width,
                y=SALVO_LAUNCH_Y_RATIO * half_height,
                z=z_ratio * half_depth,
            ),
            burst_position=Vec3(
                x=x_ratio * half_width,
                y=y_ratio * half_height,
                z=z_ratio * half_depth,
            ),
            delay_frames=index * interval_frames,
            seed_offset=index,
        )
        for index, (x_ratio, y_ratio, z_ratio) in enumerate(SALVO_BURST_RATIOS[count])
    )
    return SalvoPlan(slots=slots, interval_frames=interval_frames)
