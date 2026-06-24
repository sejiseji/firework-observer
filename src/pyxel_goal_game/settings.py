from dataclasses import dataclass

from pyxel_goal_game.constants import FPS, TITLE
from pyxel_goal_game.screen_profiles import DEFAULT_SCREEN_PROFILE, ScreenProfile


@dataclass(frozen=True)
class GameSettings:
    title: str = TITLE
    fps: int = FPS
    profile: ScreenProfile = DEFAULT_SCREEN_PROFILE
    quit_keys_enabled: bool = True

    @property
    def width(self) -> int:
        return self.profile.width

    @property
    def height(self) -> int:
        return self.profile.height
