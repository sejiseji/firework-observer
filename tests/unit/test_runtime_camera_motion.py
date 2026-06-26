from __future__ import annotations

import inspect

import pytest

from pyxel_goal_game.runtime import camera_motion
from pyxel_goal_game.runtime.camera_motion import (
    AUTO_ROTATE_BASE_SWAY,
    AUTO_ROTATE_MOTION_ORDER,
    compute_pitch_sway,
    get_auto_rotate_motion,
    get_auto_rotate_yaw_delta,
    get_pitch_sway_scale,
)
from pyxel_goal_game.runtime.state import AutoRotateSpeedMode, RuntimeShowState


def test_camera_motion_module_imports_without_pyxel_or_tools() -> None:
    source = inspect.getsource(camera_motion)

    assert "import pyxel" not in source
    assert "tools.preview_firework_box" not in source


def test_auto_rotate_motion_modes_and_speed_values_are_stable() -> None:
    modes = tuple(motion.mode for motion in AUTO_ROTATE_MOTION_ORDER)
    speeds = tuple(motion.yaw_speed for motion in AUTO_ROTATE_MOTION_ORDER)

    assert modes == (
        AutoRotateSpeedMode.SLOW,
        AutoRotateSpeedMode.NORMAL,
        AutoRotateSpeedMode.FAST,
    )
    assert speeds == (0.0035, 0.0065, 0.0100)
    assert speeds[0] < speeds[1] < speeds[2]


def test_pitch_sway_scales_are_ordered_for_comfort() -> None:
    scales = tuple(motion.pitch_sway_scale for motion in AUTO_ROTATE_MOTION_ORDER)

    assert scales == (0.25, 0.55, 0.80)
    assert scales[0] < scales[1] < scales[2]


def test_default_runtime_state_rotate_mode_remains_normal() -> None:
    assert RuntimeShowState().auto_rotate_speed_mode is AutoRotateSpeedMode.NORMAL


def test_camera_motion_helpers_are_deterministic() -> None:
    assert get_auto_rotate_yaw_delta(AutoRotateSpeedMode.SLOW) == 0.0035
    assert get_pitch_sway_scale(AutoRotateSpeedMode.FAST) == 0.80

    first = compute_pitch_sway(frame=120, mode=AutoRotateSpeedMode.NORMAL)
    second = compute_pitch_sway(frame=120, mode=AutoRotateSpeedMode.NORMAL)

    assert first == second
    assert abs(first) <= AUTO_ROTATE_BASE_SWAY * 0.55


def test_invalid_camera_motion_mode_is_rejected() -> None:
    with pytest.raises(ValueError, match="AutoRotateSpeedMode"):
        get_auto_rotate_motion("normal")  # type: ignore[arg-type]


def test_negative_pitch_sway_frame_is_rejected() -> None:
    with pytest.raises(ValueError, match="frame"):
        compute_pitch_sway(frame=-1, mode=AutoRotateSpeedMode.NORMAL)
