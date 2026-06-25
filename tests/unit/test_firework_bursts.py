from __future__ import annotations

import importlib
import math

import pytest

from pyxel_goal_game.camera3d import Vec3
from pyxel_goal_game.firework_bursts import (
    DEFAULT_RING_ORIENTATION_COUNT,
    RingOrientationBank,
    build_ring_orientation_bank,
    dot_vec3,
    generate_burst,
    generate_kiku_burst,
    generate_multi_ring_burst,
    generate_peony_burst,
    generate_ring_burst,
    generate_secondary_burst,
    generate_senrin_burst,
    generate_spiral_burst,
    generate_willow_burst,
    length_vec3,
    varied_burst_speed,
)
from pyxel_goal_game.firework_presets import (
    KIKU_PRESET,
    MULTI_RING_PRESET,
    PEONY_PRESET,
    RING_PRESET,
    SENRIN_PRESET,
    SENRIN_SECONDARY_PRESET,
    SPIRAL_PRESET,
    WILLOW_PRESET,
    FireworkKind,
    FireworkPreset,
    FireworkShape,
)

ORIGIN = Vec3(1.0, 2.0, 3.0)


def speed_of(velocity: Vec3) -> float:
    return math.sqrt(velocity.x**2 + velocity.y**2 + velocity.z**2)


def speed_in_range(speed: float, speed_range: tuple[float, float]) -> bool:
    return speed_range[0] - 1e-9 <= speed <= speed_range[1] + 1e-9


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
        speed_in_range(speed_of(particle.velocity), KIKU_PRESET.speed_range)
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
    assert all(particle.secondary_burst is None for particle in particles)


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


@pytest.mark.parametrize(
    "preset",
    [
        KIKU_PRESET,
        RING_PRESET,
        SPIRAL_PRESET,
        WILLOW_PRESET,
        PEONY_PRESET,
        MULTI_RING_PRESET,
        SENRIN_PRESET,
    ],
)
def test_burst_radius_variation_is_subtle_and_bounded(preset: FireworkPreset) -> None:
    midpoint = sum(preset.speed_range) / 2.0
    varied = [
        varied_burst_speed(base_speed=midpoint, preset=preset, index=index)
        for index in range(24)
    ]

    assert all(preset.speed_range[0] <= speed <= preset.speed_range[1] for speed in varied)
    assert min(varied) < midpoint < max(varied)
    assert max(varied) / min(varied) < 1.25


def test_generate_burst_rejects_unsupported_shapes() -> None:
    unsupported = FireworkPreset(
        kind=FireworkKind.HALO,
        label="Halo",
        shape=FireworkShape.HALO,
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

    with pytest.raises(NotImplementedError, match="HALO"):
        generate_burst(preset=unsupported, origin=ORIGIN, seed=0)


def test_firework_bursts_module_has_no_pyxel_dependency() -> None:
    module = importlib.import_module("pyxel_goal_game.firework_bursts")

    assert "pyxel" not in module.__dict__


def test_ring_orientation_bank_has_expected_count() -> None:
    bank = build_ring_orientation_bank(seed=20260623)

    assert len(bank.orientations) == DEFAULT_RING_ORIENTATION_COUNT


def test_ring_orientation_bank_is_deterministic() -> None:
    first = build_ring_orientation_bank(seed=20260623)
    second = build_ring_orientation_bank(seed=20260623)

    assert first == second


def test_different_ring_orientation_bank_seeds_differ() -> None:
    first = build_ring_orientation_bank(seed=20260623)
    second = build_ring_orientation_bank(seed=20260624)

    assert first != second


def test_ring_orientation_bank_contains_stratified_orientations() -> None:
    bank = build_ring_orientation_bank(seed=20260623)
    normal_y_values = [orientation.normal_y for orientation in bank.orientations]

    assert any(0.00 <= normal_y < 0.30 for normal_y in normal_y_values)
    assert any(0.30 <= normal_y < 0.75 for normal_y in normal_y_values)
    assert any(0.75 <= normal_y <= 0.98 for normal_y in normal_y_values)


def test_ring_orientation_bank_choose_is_deterministic() -> None:
    bank = build_ring_orientation_bank(seed=20260623)

    assert bank.choose(seed=42) == bank.choose(seed=42)


def test_empty_ring_orientation_bank_is_rejected() -> None:
    with pytest.raises(ValueError, match="orientations"):
        RingOrientationBank(())


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


def test_same_seed_and_bank_generate_identical_ring_specs() -> None:
    bank = build_ring_orientation_bank(seed=20260623)
    first = generate_ring_burst(origin=ORIGIN, seed=123, orientation_bank=bank)
    second = generate_ring_burst(origin=ORIGIN, seed=123, orientation_bank=bank)

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
        speed_in_range(speed_of(particle.velocity), RING_PRESET.speed_range)
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


def test_ring_velocity_keeps_speed_with_orientation_bank() -> None:
    bank = build_ring_orientation_bank(seed=20260623)
    particles = generate_ring_burst(origin=ORIGIN, seed=0, orientation_bank=bank)

    assert all(
        speed_in_range(speed_of(particle.velocity), RING_PRESET.speed_range)
        for particle in particles
    )


def test_ring_velocity_is_mostly_planar_relative_to_chosen_orientation() -> None:
    bank = build_ring_orientation_bank(seed=20260623)
    orientation = bank.choose(seed=0)
    particles = generate_ring_burst(origin=ORIGIN, seed=0, orientation_bank=bank)

    assert all(
        abs(dot_vec3(particle.velocity, orientation.normal))
        <= length_vec3(particle.velocity) * 0.061
        for particle in particles
    )


def test_ring_uses_y_up_plane() -> None:
    particles = generate_ring_burst(origin=ORIGIN, seed=0)

    assert any(particle.velocity.y > 0.0 for particle in particles)
    assert any(particle.velocity.y < 0.0 for particle in particles)


def test_generate_burst_supports_ring_shape() -> None:
    particles = generate_burst(preset=RING_PRESET, origin=ORIGIN, seed=0)

    assert particles == generate_ring_burst(origin=ORIGIN, seed=0)


def test_generate_burst_supports_ring_orientation_bank() -> None:
    bank = build_ring_orientation_bank(seed=20260623)
    particles = generate_burst(
        preset=RING_PRESET,
        origin=ORIGIN,
        seed=0,
        orientation_bank=bank,
    )

    assert particles == generate_ring_burst(origin=ORIGIN, seed=0, orientation_bank=bank)


def test_spiral_preset_uses_documented_values() -> None:
    assert SPIRAL_PRESET.kind is FireworkKind.SPIRAL
    assert SPIRAL_PRESET.shape is FireworkShape.SPIRAL
    assert SPIRAL_PRESET.particle_count == 120
    assert SPIRAL_PRESET.speed_range == (0.75, 1.35)
    assert SPIRAL_PRESET.life_range == (62, 94)
    assert SPIRAL_PRESET.palette == (11, 10, 7)
    assert SPIRAL_PRESET.gravity == -0.019
    assert SPIRAL_PRESET.trail.rate == 0.45


def test_same_seed_generates_identical_spiral_specs() -> None:
    first = generate_spiral_burst(origin=ORIGIN, seed=123)
    second = generate_spiral_burst(origin=ORIGIN, seed=123)

    assert first == second


def test_different_seeds_generate_different_spiral_specs() -> None:
    first = generate_spiral_burst(origin=ORIGIN, seed=123)
    second = generate_spiral_burst(origin=ORIGIN, seed=124)

    assert first != second


def test_spiral_particle_count_and_ranges() -> None:
    particles = generate_spiral_burst(origin=ORIGIN, seed=0)

    assert len(particles) == SPIRAL_PRESET.particle_count
    assert all(
        SPIRAL_PRESET.life_range[0] <= particle.life <= SPIRAL_PRESET.life_range[1]
        for particle in particles
    )
    assert all(
        speed_in_range(speed_of(particle.velocity), SPIRAL_PRESET.speed_range)
        for particle in particles
    )


def test_spiral_specs_preserve_physics_and_colors() -> None:
    particles = generate_spiral_burst(origin=ORIGIN, seed=0)

    assert all(particle.position == ORIGIN for particle in particles)
    assert all(particle.gravity < 0.0 for particle in particles)
    assert all(particle.drag == SPIRAL_PRESET.drag for particle in particles)
    assert all(particle.color in SPIRAL_PRESET.palette for particle in particles)


def test_spiral_trails_are_partial_for_known_seed() -> None:
    particles = generate_spiral_burst(origin=ORIGIN, seed=0)
    trail_count = sum(particle.has_trail for particle in particles)

    assert 0 < trail_count < len(particles)
    assert all(
        particle.trail_until_age == int(particle.life * SPIRAL_PRESET.trail.early_ratio)
        for particle in particles
    )


def test_spiral_velocity_distribution_is_3d_not_flat() -> None:
    particles = generate_spiral_burst(origin=ORIGIN, seed=0)
    x_values = [particle.velocity.x for particle in particles]
    y_values = [particle.velocity.y for particle in particles]
    z_values = [particle.velocity.z for particle in particles]

    assert max(x_values) - min(x_values) > 1.0
    assert max(y_values) - min(y_values) > 0.7
    assert max(z_values) - min(z_values) > 1.0


def test_spiral_uses_y_up_with_positive_and_negative_vertical_velocity() -> None:
    particles = generate_spiral_burst(origin=ORIGIN, seed=0)

    assert any(particle.velocity.y > 0.0 for particle in particles)
    assert any(particle.velocity.y < 0.0 for particle in particles)


def test_generate_burst_supports_spiral_shape() -> None:
    particles = generate_burst(preset=SPIRAL_PRESET, origin=ORIGIN, seed=0)

    assert particles == generate_spiral_burst(origin=ORIGIN, seed=0)


def test_willow_preset_uses_documented_values() -> None:
    assert WILLOW_PRESET.kind is FireworkKind.WILLOW
    assert WILLOW_PRESET.shape is FireworkShape.WILLOW
    assert WILLOW_PRESET.particle_count == 88
    assert WILLOW_PRESET.speed_range == (0.55, 1.10)
    assert WILLOW_PRESET.life_range == (85, 125)
    assert WILLOW_PRESET.palette == (10, 9, 4)
    assert WILLOW_PRESET.gravity == -0.040
    assert WILLOW_PRESET.trail.rate == 0.68
    assert WILLOW_PRESET.trail.early_ratio == 0.72


def test_same_seed_generates_identical_willow_specs() -> None:
    first = generate_willow_burst(origin=ORIGIN, seed=123)
    second = generate_willow_burst(origin=ORIGIN, seed=123)

    assert first == second


def test_different_seeds_generate_different_willow_specs() -> None:
    first = generate_willow_burst(origin=ORIGIN, seed=123)
    second = generate_willow_burst(origin=ORIGIN, seed=124)

    assert first != second


def test_willow_particle_count_and_life_ranges() -> None:
    particles = generate_willow_burst(origin=ORIGIN, seed=0)

    assert len(particles) == WILLOW_PRESET.particle_count
    assert all(
        WILLOW_PRESET.life_range[0] <= particle.life <= WILLOW_PRESET.life_range[1]
        for particle in particles
    )


def test_willow_velocity_components_match_loose_radial_shape() -> None:
    particles = generate_willow_burst(origin=ORIGIN, seed=0)

    assert all(
        speed_of(particle.velocity) <= WILLOW_PRESET.speed_range[1] * 1.20
        for particle in particles
    )
    assert any(particle.velocity.y < 0.0 for particle in particles)
    assert any(particle.velocity.y > 0.0 for particle in particles)
    assert any(abs(particle.velocity.x) > 0.1 for particle in particles)
    assert any(abs(particle.velocity.z) > 0.1 for particle in particles)


def test_willow_specs_preserve_physics_and_colors() -> None:
    particles = generate_willow_burst(origin=ORIGIN, seed=0)

    assert all(particle.position == ORIGIN for particle in particles)
    assert all(particle.gravity == WILLOW_PRESET.gravity for particle in particles)
    assert all(particle.drag == WILLOW_PRESET.drag for particle in particles)
    assert all(particle.color in WILLOW_PRESET.palette for particle in particles)


def test_willow_gravity_is_stronger_than_existing_presets() -> None:
    assert abs(WILLOW_PRESET.gravity) > abs(KIKU_PRESET.gravity)
    assert abs(WILLOW_PRESET.gravity) > abs(RING_PRESET.gravity)
    assert abs(WILLOW_PRESET.gravity) > abs(SPIRAL_PRESET.gravity)


def test_willow_trails_are_partial_for_known_seed() -> None:
    particles = generate_willow_burst(origin=ORIGIN, seed=0)
    trail_count = sum(particle.has_trail for particle in particles)

    assert 0 < trail_count < len(particles)
    assert all(
        particle.trail_until_age == int(particle.life * WILLOW_PRESET.trail.early_ratio)
        for particle in particles
    )


def test_willow_trail_tendency_is_longer_than_kiku_and_ring() -> None:
    assert WILLOW_PRESET.trail.rate > KIKU_PRESET.trail.rate
    assert WILLOW_PRESET.trail.rate > RING_PRESET.trail.rate
    assert WILLOW_PRESET.trail.early_ratio > KIKU_PRESET.trail.early_ratio
    assert WILLOW_PRESET.trail.early_ratio > RING_PRESET.trail.early_ratio


def test_generate_burst_supports_willow_shape() -> None:
    particles = generate_burst(preset=WILLOW_PRESET, origin=ORIGIN, seed=0)

    assert particles == generate_willow_burst(origin=ORIGIN, seed=0)


def test_peony_preset_uses_documented_values() -> None:
    assert PEONY_PRESET.kind is FireworkKind.PEONY
    assert PEONY_PRESET.shape is FireworkShape.SPHERE
    assert PEONY_PRESET.particle_count == 96
    assert PEONY_PRESET.speed_range == (0.80, 1.35)
    assert PEONY_PRESET.life_range == (42, 68)
    assert PEONY_PRESET.palette == (14, 8, 10)
    assert PEONY_PRESET.fade_mid == 8
    assert PEONY_PRESET.fade_dark == 2
    assert PEONY_PRESET.tip_color == 7
    assert PEONY_PRESET.drag == 0.982
    assert PEONY_PRESET.gravity == -0.022
    assert PEONY_PRESET.trail.rate == 0.18
    assert PEONY_PRESET.trail.early_ratio == 0.32


def test_same_seed_generates_identical_peony_specs() -> None:
    first = generate_peony_burst(origin=ORIGIN, seed=123)
    second = generate_peony_burst(origin=ORIGIN, seed=123)

    assert first == second


def test_different_seeds_generate_different_peony_specs() -> None:
    first = generate_peony_burst(origin=ORIGIN, seed=123)
    second = generate_peony_burst(origin=ORIGIN, seed=124)

    assert first != second


def test_peony_particle_count_life_and_speed_ranges() -> None:
    particles = generate_peony_burst(origin=ORIGIN, seed=0)

    assert len(particles) == PEONY_PRESET.particle_count
    assert all(
        PEONY_PRESET.life_range[0] <= particle.life <= PEONY_PRESET.life_range[1]
        for particle in particles
    )
    assert all(
        speed_in_range(speed_of(particle.velocity), PEONY_PRESET.speed_range)
        for particle in particles
    )


def test_peony_specs_preserve_physics_and_colors() -> None:
    particles = generate_peony_burst(origin=ORIGIN, seed=0)

    assert all(particle.position == ORIGIN for particle in particles)
    assert all(particle.gravity == PEONY_PRESET.gravity for particle in particles)
    assert all(particle.gravity < 0.0 for particle in particles)
    assert all(particle.drag == PEONY_PRESET.drag for particle in particles)
    assert all(particle.color in PEONY_PRESET.palette for particle in particles)
    assert all(particle.fade_mid == PEONY_PRESET.fade_mid for particle in particles)
    assert all(particle.fade_dark == PEONY_PRESET.fade_dark for particle in particles)
    assert all(particle.tip_color == PEONY_PRESET.tip_color for particle in particles)


def test_peony_trails_are_partial_for_known_seed() -> None:
    particles = generate_peony_burst(origin=ORIGIN, seed=0)
    trail_count = sum(particle.has_trail for particle in particles)

    assert 0 < trail_count < len(particles)
    assert all(
        particle.trail_until_age == int(particle.life * PEONY_PRESET.trail.early_ratio)
        for particle in particles
    )
    assert all(particle.trail_draw_every == PEONY_PRESET.trail.draw_every for particle in particles)


def test_peony_is_shorter_and_less_trailed_than_existing_presets() -> None:
    assert PEONY_PRESET.life_range[1] < KIKU_PRESET.life_range[1]
    assert PEONY_PRESET.trail.rate < KIKU_PRESET.trail.rate
    assert PEONY_PRESET.trail.early_ratio < WILLOW_PRESET.trail.early_ratio


def test_peony_uses_y_up_sphere_distribution() -> None:
    particles = generate_peony_burst(origin=ORIGIN, seed=0)

    assert any(particle.velocity.y > 0.0 for particle in particles)
    assert any(particle.velocity.y < 0.0 for particle in particles)
    assert any(abs(particle.velocity.x) > 0.01 for particle in particles)
    assert any(abs(particle.velocity.z) > 0.01 for particle in particles)


def test_generate_burst_supports_peony_shape() -> None:
    particles = generate_burst(preset=PEONY_PRESET, origin=ORIGIN, seed=0)

    assert particles == generate_peony_burst(origin=ORIGIN, seed=0)


def test_multi_ring_preset_uses_documented_values() -> None:
    assert MULTI_RING_PRESET.kind is FireworkKind.MULTI_RING
    assert MULTI_RING_PRESET.shape is FireworkShape.MULTI_RING
    assert MULTI_RING_PRESET.particle_count == 120
    assert MULTI_RING_PRESET.speed_range == (0.85, 1.55)
    assert MULTI_RING_PRESET.life_range == (58, 90)
    assert MULTI_RING_PRESET.palette == (12, 6, 7, 10)
    assert MULTI_RING_PRESET.fade_mid == 6
    assert MULTI_RING_PRESET.fade_dark == 1
    assert MULTI_RING_PRESET.tip_color == 7
    assert MULTI_RING_PRESET.drag == 0.987
    assert MULTI_RING_PRESET.gravity == -0.017
    assert MULTI_RING_PRESET.trail.rate == 0.30


def test_same_seed_generates_identical_multi_ring_specs() -> None:
    first = generate_multi_ring_burst(origin=ORIGIN, seed=123)
    second = generate_multi_ring_burst(origin=ORIGIN, seed=123)

    assert first == second


def test_same_seed_and_bank_generate_identical_multi_ring_specs() -> None:
    bank = build_ring_orientation_bank(seed=20260623)
    first = generate_multi_ring_burst(origin=ORIGIN, seed=123, orientation_bank=bank)
    second = generate_multi_ring_burst(origin=ORIGIN, seed=123, orientation_bank=bank)

    assert first == second


def test_different_seeds_generate_different_multi_ring_specs() -> None:
    first = generate_multi_ring_burst(origin=ORIGIN, seed=123)
    second = generate_multi_ring_burst(origin=ORIGIN, seed=124)

    assert first != second


def test_multi_ring_particle_count_life_and_speed_ranges() -> None:
    particles = generate_multi_ring_burst(origin=ORIGIN, seed=0)

    assert len(particles) == MULTI_RING_PRESET.particle_count
    assert all(
        MULTI_RING_PRESET.life_range[0] <= particle.life <= MULTI_RING_PRESET.life_range[1]
        for particle in particles
    )
    assert all(
        speed_in_range(speed_of(particle.velocity), MULTI_RING_PRESET.speed_range)
        for particle in particles
    )


def test_multi_ring_specs_preserve_physics_and_colors() -> None:
    particles = generate_multi_ring_burst(origin=ORIGIN, seed=0)

    assert all(particle.position == ORIGIN for particle in particles)
    assert all(particle.gravity == MULTI_RING_PRESET.gravity for particle in particles)
    assert all(particle.gravity < 0.0 for particle in particles)
    assert all(particle.drag == MULTI_RING_PRESET.drag for particle in particles)
    assert all(particle.color in MULTI_RING_PRESET.palette for particle in particles)
    assert all(particle.secondary_burst is None for particle in particles)


def test_multi_ring_trails_are_partial_for_known_seed() -> None:
    particles = generate_multi_ring_burst(origin=ORIGIN, seed=0)
    trail_count = sum(particle.has_trail for particle in particles)

    assert 0 < trail_count < len(particles)
    assert all(
        particle.trail_until_age == int(
            particle.life * MULTI_RING_PRESET.trail.early_ratio
        )
        for particle in particles
    )


def test_multi_ring_uses_3d_oriented_ring_distribution() -> None:
    particles = generate_multi_ring_burst(origin=ORIGIN, seed=0)

    assert any(particle.velocity.y > 0.0 for particle in particles)
    assert any(particle.velocity.y < 0.0 for particle in particles)
    assert any(abs(particle.velocity.x) > 0.1 for particle in particles)
    assert any(abs(particle.velocity.z) > 0.1 for particle in particles)


def test_multi_ring_has_layered_speed_bands() -> None:
    particles = generate_multi_ring_burst(origin=ORIGIN, seed=0)
    inner = [speed_of(particle.velocity) for particle in particles[:32]]
    middle = [speed_of(particle.velocity) for particle in particles[32:72]]
    outer = [speed_of(particle.velocity) for particle in particles[72:]]

    assert sum(inner) / len(inner) < sum(middle) / len(middle)
    assert sum(middle) / len(middle) < sum(outer) / len(outer)


def test_generate_burst_supports_multi_ring_shape() -> None:
    particles = generate_burst(preset=MULTI_RING_PRESET, origin=ORIGIN, seed=0)

    assert particles == generate_multi_ring_burst(origin=ORIGIN, seed=0)


def test_generate_burst_supports_multi_ring_orientation_bank() -> None:
    bank = build_ring_orientation_bank(seed=20260623)
    particles = generate_burst(
        preset=MULTI_RING_PRESET,
        origin=ORIGIN,
        seed=0,
        orientation_bank=bank,
    )

    assert particles == generate_multi_ring_burst(
        origin=ORIGIN,
        seed=0,
        orientation_bank=bank,
    )


def test_senrin_preset_uses_documented_values() -> None:
    assert SENRIN_PRESET.kind is FireworkKind.SENRIN
    assert SENRIN_PRESET.shape is FireworkShape.SENRIN_SEED
    assert SENRIN_PRESET.particle_count == 42
    assert SENRIN_PRESET.speed_range == (0.55, 0.95)
    assert SENRIN_PRESET.life_range == (32, 52)
    assert SENRIN_PRESET.palette == (7, 10, 14)
    assert SENRIN_PRESET.fade_mid == 10
    assert SENRIN_PRESET.fade_dark == 5
    assert SENRIN_PRESET.gravity == -0.012
    assert SENRIN_PRESET.secondary is SENRIN_SECONDARY_PRESET


def test_senrin_secondary_preset_uses_documented_values() -> None:
    assert SENRIN_SECONDARY_PRESET.rate == 0.78
    assert SENRIN_SECONDARY_PRESET.count_range == (8, 14)
    assert SENRIN_SECONDARY_PRESET.delay_range == (14, 28)
    assert SENRIN_SECONDARY_PRESET.speed_range == (0.28, 0.68)
    assert SENRIN_SECONDARY_PRESET.life_range == (28, 48)
    assert SENRIN_SECONDARY_PRESET.palette == (7, 10, 9, 14)
    assert SENRIN_SECONDARY_PRESET.gravity == -0.025
    assert SENRIN_SECONDARY_PRESET.trail.rate == 0.06
    assert SENRIN_SECONDARY_PRESET.trail.draw_every == 2


def test_same_seed_generates_identical_senrin_specs() -> None:
    first = generate_senrin_burst(origin=ORIGIN, seed=123)
    second = generate_senrin_burst(origin=ORIGIN, seed=123)

    assert first == second


def test_different_seeds_generate_different_senrin_specs() -> None:
    first = generate_senrin_burst(origin=ORIGIN, seed=123)
    second = generate_senrin_burst(origin=ORIGIN, seed=124)

    assert first != second


def test_senrin_primary_particle_count_life_and_speed_ranges() -> None:
    particles = generate_senrin_burst(origin=ORIGIN, seed=0)

    assert len(particles) == SENRIN_PRESET.particle_count
    assert all(
        SENRIN_PRESET.life_range[0] <= particle.life <= SENRIN_PRESET.life_range[1]
        for particle in particles
    )
    assert all(
        speed_of(particle.velocity) <= SENRIN_PRESET.speed_range[1]
        for particle in particles
    )


def test_senrin_primary_specs_preserve_physics_and_colors() -> None:
    particles = generate_senrin_burst(origin=ORIGIN, seed=0)

    assert all(particle.position == ORIGIN for particle in particles)
    assert all(particle.gravity == SENRIN_PRESET.gravity for particle in particles)
    assert all(particle.gravity < 0.0 for particle in particles)
    assert all(particle.drag == SENRIN_PRESET.drag for particle in particles)
    assert all(particle.color in SENRIN_PRESET.palette for particle in particles)


def test_senrin_primary_trails_are_partial_for_known_seed() -> None:
    particles = generate_senrin_burst(origin=ORIGIN, seed=0)
    trail_count = sum(particle.has_trail for particle in particles)

    assert 0 < trail_count < len(particles)
    assert all(
        particle.trail_until_age == int(particle.life * SENRIN_PRESET.trail.early_ratio)
        for particle in particles
    )


def test_senrin_has_partial_secondary_burst_specs() -> None:
    particles = generate_senrin_burst(origin=ORIGIN, seed=0)
    secondary_specs = [
        particle.secondary_burst
        for particle in particles
        if particle.secondary_burst is not None
    ]

    assert 0 < len(secondary_specs) < len(particles)
    assert all(
        SENRIN_SECONDARY_PRESET.delay_range[0]
        <= secondary.delay_frames
        <= SENRIN_SECONDARY_PRESET.delay_range[1]
        for secondary in secondary_specs
    )
    assert all(
        SENRIN_SECONDARY_PRESET.count_range[0]
        <= secondary.particle_count
        <= SENRIN_SECONDARY_PRESET.count_range[1]
        for secondary in secondary_specs
    )


def test_senrin_secondary_specs_match_secondary_preset() -> None:
    particles = generate_senrin_burst(origin=ORIGIN, seed=0)
    secondary = next(
        particle.secondary_burst
        for particle in particles
        if particle.secondary_burst is not None
    )

    assert secondary.speed_range == SENRIN_SECONDARY_PRESET.speed_range
    assert secondary.life_range == SENRIN_SECONDARY_PRESET.life_range
    assert secondary.palette == SENRIN_SECONDARY_PRESET.palette
    assert secondary.fade_mid == SENRIN_SECONDARY_PRESET.fade_mid
    assert secondary.fade_dark == SENRIN_SECONDARY_PRESET.fade_dark
    assert secondary.tip_color == SENRIN_SECONDARY_PRESET.tip_color
    assert secondary.drag == SENRIN_SECONDARY_PRESET.drag
    assert secondary.gravity == SENRIN_SECONDARY_PRESET.gravity
    assert secondary.trail == SENRIN_SECONDARY_PRESET.trail


def test_secondary_burst_generation_is_deterministic() -> None:
    secondary = next(
        particle.secondary_burst
        for particle in generate_senrin_burst(origin=ORIGIN, seed=0)
        if particle.secondary_burst is not None
    )

    first = generate_secondary_burst(origin=ORIGIN, spec=secondary)
    second = generate_secondary_burst(origin=ORIGIN, spec=secondary)

    assert first == second


def test_secondary_burst_particles_use_secondary_ranges() -> None:
    secondary = next(
        particle.secondary_burst
        for particle in generate_senrin_burst(origin=ORIGIN, seed=0)
        if particle.secondary_burst is not None
    )
    particles = generate_secondary_burst(origin=ORIGIN, spec=secondary)

    assert len(particles) == secondary.particle_count
    assert all(
        secondary.life_range[0] <= particle.life <= secondary.life_range[1]
        for particle in particles
    )
    assert all(particle.color in secondary.palette for particle in particles)
    assert all(particle.gravity == secondary.gravity for particle in particles)
    assert all(particle.gravity < 0.0 for particle in particles)
    assert all(particle.secondary_burst is None for particle in particles)


def test_secondary_burst_trails_are_sparse_for_known_seed() -> None:
    secondary = next(
        particle.secondary_burst
        for particle in generate_senrin_burst(origin=ORIGIN, seed=0)
        if particle.secondary_burst is not None
    )
    particles = generate_secondary_burst(origin=ORIGIN, spec=secondary)
    trail_count = sum(particle.has_trail for particle in particles)

    assert trail_count < len(particles)
    assert all(particle.trail_draw_every == secondary.trail.draw_every for particle in particles)


def test_generate_burst_supports_senrin_seed_shape() -> None:
    particles = generate_burst(preset=SENRIN_PRESET, origin=ORIGIN, seed=0)

    assert particles == generate_senrin_burst(origin=ORIGIN, seed=0)
