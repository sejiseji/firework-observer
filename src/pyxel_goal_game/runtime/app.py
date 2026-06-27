from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from dataclasses import replace
from random import Random
from typing import Any

from pyxel_goal_game.ambient_box_stars import BoxStarField, build_box_star_field
from pyxel_goal_game.camera3d import Camera3D, Vec3
from pyxel_goal_game.firework_bursts import RingOrientationBank, build_ring_orientation_bank
from pyxel_goal_game.firework_presets import FireworkKind
from pyxel_goal_game.runtime import show_controller
from pyxel_goal_game.runtime.audio import RuntimeAudio
from pyxel_goal_game.runtime.camera_motion import (
    compute_pitch_sway,
    get_auto_rotate_yaw_delta,
)
from pyxel_goal_game.runtime.effects import (
    FIREWORK_PRESETS_BY_KIND,
    GLITTER_RESIDUE_MAX,
    ActiveParticle,
    ActiveShell,
    DelayedMiniBurst,
    GlitterResidue,
    build_active_particles_for_burst,
    build_delayed_mini_burst_garnish,
    build_delayed_mini_burst_particles,
    build_glitter_residue,
    build_secondary_particles,
    create_active_shell,
)
from pyxel_goal_game.runtime.show_schedule import (
    PERSISTENT_SALVO_REPEAT_FRAMES,
    RuntimeLaunchSchedule,
    RuntimeLaunchSlot,
    build_fixed_salvo_schedule,
    build_random_count_salvo_schedule,
    build_single_launch_schedule,
)
from pyxel_goal_game.runtime.state import (
    DEFAULT_FIREWORK_KIND,
    RuntimeShowState,
    SalvoCountMode,
)
from pyxel_goal_game.runtime.ufo import (
    UfoState,
    initial_ufo_state,
    toggle_ufo_enabled,
    update_ufo_state,
)
from pyxel_goal_game.scenery_presets import (
    SCENERY_PRESET_NAMES,
    SceneryPreset,
    get_scenery_preset,
)
from pyxel_goal_game.screen_profiles import get_screen_profile
from pyxel_goal_game.wire_box import WireBox

AUTO_LAUNCH_FRAMES = 120
RING_ORIENTATION_BANK_SEED = 20260623
RUNTIME_RANDOM_SEED = 20260625
DEFAULT_RUNTIME_PROFILE_NAME = "iphone16_balanced"

try:
    import pyxel
except ModuleNotFoundError:
    pyxel: Any = None


def require_pyxel() -> Any:
    if pyxel is None:
        raise RuntimeError(
            "Pyxel is required to launch Firework Observer. "
            "Install project dependencies or use the project virtual environment."
        )
    return pyxel


class RuntimeApp:
    def __init__(self, profile_name: str = DEFAULT_RUNTIME_PROFILE_NAME) -> None:
        require_pyxel()
        from pyxel_goal_game.runtime.input import handle_runtime_input
        from pyxel_goal_game.runtime.render import RuntimeRenderer

        self.profile = get_screen_profile(profile_name)
        self.state = RuntimeShowState(
            profile_name=profile_name,
            selected_firework_kind=DEFAULT_FIREWORK_KIND,
        )
        self.camera = Camera3D.from_profile(self.profile)
        self.box = WireBox.from_profile(self.profile)
        self.ring_orientation_bank: RingOrientationBank = build_ring_orientation_bank(
            seed=RING_ORIENTATION_BANK_SEED,
            count=24,
        )
        self.particles: list[ActiveParticle] = []
        self.glitter: list[GlitterResidue] = []
        self.shells: list[ActiveShell] = []
        self.mini_bursts: list[DelayedMiniBurst] = []
        self.preview_rng = Random(RUNTIME_RANDOM_SEED)
        self.last_launched_kind = DEFAULT_FIREWORK_KIND
        self.next_persistent_salvo_frame = 0
        self.debug = True
        self.scenery = self.load_scenery()
        self.star_field: BoxStarField = build_box_star_field(self.profile)
        self.ufo_state: UfoState = initial_ufo_state(
            enabled=self.state.toggles.ufo_enabled,
        )
        self.handle_runtime_input = handle_runtime_input
        self.renderer = RuntimeRenderer(self)
        pyxel.init(
            self.profile.width,
            self.profile.height,
            fps=60,
            title=f"Firework Observer Runtime - {self.profile.name}",
        )
        self.audio = RuntimeAudio(pyxel=pyxel, enabled=self.state.toggles.audio_enabled)
        self.audio.setup()
        self.audio.start_bgm()

    @property
    def burst_label(self) -> str:
        return FIREWORK_PRESETS_BY_KIND[self.state.selected_firework_kind].label

    @property
    def last_launched_label(self) -> str:
        return FIREWORK_PRESETS_BY_KIND[self.last_launched_kind].label

    @property
    def mode_label(self) -> str:
        return "RANDOM" if self.state.toggles.random_firework_mode else "SEQ"

    def run(self) -> None:
        pyxel.run(self.update, self.draw)

    def update(self) -> None:
        self.state = replace(self.state, frame_count=pyxel.frame_count)
        self.handle_runtime_input(self)
        if self.state.toggles.auto_rotate:
            mode = self.state.auto_rotate_speed_mode
            self.camera.target_yaw += get_auto_rotate_yaw_delta(mode)
            self.camera.target_pitch = compute_pitch_sway(
                frame=pyxel.frame_count,
                mode=mode,
            )
        if self.state.toggles.auto_launch and pyxel.frame_count % AUTO_LAUNCH_FRAMES == 0:
            self.launch()
        self.schedule_persistent_salvo_if_needed()
        self.update_ufo()
        self.update_shells()
        self.launch_due_mini_bursts()
        self.camera.step_toward_target()
        for particle in self.particles:
            particle.step()
        for glitter in self.glitter:
            glitter.step()
        self.launch_secondary_bursts()
        self.particles = [
            particle for particle in self.particles if particle.is_alive()
        ][-self.profile.max_particles :]
        self.glitter = [
            glitter for glitter in self.glitter if glitter.is_alive()
        ][-GLITTER_RESIDUE_MAX:]

    def draw(self) -> None:
        self.renderer.draw()

    def handle_space_cycle(self) -> None:
        if self.state.toggles.random_firework_mode:
            self.state = replace(
                self.state,
                selected_firework_kind=self.last_launched_kind,
                toggles=replace(self.state.toggles, random_firework_mode=False),
            )
        else:
            self.state = show_controller.cycle_firework_kind(self.state)

    def enable_random_mode(self) -> None:
        self.state = replace(
            self.state,
            toggles=replace(self.state.toggles, random_firework_mode=True),
        )

    def cycle_scenery(self) -> None:
        current_index = SCENERY_PRESET_NAMES.index(self.state.selected_scenery_name)
        next_name = SCENERY_PRESET_NAMES[
            (current_index + 1) % len(SCENERY_PRESET_NAMES)
        ]
        self.state = replace(self.state, selected_scenery_name=next_name)
        self.scenery = self.load_scenery()

    def load_scenery(self) -> SceneryPreset:
        return get_scenery_preset(
            self.state.selected_scenery_name,
            profile=self.profile,
        )

    def reset_camera(self) -> None:
        self.camera.yaw = 0.6
        self.camera.pitch = 0.3
        self.camera.zoom = 1.0
        self.camera.target_yaw = 0.6
        self.camera.target_pitch = 0.3
        self.camera.target_zoom = 1.0

    def toggle_audio(self) -> None:
        self.state = show_controller.toggle_audio(self.state)
        self.audio.set_enabled(self.state.toggles.audio_enabled)

    def toggle_ufo(self) -> None:
        self.state = show_controller.toggle_ufo(self.state)
        self.ufo_state = toggle_ufo_enabled(
            self.ufo_state,
            frame=pyxel.frame_count,
        )

    def update_ufo(self) -> None:
        self.ufo_state = update_ufo_state(
            self.ufo_state,
            frame=pyxel.frame_count,
            profile=self.profile,
            seed=RUNTIME_RANDOM_SEED,
        )

    def launch(self) -> None:
        schedule = build_single_launch_schedule(
            profile=self.profile,
            start_frame=pyxel.frame_count,
            seed=self.state.seed_base,
            selected_firework_kind=self.state.selected_firework_kind,
            random_firework_mode=self.state.toggles.random_firework_mode,
            random_seed=self.state.seed_base,
            previous_firework_kind=self.last_launched_kind,
        )
        self.schedule_runtime_launches(schedule)
        self.state = show_controller.advance_seed_base(self.state, len(schedule.slots))

    def start_fixed_salvo_loop(self, count: int) -> None:
        self.state = show_controller.set_fixed_salvo_mode(self.state, count)
        self.schedule_salvo(count)
        self.next_persistent_salvo_frame = pyxel.frame_count + PERSISTENT_SALVO_REPEAT_FRAMES

    def start_random_salvo_loop(self) -> None:
        self.state = show_controller.set_random_salvo_mode(self.state)
        self.schedule_random_count_salvo()
        self.next_persistent_salvo_frame = pyxel.frame_count + PERSISTENT_SALVO_REPEAT_FRAMES

    def schedule_salvo(self, count: int) -> None:
        schedule = build_fixed_salvo_schedule(
            count=count,
            profile=self.profile,
            start_frame=pyxel.frame_count,
            base_seed=self.state.seed_base,
            selected_firework_kind=self.state.selected_firework_kind,
            random_firework_mode=self.state.toggles.random_firework_mode,
            random_seed=self.state.seed_base,
            previous_firework_kind=self.last_launched_kind,
            height_variation=self.state.toggles.height_variation,
            height_seed=self.state.seed_base,
        )
        self.schedule_runtime_launches(schedule)
        self.state = show_controller.advance_seed_base(self.state, len(schedule.slots))

    def schedule_random_count_salvo(self) -> None:
        schedule = build_random_count_salvo_schedule(
            profile=self.profile,
            start_frame=pyxel.frame_count,
            base_seed=self.state.seed_base,
            selected_firework_kind=self.state.selected_firework_kind,
            count_seed=self.state.seed_base,
            random_firework_mode=self.state.toggles.random_firework_mode,
            random_seed=self.state.seed_base,
            previous_firework_kind=self.last_launched_kind,
            height_variation=self.state.toggles.height_variation,
            height_seed=self.state.seed_base,
        )
        self.schedule_runtime_launches(schedule)
        self.state = show_controller.advance_seed_base(self.state, len(schedule.slots))

    def schedule_persistent_salvo_if_needed(self) -> None:
        if (
            self.state.salvo_count_mode is not SalvoCountMode.OFF
            and pyxel.frame_count >= self.next_persistent_salvo_frame
        ):
            if self.state.salvo_count_mode is SalvoCountMode.RANDOM:
                self.schedule_random_count_salvo()
            else:
                self.schedule_salvo(self.state.salvo_count)
            self.next_persistent_salvo_frame = (
                pyxel.frame_count + PERSISTENT_SALVO_REPEAT_FRAMES
            )

    def schedule_runtime_launches(self, schedule: RuntimeLaunchSchedule) -> None:
        for slot in schedule.slots:
            self.schedule_runtime_slot(schedule=schedule, slot=slot)

    def schedule_runtime_slot(
        self,
        *,
        schedule: RuntimeLaunchSchedule,
        slot: RuntimeLaunchSlot,
    ) -> None:
        self.shells.append(
            create_active_shell(
                launch_frame=schedule.start_frame + slot.frame_offset,
                firework_kind=slot.firework_kind,
                launch_position=slot.launch_origin,
                burst_position=slot.burst_origin,
                seed=slot.seed,
                box_height=self.profile.box_height,
                rng=self.preview_rng,
            )
        )

    def update_shells(self) -> None:
        if not self.shells:
            return
        active: list[ActiveShell] = []
        for shell in self.shells:
            if not shell.has_started(pyxel.frame_count):
                active.append(shell)
                continue
            if shell.is_complete(pyxel.frame_count):
                self.launch_burst(
                    firework_kind=shell.firework_kind,
                    origin=shell.burst_position,
                    seed=shell.seed,
                )
                continue
            shell.history.append(shell.current_position(pyxel.frame_count))
            active.append(shell)
        self.shells = active

    def launch_burst(
        self,
        *,
        firework_kind: FireworkKind,
        origin: Vec3,
        seed: int,
    ) -> None:
        self.last_launched_kind = firework_kind
        self.audio.play_explosion(pyxel.frame_count)
        self.particles.extend(
            build_active_particles_for_burst(
                firework_kind=firework_kind,
                origin=origin,
                seed=seed,
                orientation_bank=self.ring_orientation_bank,
            )
        )
        self.glitter.extend(
            build_glitter_residue(
                firework_kind=firework_kind,
                origin=origin,
                seed=seed,
            )
        )
        self.mini_bursts.extend(
            build_delayed_mini_burst_garnish(
                firework_kind=firework_kind,
                origin=origin,
                burst_frame=pyxel.frame_count,
                seed=seed,
            )
        )
        if len(self.particles) > self.profile.max_particles:
            self.particles = self.particles[-self.profile.max_particles :]

    def launch_due_mini_bursts(self) -> None:
        pending: list[DelayedMiniBurst] = []
        new_particles: list[ActiveParticle] = []
        for mini_burst in self.mini_bursts:
            if pyxel.frame_count >= mini_burst.trigger_frame:
                new_particles.extend(build_delayed_mini_burst_particles(mini_burst))
            else:
                pending.append(mini_burst)
        self.mini_bursts = pending
        self.particles.extend(new_particles)

    def launch_secondary_bursts(self) -> None:
        new_particles: list[ActiveParticle] = []
        for particle in self.particles:
            if (
                particle.secondary_burst is not None
                and not particle.secondary_triggered
                and particle.age >= particle.secondary_burst.delay_frames
            ):
                particle.secondary_triggered = True
                new_particles.extend(build_secondary_particles(particle))
        self.particles.extend(new_particles)

    def salvo_label(self) -> str:
        if self.state.salvo_count_mode is SalvoCountMode.OFF:
            return "off"
        if self.state.salvo_count_mode is SalvoCountMode.RANDOM:
            return "random"
        return str(self.state.salvo_count)


def normalize_runtime_argv(argv: Sequence[str]) -> list[str]:
    normalized = list(argv)
    if (
        len(normalized) >= 2
        and normalized[0] == "run"
        and normalized[1].endswith(".py")
    ):
        return normalized[2:]
    return normalized


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the official Firework Observer runtime.")
    parser.add_argument(
        "--profile",
        default=DEFAULT_RUNTIME_PROFILE_NAME,
        choices=("classic", "iphone16_balanced", "iphone16_large"),
        help="Screen profile to run.",
    )
    return parser.parse_args(normalize_runtime_argv(sys.argv[1:] if argv is None else argv))


def main() -> None:
    args = parse_args()
    RuntimeApp(profile_name=args.profile).run()


if __name__ == "__main__":
    main()
