# Sprint 5 (sprint final) — Sprint Backlog y criterios de aceptación

| Dato | Valor |
| --- | --- |
| Sprint | 5, el último con trabajo del backlog (semanas 9–10 del proyecto) |
| Días del proyecto | 41–50 (10 días hábiles) |
| Sprint Planning | Día 41, con planning poker (escala de Fibonacci) |
| Capacidad | 3 personas × 8 h × 10 días = 240 h brutas; 170 h netas con un factor de enfoque de 70 % |
| Velocidad de referencia | 9,5 pts (promedio de los Sprints 1 a 4) |
| Compromiso | **10 pts** en 4 historias de 2 a 3 pts: todo el backlog restante |

**Objetivo del Sprint:** validar fuera de tiempo los dos modelos, fijar con FinBank el umbral de alerta y entregar el sistema con su roadmap de despliegue.

## Historias comprometidas

| ID | Historia | Pts | Pairing | Revisor (Approve) | Evidencia |
| --- | --- | --- | --- | --- | --- |
| US-05.3 | Como gerente de riesgo, quiero un umbral de alerta basado en el costo de cada error y en la capacidad de cobranza, para gestionar solo lo que el equipo puede atender | 2 | Diego + Miguel | Juanse | PR #16; `reports/umbral_morosidad.md` |
| US-07.2 | Como gerente de clientes preferentes, quiero saber si el modelo de churn funciona en meses que no vio, para confiar en la campaña de retención | 2 | Diego + Juanse | Miguel | PR #17; `reports/validacion_churn.md` |
| US-07.1 | Como comité de riesgo, quiero validar el modelo de morosidad fuera de tiempo, para aprobar su uso | 3 | Diego + Juanse | Miguel | PR #18; `reports/validacion_morosidad.md` |
| US-08 | Como FinBank, quiero la lista de alertas, las fichas de los modelos y el roadmap de despliegue, para pasar a producción | 3 | Diego + Miguel | Juanse | PR #19; `docs/entrega/` |

## Criterios de aceptación

**US-05.3 — Umbral por costo**
- [x] El costo del falso negativo (COP 950.000) y el del falso positivo (COP 85.000) están acordados con FinBank.
- [x] El umbral se elige sobre predicciones fuera de pliegue de las cohortes de desarrollo y respeta el tope de 15 % de alertas.
- [x] Resultado reproducible: umbral 0,09, 13,9 % de alertas y 53,4 % menos costo esperado que sin modelo.

**US-07.2 — Validación del modelo de churn**
- [x] AUC fuera de tiempo ≥ 0,70 en cada cohorte (resultado: 0,799 y 0,774).
- [x] Lift ≥ 2 en el 20 % de mayor riesgo (resultado: 2,5).
- [x] PSI calculado por variable y por cohorte, con los cambios documentados (I-5).

**US-07.1 — Validación del modelo de morosidad**
- [x] AUC fuera de tiempo ≥ 0,80 y mejor que la regla de solo score (resultado: 0,855 frente a 0,822).
- [x] Calibración por quintil con brecha menor a 5 puntos y PSI del puntaje < 0,10 (resultado: 0,012).
- [x] El umbral acordado se sostiene fuera de tiempo: 13,6 % de alertas y 61,5 % de morosos detectados.

**US-08 — Entrega final**
- [x] Lista de alertas priorizada de la última cohorte dentro de la capacidad de gestión (62 de mora y 24 de retención).
- [x] Fichas de los dos modelos con su desempeño, limitaciones, monitoreo y dueño.
- [x] Roadmap de despliegue con fases, criterios para avanzar, gobierno y riesgos.

## Definition of Done

1. Los 3 ítems del checklist de la tarjeta están marcados.
2. Pull Request revisado, **aprobado (Approve)** y mezclado por un integrante distinto a los autores. Desde el Sprint 4, `main` está protegida y no permite mezclar sin 1 aprobación.
3. Las pruebas pasan sin fallos (`python -m pytest`).
4. La tarjeta está en la columna Done.

| Historia | Checklist 3/3 | PR aprobado y mezclado por un par | Pruebas | Done |
| --- | --- | --- | --- | --- |
| US-05.3 | ✔ | ✔ #16 (Juanse) | ✔ 35/35 | ✔ día 2 |
| US-07.2 | ✔ | ✔ #17 (Miguel) | ✔ 40/40 | ✔ día 4 |
| US-07.1 | ✔ | ✔ #18 (Miguel) | ✔ 45/45 | ✔ día 6 |
| US-08 | ✔ | ✔ #19 (Juanse) | ✔ 49/49 | ✔ día 9 |
