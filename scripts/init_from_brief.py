from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def md_list(items: list[str]) -> str:
    if not items:
        return "- unknown"
    return "\n".join(f"- {item}" for item in items)


def get(data: dict[str, Any], path: str, default: Any = "unknown") -> Any:
    current: Any = data
    for key in path.split("."):
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current


def write(path: Path, content: str, apply: bool) -> None:
    print(f"{'write' if apply else 'preview'}: {path}")
    if apply:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content.lstrip(), encoding="utf-8")


def build_game_brief(data: dict[str, Any]) -> str:
    return f"""
# Game Brief

## Status

Initialized from `project_brief.json`.

## Identity

- Working title: {get(data, "project_identity.working_title")}
- One-line pitch: {get(data, "project_identity.one_line_pitch")}
- Main genre: {get(data, "project_identity.main_genre")}
- Sub genre: {get(data, "project_identity.sub_genre")}
- Target platform: {get(data, "project_identity.target_platform")}
- Target audience: {get(data, "project_identity.target_audience")}
- Session length: {get(data, "project_identity.session_length")}
- Release intent: {get(data, "project_identity.release_intent")}

## North star

- First feeling: {get(data, "north_star.first_feeling")}
- Memory after play: {get(data, "north_star.memory_after_play")}
- Single most important experience: {get(data, "north_star.single_most_important_experience")}
- Must not lose: {get(data, "north_star.must_not_lose")}
- Success definition: {get(data, "north_star.success_definition")}

## Player experience

- Mood: {get(data, "player_experience.mood")}
- Pace: {get(data, "player_experience.pace")}
- Difficulty: {get(data, "player_experience.difficulty")}
- Pressure: {get(data, "player_experience.pressure")}
- Desired aftertaste: {get(data, "player_experience.desired_aftertaste")}

## Main verbs

{md_list(get(data, "player_experience.main_verbs", []))}

## Technical boundaries

- Target FPS: {get(data, "technical.target_fps")}
- Max active particles: {get(data, "technical.max_active_particles")}
- Max trail length: {get(data, "technical.max_trail_length")}
- Architecture: {get(data, "technical.architecture")}
- Deterministic simulation: {get(data, "technical.deterministic_simulation")}
- Pyxel API boundary: {get(data, "technical.pyxel_api_boundary")}

## Codex operation

- Patch size: {get(data, "codex_operation.patch_size")}
- Allow refactor: {get(data, "codex_operation.allow_refactor")}
- Allow dependency addition: {get(data, "codex_operation.allow_dependency_addition")}
- Update docs: {get(data, "codex_operation.update_docs")}
- Stop on product ambiguity: {get(data, "codex_operation.stop_on_product_ambiguity")}
"""


def build_north_star(data: dict[str, Any]) -> str:
    return f"""
# North Star

## Product one-liner

{get(data, "project_identity.one_line_pitch")}

## Current product goal

{get(data, "north_star.single_most_important_experience")}

## Primary value

The project should make the player feel:

- {get(data, "north_star.first_feeling")}
- {get(data, "player_experience.desired_aftertaste")}

## Must not lose

{get(data, "north_star.must_not_lose")}

## Success criteria

The prototype succeeds when:

- {get(data, "north_star.success_definition")}
- the core loop is playable,
- visual direction is recognizable,
- Codex can continue development from repository docs rather than hidden chat context.
"""


def build_game_design(data: dict[str, Any]) -> str:
    controls = get(data, "controls.core_controls", {})
    controls_text = "\n".join(f"- {key}: {value}" for key, value in controls.items()) or "- unknown"

    return f"""
# Game Design

## Working title

{get(data, "project_identity.working_title")}

## Genre

- Main: {get(data, "project_identity.main_genre")}
- Sub: {get(data, "project_identity.sub_genre")}

## Core loop

1. Player starts by: {get(data, "game_loop.start")}
2. Player repeatedly: {get(data, "game_loop.repeat")}
3. The game responds by: {get(data, "game_loop.response")}
4. The player progresses by: {get(data, "game_loop.progress")}
5. The loop ends when: {get(data, "game_loop.end")}

## Win / lose

- Win condition: {get(data, "game_loop.win_condition")}
- Lose condition: {get(data, "game_loop.lose_condition")}

## Controls

{controls_text}

## Design notes for Codex

- Preserve the recorded core loop unless explicitly asked to change it.
- Prefer one polished interaction over many unfinished mechanics.
- If product direction is ambiguous, record an assumption or ask for user
  feedback depending on risk.
"""


def build_player_experience(data: dict[str, Any]) -> str:
    return f"""
# Player Experience

## Desired feeling

- Mood: {get(data, "player_experience.mood")}
- Pace: {get(data, "player_experience.pace")}
- Difficulty: {get(data, "player_experience.difficulty")}
- Pressure: {get(data, "player_experience.pressure")}
- Aftertaste: {get(data, "player_experience.desired_aftertaste")}

## Player verbs

{md_list(get(data, "player_experience.main_verbs", []))}

## Review questions

After a gameplay or visual change, answer:

- What can the player do now?
- What feels better?
- What became more confusing?
- Did the change preserve the intended mood?
- Is user playtest feedback needed?
"""


def build_non_goals(data: dict[str, Any]) -> str:
    return f"""
# Non-Goals

These are intentionally out of scope unless explicitly approved.

{md_list(get(data, "non_goals", []))}

## Codex rule

Do not implement these as “helpful additions”.
If a task appears to require one of these, stop and record the conflict.
"""


def build_goal_state(data: dict[str, Any]) -> str:
    return f"""
# Goal State

## Current phase

Initialized prototype planning.

## Current goal

{get(data, "north_star.single_most_important_experience")}

## Current playable target

{get(data, "game_loop.repeat")}

## What Codex should optimize for

1. Follow `docs/product/GAME_BRIEF.md`.
2. Make small, testable changes.
3. Preserve architecture boundaries.
4. Record assumptions and risks.
5. Feed user answers back into durable docs.

## Current risks

- Codex may infer product direction beyond the brief.
- Visual quality may require subjective review.
- Performance can degrade if particles/trails are uncapped.
- Product decisions may remain hidden in chat unless documented.

## Current mitigation

- Use task queue.
- Use acceptance checklists.
- Use deterministic simulation where practical.
- Record feedback in docs and goals.
"""


def build_roadmap(data: dict[str, Any]) -> str:
    return f"""
# Roadmap

## Phase 0: Initialized brief

- [x] project brief exists
- [x] product direction documented
- [ ] user reviews initialized docs

## Phase 1: First playable loop

- [ ] run template locally
- [ ] confirm controls
- [ ] confirm first visual behavior
- [ ] add or update smoke note

## Phase 2: Core experience

- [ ] implement core verb: {", ".join(get(data, "player_experience.main_verbs", ["unknown"]))}
- [ ] tune visual feel
- [ ] tune performance budget
- [ ] record user feedback

## Phase 3: Prototype release

- [ ] create build
- [ ] draft release notes
- [ ] list known issues
- [ ] publish or archive
"""


def build_task_queue(data: dict[str, Any]) -> dict[str, Any]:
    initial_tasks = get(data, "initial_tasks", [])
    if not initial_tasks:
        initial_tasks = [
            "Review initialized docs",
            "Verify project runs",
            "Implement first core interaction",
            "Add smoke checklist result",
            "Record next user feedback",
        ]

    return {
        "version": 1,
        "policy": (
            "Keep tasks small enough for one Codex patch. "
            "Split ambiguous tasks before implementation."
        ),
        "current": [
            {
                "id": f"T{index:04d}",
                "title": title,
                "goal": title,
                "status": "todo",
                "acceptance": [
                    "Relevant docs were read",
                    "Patch is small and coherent",
                    "Tests or checklist were updated when relevant",
                    "Assumptions and risks were reported",
                ],
            }
            for index, title in enumerate(initial_tasks, start=1)
        ],
        "done": [],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("brief", type=Path, help="Path to project_brief.json")
    parser.add_argument("--apply", action="store_true", help="Actually write files")
    args = parser.parse_args()

    data = json.loads(args.brief.read_text(encoding="utf-8"))

    outputs = {
        Path("docs/product/GAME_BRIEF.md"): build_game_brief(data),
        Path("docs/product/NORTH_STAR.md"): build_north_star(data),
        Path("docs/product/GAME_DESIGN.md"): build_game_design(data),
        Path("docs/product/PLAYER_EXPERIENCE.md"): build_player_experience(data),
        Path("docs/product/NON_GOALS.md"): build_non_goals(data),
        Path("goals/GOAL_STATE.md"): build_goal_state(data),
        Path("goals/roadmap.md"): build_roadmap(data),
    }

    for path, content in outputs.items():
        write(path, content, args.apply)

    task_queue = build_task_queue(data)
    task_queue_path = Path("goals/task_queue.json")
    print(f"{'write' if args.apply else 'preview'}: {task_queue_path}")
    if args.apply:
        task_queue_path.write_text(
            json.dumps(task_queue, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    if not args.apply:
        print("\nDry run only. Add --apply to write files.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
