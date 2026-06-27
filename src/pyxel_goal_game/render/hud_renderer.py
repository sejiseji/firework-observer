from __future__ import annotations

import pyxel

from pyxel_goal_game.model.world import World


def draw_hud(world: World) -> None:
    pyxel.text(4, 4, f"particles: {len(world.particles)}", 7)
    pyxel.text(4, world.height - 8, "arrows move / space burst / q quit", 5)
