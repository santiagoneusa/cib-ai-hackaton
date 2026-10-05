---
name: impala-query
description: Write, optimize and wire Impala SQL that runs through the internal impala-helper library from Python. Use when translating a data need into an Impala query, optimizing a query on a large partitioned table, storing a query as a .sql file, or calling it from a script or notebook.
argument-hint: "<description of what data you need>"
---

# /impala-query - Write Impala SQL for impala-helper

Write an Impala query from a natural language description, following the team's query standards, and wire it into Python through `impala-helper`.

Detailed SQL patterns and anti-patterns live in `references/sql-best-practices.md`. Open it only when the query needs window functions, complex joins or performance tuning.

## Usage

```
/impala-query <description of what data you need>
```

## Workflow

### 1. Understand the Request

Parse the user's description to identify:

- **Output columns**: What fields should the result include?
- **Filters**: What conditions limit the data (time ranges, segments, statuses)?
- **Aggregations**: Are there GROUP BY operations, counts, sums, averages?
- **Joins**: Does this require combining multiple tables?
- **Ordering**: How should results be sorted?
- **Limits**: Is there a top-N or sample requirement?

### 2. Dialect

Always Impala. Do not ask for the dialect.

### 3. Discover Schema

Run metadata statements through `impala-helper` (see `references/impala-helper-api.md`):

- `SHOW TABLES IN <db>` to find candidate tables
- `DESCRIBE <db>.<table>` for columns and types
- `SHOW PARTITIONS <db>.<table>` to find the partition columns that every query must filter on

<!-- TODO(content): list the most-used databases/tables or point to the data-context reference. -->

### 4. Write the Query

Follow these best practices:

**Structure:**
- Use CTEs (WITH clauses) for readability when queries have multiple logical steps
- One CTE per logical transformation or data source
- Name CTEs descriptively (e.g., `daily_signups`, `active_users`, `revenue_by_product`)

**Performance:**
- Never use `SELECT *` in production queries -- specify only needed columns
- Filter early (push WHERE clauses as close to the base tables as possible)
- Use partition filters when available (especially date partitions)
- Prefer `EXISTS` over `IN` for subqueries with large result sets
- Use appropriate JOIN types (don't use LEFT JOIN when INNER JOIN is correct)
- Avoid correlated subqueries when a JOIN or window function works
- Be mindful of exploding joins (many-to-many)

**Readability:**
- Add comments explaining the "why" for non-obvious logic
- Use consistent indentation and formatting
- Alias tables with meaningful short names (not just `a`, `b`, `c`)
- Put each major clause on its own line

**Dialect-specific optimizations:**
- Apply dialect-specific syntax and functions (see `references/sql-best-practices.md`)
- Use dialect-appropriate date functions, string functions, and window syntax
- Note any dialect-specific performance features (e.g., Snowflake clustering, BigQuery partitioning)

### 5. Present the Query

Provide:

1. **The complete query** in a SQL code block with syntax highlighting
2. **Brief explanation** of what each CTE or section does
3. **Performance notes** if relevant (expected cost, partition usage, potential bottlenecks)
4. **Modification suggestions** -- how to adjust for common variations (different time range, different granularity, additional filters)

### 6. Save and Wire into Python

1. Save the query as a `.sql` file in the project's queries folder. Never inline SQL in Python strings.
2. Execute it from Python through `impala-helper`, passing parameters (dates, segments) instead of formatting strings.

<!-- TODO(content): add the canonical impala-helper call snippet and the queries folder path from the project structure. -->

## Examples

**Simple aggregation:**
```
/impala-query Count of orders by status for the last 30 days
```

**Complex analysis:**
```
/impala-query Cohort retention analysis -- group users by their signup month, then show what percentage are still active (had at least one event) at 1, 3, 6, and 12 months after signup
```

**Performance-critical:**
```
/impala-query We have a 500M row events table partitioned by date. Find the top 100 users by event count in the last 7 days with their most recent event type.
```

## Tips

- Mention your SQL dialect upfront to get the right syntax immediately
- If you know the table names, include them -- otherwise Claude will help you find them
- Specify if you need the query to be idempotent (safe to re-run) or one-time
- For recurring queries, mention if it should be parameterized for date ranges
