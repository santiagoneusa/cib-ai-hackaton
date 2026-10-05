# Authoring guide for this repository

This repo builds a GitHub Copilot bundle (skills, instructions, prompts) for the CIB analytics team. You are editing the **bundle**, not an analytics project: the rules inside `plugin/.github/` are content to write, not rules to follow here.

## Layout

- `plugin/.github/` is the payload installed into analytics projects by `scripts/install.py`.
  - `copilot-instructions.md`: always-on golden rules (sent with every request).
  - `instructions/*.instructions.md`: rules scoped by `applyTo` globs.
  - `skills/<name>/SKILL.md`: on-demand workflows; details in `references/`, code in `scripts/` or `assets/`, starter files in `templates/`.
  - `prompts/*.prompt.md`: multi-skill workflows.
- `docs/content-backlog.md`: what is still missing and who provides it.
- `docs/value-measurement.md`: the benchmark that proves the hackathon value.

## Filling content

- Pending work is marked `TODO(content)`. Replace the marker with the real content and delete the marker.
- Use only information the user provides (library interfaces, standards, palette). Never invent APIs, table names or rules; if something is missing, leave the marker and say so.
- Never write credentials, hostnames, internal URLs, bucket names or confidential data.
- When a rule exists both as prose and as code (structure in `scaffold.py`, colors in `org_style.py`, checks in `check_project.py`), update both in the same change.

## Token budget (the bundle is loaded into every analyst's context)

| File | Max |
|---|---|
| `plugin/.github/copilot-instructions.md` | ~400 words |
| each `*.instructions.md` | ~300 words |
| each `SKILL.md` | ~500 words; move detail to `references/` |
| each `references/*.md` | ~800 words |

- Write only what differs from general knowledge: the team's libraries, structure, rules and palette. Delete generic explanations the model already knows.
- Prefer a template or snippet over a paragraph of rules.
- Skill `description` decides when Copilot loads a skill: say what it does and when to use it, with the words analysts actually type.

## Commits

Conventional commits (`feat:`, `fix:`, `docs:`, `refactor:`, `chore:`), one logical change per commit, scoped by skill when possible, e.g. `feat(impala-query): add impala-helper API cheat sheet`.

## Verify before committing

```bash
python plugin/.github/skills/project-scaffold/scripts/scaffold.py demo --path <tmp_dir>
python plugin/.github/skills/standards-check/scripts/check_project.py <tmp_dir>/demo
```

A freshly scaffolded project must report 0 findings.
