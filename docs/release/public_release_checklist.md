# Public Release Checklist

## Entry Points

- [ ] `python3 main.py` launches the official runtime.
- [ ] `pyxel run main.py` launches the official runtime.
- [ ] `main.py` remains the public default entrypoint.
- [ ] `scripts/run_runtime_app.py` remains available as an explicit development launcher.
- [ ] `tools/preview_firework_box.py` remains a development preview harness, not the public entrypoint.

## README

- [ ] `README.md` includes a link to `README.ja.md`.
- [ ] `README.ja.md` explains the project naturally in Japanese.
- [ ] Launch commands are clear for first-time users.
- [ ] Controls are accurate for the official runtime.
- [ ] Public safety checks are documented.

## Safety

- [ ] `python3 scripts/check_public_safety.py` passes.
- [ ] No tracked local absolute paths or local machine references remain.
- [ ] Public docs use repository-relative paths such as `docs/...`, `src/...`, and `scripts/...`.

## Validation

- [ ] `python3 -m compileall src tests scripts tools main.py`
- [ ] `.venv/bin/python -m pytest`
- [ ] `.venv/bin/python -m ruff check .`
- [ ] `python3 scripts/check_all.py`
- [ ] `uv run python scripts/capture_smoke.py`
- [ ] After `pyxel app2html`, run `python3 scripts/disable_pyxel_web_gamepad.py index.html` for the public Web build. This disables Pyxel's default virtual gamepad.

## Release Decisions

- [ ] Decide whether to publish smoke reports under `reports/`.
- [ ] Decide whether to include screenshots.
- [ ] Decide GitHub-only, Pyxel Web, `.pyxapp`, itch.io, or multiple formats.
- [ ] Add a `LICENSE` file before public release.
- [ ] Draft release notes and known issues.
