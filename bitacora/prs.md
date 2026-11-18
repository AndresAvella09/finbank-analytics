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
| #10 | docs/churn-target | Miguel | Revisado y mezclado por Juanse | Definición de la variable objetivo de churn (US-06.1) | Mezclado |
| #11 | feature/data-cleaning | Juanse | Revisado y mezclado por Diego | Módulo de limpieza + pruebas + reporte de calidad; demo reutiliza el módulo (US-04.2) | Mezclado |
| #12 | feature/delinquency-baseline | Diego + Juanse (pairing, sesiones 3 y 4) | Revisado y mezclado por Miguel | Variables, modelo base de morosidad y pipeline completo (US-05.1) | Mezclado |
| #13 | docs/sprint3-log | Diego | Revisado y mezclado por Miguel | Backlog, dailies, burndown, review y retro del Sprint 3; bitácora | Mezclado |
| #15 | feature/models-sprint4 | Diego + Juanse (pairing) | Aprobado (Approve) y mezclado por Miguel | Extracto simulado, modelos de morosidad y churn (Sprint 4) | Mezclado |
| #16 | feature/threshold-calibration | Diego + Miguel (pairing) | Aprobado (Approve) y mezclado por Juanse | Umbral por costo (US-05.3) | Mezclado |
| #17 | feature/churn-validation | Diego + Juanse (pairing) | Aprobado (Approve) y mezclado por Miguel | Validación fuera de tiempo del churn (US-07.2) | Mezclado |
| #18 | feature/delinquency-validation | Diego + Juanse (pairing) | Aprobado (Approve) y mezclado por Miguel | Validación fuera de tiempo de la morosidad (US-07.1) | Mezclado |
| #19 | docs/final-delivery | Diego + Miguel (pairing) | Aprobado (Approve) y mezclado por Juanse | Scoring, fichas de los modelos y roadmap (US-08) | Mezclado |
| #20 | feature/reserve-adjustments | Diego + Juanse (pairing) | Aprobado (Approve) y mezclado por Miguel | Investigación de la deriva y ajuste del reporte de alertas (reserva) | Mezclado |
| #21 | docs/sprint5-closure | Diego | Aprobado (Approve) y mezclado por Juanse | Documentación del Sprint 5, acta de cierre y bitácora | Mezclado |

Nota: los PR #2 y #3 fueron abiertos por error desde la cuenta del Project Lead y cerrados de inmediato; cada autor reabrió el suyo desde su cuenta (#5 y #6) para mantener el flujo de revisión correcto.

Desviación registrada (Sprint 3, día 4): el archivo `appgmac.py` (demo del Sprint Review) se subió directo a `main` desde la interfaz web, sin PR (commit `99f3e42`). Se detectó en la daily del día 5, se revisó a posteriori y su refactorización entró por el flujo normal en el PR #11. Acción acordada en la retrospectiva: proteger la rama `main` con 1 aprobación obligatoria.

Nota sobre el registro de revisiones (Sprint 3): en los PR #10 a #13 la revisión quedó como comentario del revisor y merge hecho por él (en ningún caso por el autor), pero sin la revisión formal "Approve" de GitHub. A partir de esta corrección, el revisor registra un Approve antes de mezclar, en línea con la acción de la retrospectiva de proteger `main` con 1 aprobación obligatoria.

Desde el Sprint 4, la rama `main` está protegida en GitHub: un PR no se puede mezclar sin 1 aprobación (Approve), y la aprobación se descarta si llegan commits nuevos. Los PR del Sprint 5 están apilados (cada rama parte de la anterior) y se mezclaron en orden, del #15 al #21. Revisor siempre distinto a los autores y co-autores del PR.

Regla del equipo: un PR se mezcla solo tras revisión de un integrante distinto al autor del trabajo.
