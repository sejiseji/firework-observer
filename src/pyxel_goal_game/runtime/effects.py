from __future__ import annotations

import math
from collections import deque
from dataclasses import dataclass
from random import Random

from pyxel_goal_game.camera3d import Vec3
from pyxel_goal_game.firework_bursts import (
    ParticleSpawnSpec,
    RingOrientationBank,
    SecondaryBurstSpec,
    generate_burst,
    generate_secondary_burst,
)
from pyxel_goal_game.firework_presets import (
    HALO_PRESET,
    KIKU_PRESET,
    LONG_WILLOW_PRESET,
    MULTI_RING_PRESET,
    PEONY_PRESET,
    RING_PRESET,
    SENRIN_PRESET,
    SPHERE_BLOOM_PRESET,
    SPIRAL_PRESET,
    WILLOW_PRESET,
    FireworkKind,
    FireworkPreset,
    TrailPreset,
)

SHELL_MIN_FLIGHT_FRAMES = 96
SHELL_MAX_FLIGHT_FRAMES = 180
FIREWORK_SHELL_TAIL_COLORS_NEW_TO_OLD = (7, 7, 7, 10, 10, 4, 4)
FIREWORK_SHELL_TAIL_LENGTH = len(FIREWORK_SHELL_TAIL_COLORS_NEW_TO_OLD)
ACCENT_RAY_FRAMES = 12
GLITTER_RESIDUE_LIFE_RANGE = (14, 24)
GLITTER_RESIDUE_MAX = 96
MINI_BURST_GARNISH_CHANCE = 0.45
MINI_BURST_GARNISH_COUNT_RANGE = (2, 5)
MINI_BURST_GARNISH_DELAY_RANGE = (14, 40)
MINI_BURST_GARNISH_OFFSET_RANGE = (3.0, 10.0)
MINI_BURST_GARNISH_PARTICLE_RANGE = (10, 18)
MINI_BURST_GARNISH_ELIGIBLE_KINDS = frozenset(
    {
        FireworkKind.KIKU,
        FireworkKind.SPHERE_BLOOM,
        FireworkKind.PEONY,
        FireworkKind.MULTI_RING,
    }
)

FIREWORK_PRESETS_BY_KIND: dict[FireworkKind, FireworkPreset] = {
    FireworkKind.KIKU: KIKU_PRESET,
    FireworkKind.SPHERE_BLOOM: SPHERE_BLOOM_PRESET,
    FireworkKind.RING: RING_PRESET,
    FireworkKind.SPIRAL: SPIRAL_PRESET,
    FireworkKind.WILLOW: WILLOW_PRESET,
    FireworkKind.LONG_WILLOW: LONG_WILLOW_PRESET,
    FireworkKind.PEONY: PEONY_PRESET,
    FireworkKind.MULTI_RING: MULTI_RING_PRESET,
    FireworkKind.SENRIN: SENRIN_PRESET,
    FireworkKind.HALO: HALO_PRESET,
}

BURST_ACCENT_STYLES = {
    FireworkKind.KIKU: (10, 9, 7),
    FireworkKind.SPHERE_BLOOM: (7, 10, 12),
    FireworkKind.RING: (12, 6, 7),
    FireworkKind.SPIRAL: (11, 10, 7),
    FireworkKind.WILLOW: (10, 9, 4),
    FireworkKind.LONG_WILLOW: (10, 9, 4),
    FireworkKind.PEONY: (14, 8, 10),
    FireworkKind.MULTI_RING: (12, 6, 10),
    FireworkKind.SENRIN: (7, 10, 14),
    FireworkKind.HALO: (7, 10, 12),
}

ACCENT_COUNTS = {
    FireworkKind.KIKU: 8,
    FireworkKind.SPHERE_BLOOM: 7,
    FireworkKind.RING: 6,
    FireworkKind.SPIRAL: 8,
    FireworkKind.WILLOW: 5,
    FireworkKind.LONG_WILLOW: 4,
    FireworkKind.PEONY: 10,
    FireworkKind.MULTI_RING: 6,
    FireworkKind.SENRIN: 4,
    FireworkKind.HALO: 5,
}

GLITTER_RESIDUE_COUNTS = {
    FireworkKind.KIKU: 8,
    FireworkKind.SPHERE_BLOOM: 6,
    FireworkKind.RING: 6,
    FireworkKind.SPIRAL: 7,
    FireworkKind.WILLOW: 5,
    FireworkKind.LONG_WILLOW: 4,
    FireworkKind.PEONY: 8,
    FireworkKind.MULTI_RING: 6,
    FireworkKind.SENRIN: 2,
    FireworkKind.HALO: 5,
}


@dataclass(frozen=True)
class ActiveShell:
    launch_frame: int
    flight_frames: int
    firework_kind: FireworkKind
    launch_position: Vec3
    burst_position: Vec3
    seed: int
    history: deque[Vec3]

    def has_started(self, frame: int) -> bool:
        return frame >= self.launch_frame

    def is_complete(self, frame: int) -> bool:
        return frame >= self.launch_frame + self.flight_frames

    def current_position(self, frame: int) -> Vec3:
        elapsed = max(0, frame - self.launch_frame)
        progress = min(1.0, elapsed / self.flight_frames)
        return Vec3(
            x=self.launch_position.x
            + (self.burst_position.x - self.launch_position.x) * progress,
            y=self.launch_position.y
            + (self.burst_position.y - self.launch_position.y) * progress,
            z=self.launch_position.z
            + (self.burst_position.z - self.launch_position.z) * progress,
        )


@dataclass
class ActiveParticle:
    position: Vec3
    previous_position: Vec3
    velocity: Vec3
    life: int
    max_life: int
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
    secondary_triggered: bool = False
    accent_origin: Vec3 | None = None
    accent_until_age: int = 0
    accent_color: int = 0

    @classmethod
    def from_spawn(
        cls,
        spec: ParticleSpawnSpec,
        *,
        accent_origin: Vec3 | None = None,
        accent_until_age: int = 0,
        accent_color: int = 0,
    ) -> ActiveParticle:
        return cls(
            position=spec.position,
            previous_position=spec.position,
            velocity=spec.velocity,
            life=spec.life,
            max_life=spec.life,
            color=spec.color,
            fade_mid=spec.fade_mid,
            fade_dark=spec.fade_dark,
            tip_color=spec.tip_color,
            drag=spec.drag,
            gravity=spec.gravity,
            has_trail=spec.has_trail,
            trail_until_age=spec.trail_until_age,
            trail_strength=spec.trail_strength,
            trail_draw_every=spec.trail_draw_every,
            secondary_burst=spec.secondary_burst,
            accent_origin=accent_origin,
            accent_until_age=accent_until_age,
            accent_color=accent_color,
        )

    @property
    def age(self) -> int:
        return self.max_life - self.life

    def step(self) -> None:
        self.previous_position = self.position
        self.position = Vec3(
            self.position.x + self.velocity.x,
            self.position.y + self.velocity.y,
            self.position.z + self.velocity.z,
        )
        self.velocity = Vec3(
            self.velocity.x * self.drag,
            self.velocity.y * self.drag + self.gravity,
            self.velocity.z * self.drag,
        )
        self.life -= 1

    def draw_color(self) -> int:
        life_ratio = self.life / self.max_life
        if life_ratio > 0.55:
            return self.color
        if life_ratio > 0.25:
            return self.fade_mid
        return self.fade_dark

    def should_draw_trail(self, frame_count: int) -> bool:
        return (
            self.has_trail
            and self.age < self.trail_until_age
            and frame_count % self.trail_draw_every == 0
        )

    def is_alive(self) -> bool:
        return self.life > 0


@dataclass
class GlitterResidue:
    position: Vec3
    velocity: Vec3
    life: int
    max_life: int
    phase: int

    @property
    def age(self) -> int:
        return self.max_life - self.life

    def step(self) -> None:
        self.position = Vec3(
            self.position.x + self.velocity.x,
            self.position.y + self.velocity.y,
            self.position.z + self.velocity.z,
        )
        self.velocity = Vec3(
            self.velocity.x * 0.94,
            self.velocity.y * 0.94 - 0.004,
            self.velocity.z * 0.94,
        )
        self.life -= 1

    def draw_color(self) -> int | None:
        if (self.age + self.phase) % 7 == 0:
            return None
        if self.life > self.max_life * 0.62:
            return 7
        if self.life > self.max_life * 0.30:
            return 10
        return 5

    def is_alive(self) -> bool:
        return self.life > 0


@dataclass(frozen=True)
class DelayedMiniBurst:
    trigger_frame: int
    origin: Vec3
    spec: SecondaryBurstSpec


def choose_shell_flight_frames(
    *,
    launch_position: Vec3,
    burst_position: Vec3,
    box_height: float,
    rng: Random,
) -> int:
    vertical_distance = max(0.0, burst_position.y - launch_position.y)
    height_ratio = vertical_distance / box_height
    base_frames = 92 + height_ratio * 64
    speed_factor = rng.uniform(0.78, 1.28)
    jitter = rng.randint(-8, 8)
    flight_frames = int(base_frames / speed_factor + jitter)
    return max(
        SHELL_MIN_FLIGHT_FRAMES,
        min(SHELL_MAX_FLIGHT_FRAMES, flight_frames),
    )


def create_active_shell(
    *,
    launch_frame: int,
    firework_kind: FireworkKind,
    launch_position: Vec3,
    burst_position: Vec3,
    seed: int,
    box_height: float,
    rng: Random,
) -> ActiveShell:
    return ActiveShell(
        launch_frame=launch_frame,
        flight_frames=choose_shell_flight_frames(
            launch_position=launch_position,
            burst_position=burst_position,
            box_height=box_height,
            rng=rng,
        ),
        firework_kind=firework_kind,
        launch_position=launch_position,
        burst_position=burst_position,
        seed=seed,
        history=deque(maxlen=FIREWORK_SHELL_TAIL_LENGTH),
    )


def generate_firework_particles(
    *,
    firework_kind: FireworkKind,
    origin: Vec3,
    seed: int,
    orientation_bank: RingOrientationBank,
) -> tuple[ParticleSpawnSpec, ...]:
    preset = FIREWORK_PRESETS_BY_KIND[firework_kind]
    return generate_burst(
        preset=preset,
        origin=origin,
        seed=seed,
        orientation_bank=orientation_bank,
    )


def choose_accent_indexes(
    *,
    firework_kind: FireworkKind,
    seed: int,
    particle_count: int,
) -> set[int]:
    accent_count = min(ACCENT_COUNTS[firework_kind], particle_count)
    if accent_count <= 0:
        return set()
    kind_index = tuple(FIREWORK_PRESETS_BY_KIND).index(firework_kind)
    rng = Random(seed ^ ((kind_index + 1) * 0x9E3779B1))
    stride = max(1, particle_count // accent_count)
    offset = rng.randrange(stride)
    return {
        (offset + index * particle_count // accent_count) % particle_count
        for index in range(accent_count)
    }


def build_active_particles_for_burst(
    *,
    firework_kind: FireworkKind,
    origin: Vec3,
    seed: int,
    orientation_bank: RingOrientationBank,
) -> tuple[ActiveParticle, ...]:
    specs = generate_firework_particles(
        firework_kind=firework_kind,
        origin=origin,
        seed=seed,
        orientation_bank=orientation_bank,
    )
    accent_indexes = choose_accent_indexes(
        firework_kind=firework_kind,
        seed=seed,
        particle_count=len(specs),
    )
    accent_color = BURST_ACCENT_STYLES[firework_kind][2]
    return tuple(
        ActiveParticle.from_spawn(
            spec,
            accent_origin=origin if index in accent_indexes else None,
            accent_until_age=ACCENT_RAY_FRAMES if index in accent_indexes else 0,
            accent_color=accent_color if index in accent_indexes else 0,
        )
        for index, spec in enumerate(specs)
    )


def build_delayed_mini_burst_garnish(
    *,
    firework_kind: FireworkKind,
    origin: Vec3,
    burst_frame: int,
    seed: int,
) -> tuple[DelayedMiniBurst, ...]:
    if firework_kind not in MINI_BURST_GARNISH_ELIGIBLE_KINDS:
        return ()
    kind_index = tuple(FIREWORK_PRESETS_BY_KIND).index(firework_kind)
    rng = Random(seed ^ ((kind_index + 1) * 0x45D9F3B))
    if rng.random() >= MINI_BURST_GARNISH_CHANCE:
        return ()

    count = rng.randint(*MINI_BURST_GARNISH_COUNT_RANGE)
    delay = rng.randint(*MINI_BURST_GARNISH_DELAY_RANGE)
    bursts: list[DelayedMiniBurst] = []
    for index in range(count):
        offset_distance = rng.uniform(*MINI_BURST_GARNISH_OFFSET_RANGE)
        theta = rng.uniform(0.0, math.tau)
        z_scale = rng.uniform(0.55, 1.0)
        offset = Vec3(
            x=math.cos(theta) * offset_distance,
            y=rng.uniform(-2.5, 5.0),
            z=math.sin(theta) * offset_distance * z_scale,
        )
        child_origin = Vec3(
            origin.x + offset.x,
            origin.y + offset.y,
            origin.z + offset.z,
        )
        bursts.append(
            DelayedMiniBurst(
                trigger_frame=burst_frame + delay,
                origin=child_origin,
                spec=SecondaryBurstSpec(
                    delay_frames=0,
                    particle_count=rng.randint(*MINI_BURST_GARNISH_PARTICLE_RANGE),
                    seed=rng.randrange(1_000_000_000) + index,
                    speed_range=(0.20, 0.44),
                    life_range=(22, 38),
                    palette=BURST_ACCENT_STYLES[firework_kind],
                    fade_mid=5,
                    fade_dark=1,
                    tip_color=7,
                    drag=0.978,
                    gravity=-0.018,
                    trail=TrailPreset(
                        rate=0.18,
                        speed_threshold=0.28,
                        early_ratio=0.26,
                        strong_speed=0.40,
                        draw_every=2,
                    ),
                ),
            )
        )
        delay += rng.randint(5, 10)
    return tuple(bursts)


def build_delayed_mini_burst_particles(
    mini_burst: DelayedMiniBurst,
) -> tuple[ActiveParticle, ...]:
    return tuple(
        ActiveParticle.from_spawn(spec)
        for spec in generate_secondary_burst(
            origin=mini_burst.origin,
            spec=mini_burst.spec,
        )
    )


def build_secondary_particles(particle: ActiveParticle) -> tuple[ActiveParticle, ...]:
    secondary = particle.secondary_burst
    if secondary is None:
        return ()
    return tuple(
        ActiveParticle.from_spawn(spec)
        for spec in generate_secondary_burst(
            origin=particle.position,
            spec=secondary,
        )
    )


def build_glitter_residue(
    *,
    firework_kind: FireworkKind,
    origin: Vec3,
    seed: int,
) -> tuple[GlitterResidue, ...]:
    count = GLITTER_RESIDUE_COUNTS[firework_kind]
    if count <= 0:
        return ()
    kind_index = tuple(FIREWORK_PRESETS_BY_KIND).index(firework_kind)
    rng = Random(seed ^ ((kind_index + 1) * 0x517CC1B7))
    glitter: list[GlitterResidue] = []
    for _ in range(count):
        theta = rng.uniform(0.0, math.tau)
        vertical = rng.uniform(-0.15, 0.45)
        speed = rng.uniform(0.05, 0.18)
        life = rng.randint(*GLITTER_RESIDUE_LIFE_RANGE)
        glitter.append(
            GlitterResidue(
                position=origin,
                velocity=Vec3(
                    x=math.cos(theta) * speed,
                    y=vertical * speed,
                    z=math.sin(theta) * speed,
                ),
                life=life,
                max_life=life,
                phase=rng.randrange(16),
            )
        )
    return tuple(glitter)
