from __future__ import annotations

import pyxel

from pyxel_goal_game.ambient_box_stars import is_interior_face_visible, star_twinkle_color
from pyxel_goal_game.camera3d import Camera3D, ProjectedPoint
from pyxel_goal_game.runtime.effects import (
    FIREWORK_SHELL_TAIL_COLORS_NEW_TO_OLD,
    FIREWORK_SHELL_TAIL_LENGTH,
    ActiveParticle,
    ActiveShell,
    GlitterResidue,
)
from pyxel_goal_game.scenery_presets import SceneryLine, SceneryPolyline
from pyxel_goal_game.wire_box import ProjectedEdge


class RuntimeRenderer:
    def __init__(self, app: object) -> None:
        self.app = app

    def draw(self) -> None:
        pyxel.cls(0)
        projected_edges = sorted(
            self.app.box.project_edges(self.app.camera),
            key=lambda edge: edge.average_depth,
            reverse=True,
        )
        self.draw_edges(projected_edges[:8], far=True)
        self.draw_box_stars()
        self.draw_scenery_phase("back")
        self.draw_firework_shells()
        self.draw_particles()
        self.draw_glitter()
        self.draw_scenery_phase("front")
        self.draw_edges(projected_edges[8:], far=False)
        self.draw_hud()

    @property
    def camera(self) -> Camera3D:
        return self.app.camera

    def draw_edges(self, edges: list[ProjectedEdge], *, far: bool) -> None:
        for edge in edges:
            color = self.edge_color(edge=edge, far=far)
            pyxel.line(edge.start.sx, edge.start.sy, edge.end.sx, edge.end.sy, color)

    def draw_box_stars(self) -> None:
        if not self.app.state.toggles.interior_stars_visible:
            return
        visible_faces = {
            face
            for face in {star.face for star in self.app.star_field.stars}
            if is_interior_face_visible(self.camera, face)
        }
        for star in self.app.star_field.stars:
            if star.face not in visible_faces:
                continue
            color = star_twinkle_color(star, pyxel.frame_count)
            if color is None:
                continue
            projected = self.camera.project(star.position)
            pyxel.pset(projected.sx, projected.sy, color)

    def edge_color(self, *, edge: ProjectedEdge, far: bool) -> int:
        if far:
            return 1 if edge.group == "connector" else 5
        return 13 if edge.group != "connector" else 5

    def draw_scenery_phase(self, phase: str) -> None:
        if not self.app.state.toggles.scenery_visible:
            return
        for polyline in self.app.scenery.polylines:
            if polyline.phase == phase:
                self.draw_scenery_polyline(polyline)
        for line in self.app.scenery.lines:
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
        for shell in self.app.shells:
            if not shell.has_started(pyxel.frame_count):
                continue
            self.draw_firework_shell_tail(
                shell=shell,
                current=self.camera.project(shell.current_position(pyxel.frame_count)),
            )

    def draw_firework_shell_tail(
        self,
        *,
        shell: ActiveShell,
        current: ProjectedPoint,
    ) -> None:
        samples = [current]
        for position in reversed(tuple(shell.history)[:-1]):
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

    def draw_particles(self) -> None:
        draw_items = [
            (self.camera.project(particle.position), particle)
            for particle in self.app.particles
        ]
        draw_items.sort(key=lambda item: item[0].depth, reverse=True)
        for projected, particle in draw_items:
            self.draw_particle(particle=particle, projected=projected)

    def draw_particle(
        self,
        *,
        particle: ActiveParticle,
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
        if particle.should_draw_trail(pyxel.frame_count):
            previous = self.camera.project(particle.previous_position)
            pyxel.line(previous.sx, previous.sy, projected.sx, projected.sy, color)
            if particle.trail_strength >= 2:
                pyxel.pset(projected.sx, projected.sy, particle.tip_color)
            return
        pyxel.pset(projected.sx, projected.sy, color)

    def accent_ray_color(self, particle: ActiveParticle) -> int:
        if particle.age < particle.accent_until_age // 2:
            return particle.accent_color
        return particle.fade_mid

    def draw_glitter(self) -> None:
        draw_items: list[tuple[ProjectedPoint, GlitterResidue]] = [
            (self.camera.project(glitter.position), glitter)
            for glitter in self.app.glitter
        ]
        draw_items.sort(key=lambda item: item[0].depth, reverse=True)
        for projected, glitter in draw_items:
            color = glitter.draw_color()
            if color is not None:
                pyxel.pset(projected.sx, projected.sy, color)

    def draw_hud(self) -> None:
        state = self.app.state
        label = (
            self.app.last_launched_label
            if state.toggles.random_firework_mode
            else self.app.burst_label
        )
        pyxel.text(4, 4, f"Z:launch {self.app.mode_label}:{label}", 5)
        pyxel.text(4, 12, "1-5:salvo 0:rand-count H:height", 5)
        pyxel.text(
            4,
            20,
            (
                f"G:scene {self.app.scenery.label} B:{state.toggles.scenery_visible} "
                f"T:stars {state.toggles.interior_stars_visible} M:audio Q:rot"
            ),
            5,
        )
        if not self.app.debug:
            return
        pyxel.text(
            4,
            self.app.profile.height - 46,
            f"audio {state.toggles.audio_enabled}",
            5,
        )
        pyxel.text(4, self.app.profile.height - 30, f"profile {self.app.profile.name}", 5)
        pyxel.text(4, self.app.profile.height - 22, f"particles {len(self.app.particles)}", 5)
        pyxel.text(
            4,
            self.app.profile.height - 38,
            (
                f"salvo {self.app.salvo_label()} "
                f"height {state.toggles.height_variation}"
            ),
            5,
        )
        pyxel.text(
            4,
            self.app.profile.height - 14,
            f"yaw {self.camera.yaw:.2f} pitch {self.camera.pitch:.2f}",
            5,
        )
        pyxel.text(
            4,
            self.app.profile.height - 6,
            (
                f"zoom {self.camera.zoom:.2f} auto {state.toggles.auto_rotate}/"
                f"{state.toggles.auto_launch} rot {state.auto_rotate_speed_mode.value}"
            ),
            5,
        )
