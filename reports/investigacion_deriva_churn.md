# Investigación de la deriva del modelo de churn (impedimento I-5, reserva)

Trabajo hecho en la reserva de contingencia a pedido de FinBank tras la Sprint Review del Sprint 5. Para cada cohorte se compara la inactividad con la muestra de desarrollo (PSI) y el churn predicho por el modelo con el churn observado.

| Cohorte | Clientes | Días sin transacción (promedio) | PSI inactividad | Churn predicho | Churn observado | Brecha |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 99 | 17.0 | 0.060 | 10.7% | 11.1% | -0.4% |
| 2 | 113 | 17.4 | 0.018 | 8.6% | 10.6% | -2.0% |
| 3 | 108 | 16.2 | 0.038 | 10.1% | 6.5% | +3.6% |
| 4 | 117 | 17.1 | 0.011 | 9.1% | 6.8% | +2.3% |
| 5 | 99 | 18.1 | 0.007 | 9.7% | 14.1% | -4.4% |
| 6 | 104 | 17.4 | 0.022 | 9.5% | 10.6% | -1.1% |
| 7 | 99 | 16.4 | 0.014 | 9.4% | 7.1% | +2.3% |
| 8 | 88 | 17.6 | 0.093 | 10.4% | 9.1% | +1.3% |
| 9 | 100 | 17.7 | 0.017 | 9.4% | 13.0% | -3.6% |
| 10 | 108 | 16.6 | 0.009 | 9.0% | 7.4% | +1.6% |
| 11 | 104 | 20.2 | 0.061 | 12.0% | 11.5% | +0.5% |
| 12 | 119 | 30.9 | 1.906 | 17.5% | 16.8% | +0.7% |

Conclusión: la deriva está aislada en la cohorte 12 y viene acompañada de un aumento real del churn observado, que el modelo reproduce (brecha de calibración menor a 1 punto). Es un cambio de comportamiento, no un error de datos: el modelo se mantiene sin recalibrar y queda bajo monitoreo mensual del PSI, con reentrenamiento si la brecha supera 3 puntos.
