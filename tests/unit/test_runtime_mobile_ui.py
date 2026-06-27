from __future__ import annotations

import importlib
import inspect

import pytest

from pyxel_goal_game.runtime.mobile_ui import (
    MOBILE_TOGGLE_SPECS,
    MobilePanelDraft,
    menu_button_rect,
    panel_rect,
    zoom_in_button_rect,
    zoom_out_button_rect,
)
from pyxel_goal_game.runtime.state import AutoRotateSpeedMode, RuntimeShowState


def test_mobile_ui_imports_without_pyxel_or_tools_dependency() -> None:
    module = importlib.import_module("pyxel_goal_game.runtime.mobile_ui")
    source = inspect.getsource(module)

    assert "import pyxel" not in source
    assert "tools.preview_firework_box" not in source
    assert "preview_firework_box" not in source


def test_mobile_panel_draft_captures_runtime_state() -> None:
    state = RuntimeShowState()
    draft = MobilePanelDraft.from_state(state)

    assert draft.random_firework_mode is state.toggles.random_firework_mode
    assert draft.height_variation is state.toggles.height_variation
    assert draft.auto_launch is state.toggles.auto_launch
    assert draft.auto_rotate is state.toggles.auto_rotate
    assert draft.interior_stars_visible is state.toggles.interior_stars_visible
    assert draft.ufo_enabled is state.toggles.ufo_enabled
    assert draft.audio_enabled is state.toggles.audio_enabled
    assert draft.scenery_visible is state.toggles.scenery_visible
    assert draft.auto_rotate_speed_mode is AutoRotateSpeedMode.NORMAL


def test_mobile_panel_draft_toggles_known_fields_only() -> None:
    draft = MobilePanelDraft.from_state(RuntimeShowState())

    for spec in MOBILE_TOGGLE_SPECS:
        updated = draft.toggle(spec.key)
        assert getattr(updated, spec.key) is not getattr(draft, spec.key)

    with pytest.raises(ValueError, match="unknown mobile toggle"):
        draft.toggle("not_a_real_toggle")


def test_mobile_panel_draft_cycles_speed_modes() -> None:
    draft = MobilePanelDraft.from_state(RuntimeShowState())

    assert draft.auto_rotate_speed_mode is AutoRotateSpeedMode.NORMAL
    draft = draft.cycle_auto_rotate_speed()
    assert draft.auto_rotate_speed_mode is AutoRotateSpeedMode.FAST
    draft = draft.cycle_auto_rotate_speed()
    assert draft.auto_rotate_speed_mode is AutoRotateSpeedMode.SLOW


def test_mobile_layout_stays_inside_portrait_profile() -> None:
    menu = menu_button_rect(236)
    panel = panel_rect(236, 512)
    zoom_in = zoom_in_button_rect(panel)
    zoom_out = zoom_out_button_rect(panel)

    assert 0 <= menu.x < 236
    assert 0 <= menu.y < 512
    assert menu.x + menu.width <= 236
    assert panel.x + panel.width <= 236
    assert panel.y + panel.height <= 512
    assert panel.contains(zoom_in.x, zoom_in.y)
    assert panel.contains(zoom_out.x + zoom_out.width - 1, zoom_out.y + zoom_out.height - 1)
