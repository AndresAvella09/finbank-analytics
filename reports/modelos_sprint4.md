# Modelos del Sprint 4 (US-05.2, US-06.2, US-06.3)

Regresión logística sobre variables estandarizadas. Desarrollo: cohortes 1-10 del extracto simulado; las cohortes 11-12 quedan reservadas para la validación fuera de tiempo (US-07).

| Modelo | Población | n | Positivos | AUC entrenamiento | AUC CV (5 pliegues) |
| --- | --- | --- | --- | --- | --- |
| Morosidad 60 días | Todos los clientes | 4156 | 258 | 0.875 | 0.871 ± 0.027 |
| Churn 3 meses | Preferentes activos | 1035 | 99 | 0.751 | 0.737 ± 0.035 |

Referencia US-05.1: la regla de solo score alcanza AUC 0.829 sobre las mismas cohortes; el modelo de morosidad la supera.

## Morosidad 60 días: peso de las variables

| Variable | Coeficiente estandarizado |
| --- | --- |
| score_riesgo | -1.168 |
| ratio_mora_ingreso | +0.603 |
| productos_activos | +0.219 |
| antiguedad_meses | -0.176 |
| edad | -0.053 |
| es_preferente | +0.050 |
| log_ingreso | -0.026 |

## Churn 3 meses: peso de las variables

| Variable | Coeficiente estandarizado |
| --- | --- |
| dias_sin_transaccion | +0.698 |
| productos_activos | -0.618 |
| saldo_bajo_ingreso | +0.359 |
| antiguedad_meses | -0.230 |
| edad | -0.104 |
| inactividad_60d | -0.056 |
| log_saldo_promedio | +0.055 |
| score_riesgo | -0.004 |
