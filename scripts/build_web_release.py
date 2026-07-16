from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.disable_pyxel_web_gamepad import patch_file  # noqa: E402

APP_DIR_NAME = "firework-observer-web-app"
DEFAULT_OUTPUT = Path("index.html")


def repo_root() -> Path:
    return ROOT


def pyxel_bin(root: Path) -> Path:
    local = root / ".venv" / "bin" / "pyxel"
    if local.exists():
        return local
    found = shutil.which("pyxel")
    if found is None:
        msg = "pyxel command not found; install dependencies before building"
        raise RuntimeError(msg)
    return Path(found)


def copy_release_sources(root: Path, app_dir: Path) -> None:
    app_dir.mkdir(parents=True)
    shutil.copy2(root / "main.py", app_dir / "main.py")
    shutil.copytree(
        root / "src",
        app_dir / "src",
        ignore=shutil.ignore_patterns(
            "__pycache__",
            "*.pyc",
            "*.pyo",
            "*.egg-info",
            ".DS_Store",
        ),
    )


def run_command(command: list[str], *, cwd: Path) -> None:
    subprocess.run(command, cwd=cwd, check=True)


def build_web_release(output: Path, *, keep_build: bool = False) -> Path:
    root = repo_root()
    output = output if output.is_absolute() else root / output
    with tempfile.TemporaryDirectory(
        prefix="firework-observer-web-",
        dir=root / "build" if (root / "build").exists() else None,
        delete=not keep_build,
    ) as temp_name:
        temp_root = Path(temp_name)
        app_dir = temp_root / APP_DIR_NAME
        copy_release_sources(root, app_dir)

        pyxel = pyxel_bin(root)
        run_command(
            [str(pyxel), "package", str(app_dir), str(app_dir / "main.py")],
            cwd=temp_root,
        )

        pyxapp = temp_root / f"{APP_DIR_NAME}.pyxapp"
        run_command([str(pyxel), "app2html", str(pyxapp)], cwd=temp_root)

        html = temp_root / f"{APP_DIR_NAME}.html"
        patch_file(html)
        output.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(html, output)
        return output


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Build the minimal Pyxel Web release HTML.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Output HTML path. Defaults to index.html.",
    )
    parser.add_argument(
        "--keep-build",
        action="store_true",
        help="Keep the temporary build directory for inspection.",
    )
    args = parser.parse_args(argv)
    output = build_web_release(args.output, keep_build=args.keep_build)
    print(f"wrote {output.relative_to(repo_root())}")


if __name__ == "__main__":
    main()
