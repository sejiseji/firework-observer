from __future__ import annotations

import argparse
import math
import sys
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from random import Random

import pyxel

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from pyxel_goal_game.camera3d import Camera3D, ProjectedPoint, Vec3  # noqa: E402
from pyxel_goal_game.firework_bursts import (  # noqa: E402
    ParticleSpawnSpec,
    RingOrientationBank,
    SecondaryBurstSpec,
    build_ring_orientation_bank,
    generate_kiku_burst,
    generate_multi_ring_burst,
    generate_peony_burst,
    generate_ring_burst,
    generate_secondary_burst,
    generate_senrin_burst,
    generate_spiral_burst,
    generate_willow_burst,
)
from pyxel_goal_game.salvo_patterns import SalvoPlan, build_salvo_plan  # noqa: E402
from pyxel_goal_game.scenery_presets import (  # noqa: E402
    SCENERY_PRESET_NAMES,
    SceneryLine,
    SceneryPolyline,
    SceneryPreset,
    get_scenery_preset,
)
from pyxel_goal_game.screen_profiles import (  # noqa: E402
    DEFAULT_SCREEN_PROFILE_NAME,
    get_screen_profile,
)
from pyxel_goal_game.wire_box import ProjectedEdge, WireBox  # noqa: E402

PROFILE_NAME = DEFAULT_SCREEN_PROFILE_NAME
MAX_ZOOM = 2.2
MIN_ZOOM = 0.45
MAX_PITCH = 1.2
MIN_PITCH = -1.2
AUTO_LAUNCH_FRAMES = 120
PERSISTENT_SALVO_FRAMES = 210
ROCKET_MIN_FLIGHT_FRAMES = 96
ROCKET_MAX_FLIGHT_FRAMES = 180
FIREWORK_SHELL_TAIL_COLORS_NEW_TO_OLD = (7, 7, 7, 10, 10, 4, 4)
FIREWORK_SHELL_TAIL_LENGTH = len(FIREWORK_SHELL_TAIL_COLORS_NEW_TO_OLD)
RING_ORIENTATION_BANK_SEED = 20260623
PREVIEW_RANDOM_SEED = 20260625
HEIGHT_VARIATION_RATIO = 0.16
BURST_LABELS = ("Kiku", "Ring", "Spiral", "Willow", "Peony", "Multi-ring", "Senrin")
BURST_ACCENT_STYLES = (
    (10, 9, 7),
    (12, 6, 7),
    (11, 10, 7),
    (10, 9, 4),
    (14, 8, 10),
    (12, 6, 10),
    (7, 10, 14),
)
ACCENT_COUNTS = (8, 6, 8, 5, 10, 6, 4)
ACCENT_RAY_FRAMES = 12


@dataclass(frozen=True)
class PreviewRocket:
    launch_frame: int
    flight_frames: int
    burst_index: int
    launch_position: Vec3
    burst_position: Vec3
    seed: int
    history: deque[Vec3]

    def has_started(self, frame: int) -> bool:
        return frame >= self.launch_frame

    def is_complete(self, frame: int) -> bool:
        return frame >= self.launch_frame + self.flight_frames

    def current_position(self, frame: int) -> Vec3:
        elapsed = max(0, frame - self.launch_frame)
        progress = min(1.0, elapsed / self.flight_frames)
        return Vec3(
            x=self.launch_position.x
            + (self.burst_position.x - self.launch_position.x) * progress,
            y=self.launch_position.y
            + (self.burst_position.y - self.launch_position.y) * progress,
            z=self.launch_position.z
            + (self.burst_position.z - self.launch_position.z) * progress,
        )


@dataclass
class PreviewParticle:
    position: Vec3
    previous_position: Vec3
    velocity: Vec3
    life: int
    max_life: int
    color: int
    fade_mid: int
    fade_dark: int
    tip_color: int
    drag: float
    gravity: float
    has_trail: bool
    trail_until_age: int
    trail_strength: int
    trail_draw_every: int
    secondary_burst: SecondaryBurstSpec | None = None
    secondary_triggered: bool = False
    accent_origin: Vec3 | None = None
    accent_until_age: int = 0
    accent_color: int = 0

    @classmethod
    def from_spawn(
        cls,
        spec: ParticleSpawnSpec,
        *,
        accent_origin: Vec3 | None = None,
        accent_until_age: int = 0,
        accent_color: int = 0,
    ) -> PreviewParticle:
        return cls(
            position=spec.position,
            previous_position=spec.position,
            velocity=spec.velocity,
            life=spec.life,
            max_life=spec.life,
            color=spec.color,
            fade_mid=spec.fade_mid,
            fade_dark=spec.fade_dark,
            tip_color=spec.tip_color,
            drag=spec.drag,
            gravity=spec.gravity,
            has_trail=spec.has_trail,
            trail_until_age=spec.trail_until_age,
            trail_strength=spec.trail_strength,
            trail_draw_every=spec.trail_draw_every,
            secondary_burst=spec.secondary_burst,
            accent_origin=accent_origin,
            accent_until_age=accent_until_age,
            accent_color=accent_color,
        )

    @property
    def age(self) -> int:
        return self.max_life - self.life

    def step(self) -> None:
        self.previous_position = self.position
        self.position = Vec3(
            self.position.x + self.velocity.x,
            self.position.y + self.velocity.y,
            self.position.z + self.velocity.z,
        )
        self.velocity = Vec3(
            self.velocity.x * self.drag,
            self.velocity.y * self.drag + self.gravity,
            self.velocity.z * self.drag,
        )
        self.life -= 1

    def draw_color(self) -> int:
        life_ratio = self.life / self.max_life
        if life_ratio > 0.55:
            return self.color
        if life_ratio > 0.25:
            return self.fade_mid
        return self.fade_dark

    def should_draw_trail(self) -> bool:
        return (
            self.has_trail
            and self.age < self.trail_until_age
            and pyxel.frame_count % self.trail_draw_every == 0
        )

    def is_alive(self) -> bool:
        return self.life > 0


class PreviewApp:
    def __init__(self, profile_name: str) -> None:
        self.profile = get_screen_profile(profile_name)
        self.camera = Camera3D.from_profile(self.profile)
        self.box = WireBox.from_profile(self.profile)
        self.ring_orientation_bank: RingOrientationBank = build_ring_orientation_bank(
            seed=RING_ORIENTATION_BANK_SEED,
            count=24,
        )
        self.particles: list[PreviewParticle] = []
        self.burst_index = 0
        self.last_launched_index = 0
        self.random_mode = False
        self.preview_rng = Random(PREVIEW_RANDOM_SEED)
        self.rockets: list[PreviewRocket] = []
        self.persistent_salvo_enabled = False
        self.random_salvo_count = False
        self.persistent_salvo_count = 1
        self.next_persistent_salvo_frame = 0
        self.height_variation = False
        self.seed = 0
        self.auto_rotate = False
        self.auto_launch = False
        self.debug = True
        self.scenery_index = 0
        self.scenery_visible = True
        self.scenery = self.load_scenery()
        pyxel.init(
            self.profile.width,
            self.profile.height,
            fps=60,
            title=f"Firework Box Preview - {self.profile.name}",
        )
        pyxel.run(self.update, self.draw)

    @property
    def burst_label(self) -> str:
        return BURST_LABELS[self.burst_index]

    @property
    def last_launched_label(self) -> str:
        return BURST_LABELS[self.last_launched_index]

    @property
    def mode_label(self) -> str:
        return "RANDOM" if self.random_mode else "SEQ"

    def update(self) -> None:
        self.handle_input()
        if self.auto_rotate:
            self.camera.target_yaw += 0.01
            self.camera.target_pitch = math.sin(pyxel.frame_count * 0.015) * 0.35
        if self.auto_launch and pyxel.frame_count % AUTO_LAUNCH_FRAMES == 0:
            self.launch()
        self.schedule_persistent_salvo_if_needed()
        self.update_rockets()
        self.camera.step_toward_target()
        for particle in self.particles:
            particle.step()
        self.launch_secondary_bursts()
        self.particles = [
            particle for particle in self.particles if particle.is_alive()
        ][-self.profile.max_particles :]

    def handle_input(self) -> None:
        if pyxel.btn(pyxel.KEY_LEFT):
            self.camera.target_yaw -= 0.035
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.camera.target_yaw += 0.035
        if pyxel.btn(pyxel.KEY_UP):
            self.camera.target_pitch = min(MAX_PITCH, self.camera.target_pitch + 0.025)
        if pyxel.btn(pyxel.KEY_DOWN):
            self.camera.target_pitch = max(MIN_PITCH, self.camera.target_pitch - 0.025)
        if pyxel.btn(pyxel.KEY_A):
            self.camera.target_zoom = min(MAX_ZOOM, self.camera.target_zoom + 0.025)
        if pyxel.btn(pyxel.KEY_S):
            self.camera.target_zoom = max(MIN_ZOOM, self.camera.target_zoom - 0.025)
        if pyxel.btnp(pyxel.KEY_Z):
            self.launch()
        if pyxel.btnp(pyxel.KEY_0):
            self.start_random_salvo_loop()
        if pyxel.btnp(pyxel.KEY_1):
            self.start_fixed_salvo_loop(1)
        if pyxel.btnp(pyxel.KEY_2):
            self.start_fixed_salvo_loop(2)
        if pyxel.btnp(pyxel.KEY_3):
            self.start_fixed_salvo_loop(3)
        if pyxel.btnp(pyxel.KEY_4):
            self.start_fixed_salvo_loop(4)
        if pyxel.btnp(pyxel.KEY_5):
            self.start_fixed_salvo_loop(5)
        if pyxel.btnp(pyxel.KEY_SPACE):
            if self.random_mode:
                self.random_mode = False
                self.burst_index = self.last_launched_index
            else:
                self.burst_index = (self.burst_index + 1) % len(BURST_LABELS)
        if pyxel.btnp(pyxel.KEY_R):
            self.random_mode = True
        if pyxel.btnp(pyxel.KEY_C):
            self.reset_camera()
        if pyxel.btnp(pyxel.KEY_X):
            self.auto_rotate = not self.auto_rotate
        if pyxel.btnp(pyxel.KEY_V):
            self.auto_launch = not self.auto_launch
            if self.auto_launch:
                self.persistent_salvo_enabled = False
        if pyxel.btnp(pyxel.KEY_D):
            self.debug = not self.debug
        if pyxel.btnp(pyxel.KEY_H):
            self.height_variation = not self.height_variation
        if pyxel.btnp(pyxel.KEY_G):
            self.scenery_index = (self.scenery_index + 1) % len(SCENERY_PRESET_NAMES)
            self.scenery = self.load_scenery()
        if pyxel.btnp(pyxel.KEY_B):
            self.scenery_visible = not self.scenery_visible

    def load_scenery(self) -> SceneryPreset:
        return get_scenery_preset(
            SCENERY_PRESET_NAMES[self.scenery_index],
            profile=self.profile,
        )

    def reset_camera(self) -> None:
        self.camera.yaw = 0.6
        self.camera.pitch = 0.3
        self.camera.zoom = 1.0
        self.camera.target_yaw = 0.6
        self.camera.target_pitch = 0.3
        self.camera.target_zoom = 1.0

    def launch(self) -> None:
        origin = Vec3(0.0, 0.0, 0.0)
        burst_index = self.choose_launch_index()
        self.schedule_rocket(
            launch_frame=pyxel.frame_count,
            burst_index=burst_index,
            launch_position=self.default_launch_position(origin),
            burst_position=origin,
            seed=self.seed,
        )
        self.seed += 1

    def launch_burst(self, *, burst_index: int, origin: Vec3, seed: int) -> None:
        if burst_index == 0:
            specs = generate_kiku_burst(origin=origin, seed=seed)
        elif burst_index == 1:
            specs = generate_ring_burst(
                origin=origin,
                seed=seed,
                orientation_bank=self.ring_orientation_bank,
            )
        elif burst_index == 2:
            specs = generate_spiral_burst(origin=origin, seed=seed)
        elif burst_index == 3:
            specs = generate_willow_burst(origin=origin, seed=seed)
        elif burst_index == 4:
            specs = generate_peony_burst(origin=origin, seed=seed)
        elif burst_index == 5:
            specs = generate_multi_ring_burst(
                origin=origin,
                seed=seed,
                orientation_bank=self.ring_orientation_bank,
            )
        else:
            specs = generate_senrin_burst(origin=origin, seed=seed)
        self.last_launched_index = burst_index
        accent_indexes = self.choose_accent_indexes(
            burst_index=burst_index,
            seed=seed,
            particle_count=len(specs),
        )
        accent_color = BURST_ACCENT_STYLES[burst_index][2]
        self.particles.extend(
            PreviewParticle.from_spawn(
                spec,
                accent_origin=origin if index in accent_indexes else None,
                accent_until_age=ACCENT_RAY_FRAMES if index in accent_indexes else 0,
                accent_color=accent_color if index in accent_indexes else 0,
            )
            for index, spec in enumerate(specs)
        )
        if len(self.particles) > self.profile.max_particles:
            self.particles = self.particles[-self.profile.max_particles :]

    def choose_accent_indexes(
        self,
        *,
        burst_index: int,
        seed: int,
        particle_count: int,
    ) -> set[int]:
        accent_count = min(ACCENT_COUNTS[burst_index], particle_count)
        if accent_count <= 0:
            return set()
        rng = Random(seed ^ ((burst_index + 1) * 0x9E3779B1))
        stride = max(1, particle_count // accent_count)
        offset = rng.randrange(stride)
        return {
            (offset + index * particle_count // accent_count) % particle_count
            for index in range(accent_count)
        }

    def launch_secondary_bursts(self) -> None:
        new_particles: list[PreviewParticle] = []
        for particle in self.particles:
            secondary = particle.secondary_burst
            if (
                secondary is not None
                and not particle.secondary_triggered
                and particle.age >= secondary.delay_frames
            ):
                particle.secondary_triggered = True
                new_particles.extend(
                    PreviewParticle.from_spawn(spec)
                    for spec in generate_secondary_burst(
                        origin=particle.position,
                        spec=secondary,
                    )
                )
        self.particles.extend(new_particles)

    def choose_launch_index(self) -> int:
        if not self.random_mode:
            return self.burst_index
        index = self.preview_rng.randrange(len(BURST_LABELS))
        if len(BURST_LABELS) > 1 and index == self.last_launched_index:
            return (index + 1) % len(BURST_LABELS)
        return index

    def schedule_salvo(self, count: int) -> None:
        plan = build_salvo_plan(count=count, profile=self.profile)
        base_seed = self.seed
        self.seed += len(plan.slots)
        for slot, burst_index in zip(
            plan.slots,
            self.choose_salvo_burst_indexes(plan),
            strict=True,
        ):
            burst_position = self.apply_height_variation(slot.burst_position)
            self.schedule_rocket(
                launch_frame=pyxel.frame_count + slot.delay_frames,
                burst_index=burst_index,
                launch_position=slot.launch_position,
                burst_position=burst_position,
                seed=base_seed + slot.seed_offset,
            )

    def default_launch_position(self, burst_position: Vec3) -> Vec3:
        return Vec3(
            x=burst_position.x,
            y=-self.profile.box_height * 0.46,
            z=burst_position.z,
        )

    def schedule_rocket(
        self,
        *,
        launch_frame: int,
        burst_index: int,
        launch_position: Vec3,
        burst_position: Vec3,
        seed: int,
    ) -> None:
        self.rockets.append(
            PreviewRocket(
                launch_frame=launch_frame,
                flight_frames=self.choose_rocket_flight_frames(
                    launch_position=launch_position,
                    burst_position=burst_position,
                ),
                burst_index=burst_index,
                launch_position=launch_position,
                burst_position=burst_position,
                seed=seed,
                history=deque(maxlen=FIREWORK_SHELL_TAIL_LENGTH),
            )
        )

    def choose_rocket_flight_frames(
        self,
        *,
        launch_position: Vec3,
        burst_position: Vec3,
    ) -> int:
        vertical_distance = max(0.0, burst_position.y - launch_position.y)
        height_ratio = vertical_distance / self.profile.box_height
        base_frames = 92 + height_ratio * 64
        speed_factor = self.preview_rng.uniform(0.78, 1.28)
        jitter = self.preview_rng.randint(-8, 8)
        flight_frames = int(base_frames / speed_factor + jitter)
        return max(
            ROCKET_MIN_FLIGHT_FRAMES,
            min(ROCKET_MAX_FLIGHT_FRAMES, flight_frames),
        )

    def apply_height_variation(self, position: Vec3) -> Vec3:
        if not self.height_variation:
            return position
        half_height = self.profile.box_height / 2
        varied_y = position.y + self.preview_rng.uniform(
            -HEIGHT_VARIATION_RATIO,
            HEIGHT_VARIATION_RATIO,
        ) * half_height
        return Vec3(
            x=position.x,
            y=max(-half_height, min(half_height, varied_y)),
            z=position.z,
        )

    def choose_salvo_burst_indexes(self, plan: SalvoPlan) -> tuple[int, ...]:
        if not self.random_mode:
            return tuple(self.burst_index for _ in plan.slots)
        indexes: list[int] = []
        previous = self.last_launched_index
        for _ in plan.slots:
            index = self.preview_rng.randrange(len(BURST_LABELS))
            if len(BURST_LABELS) > 1 and index == previous:
                index = (index + 1) % len(BURST_LABELS)
            indexes.append(index)
            previous = index
        return tuple(indexes)

    def start_fixed_salvo_loop(self, count: int) -> None:
        self.auto_launch = False
        self.persistent_salvo_enabled = True
        self.random_salvo_count = False
        self.persistent_salvo_count = count
        self.schedule_salvo(count)
        self.next_persistent_salvo_frame = pyxel.frame_count + PERSISTENT_SALVO_FRAMES

    def start_random_salvo_loop(self) -> None:
        self.auto_launch = False
        self.persistent_salvo_enabled = True
        self.random_salvo_count = True
        self.schedule_salvo(self.choose_salvo_count())
        self.next_persistent_salvo_frame = pyxel.frame_count + PERSISTENT_SALVO_FRAMES

    def choose_salvo_count(self) -> int:
        if self.random_salvo_count:
            return self.preview_rng.randint(1, 5)
        return self.persistent_salvo_count

    def schedule_persistent_salvo_if_needed(self) -> None:
        if (
            self.persistent_salvo_enabled
            and pyxel.frame_count >= self.next_persistent_salvo_frame
        ):
            self.schedule_salvo(self.choose_salvo_count())
            self.next_persistent_salvo_frame = pyxel.frame_count + PERSISTENT_SALVO_FRAMES

    def update_rockets(self) -> None:
        if not self.rockets:
            return
        active: list[PreviewRocket] = []
        for rocket in self.rockets:
            if not rocket.has_started(pyxel.frame_count):
                active.append(rocket)
                continue
            if rocket.is_complete(pyxel.frame_count):
                self.launch_burst(
                    burst_index=rocket.burst_index,
                    origin=rocket.burst_position,
                    seed=rocket.seed,
                )
                continue
            rocket.history.append(rocket.current_position(pyxel.frame_count))
            active.append(rocket)
        self.rockets = active

    def draw(self) -> None:
        pyxel.cls(0)
        projected_edges = sorted(
            self.box.project_edges(self.camera),
            key=lambda edge: edge.average_depth,
            reverse=True,
        )
        self.draw_edges(projected_edges[:8], far=True)
        self.draw_scenery_phase("back")
        self.draw_firework_shells()
        self.draw_particles()
        self.draw_scenery_phase("front")
        self.draw_edges(projected_edges[8:], far=False)
        self.draw_hud()

    def draw_edges(self, edges: list[ProjectedEdge], *, far: bool) -> None:
        for edge in edges:
            color = self.edge_color(edge=edge, far=far)
            pyxel.line(edge.start.sx, edge.start.sy, edge.end.sx, edge.end.sy, color)

    def edge_color(self, *, edge: ProjectedEdge, far: bool) -> int:
        if far:
            return 1 if edge.group == "connector" else 5
        return 13 if edge.group != "connector" else 5

    def draw_particles(self) -> None:
        draw_items = [
            (self.camera.project(particle.position), particle)
            for particle in self.particles
        ]
        draw_items.sort(key=lambda item: item[0].depth, reverse=True)
        for projected, particle in draw_items:
            self.draw_particle(particle=particle, projected=projected)

    def draw_scenery_phase(self, phase: str) -> None:
        if not self.scenery_visible:
            return
        for polyline in self.scenery.polylines:
            if polyline.phase == phase:
                self.draw_scenery_polyline(polyline)
        for line in self.scenery.lines:
            if line.phase == phase:
                self.draw_scenery_line(line)

    def draw_scenery_polyline(self, polyline: SceneryPolyline) -> None:
        if len(polyline.points) < 2:
            return
        projected = tuple(self.camera.project(point) for point in polyline.points)
        for index in range(len(projected) - 1):
            start = projected[index]
            end = projected[index + 1]
            pyxel.line(start.sx, start.sy, end.sx, end.sy, polyline.color)

    def draw_scenery_line(self, line: SceneryLine) -> None:
        start = self.camera.project(line.start)
        end = self.camera.project(line.end)
        pyxel.line(start.sx, start.sy, end.sx, end.sy, line.color)

    def draw_firework_shells(self) -> None:
        for rocket in self.rockets:
            if not rocket.has_started(pyxel.frame_count):
                continue
            history = tuple(rocket.history)
            self.draw_firework_shell_tail(
                current=self.camera.project(rocket.current_position(pyxel.frame_count)),
                history=history,
            )

    def draw_firework_shell_tail(
        self,
        *,
        current: ProjectedPoint,
        history: tuple[Vec3, ...],
    ) -> None:
        samples = [current]
        for position in reversed(history[:-1]):
            samples.append(self.camera.project(position))
            if len(samples) >= FIREWORK_SHELL_TAIL_LENGTH:
                break

        for index in range(len(samples) - 1, 0, -1):
            start = samples[index]
            end = samples[index - 1]
            color = FIREWORK_SHELL_TAIL_COLORS_NEW_TO_OLD[index]
            pyxel.line(start.sx, start.sy, end.sx, end.sy, color)
        pyxel.pset(
            current.sx,
            current.sy,
            FIREWORK_SHELL_TAIL_COLORS_NEW_TO_OLD[0],
        )

    def draw_particle(
        self,
        *,
        particle: PreviewParticle,
        projected: ProjectedPoint,
    ) -> None:
        color = particle.draw_color()
        if particle.accent_origin is not None and particle.age < particle.accent_until_age:
            origin = self.camera.project(particle.accent_origin)
            pyxel.line(
                origin.sx,
                origin.sy,
                projected.sx,
                projected.sy,
                self.accent_ray_color(particle),
            )
        if particle.should_draw_trail():
            previous = self.camera.project(particle.previous_position)
            pyxel.line(previous.sx, previous.sy, projected.sx, projected.sy, color)
            if particle.trail_strength >= 2:
                pyxel.pset(projected.sx, projected.sy, particle.tip_color)
            return
        pyxel.pset(projected.sx, projected.sy, color)

    def accent_ray_color(self, particle: PreviewParticle) -> int:
        if particle.age < particle.accent_until_age // 2:
            return particle.accent_color
        return particle.fade_mid

    def draw_hud(self) -> None:
        label = self.last_launched_label if self.random_mode else self.burst_label
        pyxel.text(4, 4, f"Z:launch {self.mode_label}:{label}", 5)
        pyxel.text(4, 12, "1-5:salvo 0:rand-count H:height", 5)
        pyxel.text(4, 20, f"G:scene {self.scenery.label} B:{self.scenery_visible}", 5)
        if not self.debug:
            return
        pyxel.text(4, self.profile.height - 30, f"profile {self.profile.name}", 5)
        pyxel.text(4, self.profile.height - 22, f"particles {len(self.particles)}", 5)
        pyxel.text(
            4,
            self.profile.height - 38,
            f"salvo {self.salvo_label()} height {self.height_variation}",
            5,
        )
        pyxel.text(
            4,
            self.profile.height - 14,
            f"yaw {self.camera.yaw:.2f} pitch {self.camera.pitch:.2f}",
            5,
        )
        pyxel.text(
            4,
            self.profile.height - 6,
            f"zoom {self.camera.zoom:.2f} auto {self.auto_rotate}/{self.auto_launch}",
            5,
        )

    def salvo_label(self) -> str:
        if not self.persistent_salvo_enabled:
            return "off"
        if self.random_salvo_count:
            return "random"
        return str(self.persistent_salvo_count)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Manual Firework Box Pyxel preview.")
    parser.add_argument(
        "--profile",
        default=PROFILE_NAME,
        choices=("classic", "iphone16_balanced", "iphone16_large"),
        help="Screen profile to preview.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    PreviewApp(profile_name=args.profile)


if __name__ == "__main__":
    main()
