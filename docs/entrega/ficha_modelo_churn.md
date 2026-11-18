# Ficha del modelo — Churn de clientes preferentes a 3 meses

| Campo | Detalle |
| --- | --- |
| Propósito | Anticipar con 3 meses de anticipación qué clientes preferentes se irán, para activar campañas de retención |
| Historias | US-06.1 (definición), US-06.2 (variables), US-06.3 (modelo), US-07.2 (validación) |
| Población | Clientes preferentes activos con 6 o más meses de antigüedad (`docs/churn_target_definition.md`) |
| Variable objetivo | `churn_3m`: cancelación voluntaria, 60 días de inactividad o fuga de saldo mayor a 80 % en los 3 meses siguientes |
| Variables | Edad, antigüedad, productos activos, log del saldo promedio, días sin transacción, inactividad de 60 días, saldo menor al ingreso y score |
| Técnica | Regresión logística sobre variables estandarizadas (`src/finbank/models.py`) |
| Datos | Extracto de FinBank (simulado): cohortes 1–10 para desarrollo, 11–12 para validación fuera de tiempo |
| Regla de alerta | El 20 % de los preferentes con mayor probabilidad (capacidad de la campaña de retención) |

## Desempeño

| Métrica | Desarrollo (CV) | Fuera de tiempo |
| --- | --- | --- |
| AUC | 0,737 | 0,786 (cohorte 11: 0,799; cohorte 12: 0,774) |
| Churn capturado en el 20 % de mayor riesgo | — | 50 % (lift 2,5) |
| PSI del puntaje | — | 0,231 (monitorear) |

## Hallazgo de estabilidad (impedimento I-5)

`dias_sin_transaccion` cambió en la cohorte 12: su PSI es 1,91, frente a 0,06 en la cohorte 11. El modelo sigue discriminando, pero el nivel de las probabilidades se desplaza. Por eso se recalibra con las cohortes recientes antes de desplegar (ver `docs/cierre/acta_cierre.md`).

## Limitaciones y uso

- Se entrenó con un extracto simulado y la muestra de churn es pequeña (99 casos en desarrollo). Hay que reentrenar con los datos productivos.
- La variable de inactividad es sensible a cambios en el registro de transacciones digitales. Cualquier cambio de canal debe avisarse al equipo de datos.

**Monitoreo:** PSI mensual (alerta en 0,10) y churn capturado por la campaña. **Dueño del modelo:** Gerencia de Clientes Preferentes de FinBank.
