from __future__ import annotations

from pathlib import Path


def main() -> int:
    dist = Path("dist")
    dist.mkdir(exist_ok=True)
    print("Placeholder build script.")
    print("Replace this with the exact pyxel package command for your release target.")
    print("Example command depends on your Pyxel version and project entry layout.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
