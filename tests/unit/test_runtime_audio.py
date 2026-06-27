from __future__ import annotations

import inspect

import pytest

from pyxel_goal_game.runtime import audio
from pyxel_goal_game.runtime.audio import (
    BGM_HARMONY_NOTES,
    BGM_HARMONY_SOUND_ID,
    BGM_HARMONY_VOLUME,
    BGM_MELODY_NOTES,
    BGM_MELODY_SOUND_ID,
    BGM_MELODY_VOLUME,
    BGM_MUSIC_ID,
    BGM_SOUND_IDS,
    BGM_SUPPORT_NOTES,
    BGM_SUPPORT_SOUND_ID,
    BGM_SUPPORT_VOLUME,
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
    assert BGM_HARMONY_SOUND_ID != SFX_EXPLOSION_SOUND_ID
    assert BGM_SUPPORT_SOUND_ID != SFX_EXPLOSION_SOUND_ID
    assert SFX_EXPLOSION_SOUND_ID not in BGM_SOUND_IDS
    assert len(BGM_SOUND_IDS) == 3
    assert SFX_CHANNEL == 3
    assert EXPLOSION_SFX_COOLDOWN_FRAMES > 0


def test_bgm_uses_aligned_chord_harmony() -> None:
    melody_notes = BGM_MELODY_NOTES.split()
    harmony_notes = BGM_HARMONY_NOTES.split()
    support_notes = BGM_SUPPORT_NOTES.split()

    assert len(melody_notes) == len(harmony_notes) == len(support_notes)
    assert len(melody_notes) >= 80
    assert support_notes.count("r") > harmony_notes.count("r")
    assert int(BGM_MELODY_VOLUME) > int(BGM_HARMONY_VOLUME) > int(BGM_SUPPORT_VOLUME)
    assert int(BGM_MELODY_VOLUME) <= 4
    assert int(BGM_HARMONY_VOLUME) <= 2


def test_bgm_support_is_calm_mid_register_rhythm() -> None:
    support_notes = BGM_SUPPORT_NOTES.split()
    support_tones = [note for note in support_notes if note != "r"]

    assert len(support_tones) < len(support_notes) // 3
    assert {note[-1] for note in support_tones} == {"3"}
    assert set(support_tones) <= {"c3", "d3", "e3", "f3", "g3", "a3"}


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
    assert pyxel.sounds[BGM_HARMONY_SOUND_ID].calls
    assert pyxel.sounds[BGM_SUPPORT_SOUND_ID].calls
    assert pyxel.sounds[SFX_EXPLOSION_SOUND_ID].calls
    assert pyxel.musics[BGM_MUSIC_ID].calls == [
        ([BGM_MELODY_SOUND_ID], [BGM_HARMONY_SOUND_ID], [BGM_SUPPORT_SOUND_ID])
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
