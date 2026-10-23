# Sprint 3 — Bitácora de Daily Scrum

Dailies de 15 minutos facilitadas por Juan Sebastián (Scrum Master). Se registra lo que se terminó, lo que sigue y los impedimentos de cada día.

| Día (fecha) | Puntos restantes | Lo más importante | Impedimentos |
| --- | --- | --- | --- |
| 1 (12/10) | 10 | Sprint Planning con planning poker: 10 pts. Pairing Diego–Juanse: suite TDD en rojo (5 fallas) y luego en verde. Miguel arranca US-06.1 en paralelo porque no depende de US-04. | Ninguno |
| 2 (13/10) | 10 | Juanse refactoriza los validadores (Simple Design). Miguel arma el borrador de la definición de churn. | Ninguno |
| 3 (14/10) | 10 | Se mezclan los PR #1, #5 y #6. Miguel valida con el PO las ventanas de observación y desempeño. | Ninguno |
| 4 (15/10) | 7 | Se mezclan los PR #4, #8 y #9: **US-04.1 Done**. | `appgmac.py` (demo del Sprint Review) entró directo a `main` desde la interfaz web, sin PR (commit `99f3e42`). |
| 5 (16/10) | 5 | **US-06.1 Done** (PR #10). Se acuerda integrar el demo al flujo de PR dentro de US-04.2. Juanse escribe las pruebas de limpieza (rojo). Se acuerdan los criterios de aceptación de US-05.1 para poder diseñarla antes de que cierre US-04.2. | FinBank no entrega el extracto real: faltan la historia de mora a 60 días y la fecha de cancelación. El PO lo escala. Mientras tanto se sigue con los datos sintéticos. |
| 6 (19/10) | 3 | **US-04.2 Done** (PR #11, revisado por Diego). El demo ya reutiliza el módulo de limpieza. US-04 cierra el día 26 del proyecto (baseline: día 25). | Desvío de +1 día sobre la ruta crítica |
| 7 (20/10) | 3 | Pairing Diego–Juanse: pruebas de US-05.1 en rojo y tabla de variables. | Ninguno |
| 8 (21/10) | 3 | Las variables pasan a verde. Miguel prepara la solicitud formal de campos a FinBank. | Ninguno |
| 9 (22/10) | 0 | Modelo base por score y pipeline completo. **US-05.1 Done** (PR #12, revisado por Miguel). | Ninguno |
| 10 (23/10) | 0 | Sprint Review con el PO y Retrospectiva. PR #13 con la bitácora del Sprint. | — |

## Registro de impedimentos

| # | Impedimento | Tipo | Detectado | Acción | Resuelto | Impacto |
| --- | --- | --- | --- | --- | --- | --- |
| I-1 | Subida directa a `main` sin revisión (`appgmac.py`) | Proceso (DoD) | Día 4 | Revisión a posteriori; el demo se refactoriza y entra por PR (#11); se acuerda proteger la rama `main` | Día 6 | Sin retraso; incumplimiento puntual de la regla de PR |
| I-2 | FinBank no entrega el extracto real (mora a 60 d y fecha de cancelación) | Externo (riesgo de datos del Charter) | Día 5 | El PO escala; se trabaja con los datos sintéticos y el contrato de US-03; se envía la lista de campos (US-06.1) | Abierto → Sprint 4 | +1 día en US-04.2; US-05.1 queda como modelo base |
| I-3 | US-05.1 depende de la base limpia de US-04.2 | Dependencia | Día 5 | Criterios de aceptación acordados antes; las pruebas y el diseño de variables arrancan el día 7 sobre el contrato | Día 7 | Ninguno |
