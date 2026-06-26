from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from pyxel_goal_game.firework_presets import FireworkKind
from pyxel_goal_game.scenery_presets import SCENERY_PRESET_NAMES
from pyxel_goal_game.screen_profiles import DEFAULT_SCREEN_PROFILE_NAME


class AutoRotateSpeedMode(Enum):
    SLOW = "slow"
    NORMAL = "normal"
    FAST = "fast"


class SalvoCountMode(Enum):
    OFF = "off"
    FIXED = "fixed"
    RANDOM = "random"


FIRST_GENERATION_FIREWORK_ORDER = (
    FireworkKind.KIKU,
    FireworkKind.RING,
    FireworkKind.SPIRAL,
    FireworkKind.WILLOW,
    FireworkKind.PEONY,
    FireworkKind.MULTI_RING,
    FireworkKind.SENRIN,
    FireworkKind.HALO,
)

AUTO_ROTATE_SPEED_MODE_ORDER = (
    AutoRotateSpeedMode.SLOW,
    AutoRotateSpeedMode.NORMAL,
    AutoRotateSpeedMode.FAST,
)

DEFAULT_FIREWORK_KIND = FIRST_GENERATION_FIREWORK_ORDER[0]
DEFAULT_SCENERY_NAME = "city"
DEFAULT_SEED_BASE = 0
MIN_SALVO_COUNT = 1
MAX_SALVO_COUNT = 5


@dataclass(frozen=True)
class RuntimeToggles:
    random_firework_mode: bool = False
    auto_launch: bool = False
    height_variation: bool = False
    scenery_visible: bool = True
    interior_stars_visible: bool = True
    auto_rotate: bool = False


@dataclass(frozen=True)
class RuntimeShowState:
    profile_name: str = DEFAULT_SCREEN_PROFILE_NAME
    selected_firework_kind: FireworkKind = DEFAULT_FIREWORK_KIND
    selected_scenery_name: str = DEFAULT_SCENERY_NAME
    auto_rotate_speed_mode: AutoRotateSpeedMode = AutoRotateSpeedMode.NORMAL
    toggles: RuntimeToggles = RuntimeToggles()
    salvo_count_mode: SalvoCountMode = SalvoCountMode.OFF
    salvo_count: int = MIN_SALVO_COUNT
    frame_count: int = 0
    seed_base: int = DEFAULT_SEED_BASE

    def __post_init__(self) -> None:
        if not isinstance(self.selected_firework_kind, FireworkKind):
            msg = "selected_firework_kind must be a FireworkKind"
            raise ValueError(msg)
        if not isinstance(self.auto_rotate_speed_mode, AutoRotateSpeedMode):
            msg = "auto_rotate_speed_mode must be an AutoRotateSpeedMode"
            raise ValueError(msg)
        if not isinstance(self.salvo_count_mode, SalvoCountMode):
            msg = "salvo_count_mode must be a SalvoCountMode"
            raise ValueError(msg)
        if self.selected_firework_kind not in FIRST_GENERATION_FIREWORK_ORDER:
            msg = "selected_firework_kind must be a first-generation firework kind"
            raise ValueError(msg)
        if self.selected_scenery_name not in SCENERY_PRESET_NAMES:
            msg = "selected_scenery_name must be an active scenery preset name"
            raise ValueError(msg)
        if not MIN_SALVO_COUNT <= self.salvo_count <= MAX_SALVO_COUNT:
            msg = f"salvo_count must be between {MIN_SALVO_COUNT} and {MAX_SALVO_COUNT}"
            raise ValueError(msg)
        if self.frame_count < 0:
            msg = "frame_count must be non-negative"
            raise ValueError(msg)
        if self.seed_base < 0:
            msg = "seed_base must be non-negative"
            raise ValueError(msg)
