# Registro de Pull Requests — propiedad colectiva e integración continua (práctica XP 03)

Ninguna pieza de trabajo se mezcla a `main` sin revisión de un par (feature branches + PR).

| PR | Rama | Autoría | Revisión | Contenido | Estado |
| --- | --- | --- | --- | --- | --- |
| #1 | chore/repo-setup | Diego | Aprobado y mezclado por Miguel | Estructura inicial, README, .gitignore, requirements | Mezclado |
| #4 | feature/data-validators | Diego + Miguel (pairing, sesión 1) | Revisado y mezclado por Juanse | Validadores v1 | Mezclado |
| #5 | feature/sample-data | Juanse | Aprobado por Diego, mezclado por Diego | Dataset sintético de clientes | Mezclado |
| #6 | feature/data-dictionary | Miguel | Aprobado por Diego, mezclado por Diego | Diccionario de datos (US-03) | Mezclado |
| #7 | test/validator-tests | Diego + Juanse (pairing, sesión 2) | Revisa Miguel | Pruebas TDD (ciclo rojo→verde) | Mezclado |
| #8 | refactor/simplify-validators | Juanse | Revisa Miguel | Refactorización Simple Design | Mezclado |
| #9 | docs/bitacora | Diego | Revisa Juanse | Bitácora técnica de prácticas XP | Mezclado |

Nota: los PR #2 y #3 fueron abiertos por error desde la cuenta del Project Lead y cerrados de inmediato; cada autor reabrió el suyo desde su cuenta (#5 y #6) para mantener el flujo de revisión correcto.

Regla del equipo: un PR se mezcla solo tras revisión de un integrante distinto al autor del trabajo.
