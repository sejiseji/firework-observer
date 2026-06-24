from __future__ import annotations

import math
from dataclasses import dataclass
from random import Random

from pyxel_goal_game.camera3d import Vec3
from pyxel_goal_game.firework_presets import (
    KIKU_PRESET,
    FireworkPreset,
    FireworkShape,
)


@dataclass(frozen=True)
class ParticleSpawnSpec:
    position: Vec3
    velocity: Vec3
    life: int
    color: int
    fade_mid: int
    fade_dark: int
    tip_color: int
    drag: float
    gravity: float
    has_trail: bool
    trail_until_age: int
    trail_strength: int
    trail_draw_every: int


def generate_kiku_burst(
    *,
    origin: Vec3,
    seed: int,
    preset: FireworkPreset = KIKU_PRESET,
) -> tuple[ParticleSpawnSpec, ...]:
    return generate_burst(preset=preset, origin=origin, seed=seed)


def generate_burst(
    *,
    preset: FireworkPreset,
    origin: Vec3,
    seed: int,
) -> tuple[ParticleSpawnSpec, ...]:
    if preset.shape is not FireworkShape.SPHERE:
        msg = f"Unsupported firework shape: {preset.shape.name}"
        raise NotImplementedError(msg)

    rng = Random(seed)
    particles: list[ParticleSpawnSpec] = []
    for _ in range(preset.particle_count):
        speed = rng.uniform(*preset.speed_range)
        velocity = random_sphere_velocity(speed=speed, rng=rng)
        life = rng.randint(*preset.life_range)
        has_trail = (
            speed >= preset.trail.speed_threshold
            and rng.random() < preset.trail.rate
        )
        particles.append(
            ParticleSpawnSpec(
                position=origin,
                velocity=velocity,
                life=life,
                color=rng.choice(preset.palette),
                fade_mid=preset.fade_mid,
                fade_dark=preset.fade_dark,
                tip_color=preset.tip_color,
                drag=preset.drag,
                gravity=preset.gravity,
                has_trail=has_trail,
                trail_until_age=int(life * preset.trail.early_ratio),
                trail_strength=2 if speed >= preset.trail.strong_speed else 1,
                trail_draw_every=preset.trail.draw_every,
            )
        )
    return tuple(particles)


def random_sphere_velocity(*, speed: float, rng: Random) -> Vec3:
    theta = rng.uniform(0.0, math.tau)
    u = rng.uniform(-1.0, 1.0)
    r = math.sqrt(max(0.0, 1.0 - u * u))
    return Vec3(
        x=math.cos(theta) * r * speed,
        y=u * speed,
        z=math.sin(theta) * r * speed,
    )
