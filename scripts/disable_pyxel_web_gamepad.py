from __future__ import annotations

import argparse
from pathlib import Path

ENABLED_GAMEPAD = 'gamepad: "enabled"'
DISABLED_GAMEPAD = 'gamepad: "disabled"'


def disable_pyxel_web_gamepad(html: str) -> str:
    if DISABLED_GAMEPAD in html:
        return html
    if ENABLED_GAMEPAD not in html:
        msg = "Pyxel web gamepad setting was not found"
        raise ValueError(msg)
    return html.replace(ENABLED_GAMEPAD, DISABLED_GAMEPAD, 1)


def patch_file(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    patched = disable_pyxel_web_gamepad(html)
    path.write_text(patched, encoding="utf-8")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Disable the Pyxel Web virtual gamepad in generated HTML.",
    )
    parser.add_argument("html_file", type=Path)
    args = parser.parse_args(argv)
    patch_file(args.html_file)


if __name__ == "__main__":
    main()
