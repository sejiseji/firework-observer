from __future__ import annotations

import importlib

import pytest

from pyxel_goal_game.firework_presets import (
    FIREWORK_COLOR_PALETTES,
    FUTURE_FIREWORK_KINDS,
    SMILE_PRESET,
    FireworkColorPalette,
    FireworkKind,
    FireworkPreset,
    FireworkShape,
    SecondaryPreset,
    TrailPreset,
    select_firework_palette,
)


def test_future_firework_kinds_exist() -> None:
    assert set(FUTURE_FIREWORK_KINDS) == {
        FireworkKind.KIKU,
        FireworkKind.SPHERE_BLOOM,
        FireworkKind.SMILE,
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
        "SMILE",
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


def test_smile_preset_is_shaped_firework() -> None:
    assert SMILE_PRESET.kind is FireworkKind.SMILE
    assert SMILE_PRESET.label == "Smile"
    assert SMILE_PRESET.shape is FireworkShape.SMILE
    assert SMILE_PRESET.particle_count == 82
    assert SMILE_PRESET.speed_range == (0.62, 1.08)
    assert SMILE_PRESET.trail.draw_every == 2
    assert SMILE_PRESET.secondary is None


def test_firework_color_palette_construction_validates_pyxel_colors() -> None:
    palette = FireworkColorPalette("test", (7, 10), secondary_colors=(12,))

    assert palette.colors == (7, 10)
    assert palette.secondary_colors == (12,)

    with pytest.raises(ValueError, match="must not be empty"):
        FireworkColorPalette("empty", ())

    with pytest.raises(ValueError, match="valid Pyxel"):
        FireworkColorPalette("invalid", (16,))


def test_every_firework_kind_has_three_color_palettes() -> None:
    assert set(FIREWORK_COLOR_PALETTES) == set(FUTURE_FIREWORK_KINDS)
    for kind, palettes in FIREWORK_COLOR_PALETTES.items():
        assert len(palettes) == 3, kind
        for palette in palettes:
            assert palette.colors
            assert all(0 <= color <= 15 for color in palette.colors)
            if palette.secondary_colors is not None:
                assert all(0 <= color <= 15 for color in palette.secondary_colors)


def test_firework_palette_selection_is_deterministic_by_seed() -> None:
    assert select_firework_palette(FireworkKind.KIKU, 0) is select_firework_palette(
        FireworkKind.KIKU,
        0,
    )
    assert {
        select_firework_palette(FireworkKind.KIKU, seed).name
        for seed in range(6)
    } == {palette.name for palette in FIREWORK_COLOR_PALETTES[FireworkKind.KIKU]}


def test_firework_preset_module_has_no_pyxel_dependency() -> None:
    module = importlib.import_module("pyxel_goal_game.firework_presets")

    assert "pyxel" not in module.__dict__
