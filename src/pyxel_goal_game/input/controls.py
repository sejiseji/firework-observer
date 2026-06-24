from __future__ import annotations

from dataclasses import dataclass

import pyxel


@dataclass(frozen=True)
class Controls:
    dx: int = 0
    dy: int = 0
    trigger: bool = False


def read_controls() -> Controls:
    dx = int(pyxel.btn(pyxel.KEY_RIGHT)) - int(pyxel.btn(pyxel.KEY_LEFT))
    dy = int(pyxel.btn(pyxel.KEY_DOWN)) - int(pyxel.btn(pyxel.KEY_UP))
    trigger = pyxel.btnp(pyxel.KEY_SPACE)
    return Controls(dx=dx, dy=dy, trigger=trigger)
