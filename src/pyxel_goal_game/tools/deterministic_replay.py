from __future__ import annotations

from random import Random

from pyxel_goal_game.model.particle import Particle
from pyxel_goal_game.systems.particle_system import ParticleSystem


def make_sample_replay(seed: int = 0) -> list[Particle]:
    particles: list[Particle] = []
    system = ParticleSystem(random=Random(seed))
    system.spawn_burst(particles, x=80, y=60)
    for _ in range(10):
        system.update(particles)
    return particles
