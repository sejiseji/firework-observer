from __future__ import annotations

import inspect
from pathlib import Path

from pyxel_goal_game.runtime import app, effects, input, render


def test_runtime_app_modules_do_not_import_tools_preview() -> None:
    for module in (app, effects, input, render):
        source = inspect.getsource(module)
        assert "tools.preview_firework_box" not in source
        assert "preview_firework_box" not in source


def test_runtime_app_import_does_not_construct_pyxel_app() -> None:
    assert hasattr(app, "RuntimeApp")
    assert hasattr(app, "main")


def test_official_runtime_launcher_exists() -> None:
    assert Path("scripts/run_runtime_app.py").exists()
