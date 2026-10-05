---
description: Impala SQL standards for query files
applyTo: "**/*.sql"
---

# Impala SQL standards

<!-- TODO(content): proposed defaults below. Add the team's own rules, naming of temp tables, and forbidden patterns. -->

- Filter on the partition columns of every large table. Check them with `SHOW PARTITIONS` if unsure.
- Select explicit columns. Never use `SELECT *`.
- Use CTEs (`WITH`) with descriptive names, one per logical step.
- Use meaningful table aliases, not `a`, `b`, `c`.
- Keywords in UPPERCASE, identifiers in lowercase snake_case, one clause per line.
- Parameterize dates and segments instead of hardcoding them. <!-- TODO(content): document the placeholder syntax impala-helper uses. -->
- After `CREATE TABLE ... AS SELECT` or `INSERT` into a table that will be queried again, run `COMPUTE STATS`.
- Start the file with a header comment: purpose, source tables, parameters, author.
- Name files `NN_verb_subject.sql` (e.g. `01_extract_transactions.sql`). <!-- TODO(content): confirm the naming pattern. -->
