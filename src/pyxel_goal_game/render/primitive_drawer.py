from __future__ import annotations

import pyxel


def draw_soft_point(x: float, y: float, color: int) -> None:
    pyxel.pset(int(x), int(y), color)
