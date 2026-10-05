---
name: standards-check
description: Verify that a project follows the team standards (structure, file naming, Impala SQL rules, Python and notebook conventions, org_style colors, no credentials) and fix the violations. Use before finishing any task that created or edited files, before a commit or PR, or when asked to review a project.
---

# /standards-check - Validate Team Standards

## Workflow

1. Run the checker from the project root:

   ```bash
   python .github/skills/standards-check/scripts/check_project.py
   ```

   It checks folder structure, file naming, `SELECT *`, SQL headers, inline SQL, `print`, hardcoded colors and credentials, and runs `ruff` if it is installed.

2. Fix every finding in the files you created or edited. Do not touch unrelated files without asking.
3. Re-run until it reports 0 findings, or explain to the user why a finding is intentional.

Use `--json` to get a machine-readable report (used by the benchmark to measure compliance).

## Beyond the script

The script cannot judge design. Also review, briefly:

- Classes have a single responsibility; constants are not duplicated across modules.
- Notebooks delegate logic to `src/`.
- Queries filter on the partition columns of large tables.

<!-- TODO(content): add team review checklist items that cannot be automated. -->
