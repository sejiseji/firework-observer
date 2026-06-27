from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

SCRIPT_PATH = (
    Path(__file__).resolve().parents[2] / "scripts" / "disable_pyxel_web_gamepad.py"
)
SPEC = importlib.util.spec_from_file_location("disable_pyxel_web_gamepad", SCRIPT_PATH)
assert SPEC is not None
module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(module)

DISABLED_GAMEPAD = module.DISABLED_GAMEPAD
ENABLED_GAMEPAD = module.ENABLED_GAMEPAD
disable_pyxel_web_gamepad = module.disable_pyxel_web_gamepad


def test_disable_pyxel_web_gamepad_replaces_enabled_setting() -> None:
    html = f'launchPyxel({{ command: "play", {ENABLED_GAMEPAD}, base64: "..." }})'

    patched = disable_pyxel_web_gamepad(html)

    assert ENABLED_GAMEPAD not in patched
    assert DISABLED_GAMEPAD in patched


def test_disable_pyxel_web_gamepad_is_idempotent() -> None:
    html = f'launchPyxel({{ command: "play", {DISABLED_GAMEPAD}, base64: "..." }})'

    assert disable_pyxel_web_gamepad(html) == html


def test_disable_pyxel_web_gamepad_rejects_unknown_html() -> None:
    with pytest.raises(ValueError, match="gamepad setting"):
        disable_pyxel_web_gamepad("<!doctype html>")
