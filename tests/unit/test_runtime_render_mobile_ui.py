from __future__ import annotations

import inspect

from pyxel_goal_game.runtime import render


def test_mobile_panel_uses_scaled_text_and_zoom_buttons() -> None:
    source = inspect.getsource(render)

    assert "draw_scaled_text" in source
    assert "scale=scale" in source
    assert "ZOOM+" in source
    assert "ZOOM-" in source
    assert "tap toggles for instant change" in source
    assert "APPLY" not in source


def test_runtime_render_does_not_import_tools_preview() -> None:
    source = inspect.getsource(render)

    assert "tools.preview_firework_box" not in source
    assert "preview_firework_box" not in source
