# Content backlog

What the scaffold still needs. Each item lists the input required and the files to update together. Search for `TODO(content)` to find the exact spots.

## Team knowledge (needs input from the team)

- [ ] **impala-helper API**: public interface (connect, run `.sql`, parameters, return types, write tables) and a usage snippet.
  Files: `skills/impala-query/references/impala-helper-api.md`, `skills/impala-query/SKILL.md`, `skills/project-scaffold/templates/module_template.py`, `instructions/impala-sql.instructions.md` (parameter syntax).
- [ ] **harbor API**: upload/download interface, formats, limits, cloud path conventions, data classification rules.
  Files: `skills/harbor-transfer/references/harbor-api.md`, `skills/harbor-transfer/SKILL.md`.
- [ ] **Project structure**: official folder tree and file naming.
  Files: `skills/project-scaffold/references/structure.md`, `skills/project-scaffold/SKILL.md`, `scaffold.py` (`PROJECT_TREE`, `TEMPLATE_FILES`), `check_project.py` (name patterns).
- [ ] **Python standard**: confirm or replace the proposed defaults.
  Files: `instructions/python.instructions.md`, `templates/module_template.py`, `templates/pyproject.toml`.
- [ ] **Notebook standard**: naming and cell order.
  Files: `instructions/notebooks.instructions.md`, `templates/notebook_template.ipynb`, `check_project.py`.
- [ ] **Impala SQL standard**: team rules, temp table naming, forbidden patterns.
  Files: `instructions/impala-sql.instructions.md`, `check_project.py`.
- [ ] **Visual identity**: palette hex codes, fonts, sequential scale, chart rules (logo, source footer, sizes).
  Files: `skills/org-visualization/assets/org_style.py`, `references/palette.md`, `instructions/visualization.instructions.md`.
- [ ] **Core tables**: most-used databases/tables and their partition columns.
  Files: `skills/impala-query/SKILL.md` or a new `references/tables.md`.
- [ ] **Golden rules review**: final list for the always-on file.
  Files: `plugin/.github/copilot-instructions.md`.

## Token trimming (no team input needed)

The inherited data-plugin skills are generic and long (~14k words in total). Cut them down to what differs from general knowledge and move the details to `references/`.

- [ ] `analyze`, `explore-data`, `validate-data`, `statistical-analysis`: keep the workflow and checklists, drop textbook explanations; replace non-Impala SQL examples with Impala.
- [ ] `build-dashboard` (~2.7k words): keep structure, move the HTML/JS boilerplate to `assets/`, use the `org_style` palette.
- [ ] `impala-query/references/sql-best-practices.md`: keep Impala only; drop the other dialects.
- [ ] `org-visualization/references/chart-design.md`: drop what `org_style` already enforces.
- [ ] `data-context-extractor`: point generated references at `impala-query/references/` instead of producing a separate Claude skill.

## Platform checks

- [ ] Confirm the VS Code / Copilot version in the bank supports agent skills, prompt files with `agent:` and `applyTo` instructions.
- [ ] Confirm `ruff` is available in the analytics environment.
