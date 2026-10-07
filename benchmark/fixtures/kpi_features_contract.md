# kpi_features

Una fila por equipo × indicador × corte.

| Columna | Tipo | Descripción |
|---|---|---|
| codigo_equ | STRING | Código del equipo |
| equipo | STRING | Nombre del equipo |
| codigo_entorno | STRING | Código del entorno; marcado explícitamente cuando el equipo no tiene entorno |
| entorno | STRING | Nombre del entorno |
| frente | STRING | Frente del indicador (normalizado) |
| indicador | STRING | Nombre del indicador (normalizado) |
| unidad | STRING | Porcentaje, cantidad o escala |
| corte | INT | Periodo AAAAMM |
| fecha_corte | DATE | Primer día del periodo |
| resultado | DOUBLE | Valor medido |
| meta | DOUBLE | Meta del periodo |
| cumplimiento | DOUBLE | Cumplimiento validado |

<!-- TODO(content): add the extra feature columns of the reference table built from the pilot. -->
