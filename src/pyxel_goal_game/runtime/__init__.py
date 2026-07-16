"""Package-side runtime scaffolding for Firework Observer."""

from pyxel_goal_game.runtime.audio import (
    BGM_MUSIC_ID,
    EXPLOSION_SFX_COOLDOWN_FRAMES,
    SFX_CHANNEL,
    SFX_EXPLOSION_SOUND_ID,
)
from pyxel_goal_game.runtime.camera_motion import (
    AUTO_ROTATE_BASE_SWAY,
    AUTO_ROTATE_MOTION_ORDER,
    AUTO_ROTATE_SPEEDS,
    DEFAULT_AUTO_ROTATE_SPEED_INDEX,
    AutoRotateMotion,
)
from pyxel_goal_game.runtime.show_schedule import (
    INWARD_PAIR_REPEAT_FRAMES,
    PERSISTENT_SALVO_REPEAT_FRAMES,
    RuntimeLaunchSchedule,
    RuntimeLaunchSlot,
)
from pyxel_goal_game.runtime.state import (
    AUTO_ROTATE_SPEED_MODE_ORDER,
    FIRST_GENERATION_FIREWORK_ORDER,
    MOBILE_SELECTABLE_FIREWORK_ORDER,
    SINGLE_LAUNCH_RANDOM_FIREWORK_ORDER,
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
    "BGM_MUSIC_ID",
    "DEFAULT_AUTO_ROTATE_SPEED_INDEX",
    "EXPLOSION_SFX_COOLDOWN_FRAMES",
    "FIRST_GENERATION_FIREWORK_ORDER",
    "INWARD_PAIR_REPEAT_FRAMES",
    "MOBILE_SELECTABLE_FIREWORK_ORDER",
    "AutoRotateMotion",
    "AutoRotateSpeedMode",
    "PERSISTENT_SALVO_REPEAT_FRAMES",
    "RuntimeShowState",
    "RuntimeLaunchSchedule",
    "RuntimeLaunchSlot",
    "RuntimeToggles",
    "SFX_CHANNEL",
    "SFX_EXPLOSION_SOUND_ID",
    "SINGLE_LAUNCH_RANDOM_FIREWORK_ORDER",
    "SalvoCountMode",
]
