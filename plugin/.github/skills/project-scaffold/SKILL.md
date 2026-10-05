---
name: project-scaffold
description: Create a new analytics project, or add a new script, module, notebook or query file, following the team's folder structure and file naming. Use when starting a project, deciding where a new file goes, or naming a file.
argument-hint: "<project name> | <type of file to add>"
---

# /project-scaffold - Team Project Structure

Never improvise folders or file names. The structure is defined in code, in `scripts/scaffold.py` (`PROJECT_TREE`), and documented in `references/structure.md`.

## New project

Run the script instead of creating folders by hand:

```bash
python .github/skills/project-scaffold/scripts/scaffold.py <project_name> [--path <parent_dir>]
```

It creates the folder tree, `pyproject.toml` (ruff config), the constants module and a first notebook from the templates. Then fill the README header.

## New file in an existing project

| File type | Location and name | Start from |
|---|---|---|
| Python module | `src/<package>/<snake_case>.py` | `templates/module_template.py` |
| Notebook | `notebooks/NN_short_description.ipynb` | `templates/notebook_template.ipynb` |
| Query | `queries/NN_verb_subject.sql` | header in `impala-sql.instructions.md` |
| Constant | `src/<package>/constants.py` | add, never inline |

<!-- TODO(content): replace this table and PROJECT_TREE with the real team structure once confirmed. -->

## Checks

After creating files, run the `standards-check` skill.
