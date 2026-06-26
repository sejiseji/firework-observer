"""Package-side runtime scaffolding for Firework Observer."""

from pyxel_goal_game.runtime.camera_motion import (
    AUTO_ROTATE_BASE_SWAY,
    AUTO_ROTATE_MOTION_ORDER,
    AUTO_ROTATE_SPEEDS,
    DEFAULT_AUTO_ROTATE_SPEED_INDEX,
    AutoRotateMotion,
)
from pyxel_goal_game.runtime.state import (
    AUTO_ROTATE_SPEED_MODE_ORDER,
    FIRST_GENERATION_FIREWORK_ORDER,
    AutoRotateSpeedMode,
    RuntimeShowState,
    RuntimeToggles,
    SalvoCountMode,
)

__all__ = [
    "AUTO_ROTATE_BASE_SWAY",
    "AUTO_ROTATE_MOTION_ORDER",
    "AUTO_ROTATE_SPEED_MODE_ORDER",
    "AUTO_ROTATE_SPEEDS",
    "DEFAULT_AUTO_ROTATE_SPEED_INDEX",
    "FIRST_GENERATION_FIREWORK_ORDER",
    "AutoRotateMotion",
    "AutoRotateSpeedMode",
    "RuntimeShowState",
    "RuntimeToggles",
    "SalvoCountMode",
]
