# Ficha del modelo — Morosidad temprana a 60 días

| Campo | Detalle |
| --- | --- |
| Propósito | Anticipar qué clientes caerán en mora a 60 días, para gestionarlos de forma preventiva |
| Historias | US-05.1 (modelo base), US-05.2 (modelo), US-05.3 (umbral), US-07.1 (validación) |
| Población | Todos los clientes activos de la cartera en la fecha de corte |
| Variable objetivo | `mora_60d`: 1 si el cliente registra mora a 60 días después de la fecha de corte |
| Variables | Edad, log del ingreso, score de riesgo, razón mora/ingreso a la fecha de corte, segmento preferente, antigüedad y productos activos |
| Técnica | Regresión logística sobre variables estandarizadas (`src/finbank/models.py`) |
| Datos | Extracto de FinBank (simulado con el mismo contrato de datos): cohortes 1–10 para desarrollo, 11–12 para validación fuera de tiempo |
| Umbral | 0,09 de probabilidad: mínimo costo esperado (falso negativo COP 950.000, falso positivo COP 85.000) con un tope de 15 % de la cartera en alerta |

## Desempeño

| Métrica | Desarrollo (CV) | Fuera de tiempo |
| --- | --- | --- |
| AUC | 0,871 | 0,855 |
| Regla de solo score (referencia) | 0,829 | 0,822 |
| Gini / KS | — | 0,709 / 0,540 |
| Tasa de alertas con el umbral | 13,9 % | 13,6 % |
| Morosos detectados | 67,4 % | 61,5 % |
| Reducción del costo esperado | 53,4 % | 47,3 % |
| PSI del puntaje | — | 0,012 (estable) |

## Variables con más peso

El score de riesgo (a menor score, mayor riesgo) y la razón mora/ingreso a la fecha de corte explican la mayor parte del puntaje. Siguen los productos activos y la antigüedad (a más antigüedad, menor riesgo).

## Limitaciones y uso

- Se entrenó con un extracto simulado. Antes del piloto se debe reentrenar con los datos productivos de FinBank y repetir la validación de `run_models.py`.
- La razón mora/ingreso quedó en monitoreo (PSI 0,146).
- El modelo prioriza la gestión preventiva. No reemplaza la política de crédito ni las decisiones de otorgamiento.

**Monitoreo:** PSI mensual del puntaje y de las variables (alerta en 0,10), y recall y tasa de alertas por cohorte. **Dueño del modelo:** Gerencia de Riesgo de FinBank.
