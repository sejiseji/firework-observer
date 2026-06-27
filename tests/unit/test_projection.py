from __future__ import annotations

from math import isclose, pi

from pyxel_goal_game.render.projection import rotate_2d


def test_rotate_2d_quarter_turn() -> None:
    x, y = rotate_2d(1.0, 0.0, pi / 2)
    assert isclose(x, 0.0, abs_tol=1e-9)
    assert isclose(y, 1.0, abs_tol=1e-9)
