from __future__ import annotations

from pathlib import Path

IMPORTANT_FILES = [
    "AGENTS.md",
    "docs/product/NORTH_STAR.md",
    "docs/architecture/ARCHITECTURE_COMPASS.md",
    "goals/GOAL_STATE.md",
    "goals/task_queue.json",
]


def main() -> None:
    print("# Codex Task Packet\n")
    for file_name in IMPORTANT_FILES:
        path = Path(file_name)
        print(f"## {file_name}\n")
        if path.exists():
            print(path.read_text(encoding="utf-8"))
        else:
            print("(missing)")
        print("\n---\n")


if __name__ == "__main__":
    main()
