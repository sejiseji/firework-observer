from __future__ import annotations

import pyxel

from pyxel_goal_game.debug.metrics import FrameMetrics


def draw_debug_overlay(metrics: FrameMetrics) -> None:
    pyxel.text(4, 12, f"active: {metrics.active_particles}", 13)
