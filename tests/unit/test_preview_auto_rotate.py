from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.preview_firework_box import (  # noqa: E402
    AUTO_ROTATE_BASE_SWAY,
    AUTO_ROTATE_SPEEDS,
    DEFAULT_AUTO_ROTATE_SPEED_INDEX,
)


def test_auto_rotate_speed_modes_are_ordered_for_comfort() -> None:
    labels = tuple(mode[0] for mode in AUTO_ROTATE_SPEEDS)
    speeds = tuple(mode[1] for mode in AUTO_ROTATE_SPEEDS)

    assert labels == ("slow", "normal", "fast")
    assert speeds[0] < speeds[1] < speeds[2]


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
