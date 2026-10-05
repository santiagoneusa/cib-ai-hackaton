---
description: Jupyter notebook structure and naming standards
applyTo: "**/*.ipynb"
---

# Notebook standards

Start new notebooks from [notebook_template.ipynb](../skills/project-scaffold/templates/notebook_template.ipynb).

<!-- TODO(content): proposed defaults below. Confirm the naming pattern and cell order with the team. -->

## Naming

- `NN_short_description.ipynb`: two-digit execution order, lowercase, snake_case (e.g. `01_extraction.ipynb`, `02_eda.ipynb`).
- One purpose per notebook. Split it when it mixes extraction, modeling and reporting.

## Cell order

1. **Markdown header**: title, objective, author, date, inputs and outputs.
2. **Imports**: standard library, third party, then project `src/` modules.
3. **Parameters**: one cell with the constants for this run (dates, segments). No other hardcoded values.
4. **Load**: run `.sql` files through `impala-helper`.
5. **Analysis**: each section starts with a markdown cell that says what it answers.
6. **Outputs**: charts with `org_style`, tables, files written.
7. **Conclusions**: a markdown cell with findings and next steps.

## Rules

- Notebooks call functions and classes from `src/`. A function longer than ~15 lines or used twice moves to `src/`.
- Runs top to bottom in a fresh kernel without manual steps.
- No credentials, no raw connections, no inline SQL.
- Clear outputs before committing unless the notebook is a deliverable report.
