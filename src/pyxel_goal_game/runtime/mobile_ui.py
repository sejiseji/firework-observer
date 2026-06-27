from __future__ import annotations

from dataclasses import dataclass, replace

from pyxel_goal_game.runtime.state import AutoRotateSpeedMode, RuntimeShowState

MENU_BUTTON_WIDTH = 28
MENU_BUTTON_HEIGHT = 15
MENU_BUTTON_MARGIN = 4
PANEL_WIDTH = 146
PANEL_HEIGHT = 214
PANEL_MARGIN = 8
CHECKBOX_SIZE = 7
CHECKBOX_ROW_HEIGHT = 13


@dataclass(frozen=True)
class Rect:
    x: int
    y: int
    width: int
    height: int

    def contains(self, x: int, y: int) -> bool:
        return self.x <= x < self.x + self.width and self.y <= y < self.y + self.height


@dataclass(frozen=True)
class MobileToggleSpec:
    key: str
    label: str


MOBILE_TOGGLE_SPECS = (
    MobileToggleSpec("random_firework_mode", "random"),
    MobileToggleSpec("height_variation", "height"),
    MobileToggleSpec("auto_launch", "auto"),
    MobileToggleSpec("auto_rotate", "rotate"),
    MobileToggleSpec("interior_stars_visible", "stars"),
    MobileToggleSpec("ufo_enabled", "ufo"),
    MobileToggleSpec("audio_enabled", "audio"),
    MobileToggleSpec("scenery_visible", "city"),
)


@dataclass(frozen=True)
class MobilePanelDraft:
    random_firework_mode: bool
    height_variation: bool
    auto_launch: bool
    auto_rotate: bool
    interior_stars_visible: bool
    ufo_enabled: bool
    audio_enabled: bool
    scenery_visible: bool
    auto_rotate_speed_mode: AutoRotateSpeedMode

    @classmethod
    def from_state(cls, state: RuntimeShowState) -> MobilePanelDraft:
        return cls(
            random_firework_mode=state.toggles.random_firework_mode,
            height_variation=state.toggles.height_variation,
            auto_launch=state.toggles.auto_launch,
            auto_rotate=state.toggles.auto_rotate,
            interior_stars_visible=state.toggles.interior_stars_visible,
            ufo_enabled=state.toggles.ufo_enabled,
            audio_enabled=state.toggles.audio_enabled,
            scenery_visible=state.toggles.scenery_visible,
            auto_rotate_speed_mode=state.auto_rotate_speed_mode,
        )

    def toggle(self, key: str) -> MobilePanelDraft:
        if key not in {spec.key for spec in MOBILE_TOGGLE_SPECS}:
            msg = f"unknown mobile toggle: {key}"
            raise ValueError(msg)
        return replace(self, **{key: not getattr(self, key)})

    def cycle_auto_rotate_speed(self) -> MobilePanelDraft:
        order = (
            AutoRotateSpeedMode.SLOW,
            AutoRotateSpeedMode.NORMAL,
            AutoRotateSpeedMode.FAST,
        )
        index = order.index(self.auto_rotate_speed_mode)
        return replace(self, auto_rotate_speed_mode=order[(index + 1) % len(order)])


def menu_button_rect(screen_width: int) -> Rect:
    return Rect(
        x=screen_width - MENU_BUTTON_WIDTH - MENU_BUTTON_MARGIN,
        y=MENU_BUTTON_MARGIN,
        width=MENU_BUTTON_WIDTH,
        height=MENU_BUTTON_HEIGHT,
    )


def panel_rect(screen_width: int, screen_height: int) -> Rect:
    width = min(PANEL_WIDTH, max(96, screen_width - PANEL_MARGIN * 2))
    height = min(PANEL_HEIGHT, max(96, screen_height - MENU_BUTTON_HEIGHT - PANEL_MARGIN * 3))
    return Rect(
        x=max(PANEL_MARGIN, screen_width - width - PANEL_MARGIN),
        y=MENU_BUTTON_HEIGHT + PANEL_MARGIN,
        width=width,
        height=height,
    )


def checkbox_rect(panel: Rect, index: int) -> Rect:
    return Rect(
        x=panel.x + 8,
        y=panel.y + 23 + index * CHECKBOX_ROW_HEIGHT,
        width=CHECKBOX_SIZE,
        height=CHECKBOX_SIZE,
    )


def checkbox_row_rect(panel: Rect, index: int) -> Rect:
    return Rect(
        x=panel.x + 4,
        y=panel.y + 19 + index * CHECKBOX_ROW_HEIGHT,
        width=panel.width - 8,
        height=CHECKBOX_ROW_HEIGHT,
    )


def speed_button_rect(panel: Rect) -> Rect:
    return Rect(panel.x + 8, panel.y + 127, panel.width - 16, 13)


def launch_button_rect(panel: Rect) -> Rect:
    return Rect(panel.x + 8, panel.y + 145, 45, 14)


def next_button_rect(panel: Rect) -> Rect:
    return Rect(panel.x + 58, panel.y + 145, 40, 14)


def random_salvo_button_rect(panel: Rect) -> Rect:
    return Rect(panel.x + 8, panel.y + 164, panel.width - 16, 14)


def apply_button_rect(panel: Rect) -> Rect:
    return Rect(panel.x + 8, panel.y + panel.height - 23, 55, 15)


def close_button_rect(panel: Rect) -> Rect:
    return Rect(panel.x + panel.width - 39, panel.y + panel.height - 23, 31, 15)
