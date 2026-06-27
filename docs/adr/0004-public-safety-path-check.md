# ADR 0004: Public Safety Path Check

## Status

Accepted.

## Context

The project is approaching public release. Documentation, task logs, and handoff records can accidentally preserve local absolute paths, local machine names, or user-specific fragments.

Publishing those references is unnecessary and can disclose private machine information.

## Decision

Tracked project files must use repository-relative paths or neutral placeholders in durable docs and source comments.

The repository includes `scripts/check_public_safety.py` to scan tracked files for local absolute path patterns and known local fragments. `scripts/check_all.py` runs this check before tests and lint.

## Consequences

- Public release hygiene is enforced automatically.
- Future docs should prefer paths such as `docs/...`, `src/...`, `scripts/...`, `repository root`, or `<repo>`.
- Runtime behavior is not affected.
