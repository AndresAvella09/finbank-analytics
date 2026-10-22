# Modelo base de morosidad temprana (US-05.1)

Regla de referencia: `score_riesgo < umbral` => cliente en riesgo. Objetivo proxy: `en_mora_30d` (saldo en mora a 30 días > 0).

Base analítica: 22 clientes válidos, 3 con mora a 30 días.

| Umbral | TP | FP | FN | TN | Precisión | Recall | F1 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 600 | 0 | 6 | 3 | 13 | 0.000 | 0.000 | 0.000 |
| 650 | 1 | 8 | 2 | 11 | 0.111 | 0.333 | 0.167 |
| 700 | 2 | 9 | 1 | 10 | 0.182 | 0.667 | 0.286 |

Lectura: con la muestra sintética el score por sí solo separa mal a los clientes en mora; es la línea base que el modelo de US-05.2 debe superar con los extractos reales de FinBank. El umbral definitivo se acuerda con FinBank en el checkpoint de riesgo de la fase de modelado.
