from __future__ import annotations

from dataclasses import dataclass
from random import Random

from pyxel_goal_game.camera3d import Vec3
from pyxel_goal_game.firework_presets import FireworkKind
from pyxel_goal_game.runtime.state import (
    FIRST_GENERATION_FIREWORK_ORDER,
    MAX_SALVO_COUNT,
    MIN_SALVO_COUNT,
)
from pyxel_goal_game.salvo_patterns import SalvoPlan, build_salvo_plan
from pyxel_goal_game.screen_profiles import ScreenProfile

HEIGHT_VARIATION_RATIO = 0.16
PERSISTENT_SALVO_REPEAT_FRAMES = 210
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
) -> RuntimeLaunchSchedule:
    _validate_seed(seed)
    _validate_start_frame(start_frame)
    if burst_origin is None:
        burst_origin = Vec3(0.0, 0.0, 0.0)
    firework_kind = choose_runtime_firework_kind(
        selected_firework_kind=selected_firework_kind,
        random_firework_mode=random_firework_mode,
        random_seed=seed if random_seed is None else random_seed,
        previous_firework_kind=previous_firework_kind,
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


def choose_random_salvo_count(*, seed: int) -> int:
    _validate_seed(seed)
    return Random(seed).randint(MIN_SALVO_COUNT, MAX_SALVO_COUNT)


def choose_runtime_firework_kind(
    *,
    selected_firework_kind: FireworkKind,
    random_firework_mode: bool,
    random_seed: int,
    previous_firework_kind: FireworkKind | None = None,
) -> FireworkKind:
    return choose_runtime_firework_kinds(
        count=1,
        selected_firework_kind=selected_firework_kind,
        random_firework_mode=random_firework_mode,
        random_seed=random_seed,
        previous_firework_kind=previous_firework_kind,
    )[0]


def choose_runtime_firework_kinds(
    *,
    count: int,
    selected_firework_kind: FireworkKind,
    random_firework_mode: bool,
    random_seed: int,
    previous_firework_kind: FireworkKind | None = None,
) -> tuple[FireworkKind, ...]:
    if count < 1:
        msg = "count must be at least 1"
        raise ValueError(msg)
    _validate_first_generation_kind(selected_firework_kind)
    if previous_firework_kind is not None:
        _validate_first_generation_kind(previous_firework_kind)
    if not random_firework_mode:
        return tuple(selected_firework_kind for _ in range(count))

    _validate_seed(random_seed)
    rng = Random(random_seed)
    chosen: list[FireworkKind] = []
    previous = previous_firework_kind
    for _ in range(count):
        index = rng.randrange(len(FIRST_GENERATION_FIREWORK_ORDER))
        firework_kind = FIRST_GENERATION_FIREWORK_ORDER[index]
        if (
            previous is not None
            and len(FIRST_GENERATION_FIREWORK_ORDER) > 1
            and firework_kind is previous
        ):
            firework_kind = FIRST_GENERATION_FIREWORK_ORDER[
                (index + 1) % len(FIRST_GENERATION_FIREWORK_ORDER)
            ]
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
    rng = Random(seed)
    return _vary_burst_height(position=position, profile=profile, rng=rng)


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
    rng = Random(height_seed)
    return tuple(
        _vary_burst_height(position=slot.burst_position, profile=profile, rng=rng)
        for slot in plan.slots
    )


def default_shell_launch_origin(*, profile: ScreenProfile, burst_origin: Vec3) -> Vec3:
    return Vec3(
        x=burst_origin.x,
        y=-profile.box_height * 0.46,
        z=burst_origin.z,
    )


def _vary_burst_height(*, position: Vec3, profile: ScreenProfile, rng: Random) -> Vec3:
    half_height = profile.box_height / 2
    varied_y = position.y + rng.uniform(
        -HEIGHT_VARIATION_RATIO,
        HEIGHT_VARIATION_RATIO,
    ) * half_height
    return Vec3(
        x=position.x,
        y=max(-half_height, min(half_height, varied_y)),
        z=position.z,
    )


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
    if firework_kind not in FIRST_GENERATION_FIREWORK_ORDER:
        msg = "firework_kind must be a first-generation FireworkKind"
        raise ValueError(msg)
