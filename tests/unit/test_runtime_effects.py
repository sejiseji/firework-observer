from __future__ import annotations

import inspect

from pyxel_goal_game.camera3d import Vec3
from pyxel_goal_game.firework_bursts import build_ring_orientation_bank
from pyxel_goal_game.firework_presets import FireworkKind, select_firework_palette
from pyxel_goal_game.runtime import effects
from pyxel_goal_game.runtime.effects import (
    MINI_BURST_GARNISH_COUNT_RANGE,
    MINI_BURST_GARNISH_ELIGIBLE_KINDS,
    build_active_particles_for_burst,
    build_delayed_mini_burst_garnish,
    build_delayed_mini_burst_particles,
)

ORIGIN = Vec3(1.0, 18.0, -2.0)
ORIENTATION_BANK = build_ring_orientation_bank(seed=20260623)


def test_runtime_effects_module_does_not_import_tools_preview() -> None:
    source = inspect.getsource(effects)

    assert "tools.preview_firework_box" not in source
    assert "preview_firework_box" not in source


def test_delayed_mini_burst_garnish_is_deterministic_for_same_seed() -> None:
    first = build_delayed_mini_burst_garnish(
        firework_kind=FireworkKind.SPHERE_BLOOM,
        origin=ORIGIN,
        burst_frame=120,
        seed=104,
    )
    second = build_delayed_mini_burst_garnish(
        firework_kind=FireworkKind.SPHERE_BLOOM,
        origin=ORIGIN,
        burst_frame=120,
        seed=104,
    )

    assert first == second


def test_active_particles_use_seed_selected_palette_for_burst() -> None:
    particles = build_active_particles_for_burst(
        firework_kind=FireworkKind.SPHERE_BLOOM,
        origin=ORIGIN,
        seed=1,
        orientation_bank=ORIENTATION_BANK,
    )
    selected_palette = select_firework_palette(FireworkKind.SPHERE_BLOOM, 1)

    assert particles
    assert {particle.color for particle in particles} <= set(selected_palette.colors)


def test_eligible_kinds_can_produce_bounded_staggered_garnish() -> None:
    for kind in MINI_BURST_GARNISH_ELIGIBLE_KINDS:
        seed, garnish = next(
            (seed, candidate)
            for seed in range(200)
            for candidate in (
                build_delayed_mini_burst_garnish(
                    firework_kind=kind,
                    origin=ORIGIN,
                    burst_frame=300,
                    seed=seed,
                ),
            )
            if candidate
        )

        assert MINI_BURST_GARNISH_COUNT_RANGE[0] <= len(garnish)
        assert len(garnish) <= MINI_BURST_GARNISH_COUNT_RANGE[1]
        trigger_frames = [burst.trigger_frame for burst in garnish]
        assert trigger_frames == sorted(trigger_frames)
        assert len(set(trigger_frames)) == len(trigger_frames)
        assert trigger_frames[0] > 300
        for burst in garnish:
            offset = (
                (burst.origin.x - ORIGIN.x) ** 2
                + (burst.origin.y - ORIGIN.y) ** 2
                + (burst.origin.z - ORIGIN.z) ** 2
            ) ** 0.5
            assert offset <= 12.0
            assert 10 <= burst.spec.particle_count <= 18
            assert burst.spec.palette == select_firework_palette(kind, seed).colors


def test_excluded_kinds_do_not_produce_mini_burst_garnish() -> None:
    excluded = {
        FireworkKind.WILLOW,
        FireworkKind.LONG_WILLOW,
        FireworkKind.RING,
        FireworkKind.HALO,
        FireworkKind.SENRIN,
        FireworkKind.SPIRAL,
        FireworkKind.SMILE,
    }

    for kind in excluded:
        assert (
            build_delayed_mini_burst_garnish(
                firework_kind=kind,
                origin=ORIGIN,
                burst_frame=300,
                seed=0,
            )
            == ()
        )


def test_delayed_mini_burst_particles_are_small_child_bursts() -> None:
    garnish = build_delayed_mini_burst_garnish(
        firework_kind=FireworkKind.KIKU,
        origin=ORIGIN,
        burst_frame=300,
        seed=4,
    )

    assert garnish
    particles = build_delayed_mini_burst_particles(garnish[0])

    assert len(particles) == garnish[0].spec.particle_count
    assert all(particle.position == garnish[0].origin for particle in particles)
    assert all(particle.max_life <= 38 for particle in particles)
