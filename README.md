# CIB Analytics Copilot Bundle

Skills, instructions and prompts that make GitHub Copilot (VS Code) produce analytics work that follows the team standards: project structure, Python and notebook conventions, Impala queries through `impala-helper`, data transfers through `harbor`, and the organizational chart style.

## Origin

This project is a fork of Anthropic's [data plugin](https://github.com/anthropics/knowledge-work-plugins/tree/main/data) from `knowledge-work-plugins`. We kept its analysis workflows as a starting point but redesigned it for our needs:

- **Runtime**: GitHub Copilot in VS Code instead of Claude Cowork / Claude Code (`.github/` skills, instructions and prompts instead of a Claude plugin manifest).
- **Data access**: the internal `impala-helper` and `harbor` libraries instead of MCP warehouse connectors.
- **Team standards**: new skills, scoped instructions and scripts for project structure, Python and notebook conventions, Impala SQL rules and the organizational chart style.
- **Token efficiency**: always-on, path-scoped and on-demand layers, merged skills and progressive disclosure through `references/`.

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
