# Caso de refactorización — Simple Design & Refactoring (práctica XP 04)

## Contexto

Tras el ciclo verde de TDD, el módulo de validadores pasaba las pruebas pero acumulaba deuda técnica. Se refactorizó en la rama `refactor/simplify-validators` sin cambiar comportamiento: las pruebas permanecieron en verde antes y después del cambio.

## Antes (`b82764f`, rama feature/data-validators)

```python
# null check over the columns we care about
for col in ['cliente_id', 'edad', 'ingreso_mensual', 'saldo_mora_30d', 'score_riesgo']:
    n = df[col].isnull().sum()
    if n > 0:
        errores.append('nulos en ' + col + ': ' + str(n))

# score range check
fuera = df[(df['score_riesgo'] < 300) | (df['score_riesgo'] >= 850)]
```

Problemas de la versión inicial:

- Función monolítica que mezcla tres responsabilidades (nulos, rango del score, tipos de variable).
- Literales `300`/`850` duplicados en el código.
- Chequeo de nulos limitado a una lista fija de columnas (deja pasar nulos en columnas no listadas).
- Límite superior del rango con `>= 850` (marca un score de 850, que es válido, como fuera de rango).
- `KeyError` sin controlar si falta una columna del contrato.
- Tipo de retorno inconsistente (listas de strings y enteros mezclados).
- Sin type hints.

## Después (`ceaa33b`, rama refactor/simplify-validators)

- Cuatro funciones de una sola responsabilidad: `check_missing_columns(df) -> list[dict]`, `check_nulls(df) -> list[dict]`, `check_score_range(df, min_score=300, max_score=850) -> list[dict]` y `check_variable_types(df, expected_types=EXPECTED_TYPES) -> list[dict]`.
- Constantes de módulo `SCORE_MIN = 300` y `SCORE_MAX = 850` (un único punto de configuración del rango), además de `REQUIRED_COLUMNS` y `EXPECTED_TYPES` como contrato declarativo.
- Type hints en todas las firmas y helper interno `_issue()` que garantiza la forma uniforme de cada reporte.
- Orquestador `validate_dataset(df) -> dict` que consolida los resultados en una forma uniforme: lista de dicts con claves `'type'`, `'column'` y `'message'`. Las columnas ausentes del contrato se reportan (`check_missing_columns`) en lugar de lanzar excepciones.

## Por qué

Principio de diseño simple de XP: la solución más simple que cumple el contrato, sin duplicación, fácil de extender con nuevas reglas de validación.

## Verificación

La batería de pruebas (8 tests) permanece en verde antes y después del cambio; ver bitacora/pruebas.md.
