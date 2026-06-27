from __future__ import annotations

import re
import subprocess
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PublicSafetyFinding:
    path: Path
    line_number: int
    label: str
    line: str


def forbidden_patterns() -> tuple[tuple[str, re.Pattern[str]], ...]:
    local_mac_users = "/" + "Users" + "/"
    local_linux_home = "/" + "home" + "/"
    local_volumes = "/" + "Volumes" + "/"
    local_desktop_tree = "Desktop" + "/" + "AllMyFiles"
    known_local_user = "toytoy" + "toy330"
    windows_drive = r"(?<![A-Za-z0-9_])[A-Za-z]:\\"
    return (
        ("local macOS user path", re.compile(re.escape(local_mac_users))),
        ("local Linux home path", re.compile(re.escape(local_linux_home))),
        ("local macOS volume path", re.compile(re.escape(local_volumes))),
        ("local Windows drive path", re.compile(windows_drive)),
        ("local Desktop tree", re.compile(re.escape(local_desktop_tree))),
        ("known local username", re.compile(re.escape(known_local_user))),
    )


def find_forbidden_references(
    text: str,
    *,
    path: Path = Path("<memory>"),
) -> list[PublicSafetyFinding]:
    findings: list[PublicSafetyFinding] = []
    patterns = forbidden_patterns()
    for line_number, line in enumerate(text.splitlines(), start=1):
        for label, pattern in patterns:
            if pattern.search(line):
                findings.append(
                    PublicSafetyFinding(
                        path=path,
                        line_number=line_number,
                        label=label,
                        line=line.strip(),
                    )
                )
    return findings


def tracked_files(repo_root: Path) -> tuple[Path, ...]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    )
    return tuple(Path(line) for line in result.stdout.splitlines() if line)


def read_text_if_safe(path: Path) -> str | None:
    data = path.read_bytes()
    if b"\0" in data:
        return None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return None


def scan_files(
    repo_root: Path,
    paths: Iterable[Path],
) -> list[PublicSafetyFinding]:
    findings: list[PublicSafetyFinding] = []
    for relative_path in paths:
        full_path = repo_root / relative_path
        if not full_path.is_file():
            continue
        text = read_text_if_safe(full_path)
        if text is None:
            continue
        findings.extend(find_forbidden_references(text, path=relative_path))
    return findings


def scan_tracked_files(repo_root: Path) -> list[PublicSafetyFinding]:
    return scan_files(repo_root, tracked_files(repo_root))


def format_findings(findings: Sequence[PublicSafetyFinding]) -> str:
    return "\n".join(
        f"{finding.path}:{finding.line_number}: {finding.label}: {finding.line}"
        for finding in findings
    )


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    findings = scan_tracked_files(repo_root)
    if findings:
        print(format_findings(findings))
        return 1
    print("public safety check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
