# Sprint 5 — Bitácora de Daily Scrum

| Día (día del proyecto) | Puntos restantes | Lo más importante | Impedimentos |
| --- | --- | --- | --- |
| 1 (41) | 10 | Sprint Planning: 10 pts. Checkpoint de umbrales con FinBank (riesgo del Charter). Arrancan en paralelo US-05.3 (Diego–Miguel) y US-07.2 (Diego–Juanse), porque los modelos del Sprint 4 ya estaban mezclados. | FinBank pide un umbral basado en costos y no en una métrica estadística (I-4). |
| 2 (42) | 8 | **US-05.3 Done** (PR #16, aprobado por Juanse): umbral 0,09 con 13,9 % de alertas. | I-4 resuelto con la matriz de costos, sin agregar un modelo nuevo. |
| 3 (43) | 8 | La validación de churn detecta un cambio mayor en la inactividad de la cohorte 12 (PSI 1,91). Se documenta y se decide no bloquear: el modelo sigue discriminando. | I-5: deriva de una variable de comportamiento. |
| 4 (44) | 6 | **US-07.2 Done** (PR #17, revisado por Miguel). | — |
| 5 (45) | 6 | US-07.1 en curso. Miguel arranca US-08 (fichas y roadmap) en paralelo, con los criterios de aceptación ya acordados. | — |
| 6 (46) | 3 | **US-07.1 Done** (PR #18, revisado por Miguel): AUC fuera de tiempo 0,855 y umbral validado. | — |
| 7 (47) | 3 | Scoring de la cohorte 12 y lista de alertas priorizada. | — |
| 8 (48) | 3 | El PR #19 está listo, pero con `main` protegida no se puede mezclar sin Approve y el revisor está en otra tarea. | I-6: revisión pendiente. Se agenda como primer punto del día 9. |
| 9 (49) | 0 | **US-08 Done** (PR #19, aprobado por Juanse). La tarea H cierra un día antes de la línea base. | I-6 resuelto. |
| 10 (50) | 0 | Sprint Review con FinBank: acepta los 4 incrementos con 2 solicitudes, que se cargan a la reserva. Retrospectiva final. | — |

## Registro de impedimentos

| # | Impedimento | Tipo | Detectado | Gestión | Impacto |
| --- | --- | --- | --- | --- | --- |
| I-4 | FinBank pide un umbral por costo y capacidad, no por F1 o recall | Alcance (riesgo de umbrales del Charter) | Día 1 | Matriz de costos acordada en el checkpoint; se optimiza sobre las predicciones existentes | Ninguno: US-05.3 cerró el día 2 |
| I-5 | Deriva de la inactividad en la cohorte 12 (PSI 1,91) | Calidad de datos (riesgo del Charter) | Día 3 | Se documenta en US-07.2; en la Review, FinBank pide confirmar su causa antes de desplegar | 4 días de reserva (investigación) |
| I-6 | PR #19 sin revisión con `main` protegida | Proceso | Día 8 | La revisión pasa a ser el primer punto de la daily | Ninguno: Done el día 9 |
