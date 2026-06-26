from __future__ import annotations

import math
from dataclasses import dataclass
from random import Random

from pyxel_goal_game.camera3d import Vec3
from pyxel_goal_game.firework_presets import (
    HALO_PRESET,
    KIKU_PRESET,
    MULTI_RING_PRESET,
    PEONY_PRESET,
    RING_PRESET,
    SENRIN_PRESET,
    SPIRAL_PRESET,
    WILLOW_PRESET,
    FireworkKind,
    FireworkPreset,
    FireworkShape,
    SecondaryPreset,
    TrailPreset,
)

RING_ORIENTATION_BANK_SEED = 20260623
DEFAULT_RING_ORIENTATION_COUNT = 24
RING_ORIENTATION_BANDS = (
    (0.00, 0.30, 8),
    (0.30, 0.75, 10),
    (0.75, 0.98, 6),
)
MULTI_RING_LAYERS = (
    (32, 0.78, 0.00),
    (40, 1.00, 0.17),
    (48, 1.18, 0.34),
)
BURST_RADIUS_SCALE = 0.80
BURST_RADIUS_VARIATION_BY_KIND = {
    FireworkKind.KIKU: 0.04,
    FireworkKind.PEONY: 0.04,
    FireworkKind.RING: 0.03,
    FireworkKind.MULTI_RING: 0.03,
    FireworkKind.HALO: 0.025,
    FireworkKind.WILLOW: 0.04,
    FireworkKind.SPIRAL: 0.035,
    FireworkKind.SENRIN: 0.03,
}


@dataclass(frozen=True)
class SecondaryBurstSpec:
    delay_frames: int
    particle_count: int
    seed: int
    speed_range: tuple[float, float]
    life_range: tuple[int, int]
    palette: tuple[int, ...]
    fade_mid: int
    fade_dark: int
    tip_color: int
    drag: float
    gravity: float
    trail: TrailPreset


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
    secondary_burst: SecondaryBurstSpec | None = None


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


def generate_multi_ring_burst(
    *,
    origin: Vec3,
    seed: int,
    preset: FireworkPreset = MULTI_RING_PRESET,
    orientation_bank: RingOrientationBank | None = None,
) -> tuple[ParticleSpawnSpec, ...]:
    return generate_burst(
        preset=preset,
        origin=origin,
        seed=seed,
        orientation_bank=orientation_bank,
    )


def generate_halo_burst(
    *,
    origin: Vec3,
    seed: int,
    preset: FireworkPreset = HALO_PRESET,
    orientation_bank: RingOrientationBank | None = None,
) -> tuple[ParticleSpawnSpec, ...]:
    return generate_burst(
        preset=preset,
        origin=origin,
        seed=seed,
        orientation_bank=orientation_bank,
    )


def generate_peony_burst(
    *,
    origin: Vec3,
    seed: int,
    preset: FireworkPreset = PEONY_PRESET,
) -> tuple[ParticleSpawnSpec, ...]:
    return generate_burst(preset=preset, origin=origin, seed=seed)


def generate_senrin_burst(
    *,
    origin: Vec3,
    seed: int,
    preset: FireworkPreset = SENRIN_PRESET,
) -> tuple[ParticleSpawnSpec, ...]:
    return generate_burst(preset=preset, origin=origin, seed=seed)


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
    if preset.shape is FireworkShape.MULTI_RING:
        orientation = choose_ring_orientation(
            seed=seed,
            orientation_bank=orientation_bank,
        )
        return generate_multi_ring_shape_burst(
            preset=preset,
            origin=origin,
            rng=rng,
            orientation=orientation,
        )
    if preset.shape is FireworkShape.HALO:
        orientation = choose_ring_orientation(
            seed=seed,
            orientation_bank=orientation_bank,
        )
        return generate_halo_shape_burst(
            preset=preset,
            origin=origin,
            rng=rng,
            orientation=orientation,
        )
    if preset.shape is FireworkShape.SPIRAL:
        return generate_spiral_shape_burst(preset=preset, origin=origin, rng=rng)
    if preset.shape is FireworkShape.WILLOW:
        return generate_willow_shape_burst(preset=preset, origin=origin, rng=rng)
    if preset.shape is FireworkShape.SENRIN_SEED:
        return generate_senrin_shape_burst(preset=preset, origin=origin, rng=rng)

    msg = f"Unsupported firework shape: {preset.shape.name}"
    raise NotImplementedError(msg)


def generate_sphere_burst(
    *,
    preset: FireworkPreset,
    origin: Vec3,
    rng: Random,
) -> tuple[ParticleSpawnSpec, ...]:
    particles: list[ParticleSpawnSpec] = []
    for index in range(preset.particle_count):
        speed = varied_burst_speed(
            base_speed=rng.uniform(*preset.speed_range),
            preset=preset,
            index=index,
        )
        velocity = random_sphere_velocity(speed=speed, rng=rng)
        particles.append(
            make_particle_spec(
                origin=origin,
                velocity=velocity,
                speed=trail_speed_from_radius_speed(speed),
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
        speed = varied_burst_speed(
            base_speed=rng.uniform(*preset.speed_range),
            preset=preset,
            index=index,
        )
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
                speed=trail_speed_from_radius_speed(speed),
                preset=preset,
                rng=rng,
            )
        )
    return tuple(particles)


def generate_multi_ring_shape_burst(
    *,
    preset: FireworkPreset,
    origin: Vec3,
    rng: Random,
    orientation: RingOrientation,
) -> tuple[ParticleSpawnSpec, ...]:
    particles: list[ParticleSpawnSpec] = []
    for layer_count, speed_multiplier, theta_offset in MULTI_RING_LAYERS:
        for index in range(layer_count):
            base_speed = rng.uniform(*preset.speed_range)
            layer_speed = clamp_float(
                base_speed * speed_multiplier,
                minimum=preset.speed_range[0],
                maximum=preset.speed_range[1],
            )
            speed = varied_burst_speed(
                base_speed=layer_speed,
                preset=preset,
                index=len(particles),
            )
            velocity = ring_velocity(
                index=index,
                count=layer_count,
                speed=speed,
                rng=rng,
                orientation=orientation,
                theta_offset=theta_offset,
                thickness_scale=0.045,
            )
            particles.append(
                make_particle_spec(
                    origin=origin,
                    velocity=velocity,
                    speed=trail_speed_from_radius_speed(speed),
                    preset=preset,
                    rng=rng,
                )
            )
    if len(particles) != preset.particle_count:
        msg = "Multi-ring layer counts must match particle_count"
        raise ValueError(msg)
    return tuple(particles)


def generate_halo_shape_burst(
    *,
    preset: FireworkPreset,
    origin: Vec3,
    rng: Random,
    orientation: RingOrientation,
) -> tuple[ParticleSpawnSpec, ...]:
    particles: list[ParticleSpawnSpec] = []
    phase = rng.uniform(0.0, math.tau)
    for index in range(preset.particle_count):
        base_speed = rng.uniform(*preset.speed_range)
        wobble = 1.0 + 0.08 * math.sin(index * math.pi / 3.0 + phase)
        speed = varied_burst_speed(
            base_speed=clamp_float(
                base_speed * wobble,
                minimum=preset.speed_range[0],
                maximum=preset.speed_range[1],
            ),
            preset=preset,
            index=index,
        )
        velocity = halo_velocity(
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
                speed=trail_speed_from_radius_speed(speed),
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
        speed = varied_burst_speed(
            base_speed=rng.uniform(*preset.speed_range),
            preset=preset,
            index=index,
        )
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
                speed=trail_speed_from_radius_speed(speed),
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
    for index in range(preset.particle_count):
        speed = varied_burst_speed(
            base_speed=rng.uniform(*preset.speed_range),
            preset=preset,
            index=index,
        )
        velocity = willow_velocity(speed=speed, rng=rng)
        particles.append(
            make_particle_spec(
                origin=origin,
                velocity=velocity,
                speed=trail_speed_from_radius_speed(speed),
                preset=preset,
                rng=rng,
            )
        )
    return tuple(particles)


def generate_senrin_shape_burst(
    *,
    preset: FireworkPreset,
    origin: Vec3,
    rng: Random,
) -> tuple[ParticleSpawnSpec, ...]:
    particles: list[ParticleSpawnSpec] = []
    for index in range(preset.particle_count):
        speed = varied_burst_speed(
            base_speed=rng.uniform(*preset.speed_range),
            preset=preset,
            index=index,
        )
        velocity = random_sphere_velocity(speed=speed, rng=rng)
        velocity = Vec3(velocity.x, velocity.y * 0.75, velocity.z)
        particles.append(
            make_particle_spec(
                origin=origin,
                velocity=velocity,
                speed=trail_speed_from_radius_speed(speed),
                preset=preset,
                rng=rng,
                secondary_burst=make_secondary_burst_spec(
                    index=index,
                    preset=preset.secondary,
                    rng=rng,
                ),
            )
        )
    return tuple(particles)


def varied_burst_speed(
    *,
    base_speed: float,
    preset: FireworkPreset,
    index: int,
) -> float:
    amount = BURST_RADIUS_VARIATION_BY_KIND.get(preset.kind, 0.0)
    if amount <= 0.0:
        return base_speed * BURST_RADIUS_SCALE
    phase = (index + 1) * 2.399963229728653
    wobble = 1.0 + math.sin(phase) * amount
    bounded_speed = clamp_float(
        base_speed * wobble,
        minimum=preset.speed_range[0],
        maximum=preset.speed_range[1],
    )
    return bounded_speed * BURST_RADIUS_SCALE


def trail_speed_from_radius_speed(radius_speed: float) -> float:
    return radius_speed / BURST_RADIUS_SCALE


def make_particle_spec(
    *,
    origin: Vec3,
    velocity: Vec3,
    speed: float,
    preset: FireworkPreset,
    rng: Random,
    secondary_burst: SecondaryBurstSpec | None = None,
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
        secondary_burst=secondary_burst,
    )


def make_secondary_burst_spec(
    *,
    index: int,
    preset: SecondaryPreset | None,
    rng: Random,
) -> SecondaryBurstSpec | None:
    if preset is None or rng.random() >= preset.rate:
        return None
    return SecondaryBurstSpec(
        delay_frames=rng.randint(*preset.delay_range),
        particle_count=rng.randint(*preset.count_range),
        seed=rng.randrange(1_000_000_000) + index,
        speed_range=preset.speed_range,
        life_range=preset.life_range,
        palette=preset.palette,
        fade_mid=preset.fade_mid,
        fade_dark=preset.fade_dark,
        tip_color=preset.tip_color,
        drag=preset.drag,
        gravity=preset.gravity,
        trail=preset.trail,
    )


def generate_secondary_burst(
    *,
    origin: Vec3,
    spec: SecondaryBurstSpec,
) -> tuple[ParticleSpawnSpec, ...]:
    rng = Random(spec.seed)
    particles: list[ParticleSpawnSpec] = []
    for _ in range(spec.particle_count):
        speed = rng.uniform(*spec.speed_range)
        velocity = random_sphere_velocity(speed=speed, rng=rng)
        particles.append(make_secondary_particle_spec(origin, velocity, speed, spec, rng))
    return tuple(particles)


def make_secondary_particle_spec(
    origin: Vec3,
    velocity: Vec3,
    speed: float,
    spec: SecondaryBurstSpec,
    rng: Random,
) -> ParticleSpawnSpec:
    life = rng.randint(*spec.life_range)
    has_trail = speed >= spec.trail.speed_threshold and rng.random() < spec.trail.rate
    return ParticleSpawnSpec(
        position=origin,
        velocity=velocity,
        life=life,
        color=rng.choice(spec.palette),
        fade_mid=spec.fade_mid,
        fade_dark=spec.fade_dark,
        tip_color=spec.tip_color,
        drag=spec.drag,
        gravity=spec.gravity,
        has_trail=has_trail,
        trail_until_age=int(life * spec.trail.early_ratio),
        trail_strength=2 if speed >= spec.trail.strong_speed else 1,
        trail_draw_every=spec.trail.draw_every,
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
    theta_offset: float = 0.0,
    thickness_scale: float = 0.06,
) -> Vec3:
    theta = index / count * math.tau
    theta += theta_offset
    theta += rng.uniform(-0.025, 0.025)
    thickness = rng.uniform(-thickness_scale, thickness_scale)
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


def halo_velocity(
    *,
    index: int,
    count: int,
    speed: float,
    rng: Random,
    orientation: RingOrientation,
) -> Vec3:
    theta = index / count * math.tau
    theta += rng.uniform(-0.018, 0.018)
    thickness = rng.uniform(-0.035, 0.035)
    ring_direction = add_vec3(
        scale_vec3(orientation.basis_u, math.cos(theta)),
        scale_vec3(orientation.basis_v, math.sin(theta)),
    )
    direction = normalize_vec3(
        add_vec3(
            ring_direction,
            scale_vec3(orientation.normal, thickness),
        )
    )
    return scale_vec3(direction, speed)


def clamp_float(value: float, *, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))


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
