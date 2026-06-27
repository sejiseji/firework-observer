from __future__ import annotations

from pyxel_goal_game.model.particle import Particle


def get_visible_trail(particle: Particle) -> list[tuple[float, float]]:
    return particle.trail
