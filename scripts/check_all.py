from __future__ import annotations

import subprocess

COMMANDS = [
    ["python3", "scripts/check_public_safety.py"],
    ["uv", "run", "pytest"],
    ["uv", "run", "ruff", "check", "."],
]


def main() -> int:
    for command in COMMANDS:
        print(f"$ {' '.join(command)}")
        result = subprocess.run(command, check=False)
        if result.returncode != 0:
            return result.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
