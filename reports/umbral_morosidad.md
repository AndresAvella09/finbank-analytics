# Umbral de alerta del modelo de morosidad (US-05.3)

Acordado con FinBank en el checkpoint de umbrales. Se elige sobre las predicciones fuera de pliegue de las cohortes de desarrollo (1-10) y se valida fuera de tiempo en US-07.1.

| Supuesto de negocio | Valor |
| --- | --- |
| Costo de un falso negativo (mora no gestionada) | COP 950.000 |
| Costo de un falso positivo (contacto preventivo) | COP 85.000 |
| Capacidad del equipo de cobranza | 15% de la cartera por mes |

| Resultado | Valor |
| --- | --- |
| Umbral de probabilidad | 0.09 |
| Tasa de alertas | 13.9% |
| Morosos detectados (TP / TP+FN) | 174 / 258 |
| Costo esperado con el modelo | COP 114.225.000 |
| Costo esperado sin modelo | COP 245.100.000 |
| Ahorro | 53.4% |
