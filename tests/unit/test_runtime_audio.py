from __future__ import annotations

import inspect

import pytest

from pyxel_goal_game.runtime import audio
from pyxel_goal_game.runtime.audio import (
    BGM_ARPEGGIO_NOTES,
    BGM_ARPEGGIO_SOUND_ID,
    BGM_MELODY_SOUND_ID,
    BGM_MUSIC_ID,
    BGM_SHIMMER_SOUND_ID,
    BGM_SOUND_IDS,
    EXPLOSION_SFX_COOLDOWN_FRAMES,
    SFX_CHANNEL,
    SFX_EXPLOSION_SOUND_ID,
    RuntimeAudio,
    should_play_explosion_sfx,
)


class FakeSound:
    def __init__(self) -> None:
        self.calls: list[tuple[object, ...]] = []

    def set(self, *args: object) -> None:
        self.calls.append(args)


class FakeMusic:
    def __init__(self) -> None:
        self.calls: list[tuple[object, ...]] = []

    def set(self, *args: object) -> None:
        self.calls.append(args)


class FakePyxel:
    def __init__(self) -> None:
        self.sounds = [FakeSound() for _ in range(32)]
        self.musics = [FakeMusic() for _ in range(4)]
        self.playm_calls: list[tuple[object, ...]] = []
        self.play_calls: list[tuple[object, ...]] = []
        self.stop_calls = 0

    def playm(self, *args: object, **kwargs: object) -> None:
        self.playm_calls.append((*args, kwargs))

    def play(self, *args: object, **kwargs: object) -> None:
        self.play_calls.append((*args, kwargs))

    def stop(self) -> None:
        self.stop_calls += 1


def test_audio_constants_reserve_bgm_and_sfx_channels() -> None:
    assert BGM_MUSIC_ID == 0
    assert BGM_MELODY_SOUND_ID != SFX_EXPLOSION_SOUND_ID
    assert BGM_ARPEGGIO_SOUND_ID != SFX_EXPLOSION_SOUND_ID
    assert BGM_SHIMMER_SOUND_ID != SFX_EXPLOSION_SOUND_ID
    assert SFX_EXPLOSION_SOUND_ID not in BGM_SOUND_IDS
    assert len(BGM_SOUND_IDS) == 3
    assert SFX_CHANNEL == 3
    assert EXPLOSION_SFX_COOLDOWN_FRAMES > 0


def test_bgm_has_extended_arpeggio_accompaniment() -> None:
    assert len(BGM_ARPEGGIO_NOTES.split()) >= 80
    assert any(note in {"a4", "b4"} for note in BGM_ARPEGGIO_NOTES.split())


def test_explosion_sfx_cooldown_policy_is_deterministic() -> None:
    assert should_play_explosion_sfx(frame=10, last_frame=None) is True
    assert should_play_explosion_sfx(frame=17, last_frame=10) is False
    assert should_play_explosion_sfx(frame=18, last_frame=10) is True

    with pytest.raises(ValueError, match="cooldown"):
        should_play_explosion_sfx(frame=0, last_frame=None, cooldown_frames=-1)


def test_runtime_audio_sets_up_bgm_and_sfx_without_opening_window() -> None:
    pyxel = FakePyxel()
    runtime_audio = RuntimeAudio(pyxel=pyxel)

    runtime_audio.setup()
    runtime_audio.start_bgm()

    assert pyxel.sounds[BGM_MELODY_SOUND_ID].calls
    assert pyxel.sounds[BGM_ARPEGGIO_SOUND_ID].calls
    assert pyxel.sounds[BGM_SHIMMER_SOUND_ID].calls
    assert pyxel.sounds[SFX_EXPLOSION_SOUND_ID].calls
    assert pyxel.musics[BGM_MUSIC_ID].calls == [
        ([BGM_MELODY_SOUND_ID], [BGM_ARPEGGIO_SOUND_ID], [BGM_SHIMMER_SOUND_ID])
    ]
    assert pyxel.playm_calls == [(BGM_MUSIC_ID, {"loop": True})]


def test_runtime_audio_mute_stops_audio_and_blocks_sfx() -> None:
    pyxel = FakePyxel()
    runtime_audio = RuntimeAudio(pyxel=pyxel)

    runtime_audio.set_enabled(False)

    assert runtime_audio.enabled is False
    assert pyxel.stop_calls == 1
    assert runtime_audio.play_explosion(20) is False
    assert pyxel.play_calls == []


def test_runtime_audio_explosion_uses_cooldown() -> None:
    pyxel = FakePyxel()
    runtime_audio = RuntimeAudio(pyxel=pyxel)

    assert runtime_audio.play_explosion(10) is True
    assert runtime_audio.play_explosion(11) is False
    assert runtime_audio.play_explosion(18) is True

    assert pyxel.play_calls == [
        (SFX_CHANNEL, SFX_EXPLOSION_SOUND_ID, {}),
        (SFX_CHANNEL, SFX_EXPLOSION_SOUND_ID, {}),
    ]


def test_audio_module_does_not_import_tools_preview() -> None:
    source = inspect.getsource(audio)

    assert "tools.preview_firework_box" not in source
    assert "preview_firework_box" not in source
