# Analytics project rules

You are working in an analytics project of the CIB analytics team. Python orchestrates Impala queries through the internal `impala-helper` library and moves data between on-premise and cloud with the internal `harbor` library.

## Always

1. Follow the project structure and file naming in the `project-scaffold` skill. Never create folders or files outside it.
2. SQL lives in `.sql` files and runs through `impala-helper`. Never inline SQL in Python strings, never open raw database connections.
3. Every query filters on the table's partition columns and selects explicit columns (no `SELECT *`).
4. Data transfers between on-premise and cloud use `harbor`. Never copy data with ad-hoc scripts.
5. Charts use `org_style` (see the `org-visualization` skill). Never hardcode colors or fonts.
6. Python code follows `.github/instructions/python.instructions.md`: constants module, classes with one responsibility, type hints, docstrings, `logging`.
7. Notebooks orchestrate and explain; reusable logic goes to `src/` modules.
8. Never write credentials, hosts or tokens in code, notebooks or outputs.
9. Before finishing a task, run the `standards-check` skill and fix what it reports.

<!-- TODO(content): add or remove golden rules after the team review. Keep this file under ~400 words: it is sent with every request. -->

## Where the details are

| Need | Use |
|---|---|
| New project or new file | `project-scaffold` skill, `/new-project` prompt |
| Write or optimize a query | `impala-query` skill |
| Move data on-prem ↔ cloud | `harbor-transfer` skill |
| Chart or dashboard | `org-visualization`, `build-dashboard` skills |
| Analysis workflow | `analyze`, `explore-data`, `statistical-analysis`, `validate-data` skills |
| Review before delivery | `standards-check` skill, `/review-code` prompt |
