from __future__ import annotations

# ruff: noqa: E402, I001

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pyxel_goal_game.runtime.camera_motion import (
    AUTO_ROTATE_BASE_SWAY as RUNTIME_AUTO_ROTATE_BASE_SWAY,
    AUTO_ROTATE_SPEEDS as RUNTIME_AUTO_ROTATE_SPEEDS,
)
from tools.preview_firework_box import (
    AUTO_ROTATE_BASE_SWAY,
    AUTO_ROTATE_SPEEDS,
    DEFAULT_AUTO_ROTATE_SPEED_INDEX,
    GLITTER_RESIDUE_COUNTS,
    GLITTER_RESIDUE_LIFE_RANGE,
)


def test_auto_rotate_speed_modes_are_ordered_for_comfort() -> None:
    labels = tuple(mode[0] for mode in AUTO_ROTATE_SPEEDS)
    speeds = tuple(mode[1] for mode in AUTO_ROTATE_SPEEDS)

    assert labels == ("slow", "normal", "fast")
    assert speeds[0] < speeds[1] < speeds[2]


def test_preview_uses_runtime_auto_rotate_settings() -> None:
    assert AUTO_ROTATE_SPEEDS == RUNTIME_AUTO_ROTATE_SPEEDS
    assert AUTO_ROTATE_BASE_SWAY == RUNTIME_AUTO_ROTATE_BASE_SWAY


def test_auto_rotate_normal_and_fast_are_reduced_from_previous_values() -> None:
    speeds = {label: speed for label, speed, _sway_scale in AUTO_ROTATE_SPEEDS}

    assert speeds["slow"] == 0.0035
    assert speeds["normal"] < 0.0100
    assert speeds["fast"] < 0.0140
    assert speeds["fast"] == 0.0100


def test_auto_rotate_sway_scales_are_ordered() -> None:
    sways = tuple(AUTO_ROTATE_BASE_SWAY * mode[2] for mode in AUTO_ROTATE_SPEEDS)

    assert sways[0] < sways[1] < sways[2]
    assert sways[0] == AUTO_ROTATE_BASE_SWAY * 0.25
    assert sways[1] == AUTO_ROTATE_BASE_SWAY * 0.55
    assert sways[2] == AUTO_ROTATE_BASE_SWAY * 0.80


def test_auto_rotate_default_mode_remains_normal() -> None:
    assert AUTO_ROTATE_SPEEDS[DEFAULT_AUTO_ROTATE_SPEED_INDEX][0] == "normal"


def test_auto_rotate_q_cycle_order_wraps() -> None:
    indexes = []
    index = 0
    for _ in range(4):
        indexes.append(index)
        index = (index + 1) % len(AUTO_ROTATE_SPEEDS)

    assert tuple(AUTO_ROTATE_SPEEDS[index][0] for index in indexes) == (
        "slow",
        "normal",
        "fast",
        "slow",
    )


def test_glitter_residue_counts_are_sparse() -> None:
    assert len(GLITTER_RESIDUE_COUNTS) == 11
    assert max(GLITTER_RESIDUE_COUNTS) <= 12
    assert GLITTER_RESIDUE_COUNTS[9] <= 2


def test_glitter_residue_lifetime_is_short() -> None:
    assert GLITTER_RESIDUE_LIFE_RANGE[0] >= 8
    assert GLITTER_RESIDUE_LIFE_RANGE[1] <= 30
