from __future__ import annotations

import pyxel

from pyxel_goal_game.model.particle import Particle


def draw_particles(particles: list[Particle]) -> None:
    for particle in particles:
        if len(particle.trail) >= 2:
            previous = particle.trail[0]
            for point in particle.trail[1:]:
                pyxel.line(
                    int(previous[0]),
                    int(previous[1]),
                    int(point[0]),
                    int(point[1]),
                    max(1, particle.color - 1),
                )
                previous = point

        pyxel.pset(int(particle.x), int(particle.y), particle.color)
