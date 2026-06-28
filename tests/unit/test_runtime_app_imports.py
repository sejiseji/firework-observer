from __future__ import annotations

import inspect
from pathlib import Path
from types import SimpleNamespace

from pyxel_goal_game.runtime import app, effects, input, render
from pyxel_goal_game.runtime.state import RuntimeShowState, SalvoCountMode


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


def test_mobile_salvo_count_cycle_updates_active_salvo_mode() -> None:
    fake_app = SimpleNamespace(
        mobile_salvo_count_choice=2,
        state=RuntimeShowState(salvo_count_mode=SalvoCountMode.FIXED, salvo_count=2),
    )

    app.RuntimeApp.cycle_mobile_salvo_count_choice(fake_app)

    assert fake_app.mobile_salvo_count_choice == 3
    assert fake_app.state.salvo_count == 3
    assert fake_app.state.salvo_count_mode is SalvoCountMode.FIXED


def test_mobile_salvo_start_uses_synced_runtime_count() -> None:
    called: list[int] = []
    fake_app = SimpleNamespace(
        mobile_salvo_count_choice=3,
        state=RuntimeShowState(salvo_count=3),
        start_fixed_salvo_loop=called.append,
    )

    app.RuntimeApp.start_mobile_salvo_loop(fake_app)

    assert called == [3]


def test_mobile_auto_launch_toggle_preserves_selected_count() -> None:
    fake_app = SimpleNamespace(
        mobile_salvo_count_choice=4,
        state=RuntimeShowState(salvo_count=4),
    )

    app.RuntimeApp.toggle_mobile_auto_launch(fake_app)

    assert fake_app.state.toggles.auto_launch is True
    assert fake_app.state.salvo_count == 4
    assert fake_app.state.salvo_count_mode is SalvoCountMode.OFF


def test_mobile_auto_launch_uses_selected_count() -> None:
    called: list[int] = []
    fake_app = SimpleNamespace(
        mobile_salvo_count_choice=4,
        schedule_salvo=called.append,
    )

    app.RuntimeApp.schedule_mobile_auto_launch(fake_app)

    assert called == [4]


def test_mobile_auto_launch_uses_random_count_choice() -> None:
    called: list[str] = []
    fake_app = SimpleNamespace(
        mobile_salvo_count_choice=None,
        schedule_random_count_salvo=lambda: called.append("random"),
    )

    app.RuntimeApp.schedule_mobile_auto_launch(fake_app)

    assert called == ["random"]


def test_mobile_random_type_toggle_resets_random_count_choice_to_fixed_one() -> None:
    fake_app = SimpleNamespace(
        mobile_salvo_count_choice=None,
        state=RuntimeShowState(salvo_count_mode=SalvoCountMode.RANDOM),
        refresh_mobile_panel_draft=lambda: None,
    )

    app.RuntimeApp.apply_mobile_toggle(fake_app, "random_firework_mode")

    assert fake_app.state.toggles.random_firework_mode is True
    assert fake_app.mobile_salvo_count_choice == 1
    assert fake_app.state.salvo_count_mode is SalvoCountMode.FIXED
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
