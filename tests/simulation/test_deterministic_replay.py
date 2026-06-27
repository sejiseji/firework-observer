from __future__ import annotations

from pyxel_goal_game.tools.deterministic_replay import make_sample_replay


def test_sample_replay_is_deterministic() -> None:
    first = make_sample_replay(seed=123)
    second = make_sample_replay(seed=123)

    assert [(round(p.x, 4), round(p.y, 4), p.life) for p in first] == [
        (round(p.x, 4), round(p.y, 4), p.life) for p in second
    ]
