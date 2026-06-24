from __future__ import annotations

from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = PACKAGE_ROOT.parents[1]
ASSETS_ROOT = PROJECT_ROOT / "assets"
PYXEL_RESOURCE = ASSETS_ROOT / "pyxel" / "game.pyxres"
