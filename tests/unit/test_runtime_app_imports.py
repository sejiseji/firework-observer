from __future__ import annotations

import inspect
from pathlib import Path
from types import SimpleNamespace

from pyxel_goal_game.firework_presets import FireworkKind
from pyxel_goal_game.runtime import app, effects, input, render
from pyxel_goal_game.runtime.show_schedule import INWARD_PAIR_REPEAT_FRAMES
from pyxel_goal_game.runtime.state import RuntimeShowState, RuntimeToggles, SalvoCountMode
from pyxel_goal_game.screen_profiles import IPHONE16_BALANCED_PROFILE


def test_runtime_app_modules_do_not_import_tools_preview() -> None:
    for module in (app, effects, input, render):
        source = inspect.getsource(module)
        assert "tools.preview_firework_box" not in source
        assert "preview_firework_box" not in source


def test_runtime_app_import_does_not_construct_pyxel_app() -> None:
    assert hasattr(app, "RuntimeApp")
    assert hasattr(app, "main")


def test_official_runtime_launcher_exists() -> None:
    assert Path("scripts/run_runtime_app.py").exists()


def test_mobile_salvo_count_cycle_updates_runtime_state() -> None:
    fake_app = SimpleNamespace(
        mobile_salvo_count_choice=1,
        state=RuntimeShowState(),
    )

    app.RuntimeApp.cycle_mobile_salvo_count_choice(fake_app)

    assert fake_app.mobile_salvo_count_choice == 2
    assert fake_app.state.salvo_count == 2
    assert fake_app.state.salvo_count_mode is SalvoCountMode.OFF


def test_mobile_salvo_count_cycle_replaces_grand_sphere_when_count_moves_to_multi() -> None:
    fake_app = SimpleNamespace(
        mobile_salvo_count_choice=1,
        state=RuntimeShowState(selected_firework_kind=FireworkKind.GRAND_SPHERE),
    )

    app.RuntimeApp.cycle_mobile_salvo_count_choice(fake_app)

    assert fake_app.mobile_salvo_count_choice == 2
    assert fake_app.state.selected_firework_kind is FireworkKind.KIKU
    assert fake_app.state.salvo_count == 2


def test_mobile_firework_cycle_forces_count_one_for_grand_sphere() -> None:
    fake_app = SimpleNamespace(
        mobile_salvo_count_choice=app.MOBILE_INWARD_PAIR_CHOICE,
        state=RuntimeShowState(
            selected_firework_kind=FireworkKind.HALO,
            salvo_count_mode=SalvoCountMode.INWARD_PAIR,
        ),
    )

    app.RuntimeApp.handle_mobile_firework_cycle(fake_app)

    assert fake_app.state.selected_firework_kind is FireworkKind.GRAND_SPHERE
    assert fake_app.mobile_salvo_count_choice == 1
    assert fake_app.state.salvo_count == 1
    assert fake_app.state.toggles.random_firework_mode is False


def test_mobile_salvo_count_cycle_updates_active_salvo_mode() -> None:
    fake_app = SimpleNamespace(
        mobile_salvo_count_choice=2,
        state=RuntimeShowState(salvo_count_mode=SalvoCountMode.FIXED, salvo_count=2),
    )

    app.RuntimeApp.cycle_mobile_salvo_count_choice(fake_app)

    assert fake_app.mobile_salvo_count_choice == 3
    assert fake_app.state.salvo_count == 3
    assert fake_app.state.salvo_count_mode is SalvoCountMode.FIXED


def test_mobile_salvo_count_cycle_includes_inward_choice() -> None:
    fake_app = SimpleNamespace(
        mobile_salvo_count_choice=5,
        state=RuntimeShowState(),
    )

    app.RuntimeApp.cycle_mobile_salvo_count_choice(fake_app)

    assert fake_app.mobile_salvo_count_choice == app.MOBILE_INWARD_PAIR_CHOICE
    assert fake_app.state.salvo_count_mode is SalvoCountMode.OFF
    assert fake_app.state.salvo_count == 1


def test_mobile_salvo_count_cycle_updates_active_mode_to_inward() -> None:
    fake_app = SimpleNamespace(
        mobile_salvo_count_choice=5,
        state=RuntimeShowState(salvo_count_mode=SalvoCountMode.FIXED, salvo_count=5),
    )

    app.RuntimeApp.cycle_mobile_salvo_count_choice(fake_app)

    assert fake_app.mobile_salvo_count_choice == app.MOBILE_INWARD_PAIR_CHOICE
    assert fake_app.state.salvo_count_mode is SalvoCountMode.INWARD_PAIR
    assert fake_app.state.salvo_count == 1


def test_mobile_salvo_count_cycle_replaces_grand_sphere_when_count_moves_to_inward() -> None:
    fake_app = SimpleNamespace(
        mobile_salvo_count_choice=5,
        state=RuntimeShowState(
            selected_firework_kind=FireworkKind.GRAND_SPHERE,
            salvo_count_mode=SalvoCountMode.FIXED,
            salvo_count=5,
        ),
    )

    app.RuntimeApp.cycle_mobile_salvo_count_choice(fake_app)

    assert fake_app.mobile_salvo_count_choice == app.MOBILE_INWARD_PAIR_CHOICE
    assert fake_app.state.selected_firework_kind is FireworkKind.KIKU
    assert fake_app.state.salvo_count_mode is SalvoCountMode.INWARD_PAIR


def test_mobile_salvo_start_uses_synced_runtime_count() -> None:
    called: list[int] = []
    fake_app = SimpleNamespace(
        mobile_salvo_count_choice=3,
        state=RuntimeShowState(salvo_count=3),
        start_fixed_salvo_loop=called.append,
    )

    app.RuntimeApp.start_mobile_salvo_loop(fake_app)

    assert called == [3]


def test_mobile_salvo_start_uses_inward_choice() -> None:
    called: list[str] = []
    fake_app = SimpleNamespace(
        mobile_salvo_count_choice=app.MOBILE_INWARD_PAIR_CHOICE,
        start_inward_pair_salvo_loop=lambda: called.append("inward"),
    )

    app.RuntimeApp.start_mobile_salvo_loop(fake_app)

    assert called == ["inward"]


def test_count_one_grand_sphere_uses_single_launch_path() -> None:
    called: list[str] = []
    fake_app = SimpleNamespace(
        state=RuntimeShowState(selected_firework_kind=FireworkKind.GRAND_SPHERE),
        launch=lambda: called.append("launch"),
    )

    app.RuntimeApp.schedule_salvo(fake_app, 1)

    assert called == ["launch"]


def test_multi_count_grand_sphere_is_replaced_before_salvo_schedule(monkeypatch) -> None:
    scheduled = []
    fake_app = SimpleNamespace(
        profile=IPHONE16_BALANCED_PROFILE,
        state=RuntimeShowState(selected_firework_kind=FireworkKind.GRAND_SPHERE),
        last_launched_kind=None,
        schedule_runtime_launches=scheduled.append,
    )
    monkeypatch.setattr(app, "pyxel", SimpleNamespace(frame_count=10))

    app.RuntimeApp.schedule_salvo(fake_app, 2)

    assert fake_app.state.selected_firework_kind is FireworkKind.KIKU
    assert len(scheduled) == 1
    assert {slot.firework_kind for slot in scheduled[0].slots} == {FireworkKind.KIKU}


def test_single_launch_passes_height_variation_into_schedule(monkeypatch) -> None:
    scheduled = []
    fake_app = SimpleNamespace(
        profile=IPHONE16_BALANCED_PROFILE,
        state=RuntimeShowState(
            selected_firework_kind=FireworkKind.GRAND_SPHERE,
            toggles=RuntimeToggles(height_variation=True),
            seed_base=8,
        ),
        last_launched_kind=None,
        schedule_runtime_launches=scheduled.append,
    )
    monkeypatch.setattr(app, "pyxel", SimpleNamespace(frame_count=123))

    app.RuntimeApp.launch(fake_app)

    assert len(scheduled) == 1
    schedule = scheduled[0]
    assert schedule.start_frame == 123
    assert schedule.slots[0].firework_kind is FireworkKind.GRAND_SPHERE
    assert schedule.slots[0].burst_origin.y > 0.0


def test_mobile_auto_launch_toggle_preserves_selected_count() -> None:
    fake_app = SimpleNamespace(
        mobile_salvo_count_choice=4,
        state=RuntimeShowState(salvo_count=4),
    )

    app.RuntimeApp.toggle_mobile_auto_launch(fake_app)

    assert fake_app.state.toggles.auto_launch is True
    assert fake_app.state.salvo_count == 4
    assert fake_app.state.salvo_count_mode is SalvoCountMode.OFF


def test_mobile_auto_launch_toggle_does_not_store_inward_as_count() -> None:
    fake_app = SimpleNamespace(
        mobile_salvo_count_choice=app.MOBILE_INWARD_PAIR_CHOICE,
        state=RuntimeShowState(),
    )

    app.RuntimeApp.toggle_mobile_auto_launch(fake_app)

    assert fake_app.state.toggles.auto_launch is True
    assert fake_app.state.salvo_count == 1
    assert fake_app.state.salvo_count_mode is SalvoCountMode.OFF


def test_mobile_auto_launch_uses_selected_count() -> None:
    called: list[int] = []
    fake_app = SimpleNamespace(
        mobile_salvo_count_choice=4,
        schedule_salvo=called.append,
    )

    app.RuntimeApp.schedule_mobile_auto_launch(fake_app)

    assert called == [4]


def test_mobile_auto_launch_uses_inward_choice() -> None:
    called: list[str] = []
    fake_app = SimpleNamespace(
        mobile_salvo_count_choice=app.MOBILE_INWARD_PAIR_CHOICE,
        schedule_inward_pair_salvo=lambda: called.append("inward"),
    )

    app.RuntimeApp.schedule_mobile_auto_launch(fake_app)

    assert called == ["inward"]


def test_mobile_auto_launch_uses_random_count_choice() -> None:
    called: list[str] = []
    fake_app = SimpleNamespace(
        mobile_salvo_count_choice=None,
        schedule_random_count_salvo=lambda: called.append("random"),
    )

    app.RuntimeApp.schedule_mobile_auto_launch(fake_app)

    assert called == ["random"]


def test_random_salvo_count_choice_can_select_inward() -> None:
    assert app.choose_random_salvo_count_choice(seed=19) == app.MOBILE_INWARD_PAIR_CHOICE


def test_random_salvo_loop_uses_inward_repeat_when_random_selects_inward() -> None:
    called: list[str] = []
    fake_app = SimpleNamespace(
        state=RuntimeShowState(
            selected_firework_kind=FireworkKind.GRAND_SPHERE,
            seed_base=19,
        ),
        schedule_inward_pair_salvo=lambda: called.append("inward"),
    )

    repeat_frames = app.RuntimeApp.schedule_random_count_salvo(fake_app)

    assert called == ["inward"]
    assert fake_app.state.selected_firework_kind is FireworkKind.KIKU
    assert repeat_frames == INWARD_PAIR_REPEAT_FRAMES


def test_mobile_random_type_toggle_preserves_random_count_choice() -> None:
    fake_app = SimpleNamespace(
        mobile_salvo_count_choice=None,
        state=RuntimeShowState(salvo_count_mode=SalvoCountMode.RANDOM),
        refresh_mobile_panel_draft=lambda: None,
    )

    app.RuntimeApp.apply_mobile_toggle(fake_app, "random_firework_mode")

    assert fake_app.state.toggles.random_firework_mode is True
    assert fake_app.mobile_salvo_count_choice is None
    assert fake_app.state.salvo_count_mode is SalvoCountMode.RANDOM
    assert fake_app.state.salvo_count == 1


def test_mobile_random_type_toggle_preserves_inward_count_choice() -> None:
    fake_app = SimpleNamespace(
        mobile_salvo_count_choice=app.MOBILE_INWARD_PAIR_CHOICE,
        state=RuntimeShowState(salvo_count_mode=SalvoCountMode.INWARD_PAIR),
        refresh_mobile_panel_draft=lambda: None,
    )

    app.RuntimeApp.apply_mobile_toggle(fake_app, "random_firework_mode")

    assert fake_app.state.toggles.random_firework_mode is True
    assert fake_app.mobile_salvo_count_choice == app.MOBILE_INWARD_PAIR_CHOICE
    assert fake_app.state.salvo_count_mode is SalvoCountMode.INWARD_PAIR
    assert fake_app.state.salvo_count == 1


def test_mobile_random_type_toggle_preserves_fixed_count_choice() -> None:
    fake_app = SimpleNamespace(
        mobile_salvo_count_choice=3,
        state=RuntimeShowState(salvo_count_mode=SalvoCountMode.FIXED, salvo_count=3),
        refresh_mobile_panel_draft=lambda: None,
    )

    app.RuntimeApp.apply_mobile_toggle(fake_app, "random_firework_mode")

    assert fake_app.state.toggles.random_firework_mode is True
    assert fake_app.mobile_salvo_count_choice == 3
    assert fake_app.state.salvo_count_mode is SalvoCountMode.FIXED
    assert fake_app.state.salvo_count == 3


def test_mobile_box_nearest_vertical_edge_hide_toggle_updates_runtime_state() -> None:
    fake_app = SimpleNamespace(
        state=RuntimeShowState(),
        refresh_mobile_panel_draft=lambda: None,
    )

    app.RuntimeApp.apply_mobile_toggle(fake_app, "box_nearest_vertical_edge_hidden")

    assert fake_app.state.toggles.box_nearest_vertical_edge_hidden is True


def test_inward_pair_salvo_loop_sets_mode_and_repeat_frame() -> None:
    called: list[str] = []
    fake_app = SimpleNamespace(
        state=RuntimeShowState(),
        schedule_inward_pair_salvo=lambda: called.append("inward"),
        next_persistent_salvo_frame=0,
    )
    original_pyxel = app.pyxel
    app.pyxel = SimpleNamespace(frame_count=100)
    try:
        app.RuntimeApp.start_inward_pair_salvo_loop(fake_app)
    finally:
        app.pyxel = original_pyxel

    assert called == ["inward"]
    assert fake_app.state.salvo_count_mode is SalvoCountMode.INWARD_PAIR
    assert fake_app.next_persistent_salvo_frame == 100 + INWARD_PAIR_REPEAT_FRAMES
