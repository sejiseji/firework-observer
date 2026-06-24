from __future__ import annotations

import pyxel

from pyxel_goal_game.input.controls import Controls
from pyxel_goal_game.scenes.base import Scene


class TitleScene(Scene):
    def update(self, controls: Controls) -> None:
        _ = controls

    def draw(self) -> None:
        pyxel.text(32, 54, "PYXEL GOAL GAME", 7)
