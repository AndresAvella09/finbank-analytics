# Sprint 4 — Resumen (semanas 7–8, días 31–40 del proyecto)

**Objetivo del Sprint:** entrenar los modelos de morosidad a 60 días y de churn a 3 meses sobre el extracto de FinBank.

| Historia | Pts | Responsable (pairing) | Revisor | Cierre |
| --- | --- | --- | --- | --- |
| US-06.2 Variables de churn sobre la ventana de observación | 3 | Diego + Juanse | Miguel | Día 4 (día 34) |
| US-05.2 Modelo de morosidad a 60 días | 3 | Diego + Juanse | Miguel | Día 7 (día 37) |
| US-06.3 Modelo de churn a 3 meses (preferentes activos) | 3 | Diego + Juanse | Miguel | Día 9 (día 39) |
| **Total** | **9** | | | **9/9 (100 %)** |

**Resultados** (detalle en `reports/modelos_sprint4.md`): regresión logística con partición fuera de tiempo (cohortes 1–10 para desarrollo, 11–12 reservadas para la validación del Sprint 5).

| Modelo | AUC (validación cruzada, 5 pliegues) | Referencia |
| --- | --- | --- |
| Morosidad 60 días | 0,871 ± 0,027 | Regla de solo score (US-05.1): 0,829 |
| Churn 3 meses | 0,737 ± 0,035 | Azar: 0,500 |

**Impedimento I-2 (cerrado):** el extracto llegó el día 33, 2 días después de lo solicitado. Para no detener el trabajo, el equipo armó las variables de churn sobre el contrato de datos y luego las ejecutó sobre el extracto. La tarea E (modelo de morosidad) cerró el día 37 frente al día 35 de la línea base.

**Acuerdo de la retrospectiva del Sprint 3 implementado:** desde este Sprint, la rama `main` exige 1 aprobación (Approve) para mezclar un PR.

**Velocidad:** 9 de 9 puntos. El backlog pendiente para el Sprint 5 suma 10 puntos: US-05.3, US-07.1, US-07.2 y US-08.

Nota: el extracto de FinBank se simula con `scripts/generar_extracto.py` (semilla fija), con el mismo contrato de datos del extracto real.
