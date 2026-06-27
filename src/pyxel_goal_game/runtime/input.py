from __future__ import annotations

import pyxel

from pyxel_goal_game.runtime import show_controller
from pyxel_goal_game.runtime.mobile_ui import (
    MOBILE_TOGGLE_SPECS,
    audio_toggle_rect,
    bgm_toggle_rect,
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

MAX_PITCH = 1.2
MIN_PITCH = -1.2
MAX_ZOOM = 2.2
MIN_ZOOM = 0.45
MOUSE_WHEEL_ZOOM_STEP = 0.12


def handle_runtime_input(app: object) -> None:
    handle_mobile_input(app)

    if pyxel.btn(pyxel.KEY_LEFT):
        app.camera.target_yaw -= 0.035
    if pyxel.btn(pyxel.KEY_RIGHT):
        app.camera.target_yaw += 0.035
    if pyxel.btn(pyxel.KEY_UP):
        app.camera.target_pitch = min(MAX_PITCH, app.camera.target_pitch + 0.025)
    if pyxel.btn(pyxel.KEY_DOWN):
        app.camera.target_pitch = max(MIN_PITCH, app.camera.target_pitch - 0.025)
    if pyxel.btn(pyxel.KEY_A):
        app.camera.target_zoom = min(MAX_ZOOM, app.camera.target_zoom + 0.025)
    if pyxel.btn(pyxel.KEY_S):
        app.camera.target_zoom = max(MIN_ZOOM, app.camera.target_zoom - 0.025)
    mouse_wheel_y = pyxel.btnv(pyxel.MOUSE_WHEEL_Y)
    if mouse_wheel_y:
        app.camera.target_zoom = max(
            MIN_ZOOM,
            min(
                MAX_ZOOM,
                app.camera.target_zoom + mouse_wheel_y * MOUSE_WHEEL_ZOOM_STEP,
            ),
        )

    if pyxel.btnp(pyxel.KEY_Z):
        app.launch()
    if pyxel.btnp(pyxel.KEY_0):
        app.start_random_salvo_loop()
    if pyxel.btnp(pyxel.KEY_1):
        app.start_fixed_salvo_loop(1)
    if pyxel.btnp(pyxel.KEY_2):
        app.start_fixed_salvo_loop(2)
    if pyxel.btnp(pyxel.KEY_3):
        app.start_fixed_salvo_loop(3)
    if pyxel.btnp(pyxel.KEY_4):
        app.start_fixed_salvo_loop(4)
    if pyxel.btnp(pyxel.KEY_5):
        app.start_fixed_salvo_loop(5)
    if pyxel.btnp(pyxel.KEY_SPACE):
        app.handle_space_cycle()
    if pyxel.btnp(pyxel.KEY_R):
        app.enable_random_mode()
    if pyxel.btnp(pyxel.KEY_C):
        app.reset_camera()
    if pyxel.btnp(pyxel.KEY_X):
        app.state = show_controller.toggle_auto_rotate(app.state)
    if pyxel.btnp(pyxel.KEY_Q):
        app.state = show_controller.cycle_auto_rotate_speed(app.state)
    if pyxel.btnp(pyxel.KEY_V):
        app.state = show_controller.toggle_auto_launch(app.state)
    if pyxel.btnp(pyxel.KEY_D):
        app.debug = not app.debug
    if pyxel.btnp(pyxel.KEY_H):
        app.state = show_controller.toggle_height_variation(app.state)
    if pyxel.btnp(pyxel.KEY_G):
        app.cycle_scenery()
    if pyxel.btnp(pyxel.KEY_B):
        app.state = show_controller.toggle_scenery_visible(app.state)
    if pyxel.btnp(pyxel.KEY_T):
        app.state = show_controller.toggle_stars(app.state)
    if pyxel.btnp(pyxel.KEY_M):
        app.toggle_audio()
    if pyxel.btnp(pyxel.KEY_U):
        app.toggle_ufo()


def handle_mobile_input(app: object) -> None:
    button = getattr(pyxel, "MOUSE_BUTTON_LEFT", 0)
    mouse_x = int(pyxel.mouse_x)
    mouse_y = int(pyxel.mouse_y)

    if pyxel.btnp(button):
        app.notify_audio_user_gesture()
        if menu_button_rect(app.profile.width).contains(mouse_x, mouse_y):
            app.mobile_panel_open = not app.mobile_panel_open
            if app.mobile_panel_open:
                app.refresh_mobile_panel_draft()
            app.mobile_pointer_down = False
            return
        if app.mobile_panel_open:
            if handle_mobile_panel_click(app, mouse_x, mouse_y):
                app.mobile_pointer_down = False
                return
        app.mobile_pointer_down = True
        app.mobile_dragging = False
        app.mobile_drag_start_x = mouse_x
        app.mobile_drag_start_y = mouse_y
        app.mobile_drag_last_x = mouse_x
        app.mobile_drag_last_y = mouse_y

    if pyxel.btn(button) and app.mobile_pointer_down:
        dx = mouse_x - app.mobile_drag_last_x
        dy = mouse_y - app.mobile_drag_last_y
        total_dx = mouse_x - app.mobile_drag_start_x
        total_dy = mouse_y - app.mobile_drag_start_y
        if app.mobile_dragging or abs(total_dx) + abs(total_dy) >= 3:
            app.mobile_dragging = True
            app.camera.target_yaw += dx * 0.010
            app.camera.target_pitch = max(
                MIN_PITCH,
                min(MAX_PITCH, app.camera.target_pitch - dy * 0.008),
            )
        app.mobile_drag_last_x = mouse_x
        app.mobile_drag_last_y = mouse_y

    if not pyxel.btn(button):
        app.mobile_pointer_down = False
        app.mobile_dragging = False


def handle_mobile_panel_click(app: object, mouse_x: int, mouse_y: int) -> bool:
    panel = panel_rect(app.profile.width, app.profile.height)
    if not panel.contains(mouse_x, mouse_y):
        return False

    if salvo_count_button_rect(panel).contains(mouse_x, mouse_y):
        app.cycle_mobile_salvo_count_choice()
        return True

    for index, spec in enumerate(MOBILE_TOGGLE_SPECS):
        if checkbox_row_rect(panel, index).contains(mouse_x, mouse_y):
            if spec.key == "audio_enabled":
                if bgm_toggle_rect(panel).contains(mouse_x, mouse_y):
                    app.apply_mobile_toggle("bgm_enabled")
                elif audio_toggle_rect(panel).contains(mouse_x, mouse_y):
                    app.apply_mobile_toggle("audio_enabled")
                return True
            app.apply_mobile_toggle(spec.key)
            return True

    if speed_button_rect(panel).contains(mouse_x, mouse_y):
        app.cycle_mobile_auto_rotate_speed()
        return True
    if launch_button_rect(panel).contains(mouse_x, mouse_y):
        app.launch()
        return True
    if next_button_rect(panel).contains(mouse_x, mouse_y):
        app.handle_space_cycle()
        app.refresh_mobile_panel_draft()
        return True
    if random_salvo_button_rect(panel).contains(mouse_x, mouse_y):
        app.start_mobile_salvo_loop()
        app.refresh_mobile_panel_draft()
        return True
    if zoom_in_button_rect(panel).contains(mouse_x, mouse_y):
        app.camera.target_zoom = min(MAX_ZOOM, app.camera.target_zoom + 0.15)
        return True
    if zoom_out_button_rect(panel).contains(mouse_x, mouse_y):
        app.camera.target_zoom = max(MIN_ZOOM, app.camera.target_zoom - 0.15)
        return True
    if close_button_rect(panel).contains(mouse_x, mouse_y):
        app.mobile_panel_open = False
        return True

    return True
