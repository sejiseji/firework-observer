from __future__ import annotations

import pyxel

from pyxel_goal_game.input.controls import read_controls
from pyxel_goal_game.scenes.observer import ObserverScene
from pyxel_goal_game.settings import GameSettings


class GameLoop:
    def __init__(self, settings: GameSettings) -> None:
        self.settings = settings
        self.scene = ObserverScene()

    def update(self) -> None:
        if self.settings.quit_keys_enabled and (
            pyxel.btnp(pyxel.KEY_Q) or pyxel.btnp(pyxel.KEY_ESCAPE)
        ):
            pyxel.quit()

        controls = read_controls()
        self.scene.update(controls)

    def draw(self) -> None:
        pyxel.cls(0)
        self.scene.draw()
