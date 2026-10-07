# Evaluator guide

The evaluator must treat both arms identically. Say only what is written here.

## Before each run

1. Create a fresh workspace folder outside any repo with previous solutions.
   - Test 1: copy `KPIS_historico.xlsx` to `input/`.
   - Test 2: copy [fixtures/kpi_features_contract.md](fixtures/kpi_features_contract.md) to `input/` and reload the checkpoint table.
2. Harness arm only: `python scripts/install.py <workspace>`.
3. Open the folder in VS Code, start a **new chat** in **Agent** mode, select the agreed model, and check that personal custom instructions are disabled.
4. Note the start time and the run order (alternate which arm goes first in each repetition).

## Scripted answers to agent questions

| The agent asks for | Answer |
|---|---|
| On-premise DSN | `El DSN es <DSN_ONPREM>.` |
| Database / schema | `Usa la base <SANDBOX_DB>.` |
| Cloud destination for harbor | `El destino en la nube es <CLOUD_DESTINATION>.` |
| Credentials | `Las credenciales están en variables de entorno; no las escribas en el código.` |
| Anything else (business rules, structure, names, style, libraries) | `Usa tu criterio y documenta el supuesto.` |

Count every clarifying question in results.csv (`clarifying_questions`). Write down whether it asked for the DSN **before** writing the connection (`asked_dsn` = 1/0).

<!-- TODO(content): replace the placeholders with the sandbox values before the first run. Never commit real values. -->

## Correction rounds

When the agent says it is done:

1. Fill the checklist (first pass) and run `check_project.py --json` (first pass).
2. Item fails or any standards finding → send **one** correction message using only these templates, listing every failed item:
   - Functional: `La entrega no cumple lo siguiente: <items del checklist que fallan>. Corrígelo.`
   - Standards: `Los archivos no cumplen el estándar del equipo: <hallazgos de check_project>. Corrígelo.`
   - Execution error: `Al ejecutar <archivo> sale este error: <error>. Corrígelo.`
3. Repeat until everything passes or **5 rounds**, whichever comes first. Record `corrections` and the final scores.

The baseline arm gets the standards findings as text too. This is what happens today: the analyst spends prompts fixing structure and style by hand. The difference in rounds is the value of the harness.

## Time

- `agent_minutes`: sum of the time from each prompt to the agent finishing.
- `human_minutes`: time spent reading, checking and writing corrections.
- `total_minutes`: from the first prompt until accepted.

## Tokens

1. Preferred: the token or context usage shown by Copilot Chat (chat debug view / usage indicator in your VS Code version). Record input and output tokens if available.
2. Fallback: export the chat session to JSON at the end (Command Palette → *Chat: Export*) and run:
   ```bash
   python benchmark/tools/estimate_tokens.py <exported_chat.json>
   ```
   This is a consistent approximation (characters / 4), valid for comparing the arms but not as an absolute count.
3. Also record premium requests consumed (GitHub Copilot usage page, before/after the run).

## Analytical quality rubric (blind)

A reviewer who does not know which arm produced the output scores 1-5:

| Criterion | 1 | 5 |
|---|---|---|
| Diagnosis depth | Generic profiling | Finds and quantifies the real issues |
| Propositiveness | Only what was asked | Justified, useful extra rules/features/score components |
| Justification | Rules with no rationale | Every decision tied to evidence |
| Maintainability | One-off code | Re-runnable, readable, traceable |

Record the average in `quality_score`.

## Test 2 checkpoint

Build the reference `kpi_features` table **once**: take the best harness-arm Test 1 run of the pilot, review it by hand, and save its CREATE TABLE AS SELECT. Before each Test 2 run, drop and recreate it so both arms start from identical data. Update `fixtures/kpi_features_contract.md` with its extra columns.
