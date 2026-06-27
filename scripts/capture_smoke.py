from __future__ import annotations

from datetime import datetime
from pathlib import Path


def main() -> None:
    # Placeholder for future automated visual smoke capture.
    # Pyxel screenshot automation depends on the local runtime environment,
    # so the template records a smoke note instead of pretending full automation exists.
    reports_dir = Path("reports/visual_smoke")
    reports_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = reports_dir / f"smoke_{stamp}.txt"
    message = (
        "Manual visual smoke placeholder. Run the game and check "
        "goals/acceptance/visual_regression_checklist.md\n"
    )
    path.write_text(
        message,
        encoding="utf-8",
    )
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
