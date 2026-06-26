from __future__ import annotations

import importlib
import inspect

import pytest

from pyxel_goal_game.firework_presets import FireworkKind
from pyxel_goal_game.runtime import state as runtime_state
from pyxel_goal_game.runtime.state import (
    AUTO_ROTATE_SPEED_MODE_ORDER,
    FIRST_GENERATION_FIREWORK_ORDER,
    AutoRotateSpeedMode,
    RuntimeShowState,
    SalvoCountMode,
)
from pyxel_goal_game.screen_profiles import DEFAULT_SCREEN_PROFILE_NAME


def test_default_runtime_state_is_stable() -> None:
    state = RuntimeShowState()

    assert state.profile_name == DEFAULT_SCREEN_PROFILE_NAME
    assert state.selected_firework_kind is FireworkKind.KIKU
    assert state.selected_scenery_name == "city"
    assert state.auto_rotate_speed_mode is AutoRotateSpeedMode.NORMAL
    assert state.salvo_count_mode is SalvoCountMode.OFF
    assert state.salvo_count == 1
    assert state.frame_count == 0
    assert state.seed_base == 0


def test_default_toggles_are_explicit() -> None:
    toggles = RuntimeShowState().toggles

    assert toggles.random_firework_mode is False
    assert toggles.auto_launch is False
    assert toggles.height_variation is False
    assert toggles.scenery_visible is True
    assert toggles.interior_stars_visible is True
    assert toggles.auto_rotate is False


def test_first_generation_firework_order_matches_preview_cycle() -> None:
    assert FIRST_GENERATION_FIREWORK_ORDER == (
        FireworkKind.KIKU,
        FireworkKind.RING,
        FireworkKind.SPIRAL,
        FireworkKind.WILLOW,
        FireworkKind.PEONY,
        FireworkKind.MULTI_RING,
        FireworkKind.SENRIN,
        FireworkKind.HALO,
    )


def test_auto_rotate_speed_order_is_stable() -> None:
    assert AUTO_ROTATE_SPEED_MODE_ORDER == (
        AutoRotateSpeedMode.SLOW,
        AutoRotateSpeedMode.NORMAL,
        AutoRotateSpeedMode.FAST,
    )


def test_invalid_runtime_state_values_are_rejected() -> None:
    with pytest.raises(ValueError, match="auto_rotate_speed_mode"):
        RuntimeShowState(auto_rotate_speed_mode="normal")  # type: ignore[arg-type]

    with pytest.raises(ValueError, match="salvo_count"):
        RuntimeShowState(salvo_count=6)

    with pytest.raises(ValueError, match="selected_scenery_name"):
        RuntimeShowState(selected_scenery_name="mountains")


def test_runtime_scaffold_imports_without_pyxel_or_tools_dependency() -> None:
    module = importlib.import_module("pyxel_goal_game.runtime.state")

    source = inspect.getsource(module)
    assert "import pyxel" not in source
    assert "tools.preview_firework_box" not in source
    assert "tools" not in runtime_state.__name__
