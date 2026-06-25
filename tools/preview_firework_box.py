from __future__ import annotations

import argparse
import math
import sys
from dataclasses import dataclass
from pathlib import Path

import pyxel

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from pyxel_goal_game.camera3d import Camera3D, ProjectedPoint, Vec3  # noqa: E402
from pyxel_goal_game.firework_bursts import (  # noqa: E402
    ParticleSpawnSpec,
    RingOrientationBank,
    build_ring_orientation_bank,
    generate_kiku_burst,
    generate_ring_burst,
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
RING_ORIENTATION_BANK_SEED = 20260623


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

    @classmethod
    def from_spawn(cls, spec: ParticleSpawnSpec) -> PreviewParticle:
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
        self.seed = 0
        self.auto_rotate = False
        self.auto_launch = False
        self.debug = True
        pyxel.init(
            self.profile.width,
            self.profile.height,
            fps=60,
            title=f"Firework Box Preview - {self.profile.name}",
        )
        pyxel.run(self.update, self.draw)

    @property
    def burst_label(self) -> str:
        return "Kiku" if self.burst_index == 0 else "Ring"

    def update(self) -> None:
        self.handle_input()
        if self.auto_rotate:
            self.camera.target_yaw += 0.01
            self.camera.target_pitch = math.sin(pyxel.frame_count * 0.015) * 0.35
        if self.auto_launch and pyxel.frame_count % AUTO_LAUNCH_FRAMES == 0:
            self.launch()
        self.camera.step_toward_target()
        for particle in self.particles:
            particle.step()
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
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.burst_index = (self.burst_index + 1) % 2
        if pyxel.btnp(pyxel.KEY_C):
            self.reset_camera()
        if pyxel.btnp(pyxel.KEY_X):
            self.auto_rotate = not self.auto_rotate
        if pyxel.btnp(pyxel.KEY_V):
            self.auto_launch = not self.auto_launch
        if pyxel.btnp(pyxel.KEY_D):
            self.debug = not self.debug

    def reset_camera(self) -> None:
        self.camera.yaw = 0.6
        self.camera.pitch = 0.3
        self.camera.zoom = 1.0
        self.camera.target_yaw = 0.6
        self.camera.target_pitch = 0.3
        self.camera.target_zoom = 1.0

    def launch(self) -> None:
        origin = Vec3(0.0, 0.0, 0.0)
        if self.burst_index == 0:
            specs = generate_kiku_burst(origin=origin, seed=self.seed)
        else:
            specs = generate_ring_burst(
                origin=origin,
                seed=self.seed,
                orientation_bank=self.ring_orientation_bank,
            )
        self.seed += 1
        self.particles.extend(PreviewParticle.from_spawn(spec) for spec in specs)
        if len(self.particles) > self.profile.max_particles:
            self.particles = self.particles[-self.profile.max_particles :]

    def draw(self) -> None:
        pyxel.cls(0)
        projected_edges = sorted(
            self.box.project_edges(self.camera),
            key=lambda edge: edge.average_depth,
            reverse=True,
        )
        self.draw_edges(projected_edges[:8], far=True)
        self.draw_particles()
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

    def draw_particle(
        self,
        *,
        particle: PreviewParticle,
        projected: ProjectedPoint,
    ) -> None:
        color = particle.draw_color()
        if particle.should_draw_trail():
            previous = self.camera.project(particle.previous_position)
            pyxel.line(previous.sx, previous.sy, projected.sx, projected.sy, color)
            if particle.trail_strength >= 2:
                pyxel.pset(projected.sx, projected.sy, particle.tip_color)
            return
        pyxel.pset(projected.sx, projected.sy, color)

    def draw_hud(self) -> None:
        pyxel.text(4, 4, f"Z:launch SPACE:{self.burst_label}", 5)
        pyxel.text(4, 12, "ARROWS:rotate A/S:zoom X:auto V:burst", 5)
        if not self.debug:
            return
        pyxel.text(4, self.profile.height - 30, f"profile {self.profile.name}", 5)
        pyxel.text(4, self.profile.height - 22, f"particles {len(self.particles)}", 5)
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
