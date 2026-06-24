from __future__ import annotations

import math
from random import Random

from pyxel_goal_game.model.firework import DEFAULT_FIREWORK_PRESET, FireworkPreset
from pyxel_goal_game.model.particle import Particle


class ParticleSystem:
    def __init__(self, random: Random, max_particles: int = 256) -> None:
        self.random = random
        self.max_particles = max_particles

    def spawn_burst(
        self,
        particles: list[Particle],
        *,
        x: float,
        y: float,
        preset: FireworkPreset = DEFAULT_FIREWORK_PRESET,
    ) -> None:
        free_slots = max(0, self.max_particles - len(particles))
        count = min(preset.particle_count, free_slots)

        for index in range(count):
            angle = (math.tau * index / max(1, count)) + self.random.uniform(-0.05, 0.05)
            speed = preset.speed * self.random.uniform(0.75, 1.25)
            particles.append(
                Particle(
                    x=x,
                    y=y,
                    vx=math.cos(angle) * speed,
                    vy=math.sin(angle) * speed,
                    life=45,
                    color=preset.color,
                )
            )

    def update(self, particles: list[Particle]) -> None:
        alive: list[Particle] = []

        for particle in particles:
            particle.trail.append((particle.x, particle.y))
            if len(particle.trail) > DEFAULT_FIREWORK_PRESET.trail_length:
                particle.trail.pop(0)

            particle.x += particle.vx
            particle.y += particle.vy
            particle.vy += 0.015
            particle.life -= 1

            if particle.alive:
                alive.append(particle)

        particles[:] = alive
