from __future__ import annotations

import math
from dataclasses import dataclass

from pyxel_goal_game.runtime.state import AutoRotateSpeedMode


@dataclass(frozen=True)
class AutoRotateMotion:
    mode: AutoRotateSpeedMode
    yaw_speed: float
    pitch_sway_scale: float


AUTO_ROTATE_BASE_SWAY = 0.35
AUTO_ROTATE_PITCH_SWAY_FREQUENCY = 0.015

AUTO_ROTATE_MOTION_ORDER = (
    AutoRotateMotion(
        mode=AutoRotateSpeedMode.SLOW,
        yaw_speed=0.0035,
        pitch_sway_scale=0.25,
    ),
    AutoRotateMotion(
        mode=AutoRotateSpeedMode.NORMAL,
        yaw_speed=0.0065,
        pitch_sway_scale=0.55,
    ),
    AutoRotateMotion(
        mode=AutoRotateSpeedMode.FAST,
        yaw_speed=0.0100,
        pitch_sway_scale=0.80,
    ),
)

AUTO_ROTATE_SPEEDS = tuple(
    (motion.mode.value, motion.yaw_speed, motion.pitch_sway_scale)
    for motion in AUTO_ROTATE_MOTION_ORDER
)
DEFAULT_AUTO_ROTATE_SPEED_INDEX = 1

_AUTO_ROTATE_MOTION_BY_MODE = {
    motion.mode: motion for motion in AUTO_ROTATE_MOTION_ORDER
}


def get_auto_rotate_motion(mode: AutoRotateSpeedMode) -> AutoRotateMotion:
    try:
        return _AUTO_ROTATE_MOTION_BY_MODE[mode]
    except KeyError as exc:
        msg = "mode must be an AutoRotateSpeedMode"
        raise ValueError(msg) from exc


def get_auto_rotate_yaw_delta(mode: AutoRotateSpeedMode) -> float:
    return get_auto_rotate_motion(mode).yaw_speed


def get_pitch_sway_scale(mode: AutoRotateSpeedMode) -> float:
    return get_auto_rotate_motion(mode).pitch_sway_scale


def compute_pitch_sway(
    *,
    frame: int,
    mode: AutoRotateSpeedMode,
    base_amplitude: float = AUTO_ROTATE_BASE_SWAY,
) -> float:
    if frame < 0:
        msg = "frame must be non-negative"
        raise ValueError(msg)
    return (
        math.sin(frame * AUTO_ROTATE_PITCH_SWAY_FREQUENCY)
        * base_amplitude
        * get_pitch_sway_scale(mode)
    )
