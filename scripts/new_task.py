from __future__ import annotations

import json
from pathlib import Path

TASK_QUEUE = Path("goals/task_queue.json")


def main() -> None:
    data = json.loads(TASK_QUEUE.read_text(encoding="utf-8"))
    current = data.setdefault("current", [])
    next_id = f"T{len(current) + len(data.get('done', [])) + 1:04d}"
    current.append(
        {
            "id": next_id,
            "title": "New task",
            "goal": "Describe one concrete behavior change.",
            "status": "todo",
            "acceptance": ["Define acceptance criteria before implementation."],
        }
    )
    TASK_QUEUE.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"added {next_id}")


if __name__ == "__main__":
    main()
