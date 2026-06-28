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
        "KEY_U",
        "KEY_G",
        "KEY_B",
        "KEY_D",
        "KEY_A",
        "KEY_S",
        "KEY_LEFT",
        "KEY_RIGHT",
        "KEY_UP",
        "KEY_DOWN",
        "MOUSE_BUTTON_LEFT",
        "MOUSE_WHEEL_Y",
        "btnv",
    ):
        assert key_name in source


def test_runtime_input_does_not_import_tools_preview() -> None:
    source = inspect.getsource(input)

    assert "tools.preview_firework_box" not in source
    assert "preview_firework_box" not in source


def test_runtime_input_maps_mobile_panel_actions() -> None:
    source = inspect.getsource(input)

    for name in (
        "handle_mobile_input",
        "handle_mobile_panel_click",
        "menu_button_rect",
        "salvo_count_button_rect",
        "apply_mobile_toggle",
        "cycle_mobile_auto_rotate_speed",
        "cycle_mobile_salvo_count_choice",
        "start_mobile_salvo_loop",
        "audio_toggle_rect",
        "bgm_toggle_rect",
        "launch_button_rect",
        "next_button_rect",
        "random_salvo_button_rect",
        "speed_button_rect",
        "zoom_in_button_rect",
        "zoom_out_button_rect",
    ):
        assert name in source
