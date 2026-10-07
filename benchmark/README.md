# Harness benchmark

Measures what the bundle changes: **time, tokens and result quality** when developing the same analytics work with and without the harness.

| Test | Scenario | Deliverables |
|---|---|---|
| [Test 1](test-1-eda-transformation.md) | EDA and transformation of `KPIS_historico.xlsx` | EDA notebook, raw upload script (impala-helper), cleaning SQL, feature-table SQL |
| [Test 2](test-2-score-report.md) | Team score and interactive report | Score/pivot SQL, cloud transfer (harbor), interactive report reading from the cloud |

The prompts are in Spanish, like the team's real requests. Evaluator rules are in [evaluator-guide.md](evaluator-guide.md) and results go in [results.csv](results.csv).

## Design principles

1. **Same prompt, different harness.** The prompts describe *what* to build and never *how*: no folders, file names, coding style, query rules or colors. Supplying that is the harness's job, so if the prompt said it, the baseline would get it for free.
2. **Score each deliverable, not just the test.** Each test is one realistic end-to-end session, but every deliverable has its own checklist, so we can see where the harness helps.
3. **Test 2 starts from a fixed checkpoint.** Both arms start Test 2 from the same reference `kpi_features` table, so errors from Test 1 don't carry over and distort Test 2.
4. **Scripted evaluator.** Clarifying questions and correction prompts come from a fixed script, so the evaluator does not coach either arm.
5. **Repetition.** LLM output varies between runs: at least 3 runs per arm and test, alternating the order of the arms.

## Arms

| | Baseline | Harness |
|---|---|---|
| Workspace | empty folder + `input/KPIS_historico.xlsx` | same + `python scripts/install.py <workspace>` |
| `.github/` | none | bundle installed |
| Python env, impala-helper, harbor, streamlit | installed | installed (identical) |
| Model, Copilot mode | same model, Agent mode | same model, Agent mode |
| Personal custom instructions / memory | disabled | disabled |

Never open the workspace inside a folder that contains a previous solution (e.g. the DE02 interview folder): Copilot would read it and contaminate the run.

## Prerequisites

- [ ] `impala-helper` and `harbor` content filled in the bundle (`docs/content-backlog.md`). Otherwise the harness arm has no advantage on those deliverables.
- [ ] Sandbox: an on-premise Impala database for tests, a DSN, a cloud destination, and credentials set as environment variables.
- [ ] Reference `kpi_features` table for Test 2 (see [evaluator-guide.md](evaluator-guide.md#test-2-checkpoint)).
- [ ] Pilot: one run per arm of Test 1 to calibrate the checklists before the real runs.

## Metrics

| Dimension | Metric | Source |
|---|---|---|
| Time | Agent minutes (prompt → "done") and human minutes (reviewing + correcting) | stopwatch |
| Time | Correction rounds until accepted | evaluator log |
| Tokens | Tokens per session (input + output) | Copilot chat debug/usage view, or exported chat + `tools/estimate_tokens.py` |
| Cost | Premium requests consumed | GitHub Copilot usage page |
| Result | First-pass functional score (% checklist items) | test checklist |
| Result | First-pass standards compliance | `check_project.py --json` |
| Result | Analytical quality (1-5) | blind reviewer rubric |
| Result | Runs end to end without manual fixes | evaluator |

Interpreting tokens honestly: the harness *adds* input tokens to every request (instructions and skills). The value claim is that total session tokens go down because there are fewer exploration steps and correction rounds. Report both per-request and per-session tokens.

## Effort

About 2 tests × 2 arms × 3 runs = 12 sessions of 30-60 min each, plus reviewing. Plan 1-2 days with two people.
