# Value measurement

How we prove the value of the bundle: the same tasks, the same model, with and without the bundle, scored by the same automated checker.

## Metrics

| Dimension | Metric | How |
|---|---|---|
| Quality | Compliance score | `check_project.py --json` → `summary.compliance` |
| Quality | Findings per task, by rule | `check_project.py --json` → `findings[].rule` |
| Time | Correction prompts until the output is acceptable | count during the run |
| Time | Minutes until the output is acceptable | stopwatch |
| Automation | Steps done by code instead of by hand | scaffold, style, checks: count per task |

## Protocol

1. Pick 8-10 representative tasks (below). Same wording for both runs.
2. **Baseline**: a clean project without the bundle. Run each task in Copilot agent mode. Repeat 2-3 times.
3. **With bundle**: `python scripts/install.py <project>`. Same tasks, same model, same repetitions.
4. Score every result with `check_project.py --json` and log the time and correction prompts.
5. Report the averages and the deltas.

## Task set

<!-- TODO(content): replace with real, representative team tasks. -->

1. Create a new project to analyze monthly deposits by segment.
2. Write a query of transactions for the last 3 months by client type.
3. Turn that query into an extraction class and call it from a notebook.
4. Bar chart of the top 10 segments for the committee.
5. Move a result table from on-premise to cloud.
6. Refactor a messy notebook into `src/` modules.
7. Optimize a slow query on a partitioned table.
8. Review an existing project and fix the standards violations.

## Results log

| Task | Run | Bundle | Compliance | Findings | Corrections | Minutes |
|---|---|---|---|---|---|---|
| 1 | 1 | no | | | | |

## Extrapolation

`monthly hours saved = (baseline minutes - bundle minutes) × tasks per analyst per month × analysts / 60`

Also count review time saved in PRs (fewer standard-related comments) and avoided Impala cost from queries that respect partitions.
