from __future__ import annotations

from dataclasses import replace

from pyxel_goal_game.firework_presets import FireworkKind
from pyxel_goal_game.runtime.state import (
    AUTO_ROTATE_SPEED_MODE_ORDER,
    FIRST_GENERATION_FIREWORK_ORDER,
    MAX_SALVO_COUNT,
    MIN_SALVO_COUNT,
    RuntimeShowState,
    SalvoCountMode,
)


def cycle_firework_kind(state: RuntimeShowState) -> RuntimeShowState:
    return replace(
        state,
        selected_firework_kind=_next_in_order(
            state.selected_firework_kind,
            FIRST_GENERATION_FIREWORK_ORDER,
        ),
    )


def select_firework_kind(
    state: RuntimeShowState,
    firework_kind: FireworkKind,
) -> RuntimeShowState:
    if firework_kind not in FIRST_GENERATION_FIREWORK_ORDER:
        msg = "firework_kind must be a first-generation firework kind"
        raise ValueError(msg)
    return replace(state, selected_firework_kind=firework_kind)


def toggle_random_mode(state: RuntimeShowState) -> RuntimeShowState:
    return _replace_toggle(
        state,
        random_firework_mode=not state.toggles.random_firework_mode,
    )


def toggle_auto_launch(state: RuntimeShowState) -> RuntimeShowState:
    auto_launch = not state.toggles.auto_launch
    state = _replace_toggle(state, auto_launch=auto_launch)
    if auto_launch:
        return clear_persistent_salvo_mode(state)
    return state


def toggle_height_variation(state: RuntimeShowState) -> RuntimeShowState:
    return _replace_toggle(state, height_variation=not state.toggles.height_variation)


def toggle_stars(state: RuntimeShowState) -> RuntimeShowState:
    return _replace_toggle(
        state,
        interior_stars_visible=not state.toggles.interior_stars_visible,
    )


def toggle_scenery_visible(state: RuntimeShowState) -> RuntimeShowState:
    return _replace_toggle(state, scenery_visible=not state.toggles.scenery_visible)


def toggle_auto_rotate(state: RuntimeShowState) -> RuntimeShowState:
    return _replace_toggle(state, auto_rotate=not state.toggles.auto_rotate)


def toggle_audio(state: RuntimeShowState) -> RuntimeShowState:
    return _replace_toggle(state, audio_enabled=not state.toggles.audio_enabled)


def cycle_auto_rotate_speed(state: RuntimeShowState) -> RuntimeShowState:
    return replace(
        state,
        auto_rotate_speed_mode=_next_in_order(
            state.auto_rotate_speed_mode,
            AUTO_ROTATE_SPEED_MODE_ORDER,
        ),
    )


def set_fixed_salvo_mode(
    state: RuntimeShowState,
    count: int,
) -> RuntimeShowState:
    if not MIN_SALVO_COUNT <= count <= MAX_SALVO_COUNT:
        msg = f"salvo count must be between {MIN_SALVO_COUNT} and {MAX_SALVO_COUNT}"
        raise ValueError(msg)
    return replace(
        _replace_toggle(state, auto_launch=False),
        salvo_count_mode=SalvoCountMode.FIXED,
        salvo_count=count,
    )


def set_random_salvo_mode(state: RuntimeShowState) -> RuntimeShowState:
    return replace(
        _replace_toggle(state, auto_launch=False),
        salvo_count_mode=SalvoCountMode.RANDOM,
        salvo_count=MIN_SALVO_COUNT,
    )


def clear_persistent_salvo_mode(state: RuntimeShowState) -> RuntimeShowState:
    return replace(
        state,
        salvo_count_mode=SalvoCountMode.OFF,
        salvo_count=MIN_SALVO_COUNT,
    )


def tick_frame(state: RuntimeShowState, frames: int = 1) -> RuntimeShowState:
    if frames < 0:
        msg = "frames must be non-negative"
        raise ValueError(msg)
    return replace(state, frame_count=state.frame_count + frames)


def advance_seed_base(state: RuntimeShowState, amount: int = 1) -> RuntimeShowState:
    if amount < 0:
        msg = "amount must be non-negative"
        raise ValueError(msg)
    return replace(state, seed_base=state.seed_base + amount)


def _replace_toggle(state: RuntimeShowState, **changes: bool) -> RuntimeShowState:
    return replace(state, toggles=replace(state.toggles, **changes))


def _next_in_order[T](current: T, order: tuple[T, ...]) -> T:
    index = order.index(current)
    return order[(index + 1) % len(order)]
