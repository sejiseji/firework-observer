from __future__ import annotations

from dataclasses import dataclass
from typing import Any

BGM_MUSIC_ID = 0
BGM_MELODY_SOUND_ID = 16
BGM_ARPEGGIO_SOUND_ID = 17
BGM_SHIMMER_SOUND_ID = 18
BGM_SOUND_IDS = (BGM_MELODY_SOUND_ID, BGM_ARPEGGIO_SOUND_ID, BGM_SHIMMER_SOUND_ID)
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
BGM_ARPEGGIO_NOTES = (
    "c4 e4 g4 e4 c4 e4 g4 r "
    "f4 a4 b4 a4 e4 g4 b4 r "
    "c4 e4 g4 r e4 g4 b4 r "
    "f4 a4 b4 r d4 f4 a4 r "
    "e4 g4 b4 g4 f4 a4 b4 r "
    "d4 f4 a4 f4 e4 g4 b4 r "
    "g4 b4 a4 b4 f4 a4 b4 r "
    "g4 b4 a4 b4 e4 g4 b4 r "
    "a4 b4 g4 r g4 b4 a4 r "
    "c4 e4 g4 e4 c4 e4 g4 r "
    "f4 a4 b4 a4 e4 g4 b4 r "
    "b4 r g4 r e4 r c4 r"
)
BGM_SHIMMER_NOTES = (
    "r r g4 r r r b4 r "
    "r r a4 r r r b4 r "
    "r r g4 r r r b4 r "
    "r r a4 r r r b4 r "
    "r r b4 r r r a4 r "
    "r r a4 r r r b4 r "
    "r r g4 r r r a4 r "
    "r r g4 r r r b4 r "
    "r r b4 r r r a4 r "
    "r r g4 r r r b4 r "
    "r r a4 r r r b4 r "
    "r r r r g4 r r r"
)
EXPLOSION_SFX_NOTES = "c1 c1 c0 c0 r"


@dataclass
class RuntimeAudio:
    pyxel: Any
    enabled: bool = True
    last_explosion_frame: int | None = None

    def setup(self) -> None:
        self.pyxel.sounds[BGM_MELODY_SOUND_ID].set(
            BGM_MELODY_NOTES,
            "p",
            "332232223222322232223222322232223222322232223222",
            "n",
            28,
        )
        self.pyxel.sounds[BGM_ARPEGGIO_SOUND_ID].set(
            BGM_ARPEGGIO_NOTES,
            "p",
            "111011101110111011101110111011101110111011101110111011101110111011101110111011101110111011101110",
            "n",
            18,
        )
        self.pyxel.sounds[BGM_SHIMMER_SOUND_ID].set(
            BGM_SHIMMER_NOTES,
            "p",
            "000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001",
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
            [BGM_ARPEGGIO_SOUND_ID],
            [BGM_SHIMMER_SOUND_ID],
        )

    def start_bgm(self) -> None:
        if self.enabled:
            self.pyxel.playm(BGM_MUSIC_ID, loop=True)

    def set_enabled(self, enabled: bool) -> None:
        if self.enabled == enabled:
            return
        self.enabled = enabled
        if enabled:
            self.start_bgm()
        else:
            self.pyxel.stop()

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
