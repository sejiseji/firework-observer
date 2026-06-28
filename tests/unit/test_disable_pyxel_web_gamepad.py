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
PYXEL_SCRIPT_TAG = module.PYXEL_SCRIPT_TAG
SAFARI_AUDIO_UNLOCK_MARKER = module.SAFARI_AUDIO_UNLOCK_MARKER
disable_pyxel_web_gamepad = module.disable_pyxel_web_gamepad
install_safari_audio_unlock = module.install_safari_audio_unlock
patch_pyxel_web_html = module.patch_pyxel_web_html


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


def test_install_safari_audio_unlock_injects_after_pyxel_script() -> None:
    html = f"<!doctype html>\n{PYXEL_SCRIPT_TAG}\n<script>launchPyxel({{}})</script>"

    patched = install_safari_audio_unlock(html)

    assert SAFARI_AUDIO_UNLOCK_MARKER in patched
    assert patched.index(PYXEL_SCRIPT_TAG) < patched.index(SAFARI_AUDIO_UNLOCK_MARKER)


def test_install_safari_audio_unlock_is_idempotent() -> None:
    html = f"<!doctype html>\n{PYXEL_SCRIPT_TAG}\n<script>launchPyxel({{}})</script>"
    patched = install_safari_audio_unlock(html)

    assert install_safari_audio_unlock(patched) == patched


def test_install_safari_audio_unlock_rejects_unknown_html() -> None:
    with pytest.raises(ValueError, match="Pyxel web script"):
        install_safari_audio_unlock("<!doctype html>")


def test_patch_pyxel_web_html_patches_gamepad_and_safari_audio() -> None:
    html = (
        f"<!doctype html>\n{PYXEL_SCRIPT_TAG}\n"
        f'<script>launchPyxel({{ {ENABLED_GAMEPAD}, base64: "..." }})</script>'
    )

    patched = patch_pyxel_web_html(html)

    assert ENABLED_GAMEPAD not in patched
    assert DISABLED_GAMEPAD in patched
    assert SAFARI_AUDIO_UNLOCK_MARKER in patched


def test_patch_pyxel_web_html_is_idempotent() -> None:
    html = (
        f"<!doctype html>\n{PYXEL_SCRIPT_TAG}\n"
        f'<script>launchPyxel({{ {ENABLED_GAMEPAD}, base64: "..." }})</script>'
    )
    patched = patch_pyxel_web_html(html)

    assert patch_pyxel_web_html(patched) == patched
