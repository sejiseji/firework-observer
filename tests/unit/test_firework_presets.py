from __future__ import annotations

import importlib

import pytest

from pyxel_goal_game.firework_presets import (
    FUTURE_FIREWORK_KINDS,
    FireworkKind,
    FireworkPreset,
    FireworkShape,
    SecondaryPreset,
    TrailPreset,
)


def test_future_firework_kinds_exist() -> None:
    assert set(FUTURE_FIREWORK_KINDS) == {
        FireworkKind.KIKU,
        FireworkKind.SPHERE_BLOOM,
        FireworkKind.PEONY,
        FireworkKind.RING,
        FireworkKind.WILLOW,
        FireworkKind.LONG_WILLOW,
        FireworkKind.SPIRAL,
        FireworkKind.MULTI_RING,
        FireworkKind.HALO,
        FireworkKind.SENRIN,
    }


def test_future_firework_shapes_exist() -> None:
    assert {shape.name for shape in FireworkShape} == {
        "SPHERE",
        "RING",
        "WILLOW",
        "SPIRAL",
        "MULTI_RING",
        "HALO",
        "SENRIN_SEED",
    }


def test_trail_preset_construction() -> None:
    trail = TrailPreset(
        rate=0.32,
        speed_threshold=1.05,
        early_ratio=0.48,
        strong_speed=1.45,
    )

    assert trail.draw_every == 1


def test_trail_preset_rejects_invalid_draw_every() -> None:
    with pytest.raises(ValueError, match="draw_every"):
        TrailPreset(
            rate=0.1,
            speed_threshold=0.0,
            early_ratio=0.5,
            strong_speed=1.0,
            draw_every=0,
        )


def test_firework_preset_can_represent_negative_gravity_and_partial_trails() -> None:
    trail = TrailPreset(
        rate=0.32,
        speed_threshold=1.05,
        early_ratio=0.48,
        strong_speed=1.45,
    )
    preset = FireworkPreset(
        kind=FireworkKind.KIKU,
        label="Kiku",
        shape=FireworkShape.SPHERE,
        particle_count=112,
        speed_range=(0.90, 1.65),
        life_range=(55, 85),
        palette=(10, 9, 7),
        fade_mid=9,
        fade_dark=2,
        tip_color=7,
        drag=0.985,
        gravity=-0.025,
        trail=trail,
    )

    assert preset.gravity < 0.0
    assert preset.trail.rate < 1.0
    assert preset.secondary is None


def test_secondary_preset_construction() -> None:
    trail = TrailPreset(
        rate=0.06,
        speed_threshold=0.0,
        early_ratio=0.25,
        strong_speed=0.5,
        draw_every=2,
    )
    secondary = SecondaryPreset(
        rate=0.78,
        count_range=(8, 14),
        delay_range=(14, 28),
        speed_range=(0.28, 0.68),
        life_range=(28, 48),
        palette=(7, 10, 9, 14),
        fade_mid=9,
        fade_dark=2,
        tip_color=7,
        drag=0.982,
        gravity=-0.025,
        trail=trail,
    )

    assert secondary.gravity < 0.0
    assert secondary.trail.draw_every == 2


def test_firework_preset_module_has_no_pyxel_dependency() -> None:
    module = importlib.import_module("pyxel_goal_game.firework_presets")

    assert "pyxel" not in module.__dict__
