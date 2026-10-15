# Reporte de ejecución de pruebas — TDD (práctica XP 02)

Suite: `tests/test_validators.py` (8 pruebas unitarias, pytest). Comando: `python -m pytest -v` desde la raíz del repositorio.

El módulo se construyó con el ciclo rojo→verde de TDD: primero se escribieron las 8 pruebas que codifican el contrato de datos (diccionario de datos de US-03), dejando visible el fallo; después se corrigió el módulo hasta pasar la suite completa.

## 1. Ciclo rojo — 12/10/2026 (commit `089febe`)

Pruebas codificando el contrato contra la versión inicial del módulo: 5 fallan (los defectos que el contrato exige corregir), 3 pasan.

```text
FAILED tests/test_validators.py::test_nulls_in_all_columns_are_reported
FAILED tests/test_validators.py::test_score_range_bounds_are_inclusive
FAILED tests/test_validators.py::test_ingreso_mensual_accepts_int_and_float
FAILED tests/test_validators.py::test_missing_column_is_reported_not_crash
FAILED tests/test_validators.py::test_result_shape_is_consistent
========================= 5 failed, 3 passed in 3.87s =========================
```

## 2. Ciclo verde — 12/10/2026 (commit `ccf0bd0`)

Correcciones mínimas al módulo (nulos sobre todas las columnas, rango del score inclusivo en 300 y 850, ingreso_mensual acepta int64/float64, columnas faltantes se reportan sin interrumpir, forma de resultado uniforme): la suite completa pasa.

```text
============================== 8 passed in 2.21s ==============================
```

## 3. Verificación post-refactorización — 13/10/2026 (commit `ceaa33b`)

Tras la refactorización Simple Design (sin cambio de comportamiento), la suite se mantiene en verde:

```text
============================== 8 passed in 2.57s ==============================
```

## Conclusión

Ninguna tarea de US-04 se dio por terminada con la suite en rojo; el reporte queda registrado en esta bitácora y el historial de commits refleja el orden red→green→refactor.
