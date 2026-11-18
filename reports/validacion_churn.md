# Validación fuera de tiempo del modelo de churn (US-07.2)

Modelo entrenado con las cohortes 1-10 y evaluado sobre las cohortes 11-12 (preferentes activos).

| Métrica | Valor |
| --- | --- |
| Clientes fuera de tiempo / churn observados | 223 / 32 |
| AUC fuera de tiempo | 0.786 |
| AUC cohorte 11 | 0.799 |
| AUC cohorte 12 | 0.774 |
| Churn capturado en el 20 % de mayor riesgo | 50% (lift 2.5) |
| PSI del puntaje (desarrollo vs. fuera de tiempo) | 0.231 (monitorear) |

## Estabilidad de las variables (PSI)

| Variable | PSI | Estado |
| --- | --- | --- |
| dias_sin_transaccion | 0.596 | cambio mayor |
| log_saldo_promedio | 0.049 | estable |
| score_riesgo | 0.044 | estable |
| antiguedad_meses | 0.036 | estable |
| inactividad_60d | 0.033 | estable |
| productos_activos | 0.026 | estable |
| edad | 0.024 | estable |
| saldo_bajo_ingreso | 0.004 | estable |

PSI de `dias_sin_transaccion` por cohorte: cohorte 11: 0.06, cohorte 12: 1.91.

Lectura: el modelo discrimina bien fuera de tiempo, pero la inactividad de la cohorte 12 cambió (impedimento I-5). Antes de desplegar se recomienda recalibrar con las cohortes recientes y monitorear el PSI mensualmente (umbral de alerta 0,10).
