from __future__ import annotations

import math
from dataclasses import dataclass
from random import Random

from pyxel_goal_game.camera3d import Vec3
from pyxel_goal_game.firework_presets import (
    KIKU_PRESET,
    RING_PRESET,
    SPIRAL_PRESET,
    WILLOW_PRESET,
    FireworkPreset,
    FireworkShape,
)

RING_ORIENTATION_BANK_SEED = 20260623
DEFAULT_RING_ORIENTATION_COUNT = 24
RING_ORIENTATION_BANDS = (
    (0.00, 0.30, 8),
    (0.30, 0.75, 10),
    (0.75, 0.98, 6),
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


@dataclass(frozen=True)
class RingOrientation:
    normal: Vec3
    basis_u: Vec3
    basis_v: Vec3
    azimuth: float
    normal_y: float
    roll: float


@dataclass(frozen=True)
class RingOrientationBank:
    orientations: tuple[RingOrientation, ...]

    def __post_init__(self) -> None:
        if not self.orientations:
            msg = "orientations must not be empty"
            raise ValueError(msg)

    def choose(self, seed: int) -> RingOrientation:
        rng = Random(seed)
        return self.orientations[rng.randrange(len(self.orientations))]


def generate_kiku_burst(
    *,
    origin: Vec3,
    seed: int,
    preset: FireworkPreset = KIKU_PRESET,
) -> tuple[ParticleSpawnSpec, ...]:
    return generate_burst(preset=preset, origin=origin, seed=seed)


def generate_ring_burst(
    *,
    origin: Vec3,
    seed: int,
    preset: FireworkPreset = RING_PRESET,
    orientation_bank: RingOrientationBank | None = None,
) -> tuple[ParticleSpawnSpec, ...]:
    return generate_burst(
        preset=preset,
        origin=origin,
        seed=seed,
        orientation_bank=orientation_bank,
    )


def generate_spiral_burst(
    *,
    origin: Vec3,
    seed: int,
    preset: FireworkPreset = SPIRAL_PRESET,
) -> tuple[ParticleSpawnSpec, ...]:
    return generate_burst(preset=preset, origin=origin, seed=seed)


def generate_willow_burst(
    *,
    origin: Vec3,
    seed: int,
    preset: FireworkPreset = WILLOW_PRESET,
) -> tuple[ParticleSpawnSpec, ...]:
    return generate_burst(preset=preset, origin=origin, seed=seed)


def generate_burst(
    *,
    preset: FireworkPreset,
    origin: Vec3,
    seed: int,
    orientation_bank: RingOrientationBank | None = None,
) -> tuple[ParticleSpawnSpec, ...]:
    rng = Random(seed)
    if preset.shape is FireworkShape.SPHERE:
        return generate_sphere_burst(preset=preset, origin=origin, rng=rng)
    if preset.shape is FireworkShape.RING:
        orientation = choose_ring_orientation(
            seed=seed,
            orientation_bank=orientation_bank,
        )
        return generate_ring_shape_burst(
            preset=preset,
            origin=origin,
            rng=rng,
            orientation=orientation,
        )
    if preset.shape is FireworkShape.SPIRAL:
        return generate_spiral_shape_burst(preset=preset, origin=origin, rng=rng)
    if preset.shape is FireworkShape.WILLOW:
        return generate_willow_shape_burst(preset=preset, origin=origin, rng=rng)

    msg = f"Unsupported firework shape: {preset.shape.name}"
    raise NotImplementedError(msg)


def generate_sphere_burst(
    *,
    preset: FireworkPreset,
    origin: Vec3,
    rng: Random,
) -> tuple[ParticleSpawnSpec, ...]:
    particles: list[ParticleSpawnSpec] = []
    for _ in range(preset.particle_count):
        speed = rng.uniform(*preset.speed_range)
        velocity = random_sphere_velocity(speed=speed, rng=rng)
        particles.append(
            make_particle_spec(
                origin=origin,
                velocity=velocity,
                speed=speed,
                preset=preset,
                rng=rng,
            )
        )
    return tuple(particles)


def generate_ring_shape_burst(
    *,
    preset: FireworkPreset,
    origin: Vec3,
    rng: Random,
    orientation: RingOrientation,
) -> tuple[ParticleSpawnSpec, ...]:
    particles: list[ParticleSpawnSpec] = []
    for index in range(preset.particle_count):
        speed = rng.uniform(*preset.speed_range)
        velocity = ring_velocity(
            index=index,
            count=preset.particle_count,
            speed=speed,
            rng=rng,
            orientation=orientation,
        )
        particles.append(
            make_particle_spec(
                origin=origin,
                velocity=velocity,
                speed=speed,
                preset=preset,
                rng=rng,
            )
        )
    return tuple(particles)


def generate_spiral_shape_burst(
    *,
    preset: FireworkPreset,
    origin: Vec3,
    rng: Random,
) -> tuple[ParticleSpawnSpec, ...]:
    particles: list[ParticleSpawnSpec] = []
    for index in range(preset.particle_count):
        speed = rng.uniform(*preset.speed_range)
        velocity = spiral_velocity(
            index=index,
            count=preset.particle_count,
            speed=speed,
            rng=rng,
        )
        particles.append(
            make_particle_spec(
                origin=origin,
                velocity=velocity,
                speed=speed,
                preset=preset,
                rng=rng,
            )
        )
    return tuple(particles)


def generate_willow_shape_burst(
    *,
    preset: FireworkPreset,
    origin: Vec3,
    rng: Random,
) -> tuple[ParticleSpawnSpec, ...]:
    particles: list[ParticleSpawnSpec] = []
    for _ in range(preset.particle_count):
        speed = rng.uniform(*preset.speed_range)
        velocity = willow_velocity(speed=speed, rng=rng)
        particles.append(
            make_particle_spec(
                origin=origin,
                velocity=velocity,
                speed=speed,
                preset=preset,
                rng=rng,
            )
        )
    return tuple(particles)


def make_particle_spec(
    *,
    origin: Vec3,
    velocity: Vec3,
    speed: float,
    preset: FireworkPreset,
    rng: Random,
) -> ParticleSpawnSpec:
    life = rng.randint(*preset.life_range)
    has_trail = (
        speed >= preset.trail.speed_threshold
        and rng.random() < preset.trail.rate
    )
    return ParticleSpawnSpec(
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


def random_sphere_velocity(*, speed: float, rng: Random) -> Vec3:
    theta = rng.uniform(0.0, math.tau)
    u = rng.uniform(-1.0, 1.0)
    r = math.sqrt(max(0.0, 1.0 - u * u))
    return Vec3(
        x=math.cos(theta) * r * speed,
        y=u * speed,
        z=math.sin(theta) * r * speed,
    )


def ring_velocity(
    *,
    index: int,
    count: int,
    speed: float,
    rng: Random,
    orientation: RingOrientation,
) -> Vec3:
    theta = index / count * math.tau
    theta += rng.uniform(-0.025, 0.025)
    thickness = rng.uniform(-0.06, 0.06)
    planar_scale = math.sqrt(max(0.0, 1.0 - thickness * thickness))
    plane_direction = add_vec3(
        scale_vec3(orientation.basis_u, math.cos(theta)),
        scale_vec3(orientation.basis_v, math.sin(theta)),
    )
    direction = add_vec3(
        scale_vec3(plane_direction, planar_scale),
        scale_vec3(orientation.normal, thickness),
    )
    return scale_vec3(direction, speed)


def spiral_velocity(*, index: int, count: int, speed: float, rng: Random) -> Vec3:
    t = index / max(1, count - 1)
    theta = index * 0.42
    theta += rng.uniform(-0.05, 0.05)
    radius = 0.72 + 0.28 * t
    direction = Vec3(
        x=math.cos(theta) * radius,
        y=(t - 0.5) * 1.15 + rng.uniform(-0.08, 0.08),
        z=math.sin(theta) * radius,
    )
    return scale_vec3(normalize_vec3(direction), speed)


def willow_velocity(*, speed: float, rng: Random) -> Vec3:
    theta = rng.uniform(0.0, math.tau)
    radial = rng.uniform(0.35, 1.0) * speed
    return Vec3(
        x=math.cos(theta) * radial,
        y=rng.uniform(-0.15, 0.65) * speed,
        z=math.sin(theta) * radial,
    )


def choose_ring_orientation(
    *,
    seed: int,
    orientation_bank: RingOrientationBank | None,
) -> RingOrientation:
    if orientation_bank is not None:
        return orientation_bank.choose(seed)
    return make_ring_orientation(Random(seed ^ 0xA17E))


def build_ring_orientation_bank(
    *,
    seed: int = RING_ORIENTATION_BANK_SEED,
    count: int = DEFAULT_RING_ORIENTATION_COUNT,
) -> RingOrientationBank:
    if count < 1:
        msg = "count must be at least 1"
        raise ValueError(msg)
    rng = Random(seed)
    orientations: list[RingOrientation] = []
    for min_y, max_y, band_count in RING_ORIENTATION_BANDS:
        for _ in range(scaled_band_count(count=count, band_count=band_count)):
            orientations.append(
                make_ring_orientation_in_band(rng=rng, min_y=min_y, max_y=max_y)
            )
    while len(orientations) < count:
        orientations.append(make_ring_orientation(rng))
    return RingOrientationBank(orientations=tuple(orientations[:count]))


def scaled_band_count(*, count: int, band_count: int) -> int:
    if count == DEFAULT_RING_ORIENTATION_COUNT:
        return band_count
    return max(1, round(count * band_count / DEFAULT_RING_ORIENTATION_COUNT))


def make_ring_orientation(rng: Random) -> RingOrientation:
    band = RING_ORIENTATION_BANDS[rng.randrange(len(RING_ORIENTATION_BANDS))]
    return make_ring_orientation_in_band(rng=rng, min_y=band[0], max_y=band[1])


def make_ring_orientation_in_band(
    *,
    rng: Random,
    min_y: float,
    max_y: float,
) -> RingOrientation:
    normal_y = rng.uniform(min_y, max_y)
    azimuth = rng.uniform(0.0, math.tau)
    horizontal = math.sqrt(max(0.0, 1.0 - normal_y * normal_y))
    normal = Vec3(
        x=math.cos(azimuth) * horizontal,
        y=normal_y,
        z=math.sin(azimuth) * horizontal,
    )
    roll = rng.uniform(0.0, math.tau)
    basis_u, basis_v = make_ring_basis(normal=normal, roll=roll)
    return RingOrientation(
        normal=normal,
        basis_u=basis_u,
        basis_v=basis_v,
        azimuth=azimuth,
        normal_y=normal_y,
        roll=roll,
    )


def make_ring_basis(*, normal: Vec3, roll: float) -> tuple[Vec3, Vec3]:
    reference = Vec3(1.0, 0.0, 0.0) if abs(normal.y) > 0.92 else Vec3(0.0, 1.0, 0.0)
    base_u = normalize_vec3(cross_vec3(reference, normal))
    base_v = normalize_vec3(cross_vec3(normal, base_u))
    rolled_u = add_vec3(
        scale_vec3(base_u, math.cos(roll)),
        scale_vec3(base_v, math.sin(roll)),
    )
    rolled_v = add_vec3(
        scale_vec3(base_u, -math.sin(roll)),
        scale_vec3(base_v, math.cos(roll)),
    )
    return normalize_vec3(rolled_u), normalize_vec3(rolled_v)


def add_vec3(first: Vec3, second: Vec3) -> Vec3:
    return Vec3(
        x=first.x + second.x,
        y=first.y + second.y,
        z=first.z + second.z,
    )


def scale_vec3(vector: Vec3, scale: float) -> Vec3:
    return Vec3(x=vector.x * scale, y=vector.y * scale, z=vector.z * scale)


def dot_vec3(first: Vec3, second: Vec3) -> float:
    return first.x * second.x + first.y * second.y + first.z * second.z


def cross_vec3(first: Vec3, second: Vec3) -> Vec3:
    return Vec3(
        x=first.y * second.z - first.z * second.y,
        y=first.z * second.x - first.x * second.z,
        z=first.x * second.y - first.y * second.x,
    )


def length_vec3(vector: Vec3) -> float:
    return math.sqrt(dot_vec3(vector, vector))


def normalize_vec3(vector: Vec3) -> Vec3:
    length = length_vec3(vector)
    if length <= 0.0:
        msg = "Cannot normalize a zero-length vector"
        raise ValueError(msg)
    return scale_vec3(vector, 1.0 / length)
