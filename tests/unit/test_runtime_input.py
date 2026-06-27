from __future__ import annotations

import inspect

from pyxel_goal_game.runtime import input


def test_runtime_input_maps_first_generation_controls() -> None:
    source = inspect.getsource(input)

    for key_name in (
        "KEY_SPACE",
        "KEY_R",
        "KEY_Z",
        "KEY_V",
        "KEY_0",
        "KEY_1",
        "KEY_2",
        "KEY_3",
        "KEY_4",
        "KEY_5",
        "KEY_H",
        "KEY_X",
        "KEY_Q",
        "KEY_T",
        "KEY_M",
        "KEY_G",
        "KEY_B",
        "KEY_D",
        "KEY_A",
        "KEY_S",
        "KEY_LEFT",
        "KEY_RIGHT",
        "KEY_UP",
        "KEY_DOWN",
    ):
        assert key_name in source


def test_runtime_input_does_not_import_tools_preview() -> None:
    source = inspect.getsource(input)

    assert "tools.preview_firework_box" not in source
    assert "preview_firework_box" not in source
