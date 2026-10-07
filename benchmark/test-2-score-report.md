# Test 2 - Team score and interactive report

**Starting state:** a fresh workspace (not the Test 1 one) with only `input/kpi_features_contract.md` (the column contract from Test 1), plus `.github/` in the harness arm. The reference `kpi_features` table has been reloaded in the sandbox ([checkpoint](evaluator-guide.md#test-2-checkpoint)). New chat, Agent mode.

**Paste exactly the prompt below.** Do not add context or hints.

## Prompt

```text
Contexto
Eres parte del equipo de analítica de CIB. En Impala on-premise ya existe la tabla kpi_features con el histórico mensual de KPIs por equipo: una fila por equipo × indicador × corte, con las columnas codigo_equ, equipo, codigo_entorno, entorno, frente, indicador, unidad, corte (AAAAMM), fecha_corte, resultado, meta y cumplimiento, más algunas features adicionales (el detalle está en input/kpi_features_contract.md). Los indicadores tienen unidades distintas (porcentaje, cantidad, escala), algunos equipos no tienen entorno y no todos los equipos reportan todos los indicadores todos los meses.

El área de Estrategia quiere un score de desempeño por equipo para decidir dónde enfocar acompañamiento, y un reporte interactivo para consultarlo.

Construye lo siguiente, en este orden:

1. SQL del score
   - Crea en Impala, ejecutándola con la librería interna impala-helper, una tabla pivote con una fila por equipo × corte que calcule un score de desempeño.
   - Sé creativo y propositivo con la lógica del score. Por ejemplo: comparar el valor actual de cada indicador contra el promedio histórico del equipo y contra el promedio de los demás equipos en el mismo corte, marcar cuando está peor que su promedio, medias móviles en el tiempo, tendencia, estabilidad o cumplimiento de la meta.
   - El score debe ser comparable entre indicadores con unidades distintas y entre equipos que reportan distintos indicadores. Justifica la normalización, los pesos y cómo tratas los datos faltantes.
   - Además del score final, deja en la tabla sus componentes, para poder explicar por qué un equipo tiene ese resultado, y una clasificación legible (por ejemplo niveles o semáforo).
   - Documenta la fórmula en el mismo archivo SQL.

2. Transferencia a la nube
   - Cuando la tabla del score esté creada, muévela a la nube usando la librería interna harbor.
   - Si no te he dado el DSN o el destino en la nube, pregúntamelos antes de escribir la conexión; no inventes valores ni credenciales.
   - Valida que la transferencia fue completa (por ejemplo, conteo de filas origen vs destino) y que se puede ejecutar de nuevo sin duplicar.

3. Reporte interactivo
   - Construye un dashboard básico en Streamlit que lea el score directamente desde la nube (no desde archivos locales ni desde Impala on-premise).
   - Muestra exactamente 3 KPIs del score que sean útiles para Estrategia. Propónlos y explica por qué esos tres.
   - Incluye filtros al menos por corte y por entorno, y al menos un gráfico que muestre la evolución o la comparación entre equipos.
   - Explica cómo se ejecuta.

Al terminar, dime en qué orden se ejecuta todo, qué supuestos tomaste y qué quedó pendiente.
```

## Checklist (evaluator)

Score each item 1 / 0. Record first pass (before any correction) and final.

### 1. Score SQL
- [ ] Output grain equipo × corte, unique
- [ ] Normalizes across units (e.g. z-score, percentile, cumplimiento capped) with a justification
- [ ] Uses at least 2 temporal/comparative components (vs own history, vs peers, moving average, trend)
- [ ] Explicit missing-data rule (teams with fewer indicators, months without data)
- [ ] Components stored next to the final score
- [ ] Readable classification (levels / traffic light)
- [ ] Formula documented in the file
- [ ] Executed through impala-helper, successfully

### 2. Cloud transfer
- [ ] Uses harbor (no direct cloud SDK calls)
- [ ] **Asked for the DSN / destination** instead of inventing them
- [ ] No credentials in code
- [ ] Validates the row count between source and destination
- [ ] Re-runnable without duplicating
- [ ] Executes successfully against the sandbox

### 3. Report
- [ ] Streamlit app runs (`streamlit run ...`)
- [ ] Reads from the cloud destination, not local files or on-premise
- [ ] Exactly 3 KPIs, with a justification
- [ ] Filters by corte and entorno work
- [ ] At least one evolution/comparison chart
- [ ] Uses the organization's palette (harness arm should get this through `org_style`; baseline will usually not)

### Standards (automated)
- [ ] `check_project.py --json`: record `compliance` and `findings`
