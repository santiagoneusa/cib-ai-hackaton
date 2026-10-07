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

1. Use the benchmark tests (below). Same prompt wording for both arms.
2. **Baseline**: a clean project without the bundle. Run each task in Copilot agent mode. Repeat at least 3 times.
3. **With bundle**: `python scripts/install.py <project>`. Same tasks, same model, same repetitions.
4. Score every result with `check_project.py --json` and log the time and correction prompts.
5. Report the averages and the deltas.

## Task set

The executable benchmark, with full prompts, checklists and evaluator script, is in [benchmark/](../benchmark/README.md):

1. **Test 1**: EDA and transformation of `KPIS_historico.xlsx` (notebook, impala-helper upload, cleaning SQL, feature table).
2. **Test 2**: team score, harbor transfer to the cloud and an interactive Streamlit report.

## Results log

Record every run in [benchmark/results.csv](../benchmark/results.csv).

## Extrapolation

`monthly hours saved = (baseline minutes - bundle minutes) × tasks per analyst per month × analysts / 60`

Also count review time saved in PRs (fewer standard-related comments) and avoided Impala cost from queries that respect partitions.
