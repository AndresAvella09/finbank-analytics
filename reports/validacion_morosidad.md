# Validación fuera de tiempo del modelo de morosidad (US-07.1)

Modelo entrenado con las cohortes 1-10 y evaluado sobre las cohortes 11-12, que no vio en el entrenamiento.

| Métrica | Valor |
| --- | --- |
| Clientes fuera de tiempo / morosos a 60 días | 844 / 52 |
| AUC fuera de tiempo | 0.855 (regla de solo score: 0.822) |
| Gini | 0.709 |
| KS | 0.540 |
| Brier | 0.0446 |
| PSI del puntaje | 0.012 (estable) |
| Umbral acordado (US-05.3) | 0.09 |
| Tasa de alertas fuera de tiempo | 13.6% |
| Morosos detectados | 32 de 52 (61.5%) |
| Ahorro de costo esperado frente a no usar modelo | 47.3% |

## Calibración por quintil de riesgo

| Quintil | Clientes | Tasa predicha | Tasa observada |
| --- | --- | --- | --- |
| 1 | 169 | 0.005 | 0.000 |
| 2 | 169 | 0.011 | 0.012 |
| 3 | 168 | 0.022 | 0.036 |
| 4 | 169 | 0.043 | 0.053 |
| 5 | 169 | 0.214 | 0.207 |

## Estabilidad de las variables (PSI)

| Variable | PSI | Estado |
| --- | --- | --- |
| ratio_mora_ingreso | 0.146 | monitorear |
| score_riesgo | 0.017 | estable |
| productos_activos | 0.010 | estable |
| antiguedad_meses | 0.009 | estable |
| log_ingreso | 0.006 | estable |
| edad | 0.006 | estable |
| es_preferente | 0.001 | estable |

Lectura: el modelo mantiene su capacidad de discriminación fuera de tiempo, está calibrado por quintiles y el umbral acordado respeta la capacidad de cobranza. La razón mora/ingreso queda en monitoreo (PSI entre 0,10 y 0,25).
