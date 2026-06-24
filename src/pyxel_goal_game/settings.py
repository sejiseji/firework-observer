from dataclasses import dataclass

from pyxel_goal_game.constants import FPS, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE


@dataclass(frozen=True)
class GameSettings:
    title: str = TITLE
    width: int = SCREEN_WIDTH
    height: int = SCREEN_HEIGHT
    fps: int = FPS
    quit_keys_enabled: bool = True
