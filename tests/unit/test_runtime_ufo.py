from __future__ import annotations

import inspect

from pyxel_goal_game.runtime import ufo
from pyxel_goal_game.runtime.ufo import (
    UFO_CHECK_INTERVAL_FRAMES,
    UFO_INITIAL_DELAY_FRAMES,
    UfoState,
    build_ufo_flyby,
    initial_ufo_state,
    toggle_ufo_enabled,
    update_ufo_state,
)
from pyxel_goal_game.screen_profiles import get_screen_profile


def test_ufo_module_is_pure_runtime_helper() -> None:
    source = inspect.getsource(ufo)

    assert "import pyxel" not in source
    assert "tools.preview_firework_box" not in source
    assert "preview_firework_box" not in source


def test_initial_ufo_state_delays_first_possible_appearance() -> None:
    state = initial_ufo_state(start_frame=12)

    assert state.active is None
    assert state.next_check_frame == 12 + UFO_INITIAL_DELAY_FRAMES
    assert state.enabled is True


def test_ufo_flyby_is_deterministic_and_upper_region() -> None:
    profile = get_screen_profile("iphone16_balanced")
    first = build_ufo_flyby(profile=profile, start_frame=100, seed=1234)
    second = build_ufo_flyby(profile=profile, start_frame=100, seed=1234)

    assert first == second
    assert first.duration_frames > 0
    assert first.radius > 0
    half_width = profile.box_width / 2
    half_height = profile.box_height / 2
    half_depth = profile.box_depth / 2
    for point in (first.start, first.end, first.position_at(first.start_frame + 30)):
        assert -half_width <= point.x <= half_width
        assert point.y > half_height * 0.25
        assert -half_depth <= point.z <= half_depth


def test_ufo_state_never_stacks_active_flybys() -> None:
    profile = get_screen_profile("iphone16_balanced")
    flyby = build_ufo_flyby(profile=profile, start_frame=100, seed=44)
    state = UfoState(active=flyby, next_check_frame=100, enabled=True)

    updated = update_ufo_state(
        state,
        frame=flyby.start_frame + 20,
        profile=profile,
        seed=1,
    )

    assert updated.active == flyby


def test_ufo_state_uses_cooldown_after_finished_flyby() -> None:
    profile = get_screen_profile("iphone16_balanced")
    flyby = build_ufo_flyby(profile=profile, start_frame=100, seed=44)
    state = UfoState(active=flyby, next_check_frame=100, enabled=True)

    updated = update_ufo_state(
        state,
        frame=flyby.end_frame,
        profile=profile,
        seed=1,
    )

    assert updated.active is None
    assert updated.next_check_frame > flyby.end_frame


def test_ufo_scheduler_is_rare_not_always_active() -> None:
    profile = get_screen_profile("iphone16_balanced")
    state = initial_ufo_state()

    updated = update_ufo_state(
        state,
        frame=state.next_check_frame,
        profile=profile,
        seed=77,
    )

    assert updated.active is None or updated.active.start_frame == state.next_check_frame
    if updated.active is None:
        assert updated.next_check_frame == state.next_check_frame + UFO_CHECK_INTERVAL_FRAMES


def test_ufo_toggle_disables_and_clears_active_flyby() -> None:
    profile = get_screen_profile("iphone16_balanced")
    flyby = build_ufo_flyby(profile=profile, start_frame=100, seed=44)
    state = UfoState(active=flyby, next_check_frame=100, enabled=True)

    disabled = toggle_ufo_enabled(state, frame=150)
    updated = update_ufo_state(disabled, frame=200, profile=profile)

    assert disabled.enabled is False
    assert disabled.active is None
    assert updated.active is None
