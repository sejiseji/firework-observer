from __future__ import annotations

from pyxel_goal_game.tools.deterministic_replay import make_sample_replay


def test_particle_snapshot_shape() -> None:
    particles = make_sample_replay(seed=0)
    assert len(particles) > 0
    assert all(p.life == 35 for p in particles)
