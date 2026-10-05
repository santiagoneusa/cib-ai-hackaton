---
description: Start a new analytics project with the team structure, first query and first notebook
agent: agent
argument-hint: "<project_name> <business question>"
---

Create a new analytics project for: ${input:request:project_name and business question}

1. Use the `project-scaffold` skill to generate the project with `scaffold.py`. Do not create folders by hand.
2. Fill the README objective with the business question.
3. Use the `impala-query` skill to write the first extraction query in `queries/`.
4. Add the extraction class in `src/` following `module_template.py`, and call it from `notebooks/01_extraction.ipynb`.
5. Run the `standards-check` skill and fix every finding.
6. Summarize what was created and what the user must fill (tables, parameters).
