from __future__ import annotations

from pathlib import Path

import pyxel


def load_pyxel_resource(path: Path) -> None:
    if path.exists():
        pyxel.load(str(path))
