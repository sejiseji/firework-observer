from __future__ import annotations

from dataclasses import dataclass, field

from pyxel_goal_game.model.camera import Camera
from pyxel_goal_game.model.particle import Particle
from pyxel_goal_game.screen_profiles import DEFAULT_SCREEN_PROFILE


@dataclass
class World:
    focus_x: int
    focus_y: int
    width: int
    height: int
    camera: Camera = field(default_factory=Camera)
    particles: list[Particle] = field(default_factory=list)

    @classmethod
    def initial(
        cls,
        *,
        width: int = DEFAULT_SCREEN_PROFILE.width,
        height: int = DEFAULT_SCREEN_PROFILE.height,
    ) -> World:
        return cls(focus_x=width // 2, focus_y=height // 2, width=width, height=height)

    def clamp_focus(self) -> None:
        self.focus_x = max(0, min(self.width - 1, self.focus_x))
        self.focus_y = max(0, min(self.height - 1, self.focus_y))
