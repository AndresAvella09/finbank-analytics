# Diccionario de datos — Clientes FinBank

Artefacto de la historia de usuario US-03 (requisitos de datos), cerrada el día 17 del proyecto (06/10/2026). Define el contrato de datos que gobierna la validación del conjunto de clientes en US-04.

| Campo | Tipo | Descripción | Rango / valores | Política de nulos |
| --- | --- | --- | --- | --- |
| cliente_id | string | Identificador único del cliente | C-XXXX | No admite nulos |
| edad | int | Edad del cliente en años | 18–75 | No admite nulos |
| ingreso_mensual | int/float | Ingreso mensual declarado en COP | >= 0 | No admite nulos |
| saldo_mora_30d | float | Saldo en mora a 30 días en COP | >= 0 | Admite nulos — imputar a 0 en limpieza |
| score_riesgo | int | Score de riesgo crediticio estilo FICO | 300–850 inclusive | No admite nulos |
| tipo_cliente | string | Segmento del cliente | 'preferente' o 'regular' | No admite nulos |
| activo | string | Indicador de cliente activo | 'si' o 'no' | No admite nulos |

Fuente: datos sintéticos de ejemplo para el pipeline de validación; los datos reales de FinBank se procesan bajo el mismo contrato.
