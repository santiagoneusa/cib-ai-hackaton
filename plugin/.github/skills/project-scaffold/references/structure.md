# Project structure

<!-- TODO(content): replace with the team's official structure, then mirror it in scripts/scaffold.py (PROJECT_TREE). Explain only what is not obvious from the names. -->

Proposed default:

```
<project_name>/
├── README.md               # objective, owner, how to run
├── pyproject.toml          # ruff config (from templates/)
├── queries/                # NN_verb_subject.sql, executed with impala-helper
├── notebooks/              # NN_short_description.ipynb, orchestration + narrative
├── src/<project_name>/     # reusable code: classes, functions
│   ├── __init__.py
│   └── constants.py        # paths, tables, thresholds (UPPER_SNAKE_CASE)
├── outputs/
│   ├── figures/            # written by org_style.save
│   └── data/               # small exported results only
└── tests/
```

## Rules

- `outputs/` is generated content and is not committed except for deliverables.
- No data files in `src/`, `queries/` or `notebooks/`.
