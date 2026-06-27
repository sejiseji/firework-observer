from __future__ import annotations

import inspect

import pytest

from pyxel_goal_game.firework_presets import FireworkKind
from pyxel_goal_game.runtime import show_controller
from pyxel_goal_game.runtime.show_controller import (
    advance_seed_base,
    clear_persistent_salvo_mode,
    cycle_auto_rotate_speed,
    cycle_firework_kind,
    set_fixed_salvo_mode,
    set_random_salvo_mode,
    tick_frame,
    toggle_audio,
    toggle_auto_launch,
    toggle_auto_rotate,
    toggle_height_variation,
    toggle_random_mode,
    toggle_scenery_visible,
    toggle_stars,
    toggle_ufo,
)
from pyxel_goal_game.runtime.state import (
    AutoRotateSpeedMode,
    RuntimeShowState,
    SalvoCountMode,
)


def test_firework_kind_cycle_follows_preview_order() -> None:
    state = RuntimeShowState()
    observed = []

    for _ in range(11):
        observed.append(state.selected_firework_kind)
        state = cycle_firework_kind(state)

    assert tuple(observed) == (
        FireworkKind.KIKU,
        FireworkKind.SPHERE_BLOOM,
        FireworkKind.SMILE,
        FireworkKind.RING,
        FireworkKind.SPIRAL,
        FireworkKind.WILLOW,
        FireworkKind.LONG_WILLOW,
        FireworkKind.PEONY,
        FireworkKind.MULTI_RING,
        FireworkKind.SENRIN,
        FireworkKind.HALO,
    )
    assert state.selected_firework_kind is FireworkKind.KIKU


def test_auto_rotate_speed_cycle_starts_from_default_normal() -> None:
    state = RuntimeShowState()

    state = cycle_auto_rotate_speed(state)
    assert state.auto_rotate_speed_mode is AutoRotateSpeedMode.FAST

    state = cycle_auto_rotate_speed(state)
    assert state.auto_rotate_speed_mode is AutoRotateSpeedMode.SLOW

    state = cycle_auto_rotate_speed(state)
    assert state.auto_rotate_speed_mode is AutoRotateSpeedMode.NORMAL


def test_toggles_flip_deterministically() -> None:
    state = RuntimeShowState()

    assert toggle_random_mode(state).toggles.random_firework_mode is True
    assert toggle_auto_launch(state).toggles.auto_launch is True
    assert toggle_height_variation(state).toggles.height_variation is True
    assert toggle_stars(state).toggles.interior_stars_visible is False
    assert toggle_scenery_visible(state).toggles.scenery_visible is False
    assert toggle_auto_rotate(state).toggles.auto_rotate is True
    assert toggle_audio(state).toggles.audio_enabled is False
    assert toggle_ufo(state).toggles.ufo_enabled is False

    assert toggle_random_mode(toggle_random_mode(state)).toggles.random_firework_mode is False


def test_fixed_salvo_modes_accept_one_through_five() -> None:
    for count in range(1, 6):
        state = set_fixed_salvo_mode(RuntimeShowState(), count)
        assert state.salvo_count_mode is SalvoCountMode.FIXED
        assert state.salvo_count == count
        assert state.toggles.auto_launch is False


def test_random_salvo_mode_can_be_represented() -> None:
    state = set_random_salvo_mode(RuntimeShowState())

    assert state.salvo_count_mode is SalvoCountMode.RANDOM
    assert state.salvo_count == 1
    assert state.toggles.auto_launch is False


def test_invalid_salvo_counts_are_rejected() -> None:
    with pytest.raises(ValueError, match="salvo count"):
        set_fixed_salvo_mode(RuntimeShowState(), 0)

    with pytest.raises(ValueError, match="salvo count"):
        set_fixed_salvo_mode(RuntimeShowState(), 6)


def test_auto_launch_and_persistent_salvo_are_mutually_exclusive() -> None:
    state = set_fixed_salvo_mode(RuntimeShowState(), 3)

    state = toggle_auto_launch(state)

    assert state.toggles.auto_launch is True
    assert state.salvo_count_mode is SalvoCountMode.OFF
    assert state.salvo_count == 1


def test_clear_persistent_salvo_mode_returns_to_off() -> None:
    state = clear_persistent_salvo_mode(set_random_salvo_mode(RuntimeShowState()))

    assert state.salvo_count_mode is SalvoCountMode.OFF
    assert state.salvo_count == 1


def test_frame_and_seed_helpers_are_pure_and_validated() -> None:
    state = RuntimeShowState()

    assert tick_frame(state, 4).frame_count == 4
    assert advance_seed_base(state, 3).seed_base == 3
    assert state.frame_count == 0
    assert state.seed_base == 0

    with pytest.raises(ValueError, match="frames"):
        tick_frame(state, -1)

    with pytest.raises(ValueError, match="amount"):
        advance_seed_base(state, -1)


def test_show_controller_imports_without_pyxel_or_tools_dependency() -> None:
    source = inspect.getsource(show_controller)

    assert "import pyxel" not in source
    assert "tools.preview_firework_box" not in source
