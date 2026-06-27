from __future__ import annotations

from dataclasses import dataclass
from typing import Any

BGM_MUSIC_ID = 0
BGM_MELODY_SOUND_ID = 16
BGM_HARMONY_SOUND_ID = 17
BGM_SUPPORT_SOUND_ID = 18
BGM_SOUND_IDS = (BGM_MELODY_SOUND_ID, BGM_HARMONY_SOUND_ID, BGM_SUPPORT_SOUND_ID)
BGM_CHANNELS = (0, 1, 2)
SFX_EXPLOSION_SOUND_ID = 0
SFX_CHANNEL = 3
EXPLOSION_SFX_COOLDOWN_FRAMES = 8

BGM_MELODY_NOTES = (
    "c4 c4 g4 g4 a4 a4 g4 r "
    "f4 f4 e4 e4 d4 d4 c4 r "
    "c4 r g4 g4 a4 r g4 r "
    "f4 r e4 e4 d4 r c4 r "
    "g4 a4 b4 r a4 g4 e4 r "
    "f4 g4 a4 r g4 e4 d4 r "
    "g4 g4 f4 f4 e4 e4 d4 r "
    "g4 g4 f4 f4 e4 e4 d4 r "
    "a4 r g4 r f4 e4 d4 r "
    "c4 c4 g4 g4 a4 a4 g4 r "
    "f4 f4 e4 e4 d4 d4 c4 r "
    "r r g4 r e4 r c4 r"
)
BGM_HARMONY_NOTES = (
    "e4 e4 e4 e4 f4 f4 e4 r "
    "a4 a4 g4 g4 f4 f4 e4 r "
    "e4 r e4 e4 f4 r e4 r "
    "a4 r g4 g4 f4 r e4 r "
    "e4 f4 g4 r f4 e4 c4 r "
    "a4 b4 c4 r b4 g4 f4 r "
    "b4 b4 a4 a4 g4 g4 f4 r "
    "b4 b4 a4 a4 g4 g4 f4 r "
    "f4 r e4 r d4 c4 f4 r "
    "e4 e4 e4 e4 f4 f4 e4 r "
    "a4 a4 g4 g4 f4 f4 e4 r "
    "r r e4 r c4 r e4 r"
)
BGM_SUPPORT_NOTES = (
    "c3 r r r g3 r r r "
    "f3 r r r c3 g3 r r "
    "c3 r r r g3 r r r "
    "f3 r r r d3 a3 r r "
    "e3 r r r f3 r r r "
    "d3 r r r e3 g3 r r "
    "g3 r r r f3 r r r "
    "g3 r r r e3 r r r "
    "a3 r r r f3 r r r "
    "c3 r r r g3 r r r "
    "f3 r r r c3 g3 r r "
    "r r c3 r g3 r r r"
)
BGM_MELODY_VOLUME = "4"
BGM_HARMONY_VOLUME = "2"
BGM_SUPPORT_VOLUME = "1"
EXPLOSION_SFX_NOTES = "c1 c1 c0 c0 r"


@dataclass
class RuntimeAudio:
    pyxel: Any
    enabled: bool = True
    bgm_enabled: bool = True
    last_explosion_frame: int | None = None
    user_gesture_unlocked: bool = False

    def setup(self) -> None:
        self.pyxel.sounds[BGM_MELODY_SOUND_ID].set(
            BGM_MELODY_NOTES,
            "p",
            BGM_MELODY_VOLUME,
            "n",
            28,
        )
        self.pyxel.sounds[BGM_HARMONY_SOUND_ID].set(
            BGM_HARMONY_NOTES,
            "p",
            BGM_HARMONY_VOLUME,
            "n",
            28,
        )
        self.pyxel.sounds[BGM_SUPPORT_SOUND_ID].set(
            BGM_SUPPORT_NOTES,
            "p",
            BGM_SUPPORT_VOLUME,
            "n",
            28,
        )
        self.pyxel.sounds[SFX_EXPLOSION_SOUND_ID].set(
            EXPLOSION_SFX_NOTES,
            "n",
            "76530",
            "fffff",
            6,
        )
        self.pyxel.musics[BGM_MUSIC_ID].set(
            [BGM_MELODY_SOUND_ID],
            [BGM_HARMONY_SOUND_ID],
            [BGM_SUPPORT_SOUND_ID],
        )

    def start_bgm(self) -> None:
        if self.enabled and self.bgm_enabled:
            self.pyxel.playm(BGM_MUSIC_ID, loop=True)

    def notify_user_gesture(self) -> None:
        if self.user_gesture_unlocked:
            return
        self.user_gesture_unlocked = True
        self.start_bgm()

    def set_enabled(self, enabled: bool) -> None:
        if self.enabled == enabled:
            return
        self.enabled = enabled
        if enabled:
            self.start_bgm()
        else:
            self.pyxel.stop()

    def set_bgm_enabled(self, enabled: bool) -> None:
        if self.bgm_enabled == enabled:
            return
        self.bgm_enabled = enabled
        if enabled:
            self.start_bgm()
        else:
            self.stop_bgm()

    def stop_bgm(self) -> None:
        for channel in BGM_CHANNELS:
            self.pyxel.stop(channel)

    def play_explosion(self, frame: int) -> bool:
        if not self.enabled:
            return False
        if not should_play_explosion_sfx(
            frame=frame,
            last_frame=self.last_explosion_frame,
            cooldown_frames=EXPLOSION_SFX_COOLDOWN_FRAMES,
        ):
            return False
        self.pyxel.play(SFX_CHANNEL, SFX_EXPLOSION_SOUND_ID)
        self.last_explosion_frame = frame
        return True


def should_play_explosion_sfx(
    *,
    frame: int,
    last_frame: int | None,
    cooldown_frames: int = EXPLOSION_SFX_COOLDOWN_FRAMES,
) -> bool:
    if cooldown_frames < 0:
        msg = "cooldown_frames must be non-negative"
        raise ValueError(msg)
    if last_frame is None:
        return True
    return frame - last_frame >= cooldown_frames
