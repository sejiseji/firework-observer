from __future__ import annotations

from random import Random

from pyxel_goal_game.systems.particle_system import ParticleSystem


def test_spawn_burst_respects_max_particles() -> None:
    particles = []
    system = ParticleSystem(random=Random(0), max_particles=10)

    system.spawn_burst(particles, x=80, y=60)

    assert len(particles) == 10


def test_particles_eventually_die() -> None:
    particles = []
    system = ParticleSystem(random=Random(0), max_particles=64)

    system.spawn_burst(particles, x=80, y=60)
    for _ in range(60):
        system.update(particles)

    assert particles == []
