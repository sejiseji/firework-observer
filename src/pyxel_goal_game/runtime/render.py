from __future__ import annotations

from typing import Any

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
from pyxel_goal_game.runtime.mobile_ui import (
    MOBILE_TOGGLE_SPECS,
    Rect,
    bgm_checkbox_rect,
    checkbox_rect,
    checkbox_row_rect,
    close_button_rect,
    launch_button_rect,
    menu_button_rect,
    next_button_rect,
    panel_rect,
    random_salvo_button_rect,
    salvo_count_button_rect,
    speed_button_rect,
    zoom_in_button_rect,
    zoom_out_button_rect,
)
from pyxel_goal_game.scenery_presets import SceneryLine, SceneryPolyline
from pyxel_goal_game.wire_box import ProjectedEdge

PYXEL_FONT_HEIGHT = 7


def scaled_blt_top_left_position(
    x: int,
    y: int,
    width: int,
    height: int,
    scale: int,
) -> tuple[int, int]:
    if scale < 1:
        msg = "scale must be at least 1"
        raise ValueError(msg)
    return (
        x + (width * (scale - 1) + 1) // 2,
        y + (height * (scale - 1) + 1) // 2,
    )


class RuntimeRenderer:
    def __init__(self, app: object) -> None:
        self.app = app
        self._scaled_text_image: Any | None = None

    def draw(self) -> None:
        pyxel.cls(0)
        projected_edges = sorted(
            self.app.box.project_edges(self.app.camera),
            key=lambda edge: edge.average_depth,
            reverse=True,
        )
        self.draw_edges(projected_edges[:8], far=True)
        self.draw_box_stars()
        self.draw_ufo()
        self.draw_scenery_phase("back")
        self.draw_firework_shells()
        self.draw_particles()
        self.draw_glitter()
        self.draw_scenery_phase("front")
        self.draw_edges(projected_edges[8:], far=False)
        self.draw_hud()
        self.draw_mobile_ui()

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

    def draw_ufo(self) -> None:
        flyby = self.app.ufo_state.active
        if flyby is None or not flyby.is_active(pyxel.frame_count):
            return
        wireframe = flyby.wireframe_at(pyxel.frame_count)
        for edge in wireframe.edges:
            start = self.camera.project(edge.start)
            end = self.camera.project(edge.end)
            pyxel.line(start.sx, start.sy, end.sx, end.sy, 5)
        for light in wireframe.lights:
            projected = self.camera.project(light)
            pyxel.pset(projected.sx, projected.sy, 7)

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
            if particle.trail_history_frames > 0:
                self.draw_long_particle_trail(particle)
            previous = self.camera.project(particle.previous_position)
            pyxel.line(previous.sx, previous.sy, projected.sx, projected.sy, color)
            if particle.trail_strength >= 2:
                pyxel.pset(projected.sx, projected.sy, particle.tip_color)
            return
        pyxel.pset(projected.sx, projected.sy, color)

    def draw_long_particle_trail(self, particle: ActiveParticle) -> None:
        samples = particle.trail_history
        if len(samples) < 2:
            return
        segment_count = len(samples) - 1
        for index in range(segment_count):
            if not particle.should_draw_long_trail_segment(index, segment_count):
                continue
            start = self.camera.project(samples[index])
            end = self.camera.project(samples[index + 1])
            pyxel.line(
                start.sx,
                start.sy,
                end.sx,
                end.sy,
                particle.long_trail_segment_color(index, segment_count),
            )

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
                f"T:stars {state.toggles.interior_stars_visible}"
            ),
            5,
        )
        pyxel.text(
            4,
            28,
            f"M:audio U:ufo {state.toggles.ufo_enabled} Q:rot",
            5,
        )
        if not self.app.debug:
            return
        pyxel.text(
            4,
            self.app.profile.height - 46,
            f"audio {state.toggles.audio_enabled} bgm {state.toggles.bgm_enabled}",
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

    def draw_mobile_ui(self) -> None:
        menu = menu_button_rect(self.app.profile.width)
        menu_color = 13 if self.app.mobile_panel_open else 5
        pyxel.rect(menu.x, menu.y, menu.width, menu.height, 0)
        pyxel.rectb(menu.x, menu.y, menu.width, menu.height, menu_color)
        self.draw_scaled_text(menu.x + 6, menu.y + 5, "MENU", menu_color)
        if self.app.mobile_panel_open:
            self.draw_mobile_panel()

    def draw_mobile_panel(self) -> None:
        panel = panel_rect(self.app.profile.width, self.app.profile.height)
        draft = self.app.mobile_panel_draft
        pyxel.rect(panel.x, panel.y, panel.width, panel.height, 0)
        pyxel.rectb(panel.x, panel.y, panel.width, panel.height, 13)
        self.draw_scaled_text(panel.x + 10, panel.y + 12, "MOBILE", 7)
        pyxel.text(panel.x + 10, panel.y + 30, "tap toggles for instant change", 5)

        self.draw_mobile_button(
            salvo_count_button_rect(panel),
            f"COUNT {self.app.mobile_salvo_count_label()}",
            10,
        )

        for index, spec in enumerate(MOBILE_TOGGLE_SPECS):
            row = checkbox_row_rect(panel, index)
            box = checkbox_rect(panel, index)
            value = bool(getattr(draft, spec.key))
            pyxel.rectb(box.x, box.y, box.width, box.height, 5)
            if value:
                pyxel.line(box.x + 2, box.y + 6, box.x + 5, box.y + 10, 7)
                pyxel.line(box.x + 5, box.y + 10, box.x + 10, box.y + 2, 7)
            self.draw_scaled_text(row.x + 24, row.y + 5, spec.label.upper(), 5)
            if spec.key == "audio_enabled":
                bgm_box = bgm_checkbox_rect(panel)
                pyxel.rectb(bgm_box.x, bgm_box.y, bgm_box.width, bgm_box.height, 5)
                if draft.bgm_enabled:
                    pyxel.line(
                        bgm_box.x + 2,
                        bgm_box.y + 6,
                        bgm_box.x + 5,
                        bgm_box.y + 10,
                        7,
                    )
                    pyxel.line(
                        bgm_box.x + 5,
                        bgm_box.y + 10,
                        bgm_box.x + 10,
                        bgm_box.y + 2,
                        7,
                    )
                self.draw_scaled_text(bgm_box.x + 18, row.y + 5, "BGM", 5)

        speed = speed_button_rect(panel)
        pyxel.rectb(speed.x, speed.y, speed.width, speed.height, 5)
        self.draw_scaled_text(
            speed.x + 5,
            speed.y + 7,
            f"SPEED {draft.auto_rotate_speed_mode.value.upper()}",
            5,
        )

        self.draw_mobile_button(launch_button_rect(panel), "LAUNCH", 11)
        self.draw_mobile_button(next_button_rect(panel), "NEXT", 11)
        self.draw_mobile_button(random_salvo_button_rect(panel), "SALVO START", 11)
        self.draw_mobile_button(zoom_in_button_rect(panel), "ZOOM+", 5)
        self.draw_mobile_button(zoom_out_button_rect(panel), "ZOOM-", 5)
        self.draw_mobile_button(close_button_rect(panel), "CLOSE", 8)

    def draw_mobile_button(self, rect: Rect, label: str, color: int) -> None:
        pyxel.rectb(rect.x, rect.y, rect.width, rect.height, color)
        self.draw_scaled_text(rect.x + 6, rect.y + 7, label, color)

    def draw_scaled_text(
        self,
        x: int,
        y: int,
        text: str,
        color: int,
        *,
        scale: int = 2,
    ) -> None:
        if self._scaled_text_image is None:
            self._scaled_text_image = pyxel.Image(128, 8)
        image = self._scaled_text_image
        image.cls(0)
        image.text(0, 0, text, color)
        width = min(image.width, max(1, len(text) * 4 + 2))
        blt_x, blt_y = scaled_blt_top_left_position(
            x,
            y,
            width,
            PYXEL_FONT_HEIGHT,
            scale,
        )
        pyxel.blt(blt_x, blt_y, image, 0, 0, width, PYXEL_FONT_HEIGHT, 0, scale=scale)
