# Sprint 3 — Sprint Backlog y criterios de aceptación

| Dato | Valor |
| --- | --- |
| Sprint | 3 (semanas 5–6 del proyecto) |
| Fechas | 12/10/2026 – 23/10/2026 (días 21–30 del proyecto, 10 días hábiles) |
| Sprint Planning | 12/10/2026, primera vez con planning poker (escala de Fibonacci) |
| Capacidad | 3 personas × 8 h × 10 días = 240 h brutas; 170 h netas con un factor de enfoque de 70 % |
| Velocidad de referencia | 9,5 pts (promedio de los Sprints 1 y 2) |
| Compromiso | **10 pts** en 4 historias de 2 a 3 pts |

**Objetivo del Sprint:** cerrar la preparación de datos (US-04), que venía arrastrada del Sprint 2, y dejar listas las bases del modelado de morosidad (US-05) y churn (US-06) para el Sprint 4.

## Historias comprometidas

US-04 (5 pts en el Sprint 2) y las historias de modelado se partieron en piezas de 3 puntos o menos, como acordamos en la retrospectiva del Corte 2.

| ID | Historia | Pts | Responsable | Revisor | Evidencia |
| --- | --- | --- | --- | --- | --- |
| US-04.1 | Como analista de riesgo, quiero validar la integridad del conjunto de clientes contra el contrato de datos, para no modelar sobre datos corruptos | 3 | Diego (pairing con Miguel y Juanse) | Juanse / Miguel | PR #4, #7, #8; 8 pruebas |
| US-06.1 | Como gerente de retención, quiero una definición acordada de churn de clientes preferentes, para que el modelo prediga lo que el negocio necesita | 2 | Miguel | Juanse | PR #10; `docs/churn_target_definition.md` |
| US-04.2 | Como científico de datos, quiero una base analítica limpia con un reporte de calidad, para entrenar los modelos sobre registros válidos | 2 | Juanse | Diego | PR #11; 9 pruebas; `reports/calidad_datos.md` |
| US-05.1 | Como analista de riesgo, quiero las variables y un modelo base de morosidad, para tener la línea que el modelo final debe superar | 3 | Diego + Juanse (pairing) | Miguel | PR #12; 7 pruebas; `reports/baseline_morosidad.md` |

## Criterios de aceptación

**US-04.1 — Validación de integridad**
- [x] Se detectan columnas faltantes, nulos en todas las columnas, scores fuera de 300–850 (inclusive) y tipos incorrectos.
- [x] El reporte de errores tiene una forma uniforme (`type`, `column`, `message`) y no se interrumpe cuando falta una columna.
- [x] La suite TDD de 8 pruebas pasa (rojo → verde → refactor).

**US-06.1 — Definición de churn**
- [x] La población (preferentes activos), la definición de los eventos de churn y las exclusiones están aprobadas por el PO.
- [x] Las ventanas de 12 meses de observación y 3 meses de desempeño son coherentes con el Charter.
- [x] Los campos adicionales que se le piden a FinBank están documentados.

**US-04.2 — Limpieza y base analítica**
- [x] Los nulos de `saldo_mora_30d` se imputan a 0 y cada imputación queda registrada.
- [x] Se excluyen los registros que violan reglas de fila del contrato (formato e unicidad del ID, edad 18–75, score 300–850, categorías válidas).
- [x] Sobre la muestra quedan 22 de 25 registros válidos, con 1 imputación y un reporte de calidad generado automáticamente.

**US-05.1 — Variables y modelo base de morosidad**
- [x] Tabla de variables reproducible (edad, ingreso, score, banda FICO, razón mora/ingreso, segmento, actividad).
- [x] Objetivo proxy `en_mora_30d` definido. La etiqueta de 60 días queda condicionada a los datos reales.
- [x] Regla base por score evaluada con una matriz de confusión y sensibilidad de umbral (600/650/700), y pipeline completo ejecutable con `python run_pipeline.py`.

## Definition of Done (sin cambios frente al Corte 2)

1. Los 3 ítems del checklist de la tarjeta están marcados.
2. Pull Request aprobado por un integrante distinto al autor.
3. Las pruebas pasan sin fallos (`python -m pytest`).
4. La tarjeta está en la columna Done.

| Historia | Checklist 3/3 | PR aprobado por un par | Pruebas | Done |
| --- | --- | --- | --- | --- |
| US-04.1 | ✔ | ✔ (#4 Juanse, #7 y #8 Miguel) | ✔ 8/8 | ✔ día 4 |
| US-06.1 | ✔ | ✔ (#10 Juanse) | ✔ suite completa en verde | ✔ día 5 |
| US-04.2 | ✔ | ✔ (#11 Diego) | ✔ 17/17 | ✔ día 6 |
| US-05.1 | ✔ | ✔ (#12 Miguel) | ✔ 24/24 | ✔ día 9 |
