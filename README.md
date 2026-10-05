# CIB Analytics Copilot Bundle

Skills, instructions and prompts that make GitHub Copilot (VS Code) produce analytics work that follows the team standards: project structure, Python and notebook conventions, Impala queries through `impala-helper`, data transfers through `harbor`, and the organizational chart style.

Based on Anthropic's open-source data plugin, adapted for Copilot and for the team's stack.

## The problem

Copilot does not know the team's conventions, so it improvises folders and file names, writes Python without classes or constants, inlines SQL or skips partition filters, and uses arbitrary chart colors. Every task then needs correction prompts and review comments.

## How it works

The bundle has three layers, each loaded only when needed to save tokens:

| Layer | Loaded | Content |
|---|---|---|
| Always-on rules | every request | `copilot-instructions.md`: short golden rules |
| Scoped rules | when a matching file is open | `instructions/*.instructions.md` for `.py`, `.ipynb`, `.sql`, charts |
| Skills | when the task needs them | workflows plus references, templates and scripts |

Rules that matter most are enforced by code rather than prose:

- `scaffold.py` generates the project structure.
- `org_style.py` owns the palette and fonts.
- `check_project.py` validates structure, naming, SQL, Python, colors and credentials, and outputs a compliance score.

## Contents

```
plugin/.github/
├── copilot-instructions.md
├── instructions/   python · notebooks · impala-sql · visualization
├── prompts/        new-project · review-code
└── skills/
    ├── project-scaffold      structure, templates, scaffold.py
    ├── impala-query          Impala SQL via impala-helper
    ├── harbor-transfer       on-premise ↔ cloud via harbor
    ├── org-visualization     charts with org_style
    ├── standards-check       check_project.py
    ├── analyze · explore-data · statistical-analysis · validate-data · build-dashboard
    └── data-context-extractor
```

## Install in a project

```bash
python scripts/install.py <path_to_project>
```

Then, in Copilot Chat (agent mode), try `/new-project` or `/review-code`.

## Status

This is a scaffold. Team-specific content is marked `TODO(content)` and tracked in [docs/content-backlog.md](docs/content-backlog.md). The value benchmark is in [docs/value-measurement.md](docs/value-measurement.md). Contributor rules are in [.github/copilot-instructions.md](.github/copilot-instructions.md).
