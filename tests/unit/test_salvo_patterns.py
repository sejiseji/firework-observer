from __future__ import annotations

import pytest

from pyxel_goal_game.camera3d import Vec3
from pyxel_goal_game.salvo_patterns import (
    DEFAULT_SALVO_INTERVAL_FRAMES,
    SALVO_LAUNCH_Y_RATIO,
    build_salvo_plan,
)
from pyxel_goal_game.screen_profiles import (
    CLASSIC_PROFILE,
    IPHONE16_BALANCED_PROFILE,
    ScreenProfile,
)


def assert_inside_box(point: Vec3, profile: ScreenProfile) -> None:
    assert -profile.box_width / 2 <= point.x <= profile.box_width / 2
    assert -profile.box_height / 2 <= point.y <= profile.box_height / 2
    assert -profile.box_depth / 2 <= point.z <= profile.box_depth / 2


@pytest.mark.parametrize("count", [1, 2, 3, 4, 5])
def test_build_salvo_plan_has_requested_slot_count(count: int) -> None:
    plan = build_salvo_plan(count=count, profile=CLASSIC_PROFILE)

    assert len(plan.slots) == count
    assert plan.interval_frames == DEFAULT_SALVO_INTERVAL_FRAMES


@pytest.mark.parametrize("count", [0, 6])
def test_build_salvo_plan_rejects_invalid_counts(count: int) -> None:
    with pytest.raises(ValueError, match="count"):
        build_salvo_plan(count=count, profile=CLASSIC_PROFILE)


def test_build_salvo_plan_rejects_invalid_interval() -> None:
    with pytest.raises(ValueError, match="interval_frames"):
        build_salvo_plan(count=1, profile=CLASSIC_PROFILE, interval_frames=0)


@pytest.mark.parametrize("count", [1, 2, 3, 4, 5])
def test_salvo_positions_are_inside_box(count: int) -> None:
    plan = build_salvo_plan(count=count, profile=IPHONE16_BALANCED_PROFILE)

    for slot in plan.slots:
        assert_inside_box(slot.launch_position, IPHONE16_BALANCED_PROFILE)
        assert_inside_box(slot.burst_position, IPHONE16_BALANCED_PROFILE)


def test_salvo_delay_frames_are_consecutive_interval_steps() -> None:
    plan = build_salvo_plan(
        count=5,
        profile=CLASSIC_PROFILE,
        interval_frames=9,
    )

    assert [slot.delay_frames for slot in plan.slots] == [0, 9, 18, 27, 36]
    assert [slot.seed_offset for slot in plan.slots] == [0, 1, 2, 3, 4]


def test_single_salvo_uses_center_high_burst_position() -> None:
    plan = build_salvo_plan(count=1, profile=CLASSIC_PROFILE)
    slot = plan.slots[0]

    assert slot.launch_position == Vec3(
        x=0.0,
        y=SALVO_LAUNCH_Y_RATIO * CLASSIC_PROFILE.box_height / 2,
        z=0.0,
    )
    assert slot.burst_position == Vec3(
        x=0.0,
        y=0.55 * CLASSIC_PROFILE.box_height / 2,
        z=0.0,
    )


def test_salvo_positions_scale_with_profile_dimensions() -> None:
    classic = build_salvo_plan(count=5, profile=CLASSIC_PROFILE)
    balanced = build_salvo_plan(count=5, profile=IPHONE16_BALANCED_PROFILE)

    assert balanced.slots[0].burst_position.x == classic.slots[0].burst_position.x
    assert balanced.slots[0].burst_position.z == classic.slots[0].burst_position.z
    assert balanced.slots[2].burst_position.y > classic.slots[2].burst_position.y
    assert balanced.slots[2].launch_position.y < classic.slots[2].launch_position.y


def test_salvo_plan_is_deterministic_for_same_profile_and_count() -> None:
    first = build_salvo_plan(count=4, profile=IPHONE16_BALANCED_PROFILE)
    second = build_salvo_plan(count=4, profile=IPHONE16_BALANCED_PROFILE)

    assert first == second
