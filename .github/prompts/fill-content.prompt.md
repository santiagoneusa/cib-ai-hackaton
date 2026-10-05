---
description: Fill TODO(content) markers in the bundle from information the user provides
agent: agent
argument-hint: "<area: impala-helper | harbor | structure | python | notebooks | sql | palette>"
---

Fill the pending content for: ${input:area:area to fill}

1. Find the related `TODO(content)` markers in `plugin/` and the matching row in `docs/content-backlog.md`.
2. Ask the user for whatever input is missing (library interface, standard, palette). Do not invent it.
3. Write the content within the token budget in `.github/copilot-instructions.md`, keeping prose and code (scaffold.py, org_style.py, check_project.py) in sync.
4. Run the verification commands from `.github/copilot-instructions.md`.
5. Tick the item in `docs/content-backlog.md` and commit with a conventional commit scoped to the skill.
