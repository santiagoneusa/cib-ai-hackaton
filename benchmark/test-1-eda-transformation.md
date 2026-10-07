# Test 1 - EDA and transformation

**Starting state:** workspace with only `input/KPIS_historico.xlsx` (plus `.github/` in the harness arm). New chat, Agent mode.

**Paste exactly the prompt below.** Do not add context or hints.

## Prompt

```text
Contexto
Eres parte del equipo de analítica de CIB. El área de Estrategia Corporativa hace seguimiento mensual a sus equipos (EQU) mediante KPIs agrupados por frentes. El histórico está consolidado en el archivo input/KPIS_historico.xlsx y hay dudas sobre si los números reflejan la realidad. Necesitamos una base confiable en Impala (on-premise) que luego se usará para construir un score de desempeño por equipo.

El archivo tiene tres hojas:
- query: Frente, Corte, Codigo_EQU, EQU, Indicador, Resultado, Meta, Cumplimiento.
- catalogo_indicadores: Frente, Indicador, definición (qué mide y para qué) y Unidad.
- catalogo_entornos: Codigo_EQU, Tipo, EQU, Codigo_Padre y Nombre_Padre (entorno al que pertenece cada equipo vigente hoy).
Los catálogos son la documentación oficial, pero no asumas que están completos ni que coinciden con los datos: valídalos.

Construye lo siguiente, en este orden:

1. Notebook de análisis inicial
   - Explica qué representa cada fila de la hoja query y qué columnas la identifican (llave natural).
   - Perfila los datos: tipos, nulos, duplicados (exactos y por llave), rangos y valores atípicos, cobertura por corte, frente e indicador.
   - Contrasta la base con ambos catálogos: indicadores sin catálogo o con nombres distintos, equipos sin entorno, frentes inconsistentes, diferencias de nombres para un mismo código.
   - Verifica si Cumplimiento es coherente con Resultado y Meta.
   - Termina con un registro de problemas de calidad: problema, evidencia cuantificada, impacto potencial y tratamiento propuesto (corregir, excluir, marcar o aceptar).
   - Incluye gráficos solo donde aporten a entender un problema.
   - El notebook debe ejecutarse de principio a fin sin pasos manuales.

2. Script de carga a Impala
   - Lee las tres hojas del Excel y cárgalas sin transformar como tablas crudas en Impala on-premise usando la librería interna impala-helper.
   - Agrega metadatos de carga (fecha de carga y archivo origen).
   - Debe poder ejecutarse de nuevo sin duplicar datos.
   - La conexión es por DSN. Si no te lo he dado, pregúntamelo antes de escribir la conexión; no inventes valores ni credenciales.

3. SQL de limpieza
   - A partir de las tablas crudas, crea las tablas limpias aplicando el tratamiento decidido en el registro de calidad: duplicados, normalización de textos y nombres, tipos de datos (por ejemplo el corte como fecha), nulos, columnas o registros sin información útil y valores incoherentes.
   - Sé propositivo: propón las reglas que consideres necesarias y justifica cada una con la evidencia del notebook.
   - Deja trazabilidad de lo que excluyes o corriges (por ejemplo una tabla de rechazos o columnas de marca con el motivo).

4. SQL de la tabla de features
   - Crea la tabla kpi_features con granularidad equipo × indicador × corte, que será el insumo de un score de desempeño por equipo en otra tarea.
   - Debe tener como mínimo estas columnas: codigo_equ, equipo, codigo_entorno, entorno, frente, indicador, unidad, corte (AAAAMM, entero), fecha_corte (fecha), resultado, meta, cumplimiento.
   - Los equipos sin entorno deben quedar identificados explícitamente, no descartados.
   - Propón features adicionales útiles para comparar equipos en el tiempo y justifícalas.

Al terminar, dime en qué orden se ejecuta todo, qué supuestos tomaste y qué quedó pendiente.
```

## Checklist (evaluator)

Score each item 1 / 0. Record first pass (before any correction) and final.

### 1. EDA notebook
- [ ] Identifies the grain and natural key (Codigo_EQU × Indicador × Corte, possibly Frente)
- [ ] Quantifies exact duplicates (2,182) and key duplicates
- [ ] Quantifies nulls per column (e.g. EQU 6,185; Resultado 462; Meta 308; Cumplimiento 265; Codigo_EQU 36)
- [ ] Detects the frente typo "Modeos de trabajo y Agilidad" vs "Modelos de trabajo y Agilidad"
- [ ] Detects indicators missing from catalogo_indicadores (the data has far more indicators than the 13 in the catalog)
- [ ] Detects teams without an entorno / not in catalogo_entornos, and the "CdE sin Entorno" value
- [ ] Detects out-of-range Cumplimiento (min ≈ -1,873, max ≈ 155) and checks it against Resultado/Meta
- [ ] Quality register with problem, quantified evidence, impact and treatment
- [ ] Runs top to bottom

### 2. Upload script
- [ ] Uses impala-helper (no raw connections or other drivers)
- [ ] **Asked for the DSN** instead of inventing it
- [ ] No credentials in code
- [ ] Loads the 3 sheets with load metadata
- [ ] Re-runnable without duplicating (overwrite/partition/truncate strategy)
- [ ] Executes successfully against the sandbox

### 3. Cleaning SQL
- [ ] Deduplicates with an explicit rule
- [ ] Normalizes frente/indicator/team names
- [ ] Casts corte to a date
- [ ] Explicit null and incoherent-value treatment
- [ ] Each rule justified in comments
- [ ] Traceability of excluded/corrected rows
- [ ] Executes successfully

### 4. Feature SQL
- [ ] `kpi_features` exists with the minimum contract columns and types
- [ ] Grain equipo × indicador × corte is unique (verify with a COUNT/GROUP BY)
- [ ] Teams without entorno flagged, not dropped
- [ ] At least 2 justified extra features
- [ ] Executes successfully

### Standards (automated)
- [ ] `python .github/skills/standards-check/scripts/check_project.py --json` (use the copy from the bundle repo for the baseline arm). Record `compliance` and `findings` in results.csv.
