from __future__ import annotations

import subprocess


def main() -> int:
    result = subprocess.run(["git", "diff", "--stat"], check=False)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
