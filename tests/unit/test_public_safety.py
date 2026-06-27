from __future__ import annotations

from pathlib import Path

from scripts.check_public_safety import (
    find_forbidden_references,
    scan_tracked_files,
)


def test_public_safety_checker_flags_local_machine_references() -> None:
    sample = "\n".join(
        (
            "safe path: docs/product/GAME_DESIGN.md",
            "mac path: " + "/" + "Users" + "/someone/project",
            "home path: " + "/" + "home" + "/someone/project",
            "volume path: " + "/" + "Volumes" + "/drive/project",
            "desktop tree: Desktop" + "/" + "AllMyFiles/project",
            "known user: toytoy" + "toy330",
            "windows path: C:" + "\\" + "project",
        )
    )

    findings = find_forbidden_references(sample)
    labels = {finding.label for finding in findings}

    assert "local macOS user path" in labels
    assert "local Linux home path" in labels
    assert "local macOS volume path" in labels
    assert "local Desktop tree" in labels
    assert "known local username" in labels
    assert "local Windows drive path" in labels


def test_public_safety_checker_allows_repository_relative_paths() -> None:
    sample = "\n".join(
        (
            "docs/product/GAME_DESIGN.md",
            "src/pyxel_goal_game/runtime/app.py",
            "<repo>/docs/research/visual_tuning_checklist.md",
            "repository root",
            "<uv-cache>",
        )
    )

    assert find_forbidden_references(sample) == []


def test_tracked_tree_has_no_local_machine_references() -> None:
    assert scan_tracked_files(Path.cwd()) == []
