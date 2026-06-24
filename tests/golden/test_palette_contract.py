from __future__ import annotations

from pyxel_goal_game.render import palette


def test_palette_contract_values_are_pyxel_colors() -> None:
    values = [
        palette.BACKGROUND_COLOR,
        palette.FOCUS_COLOR,
        palette.TEXT_COLOR,
    ]
    assert all(0 <= value <= 15 for value in values)
