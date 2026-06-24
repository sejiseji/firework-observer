from __future__ import annotations

from dataclasses import dataclass, field

from pyxel_goal_game.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from pyxel_goal_game.model.camera import Camera
from pyxel_goal_game.model.particle import Particle


@dataclass
class World:
    focus_x: int
    focus_y: int
    camera: Camera = field(default_factory=Camera)
    particles: list[Particle] = field(default_factory=list)

    @classmethod
    def initial(cls) -> World:
        return cls(focus_x=SCREEN_WIDTH // 2, focus_y=SCREEN_HEIGHT // 2)

    def clamp_focus(self) -> None:
        self.focus_x = max(0, min(SCREEN_WIDTH - 1, self.focus_x))
        self.focus_y = max(0, min(SCREEN_HEIGHT - 1, self.focus_y))
