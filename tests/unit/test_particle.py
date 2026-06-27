from __future__ import annotations

from pyxel_goal_game.model.particle import Particle


def test_particle_alive_depends_on_life() -> None:
    assert Particle(x=0, y=0, vx=0, vy=0, life=1).alive
    assert not Particle(x=0, y=0, vx=0, vy=0, life=0).alive
