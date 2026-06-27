from __future__ import annotations

import inspect

import pytest

from pyxel_goal_game.camera3d import Vec3
from pyxel_goal_game.firework_presets import FireworkKind
from pyxel_goal_game.runtime import show_schedule
from pyxel_goal_game.runtime.show_schedule import (
    PERSISTENT_SALVO_REPEAT_FRAMES,
    RuntimeLaunchSchedule,
    build_fixed_salvo_schedule,
    build_random_count_salvo_schedule,
    build_single_launch_schedule,
    choose_random_salvo_count,
    choose_runtime_burst_height,
    choose_runtime_firework_kinds,
    default_shell_launch_origin,
)
from pyxel_goal_game.runtime.state import FIRST_GENERATION_FIREWORK_ORDER
from pyxel_goal_game.screen_profiles import CLASSIC_PROFILE, IPHONE16_BALANCED_PROFILE


def assert_inside_box(point: Vec3) -> None:
    profile = IPHONE16_BALANCED_PROFILE
    assert -profile.box_width / 2 <= point.x <= profile.box_width / 2
    assert -profile.box_height / 2 <= point.y <= profile.box_height / 2
    assert -profile.box_depth / 2 <= point.z <= profile.box_depth / 2


def test_show_schedule_imports_without_pyxel_or_tools() -> None:
    source = inspect.getsource(show_schedule)

    assert "import pyxel" not in source
    assert "tools.preview_firework_box" not in source


def test_single_launch_schedule_has_one_slot() -> None:
    schedule = build_single_launch_schedule(
        profile=IPHONE16_BALANCED_PROFILE,
        start_frame=24,
        seed=7,
        selected_firework_kind=FireworkKind.KIKU,
    )

    assert isinstance(schedule, RuntimeLaunchSchedule)
    assert schedule.start_frame == 24
    assert schedule.repeat_after_frames is None
    assert len(schedule.slots) == 1
    slot = schedule.slots[0]
    assert slot.frame_offset == 0
    assert slot.firework_kind is FireworkKind.KIKU
    assert slot.seed == 7
    assert slot.burst_origin == Vec3(0.0, 0.0, 0.0)
    assert slot.launch_origin == default_shell_launch_origin(
        profile=IPHONE16_BALANCED_PROFILE,
        burst_origin=slot.burst_origin,
    )


@pytest.mark.parametrize("count", [1, 2, 3, 4, 5])
def test_fixed_salvo_schedule_slot_counts_and_offsets(count: int) -> None:
    schedule = build_fixed_salvo_schedule(
        count=count,
        profile=IPHONE16_BALANCED_PROFILE,
        start_frame=100,
        base_seed=40,
        selected_firework_kind=FireworkKind.RING,
    )

    assert len(schedule.slots) == count
    assert [slot.frame_offset for slot in schedule.slots] == [
        index * 12 for index in range(count)
    ]
    assert [slot.seed for slot in schedule.slots] == [
        40 + index for index in range(count)
    ]
    assert {slot.firework_kind for slot in schedule.slots} == {FireworkKind.RING}


def test_random_count_salvo_count_stays_in_allowed_range() -> None:
    counts = {choose_random_salvo_count(seed=seed) for seed in range(20)}

    assert all(1 <= count <= 5 for count in counts)
    assert len(counts) > 1


def test_fixed_schedule_is_deterministic_for_same_inputs() -> None:
    first = build_fixed_salvo_schedule(
        count=5,
        profile=IPHONE16_BALANCED_PROFILE,
        start_frame=10,
        base_seed=99,
        selected_firework_kind=FireworkKind.PEONY,
        random_firework_mode=True,
        random_seed=123,
        previous_firework_kind=FireworkKind.KIKU,
        height_variation=True,
        height_seed=456,
        repeat_after_frames=PERSISTENT_SALVO_REPEAT_FRAMES,
    )
    second = build_fixed_salvo_schedule(
        count=5,
        profile=IPHONE16_BALANCED_PROFILE,
        start_frame=10,
        base_seed=99,
        selected_firework_kind=FireworkKind.PEONY,
        random_firework_mode=True,
        random_seed=123,
        previous_firework_kind=FireworkKind.KIKU,
        height_variation=True,
        height_seed=456,
        repeat_after_frames=PERSISTENT_SALVO_REPEAT_FRAMES,
    )

    assert first == second
    assert first.repeat_after_frames == PERSISTENT_SALVO_REPEAT_FRAMES


def test_different_seed_can_change_random_kind_schedule() -> None:
    first = choose_runtime_firework_kinds(
        count=3,
        selected_firework_kind=FireworkKind.KIKU,
        random_firework_mode=True,
        random_seed=1,
    )
    second = choose_runtime_firework_kinds(
        count=3,
        selected_firework_kind=FireworkKind.KIKU,
        random_firework_mode=True,
        random_seed=3,
    )

    assert first != second


def test_random_firework_selection_uses_first_generation_kinds_only() -> None:
    kinds = choose_runtime_firework_kinds(
        count=24,
        selected_firework_kind=FireworkKind.KIKU,
        random_firework_mode=True,
        random_seed=0,
    )

    assert set(kinds).issubset(set(FIRST_GENERATION_FIREWORK_ORDER))


def test_scheduled_firework_kind_is_frozen_per_slot() -> None:
    schedule = build_fixed_salvo_schedule(
        count=5,
        profile=IPHONE16_BALANCED_PROFILE,
        start_frame=0,
        base_seed=5,
        selected_firework_kind=FireworkKind.WILLOW,
        random_firework_mode=True,
        random_seed=2,
    )

    assert tuple(slot.firework_kind for slot in schedule.slots) == (
        FireworkKind.KIKU,
        FireworkKind.SPHERE_BLOOM,
        FireworkKind.SMILE,
        FireworkKind.WILLOW,
        FireworkKind.SMILE,
    )


def test_height_variation_stays_inside_box() -> None:
    base = Vec3(0.0, IPHONE16_BALANCED_PROFILE.box_height / 2 * 0.90, 0.0)
    varied = choose_runtime_burst_height(
        position=base,
        profile=IPHONE16_BALANCED_PROFILE,
        height_variation=True,
        seed=8,
    )

    assert_inside_box(varied)
    assert varied.x == base.x
    assert varied.z == base.z


def test_schedule_origins_are_inside_box() -> None:
    schedule = build_fixed_salvo_schedule(
        count=5,
        profile=IPHONE16_BALANCED_PROFILE,
        start_frame=0,
        base_seed=11,
        selected_firework_kind=FireworkKind.MULTI_RING,
        height_variation=True,
        height_seed=12,
    )

    for slot in schedule.slots:
        assert_inside_box(slot.launch_origin)
        assert_inside_box(slot.burst_origin)


def test_random_count_schedule_uses_deterministic_count() -> None:
    schedule = build_random_count_salvo_schedule(
        profile=CLASSIC_PROFILE,
        start_frame=0,
        base_seed=2,
        selected_firework_kind=FireworkKind.HALO,
        count_seed=2,
    )

    assert len(schedule.slots) == 1


def test_invalid_salvo_count_and_seed_are_rejected() -> None:
    with pytest.raises(ValueError, match="count"):
        build_fixed_salvo_schedule(
            count=0,
            profile=IPHONE16_BALANCED_PROFILE,
            start_frame=0,
            base_seed=1,
            selected_firework_kind=FireworkKind.KIKU,
        )

    with pytest.raises(ValueError, match="seed"):
        choose_random_salvo_count(seed=-1)
