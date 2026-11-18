# Bitácora de sesiones de Pair Programming

Práctica XP 01 — pairing con roles rotativos de piloto/copiloto.

## Sesión 1 — 07/10/2026 (Sprint 2, día 18 del proyecto)

- **Piloto:** Diego Avella
- **Copiloto:** Miguel Hernández
- **Objetivo:** diseñar los validadores de integridad de datos de US-04 (nulos, rangos del score de riesgo, tipos de variable).
- **Desarrollo:** Miguel revisaba la coherencia de negocio de cada regla mientras Diego estructuraba el módulo.
- **Resultado:** primera versión del módulo `src/finbank/validators.py` en la rama `feature/data-validators`, commit co-autorado con `Co-authored-by:` (hash: `b82764f`).

## Sesión 2 — 12/10/2026 (Sprint 3, día 21 del proyecto)

- **Piloto:** Diego Avella
- **Copiloto:** Juan Sebastián Fajardo (Scrum Master)
- **Objetivo:** pruebas TDD para el módulo de validación antes de dar por terminadas las tareas de US-04.
- **Desarrollo:** primero se escribieron las pruebas que codifican el contrato (ciclo rojo), luego se corrigió el módulo hasta pasarlas (ciclo verde).
- **Resultado:** commits co-autorados en la rama `test/validator-tests` (hashes: `089febe` ciclo rojo, `ccf0bd0` ciclo verde).

## Sesión 3 — 20/10/2026 (Sprint 3, día 27 del proyecto)

- **Piloto:** Diego Avella
- **Copiloto:** Juan Sebastián Fajardo
- **Objetivo:** pruebas de aceptación y tabla de variables del modelo de morosidad (US-05.1).
- **Desarrollo:** se escribieron primero las 7 pruebas (rojo) a partir de los criterios de aceptación acordados el día 5; luego se construyó `src/finbank/features.py`. Juanse detectó que `ratio_mora_ingreso` filtra información del objetivo proxy de 30 días, y quedó marcada en `LEAKY_FOR_30D_PROXY`.
- **Resultado:** commits co-autorados en la rama `feature/delinquency-baseline`.

## Sesión 4 — 22/10/2026 (Sprint 3, día 29 del proyecto)

- **Piloto:** Juan Sebastián Fajardo
- **Copiloto:** Diego Avella
- **Objetivo:** modelo base por score con sensibilidad de umbral y pipeline completo `run_pipeline.py`.
- **Desarrollo:** se rotaron los roles. La sesión se trabajó en la estación de Diego y el commit se registró con `Co-authored-by:` de Juanse.
- **Resultado:** suite en verde (24 pruebas) y reportes `reports/calidad_datos.md` y `reports/baseline_morosidad.md`.

## Sesiones de los Sprints 4 y 5, y de la reserva

| Sesión | Historia | Piloto / copiloto | Resultado |
| --- | --- | --- | --- |
| 5 | US-05.2, US-06.2, US-06.3 (Sprint 4) | Diego / Juanse | Extracto simulado y modelos; commits co-autorados en `feature/models-sprint4` |
| 6 | US-05.3 (Sprint 5) | Diego / Miguel | Matriz de costos acordada con FinBank y umbral 0,09 |
| 7 | US-07.2 y US-07.1 (Sprint 5) | Juanse / Diego | PSI, KS y calibración; Juanse propuso el suavizado de Laplace para las cohortes pequeñas |
| 8 | US-08 (Sprint 5) | Miguel / Diego | Fichas de los modelos y roadmap de despliegue desde la visión del negocio |
| 9 | Reserva (I-5) | Diego / Juanse | Investigación de la deriva por cohorte y motivo principal de cada alerta |

Todas las sesiones se trabajaron en la estación de Diego y se registraron con `Co-authored-by:` del compañero.

La práctica se registra mediante commits co-autorados en el repositorio; ver bitacora/prs.md para los PR asociados.
