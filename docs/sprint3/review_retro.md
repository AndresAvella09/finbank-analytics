# Sprint 3 — Sprint Review y Retrospectiva

Fecha: 23/10/2026 (día 30 del proyecto). Asistentes: Diego Avella (PO), Miguel Hernández y Juan Sebastián Fajardo (SM, facilitador).

## Sprint Review

| Métrica | Sprint 1 | Sprint 2 | Sprint 3 |
| --- | --- | --- | --- |
| Comprometido | 11 | 16 | 10 |
| Completado (velocidad) | 8 | 11 | 10 |
| Cumplimiento | 73 % | 69 % | 100 % |
| Historias Done / comprometidas | 2/3 | 3/4 | 4/4 |
| Pts cerrados en la semana 1 | 0 | 0 | 5 |

Velocidad promedio de los 3 Sprints: **9,67 pts**.

El incremento que se mostró al PO fue el pipeline completo (`python run_pipeline.py`): validación → limpieza (22 de 25 registros válidos) → variables → modelo base de morosidad, más la definición de churn y el demo `appgmac.py`, que ya usa el módulo de limpieza. La suite tiene 24 pruebas en verde.

El PO aceptó las 4 historias. US-04 (tarea D del Charter) cierra el día 26 frente al día 25 de la línea base, así que el desvío acumulado en la ruta crítica es de 1 día y quedan 9 de los 10 días de contingencia.

## Cumplimiento de los acuerdos de la retrospectiva anterior

| Acuerdo (Corte 2) | Resultado en el Sprint 3 |
| --- | --- |
| Comprometer entre 9 y 10 pts | Cumplido: 10 pts |
| Historias de 3 pts o menos | Cumplido: 4 historias de 2–3 pts |
| Incluir el arrastre de US-04 | Cumplido: US-04.1 y US-04.2 Done |
| Planning poker | Cumplido desde el Sprint Planning del día 1 |
| Arrancar en paralelo con criterios de aceptación acordados | Cumplido: US-06.1 desde el día 1; diseño de US-05.1 antes de que cerrara US-04.2 |
| Commits co-autorados | Cumplido: pairing con `Co-authored-by:` en US-04.1 y US-05.1 |
| No concentrar cierres en la semana 2 | Cumplido: 5 de 10 pts cerrados en la semana 1 (0 en los Sprints 1 y 2) |
| Plan alterno ante esperas | Cumplido: se siguió con datos sintéticos mientras llega el extracto real |

## Retrospectiva

**Start (empezar a hacer)**
- Proteger la rama `main` con al menos 1 aprobación obligatoria, para que la regla de PR no dependa de la disciplina.
- Pedir los datos al cliente con un Sprint de anticipación, con la lista de campos y una fecha comprometida.
- Registrar los impedimentos externos en el tablero con su fecha de escalamiento.

**Stop (dejar de hacer)**
- Subir archivos a `main` desde la interfaz web.
- Dejar la actualización de la bitácora para el último día del Sprint.

**Continue (seguir haciendo)**
- Comprometer según la velocidad real y mantener historias de 3 pts o menos.
- TDD rojo → verde → refactor, pairing con co-autoría y revisión rotativa entre los tres.
- Dailies cortas con un registro explícito de impedimentos.

**Acción prioritaria para el Sprint 4:** comprometer entre 9 y 10 pts con US-05.2 (modelo de morosidad sobre los datos reales) y US-06.2 (variables de churn), condicionados a que FinBank entregue el extracto (I-2) al inicio del Sprint 4 (día 31).
