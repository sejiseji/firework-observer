from __future__ import annotations

import importlib
import math

import pytest

from pyxel_goal_game.camera3d import Vec3
from pyxel_goal_game.firework_bursts import (
    generate_burst,
    generate_kiku_burst,
    generate_ring_burst,
)
from pyxel_goal_game.firework_presets import (
    KIKU_PRESET,
    RING_PRESET,
    FireworkKind,
    FireworkPreset,
    FireworkShape,
)

ORIGIN = Vec3(1.0, 2.0, 3.0)


def speed_of(velocity: Vec3) -> float:
    return math.sqrt(velocity.x**2 + velocity.y**2 + velocity.z**2)


def test_kiku_preset_uses_protected_values() -> None:
    assert KIKU_PRESET.kind is FireworkKind.KIKU
    assert KIKU_PRESET.shape is FireworkShape.SPHERE
    assert KIKU_PRESET.particle_count == 112
    assert KIKU_PRESET.speed_range == (0.90, 1.65)
    assert KIKU_PRESET.life_range == (55, 85)
    assert KIKU_PRESET.palette == (10, 9, 7)
    assert KIKU_PRESET.gravity == -0.025
    assert KIKU_PRESET.trail.rate == 0.32


def test_same_seed_generates_identical_kiku_specs() -> None:
    first = generate_kiku_burst(origin=ORIGIN, seed=123)
    second = generate_kiku_burst(origin=ORIGIN, seed=123)

    assert first == second


def test_different_seeds_generate_different_kiku_specs() -> None:
    first = generate_kiku_burst(origin=ORIGIN, seed=123)
    second = generate_kiku_burst(origin=ORIGIN, seed=124)

    assert first != second


def test_kiku_particle_count_and_ranges() -> None:
    particles = generate_kiku_burst(origin=ORIGIN, seed=0)

    assert len(particles) == KIKU_PRESET.particle_count
    assert all(
        KIKU_PRESET.life_range[0] <= particle.life <= KIKU_PRESET.life_range[1]
        for particle in particles
    )
    assert all(
        KIKU_PRESET.speed_range[0] <= speed_of(particle.velocity) <= KIKU_PRESET.speed_range[1]
        for particle in particles
    )


def test_kiku_specs_preserve_physics_and_colors() -> None:
    particles = generate_kiku_burst(origin=ORIGIN, seed=0)

    assert all(particle.position == ORIGIN for particle in particles)
    assert all(particle.gravity < 0.0 for particle in particles)
    assert all(particle.drag == KIKU_PRESET.drag for particle in particles)
    assert all(particle.color in KIKU_PRESET.palette for particle in particles)
    assert all(particle.fade_mid == KIKU_PRESET.fade_mid for particle in particles)
    assert all(particle.fade_dark == KIKU_PRESET.fade_dark for particle in particles)
    assert all(particle.tip_color == KIKU_PRESET.tip_color for particle in particles)


def test_kiku_trails_are_partial_for_known_seed() -> None:
    particles = generate_kiku_burst(origin=ORIGIN, seed=0)
    trail_count = sum(particle.has_trail for particle in particles)

    assert 0 < trail_count < len(particles)
    assert all(
        particle.trail_until_age == int(particle.life * KIKU_PRESET.trail.early_ratio)
        for particle in particles
    )
    assert all(particle.trail_draw_every == KIKU_PRESET.trail.draw_every for particle in particles)


def test_kiku_velocity_distribution_is_3d_not_flat() -> None:
    particles = generate_kiku_burst(origin=ORIGIN, seed=0)

    assert any(abs(particle.velocity.x) > 0.01 for particle in particles)
    assert any(abs(particle.velocity.y) > 0.01 for particle in particles)
    assert any(abs(particle.velocity.z) > 0.01 for particle in particles)


def test_generate_burst_rejects_unsupported_shapes() -> None:
    unsupported = FireworkPreset(
        kind=FireworkKind.SPIRAL,
        label="Spiral",
        shape=FireworkShape.SPIRAL,
        particle_count=1,
        speed_range=(1.0, 1.0),
        life_range=(1, 1),
        palette=(7,),
        fade_mid=7,
        fade_dark=1,
        tip_color=7,
        drag=1.0,
        gravity=-0.01,
        trail=KIKU_PRESET.trail,
    )

    with pytest.raises(NotImplementedError, match="SPIRAL"):
        generate_burst(preset=unsupported, origin=ORIGIN, seed=0)


def test_firework_bursts_module_has_no_pyxel_dependency() -> None:
    module = importlib.import_module("pyxel_goal_game.firework_bursts")

    assert "pyxel" not in module.__dict__


def test_ring_preset_uses_documented_values() -> None:
    assert RING_PRESET.kind is FireworkKind.RING
    assert RING_PRESET.shape is FireworkShape.RING
    assert RING_PRESET.particle_count == 104
    assert RING_PRESET.speed_range == (1.05, 1.45)
    assert RING_PRESET.life_range == (58, 82)
    assert RING_PRESET.palette == (12, 6, 7)
    assert RING_PRESET.gravity == -0.018
    assert RING_PRESET.trail.rate == 0.38


def test_same_seed_generates_identical_ring_specs() -> None:
    first = generate_ring_burst(origin=ORIGIN, seed=123)
    second = generate_ring_burst(origin=ORIGIN, seed=123)

    assert first == second


def test_different_seeds_generate_different_ring_specs() -> None:
    first = generate_ring_burst(origin=ORIGIN, seed=123)
    second = generate_ring_burst(origin=ORIGIN, seed=124)

    assert first != second


def test_ring_particle_count_and_ranges() -> None:
    particles = generate_ring_burst(origin=ORIGIN, seed=0)

    assert len(particles) == RING_PRESET.particle_count
    assert all(
        RING_PRESET.life_range[0] <= particle.life <= RING_PRESET.life_range[1]
        for particle in particles
    )
    assert all(
        RING_PRESET.speed_range[0] <= speed_of(particle.velocity) <= RING_PRESET.speed_range[1]
        for particle in particles
    )


def test_ring_specs_preserve_physics_and_colors() -> None:
    particles = generate_ring_burst(origin=ORIGIN, seed=0)

    assert all(particle.position == ORIGIN for particle in particles)
    assert all(particle.gravity < 0.0 for particle in particles)
    assert all(particle.drag == RING_PRESET.drag for particle in particles)
    assert all(particle.color in RING_PRESET.palette for particle in particles)


def test_ring_trails_are_partial_for_known_seed() -> None:
    particles = generate_ring_burst(origin=ORIGIN, seed=0)
    trail_count = sum(particle.has_trail for particle in particles)

    assert 0 < trail_count < len(particles)
    assert all(
        particle.trail_until_age == int(particle.life * RING_PRESET.trail.early_ratio)
        for particle in particles
    )


def test_ring_velocity_is_mostly_planar_with_small_z_thickness() -> None:
    particles = generate_ring_burst(origin=ORIGIN, seed=0)

    assert all(
        abs(particle.velocity.z) <= speed_of(particle.velocity) * 0.061
        for particle in particles
    )


def test_ring_uses_y_up_plane() -> None:
    particles = generate_ring_burst(origin=ORIGIN, seed=0)

    assert any(particle.velocity.y > 0.0 for particle in particles)
    assert any(particle.velocity.y < 0.0 for particle in particles)


def test_generate_burst_supports_ring_shape() -> None:
    particles = generate_burst(preset=RING_PRESET, origin=ORIGIN, seed=0)

    assert particles == generate_ring_burst(origin=ORIGIN, seed=0)
