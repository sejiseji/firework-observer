from __future__ import annotations

import pyxel

from pyxel_goal_game.loop import GameLoop
from pyxel_goal_game.settings import GameSettings


class App:
    """Pyxel boundary.

    Keep Pyxel initialization and pyxel.run here so most game logic can remain testable.
    """

    def __init__(self, settings: GameSettings | None = None) -> None:
        self.settings = settings or GameSettings()
        pyxel.init(
            self.settings.width,
            self.settings.height,
            title=self.settings.title,
            fps=self.settings.fps,
        )
        self.loop = GameLoop(settings=self.settings)

    def run(self) -> None:
        pyxel.run(self.loop.update, self.loop.draw)


def main() -> None:
    App().run()
