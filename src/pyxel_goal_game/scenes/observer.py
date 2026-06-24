from __future__ import annotations

from random import Random

import pyxel

from pyxel_goal_game.input.controls import Controls
from pyxel_goal_game.model.world import World
from pyxel_goal_game.render.hud_renderer import draw_hud
from pyxel_goal_game.render.particle_renderer import draw_particles
from pyxel_goal_game.systems.particle_system import ParticleSystem


class ObserverScene:
    def __init__(self) -> None:
        self.world = World.initial()
        self.particle_system = ParticleSystem(random=Random(0))

    def update(self, controls: Controls) -> None:
        self.world.focus_x += controls.dx
        self.world.focus_y += controls.dy
        self.world.clamp_focus()

        if controls.trigger:
            self.particle_system.spawn_burst(
                self.world.particles,
                x=float(self.world.focus_x),
                y=float(self.world.focus_y),
            )

        self.particle_system.update(self.world.particles)

    def draw(self) -> None:
        pyxel.circ(self.world.focus_x, self.world.focus_y, 2, 11)
        draw_particles(self.world.particles)
        draw_hud(self.world)
