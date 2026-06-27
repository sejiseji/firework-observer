from __future__ import annotations

import pytest

from pyxel_goal_game.runtime.app import (
    DEFAULT_RUNTIME_PROFILE_NAME,
    normalize_runtime_argv,
    parse_args,
)


@pytest.mark.parametrize(
    ("argv", "expected"),
    [
        ([], []),
        (["run", "main.py"], []),
        (["run", "./main.py"], []),
        (["run", "fireworksbox/main.py"], []),
        (
            ["run", "main.py", "--profile", "iphone16_balanced"],
            ["--profile", "iphone16_balanced"],
        ),
        (["--profile", "iphone16_balanced"], ["--profile", "iphone16_balanced"]),
    ],
)
def test_normalize_runtime_argv(argv: list[str], expected: list[str]) -> None:
    assert normalize_runtime_argv(argv) == expected


def test_parse_args_default_profile_is_public_friendly() -> None:
    args = parse_args([])

    assert args.profile == DEFAULT_RUNTIME_PROFILE_NAME
    assert args.profile == "iphone16_balanced"


def test_parse_args_accepts_profile_after_pyxel_run_wrapper() -> None:
    args = parse_args(["run", "main.py", "--profile", "iphone16_balanced"])

    assert args.profile == "iphone16_balanced"


def test_parse_args_still_rejects_invalid_args() -> None:
    with pytest.raises(SystemExit):
        parse_args(["run", "main.py", "--bad"])
