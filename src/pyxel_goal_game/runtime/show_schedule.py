from __future__ import annotations

from dataclasses import dataclass
from random import Random

from pyxel_goal_game.camera3d import Vec3
from pyxel_goal_game.firework_presets import FireworkKind
from pyxel_goal_game.runtime.state import (
    FIRST_GENERATION_FIREWORK_ORDER,
    MAX_SALVO_COUNT,
    MIN_SALVO_COUNT,
    SINGLE_LAUNCH_RANDOM_FIREWORK_ORDER,
)
from pyxel_goal_game.salvo_patterns import (
    DEFAULT_SALVO_INTERVAL_FRAMES,
    SALVO_LAUNCH_Y_RATIO,
    SalvoPlan,
    build_salvo_plan,
)
from pyxel_goal_game.screen_profiles import ScreenProfile

HEIGHT_VARIATION_LEVEL_RATIOS = (0.36, 0.50, 0.64)
PERSISTENT_SALVO_REPEAT_FRAMES = 210
INWARD_PAIR_REPEAT_FRAMES = 240
INWARD_PAIR_INTERVAL_FRAMES = DEFAULT_SALVO_INTERVAL_FRAMES
INWARD_PAIR_SLOT_COUNT = 10
INWARD_PAIR_WAVE_PAIRS = ((0, 9), (1, 8), (2, 7), (3, 6), (4, 5))
INWARD_PAIR_X_RATIO_START = -0.78
INWARD_PAIR_X_RATIO_END = 0.78
DEFAULT_SINGLE_LAUNCH_FRAME_OFFSET = 0


@dataclass(frozen=True)
class RuntimeLaunchSlot:
    frame_offset: int
    launch_origin: Vec3
    burst_origin: Vec3
    firework_kind: FireworkKind
    seed: int


@dataclass(frozen=True)
class RuntimeLaunchSchedule:
    start_frame: int
    slots: tuple[RuntimeLaunchSlot, ...]
    repeat_after_frames: int | None = None


def build_single_launch_schedule(
    *,
    profile: ScreenProfile,
    start_frame: int,
    seed: int,
    selected_firework_kind: FireworkKind,
    random_firework_mode: bool = False,
    random_seed: int | None = None,
    previous_firework_kind: FireworkKind | None = None,
    burst_origin: Vec3 | None = None,
    height_variation: bool = False,
    height_seed: int | None = None,
) -> RuntimeLaunchSchedule:
    _validate_seed(seed)
    _validate_start_frame(start_frame)
    if burst_origin is None:
        burst_origin = Vec3(0.0, 0.0, 0.0)
    burst_origin = choose_runtime_burst_height(
        position=burst_origin,
        profile=profile,
        height_variation=height_variation,
        seed=seed if height_seed is None else height_seed,
    )
    firework_kind = choose_runtime_firework_kind(
        selected_firework_kind=selected_firework_kind,
        random_firework_mode=random_firework_mode,
        random_seed=seed if random_seed is None else random_seed,
        previous_firework_kind=previous_firework_kind,
        random_firework_order=SINGLE_LAUNCH_RANDOM_FIREWORK_ORDER,
    )
    return RuntimeLaunchSchedule(
        start_frame=start_frame,
        slots=(
            RuntimeLaunchSlot(
                frame_offset=DEFAULT_SINGLE_LAUNCH_FRAME_OFFSET,
                launch_origin=default_shell_launch_origin(
                    profile=profile,
                    burst_origin=burst_origin,
                ),
                burst_origin=burst_origin,
                firework_kind=firework_kind,
                seed=seed,
            ),
        ),
    )


def build_fixed_salvo_schedule(
    *,
    count: int,
    profile: ScreenProfile,
    start_frame: int,
    base_seed: int,
    selected_firework_kind: FireworkKind,
    random_firework_mode: bool = False,
    random_seed: int | None = None,
    previous_firework_kind: FireworkKind | None = None,
    height_variation: bool = False,
    height_seed: int | None = None,
    repeat_after_frames: int | None = None,
) -> RuntimeLaunchSchedule:
    _validate_start_frame(start_frame)
    _validate_seed(base_seed)
    _validate_salvo_count(count)
    plan = build_salvo_plan(count=count, profile=profile)
    firework_kinds = choose_runtime_firework_kinds(
        count=len(plan.slots),
        selected_firework_kind=selected_firework_kind,
        random_firework_mode=random_firework_mode,
        random_seed=base_seed if random_seed is None else random_seed,
        previous_firework_kind=previous_firework_kind,
    )
    burst_origins = choose_runtime_burst_origins(
        plan=plan,
        profile=profile,
        height_variation=height_variation,
        height_seed=base_seed if height_seed is None else height_seed,
    )
    return RuntimeLaunchSchedule(
        start_frame=start_frame,
        slots=tuple(
            RuntimeLaunchSlot(
                frame_offset=slot.delay_frames,
                launch_origin=slot.launch_position,
                burst_origin=burst_origin,
                firework_kind=firework_kind,
                seed=base_seed + slot.seed_offset,
            )
            for slot, burst_origin, firework_kind in zip(
                plan.slots,
                burst_origins,
                firework_kinds,
                strict=True,
            )
        ),
        repeat_after_frames=repeat_after_frames,
    )


def build_random_count_salvo_schedule(
    *,
    profile: ScreenProfile,
    start_frame: int,
    base_seed: int,
    selected_firework_kind: FireworkKind,
    count_seed: int,
    random_firework_mode: bool = False,
    random_seed: int | None = None,
    previous_firework_kind: FireworkKind | None = None,
    height_variation: bool = False,
    height_seed: int | None = None,
    repeat_after_frames: int | None = None,
) -> RuntimeLaunchSchedule:
    count = choose_random_salvo_count(seed=count_seed)
    return build_fixed_salvo_schedule(
        count=count,
        profile=profile,
        start_frame=start_frame,
        base_seed=base_seed,
        selected_firework_kind=selected_firework_kind,
        random_firework_mode=random_firework_mode,
        random_seed=random_seed,
        previous_firework_kind=previous_firework_kind,
        height_variation=height_variation,
        height_seed=height_seed,
        repeat_after_frames=repeat_after_frames,
    )


def build_inward_pair_salvo_schedule(
    *,
    profile: ScreenProfile,
    start_frame: int,
    base_seed: int,
    selected_firework_kind: FireworkKind,
    random_firework_mode: bool = False,
    random_seed: int | None = None,
    previous_firework_kind: FireworkKind | None = None,
    height_variation: bool = False,
    height_seed: int | None = None,
    repeat_after_frames: int | None = None,
    interval_frames: int = INWARD_PAIR_INTERVAL_FRAMES,
) -> RuntimeLaunchSchedule:
    _validate_start_frame(start_frame)
    _validate_seed(base_seed)
    if interval_frames < 1:
        msg = "interval_frames must be at least 1"
        raise ValueError(msg)
    wave_kinds = choose_runtime_firework_kinds(
        count=len(INWARD_PAIR_WAVE_PAIRS),
        selected_firework_kind=selected_firework_kind,
        random_firework_mode=random_firework_mode,
        random_seed=base_seed if random_seed is None else random_seed,
        previous_firework_kind=previous_firework_kind,
    )
    launch_positions, burst_positions = build_inward_pair_positions(
        profile=profile,
        height_variation=height_variation,
        height_seed=base_seed if height_seed is None else height_seed,
    )
    slots: list[RuntimeLaunchSlot] = []
    for wave_index, (left_index, right_index) in enumerate(INWARD_PAIR_WAVE_PAIRS):
        frame_offset = wave_index * interval_frames
        firework_kind = wave_kinds[wave_index]
        seed_offset = wave_index * 6
        for slot_index, pair_seed_offset in (
            (left_index, seed_offset),
            (right_index, seed_offset + 3),
        ):
            slots.append(
                RuntimeLaunchSlot(
                    frame_offset=frame_offset,
                    launch_origin=launch_positions[slot_index],
                    burst_origin=burst_positions[slot_index],
                    firework_kind=firework_kind,
                    seed=base_seed + pair_seed_offset,
                )
            )
    return RuntimeLaunchSchedule(
        start_frame=start_frame,
        slots=tuple(slots),
        repeat_after_frames=repeat_after_frames,
    )


def build_inward_pair_positions(
    *,
    profile: ScreenProfile,
    height_variation: bool = False,
    height_seed: int = 0,
) -> tuple[tuple[Vec3, ...], tuple[Vec3, ...]]:
    _validate_seed(height_seed)
    half_width = profile.box_width / 2
    half_height = profile.box_height / 2
    half_depth = profile.box_depth / 2
    x_step = (INWARD_PAIR_X_RATIO_END - INWARD_PAIR_X_RATIO_START) / (
        INWARD_PAIR_SLOT_COUNT - 1
    )
    x_positions = tuple(
        (INWARD_PAIR_X_RATIO_START + index * x_step) * half_width
        for index in range(INWARD_PAIR_SLOT_COUNT)
    )
    burst_y_by_wave = (0.42, 0.52, 0.62, 0.56, 0.48)
    z_by_wave = (0.10, -0.07, 0.05, -0.03, 0.02)
    launch_positions = [Vec3(x=x, y=SALVO_LAUNCH_Y_RATIO * half_height, z=0.0) for x in x_positions]
    burst_positions = [Vec3(x=x, y=0.0, z=0.0) for x in x_positions]
    for wave_index, (left_index, right_index) in enumerate(INWARD_PAIR_WAVE_PAIRS):
        y = burst_y_by_wave[wave_index] * half_height
        if height_variation:
            y = _choose_three_step_height(
                profile=profile,
                seed=height_seed + wave_index,
            )
        z = z_by_wave[wave_index] * half_depth
        burst_positions[left_index] = Vec3(x=x_positions[left_index], y=y, z=z)
        burst_positions[right_index] = Vec3(x=x_positions[right_index], y=y, z=-z)
    return tuple(launch_positions), tuple(burst_positions)


def choose_random_salvo_count(*, seed: int) -> int:
    _validate_seed(seed)
    return Random(seed).randint(MIN_SALVO_COUNT, MAX_SALVO_COUNT)


def choose_runtime_firework_kind(
    *,
    selected_firework_kind: FireworkKind,
    random_firework_mode: bool,
    random_seed: int,
    previous_firework_kind: FireworkKind | None = None,
    random_firework_order: tuple[FireworkKind, ...] = FIRST_GENERATION_FIREWORK_ORDER,
) -> FireworkKind:
    return choose_runtime_firework_kinds(
        count=1,
        selected_firework_kind=selected_firework_kind,
        random_firework_mode=random_firework_mode,
        random_seed=random_seed,
        previous_firework_kind=previous_firework_kind,
        random_firework_order=random_firework_order,
    )[0]


def choose_runtime_firework_kinds(
    *,
    count: int,
    selected_firework_kind: FireworkKind,
    random_firework_mode: bool,
    random_seed: int,
    previous_firework_kind: FireworkKind | None = None,
    random_firework_order: tuple[FireworkKind, ...] = FIRST_GENERATION_FIREWORK_ORDER,
) -> tuple[FireworkKind, ...]:
    if count < 1:
        msg = "count must be at least 1"
        raise ValueError(msg)
    _validate_firework_kind(selected_firework_kind)
    if previous_firework_kind is not None:
        _validate_firework_kind(previous_firework_kind)
    if not random_firework_order:
        msg = "random_firework_order must not be empty"
        raise ValueError(msg)
    for firework_kind in random_firework_order:
        _validate_firework_kind(firework_kind)
    if selected_firework_kind not in random_firework_order:
        msg = "selected_firework_kind must be in random_firework_order"
        raise ValueError(msg)
    if not random_firework_mode:
        return tuple(selected_firework_kind for _ in range(count))

    _validate_seed(random_seed)
    rng = Random(random_seed)
    chosen: list[FireworkKind] = []
    previous = previous_firework_kind
    for _ in range(count):
        index = rng.randrange(len(random_firework_order))
        firework_kind = random_firework_order[index]
        if (
            previous is not None
            and previous in random_firework_order
            and len(random_firework_order) > 1
            and firework_kind is previous
        ):
            firework_kind = random_firework_order[(index + 1) % len(random_firework_order)]
        chosen.append(firework_kind)
        previous = firework_kind
    return tuple(chosen)


def choose_runtime_burst_height(
    *,
    position: Vec3,
    profile: ScreenProfile,
    height_variation: bool,
    seed: int,
) -> Vec3:
    if not height_variation:
        return position
    _validate_seed(seed)
    return _with_three_step_height(position=position, profile=profile, seed=seed)


def choose_runtime_burst_origins(
    *,
    plan: SalvoPlan,
    profile: ScreenProfile,
    height_variation: bool,
    height_seed: int,
) -> tuple[Vec3, ...]:
    if not height_variation:
        return tuple(slot.burst_position for slot in plan.slots)
    _validate_seed(height_seed)
    return tuple(
        _with_three_step_height(
            position=slot.burst_position,
            profile=profile,
            seed=height_seed + index,
        )
        for index, slot in enumerate(plan.slots)
    )


def default_shell_launch_origin(*, profile: ScreenProfile, burst_origin: Vec3) -> Vec3:
    return Vec3(
        x=burst_origin.x,
        y=-profile.box_height * 0.46,
        z=burst_origin.z,
    )


def _with_three_step_height(*, position: Vec3, profile: ScreenProfile, seed: int) -> Vec3:
    return Vec3(
        x=position.x,
        y=_choose_three_step_height(profile=profile, seed=seed),
        z=position.z,
    )


def _choose_three_step_height(*, profile: ScreenProfile, seed: int) -> float:
    _validate_seed(seed)
    half_height = profile.box_height / 2
    ratio = HEIGHT_VARIATION_LEVEL_RATIOS[Random(seed).randrange(3)]
    return _clamp_to_half_height(ratio * half_height, half_height)


def _clamp_to_half_height(value: float, half_height: float) -> float:
    return max(-half_height, min(half_height, value))


def _validate_salvo_count(count: int) -> None:
    if not MIN_SALVO_COUNT <= count <= MAX_SALVO_COUNT:
        msg = f"count must be between {MIN_SALVO_COUNT} and {MAX_SALVO_COUNT}"
        raise ValueError(msg)


def _validate_start_frame(start_frame: int) -> None:
    if start_frame < 0:
        msg = "start_frame must be non-negative"
        raise ValueError(msg)


def _validate_seed(seed: int) -> None:
    if seed < 0:
        msg = "seed must be non-negative"
        raise ValueError(msg)


def _validate_first_generation_kind(firework_kind: FireworkKind) -> None:
    _validate_firework_kind(firework_kind)
    if firework_kind not in FIRST_GENERATION_FIREWORK_ORDER:
        msg = "firework_kind must be a first-generation FireworkKind"
        raise ValueError(msg)


def _validate_firework_kind(firework_kind: FireworkKind) -> None:
    if not isinstance(firework_kind, FireworkKind):
        msg = "firework_kind must be a FireworkKind"
        raise ValueError(msg)
