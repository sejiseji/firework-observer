from __future__ import annotations

from pathlib import Path

REQUIRED = [
    "AGENTS.md",
    "goals/GOAL_STATE.md",
    "goals/task_queue.json",
    "docs/product/NORTH_STAR.md",
]


def main() -> int:
    missing = [path for path in REQUIRED if not Path(path).exists()]
    if missing:
        for path in missing:
            print(f"missing: {path}")
        return 1

    print("handoff baseline files exist")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
