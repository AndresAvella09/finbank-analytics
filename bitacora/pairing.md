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

La práctica se registra mediante commits co-autorados en el repositorio; ver bitacora/prs.md para los PR asociados.
