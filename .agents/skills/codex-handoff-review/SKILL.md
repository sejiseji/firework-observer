# Codex Handoff Review Skill

Use this when receiving a Codex implementation result.

## Inputs

- original task
- changed files
- diff summary
- test output
- user-visible behavior
- known failures

## Output

Recommend one of:

- Commit
- Revise before commit
- Revert
- Split task
- Ask user for product decision

Do not approve a change only because tests pass.
Check whether it matches the product goal.
