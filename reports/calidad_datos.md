# Reporte de calidad de datos (US-04.2)

Fuente: `data/sample_clientes.csv`. Generado con `PYTHONPATH=src python -m finbank.cleaning`.

| Métrica | Valor |
| --- | --- |
| Registros de entrada | 25 |
| Registros válidos (pasan a modelado) | 22 |
| Registros excluidos | 3 |
| Valores imputados | 1 |

## Violaciones al contrato de datos

| cliente_id | Campo | Regla | Valor |
| --- | --- | --- | --- |
| C-0007 | score_riesgo | rango 300-850 | 287.0 |
| C-0013 | edad | no admite nulos | (vacío) |
| C-0022 | score_riesgo | no admite nulos | (vacío) |

## Imputaciones

| cliente_id | Campo | Acción |
| --- | --- | --- |
| C-0018 | saldo_mora_30d | nulo imputado a 0 |
