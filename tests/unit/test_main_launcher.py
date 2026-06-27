from __future__ import annotations

from pathlib import Path


def test_main_py_is_thin_runtime_launcher() -> None:
    source = Path("main.py").read_text(encoding="utf-8")

    assert "pyxel_goal_game.runtime.app import main as runtime_main" in source
    assert "tools.preview_firework_box" not in source
    assert "preview_firework_box" not in source
    assert "class " not in source
    assert "pyxel.run" not in source
    assert len(source.splitlines()) <= 24
