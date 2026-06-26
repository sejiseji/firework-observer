from __future__ import annotations

import pyxel

from pyxel_goal_game.runtime import show_controller

MAX_PITCH = 1.2
MIN_PITCH = -1.2
MAX_ZOOM = 2.2
MIN_ZOOM = 0.45


def handle_runtime_input(app: object) -> None:
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
