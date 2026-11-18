# Definición de la variable objetivo de churn — US-06.1

Artefacto de la historia de usuario **US-06.1** (Sprint 3, cerrada el día 25 del proyecto, 16/10/2026). Define qué significa que un cliente de FinBank "se fue", sobre qué población se mide y con qué ventanas de tiempo, para que el modelado de churn (US-06.2 en adelante) arranque con criterios de aceptación acordados y no tenga que esperar a los datos reales.

Responsable: Miguel Hernández (analista de negocio). Revisión: Juan Sebastián Fajardo. Aprobación de negocio: Diego Avella (Product Owner).

## 1. Problema de negocio

FinBank pierde COP $18.200M al año por cancelaciones de clientes preferentes y hoy no tiene una alerta temprana que le permita intervenir antes de que ocurran. El Charter pide anticipar la cancelación **con tres meses de anticipación**.

## 2. Población objetivo

| Criterio | Regla |
| --- | --- |
| Segmento | Solo clientes con `tipo_cliente = 'preferente'` |
| Estado en la fecha de corte | `activo = 'si'` (no se predice churn de quien ya se fue) |
| Antigüedad mínima | 6 meses como cliente en la fecha de corte |
| Exclusiones | Clientes fallecidos, cuentas embargadas, clientes en cobro jurídico y empleados de FinBank |

Los clientes regulares quedan por fuera del alcance de US-06. Esto se acordó con el Product Owner para no ampliar el alcance sin control (riesgo de *scope creep* del Charter, sección 8).

## 3. Definición de churn

Un cliente preferente activo en la fecha de corte **t** es churn (`churn_3m = 1`) si dentro de la ventana de desempeño (t, t + 3 meses] ocurre al menos uno de estos eventos:

1. **Cancelación voluntaria** de todos sus productos de ahorro e inversión.
2. **Inactividad**: no registra transacciones iniciadas por él durante 60 días seguidos.
3. **Fuga de saldo**: el saldo promedio cae más de 80 % frente al promedio de los 6 meses anteriores a t.

Si no ocurre ninguno de los tres eventos, `churn_3m = 0`. Una cancelación por fallecimiento o una decisión del banco (cierre por riesgo o cumplimiento) **no** cuenta como churn y saca al cliente de la muestra.

## 4. Ventanas de tiempo

| Ventana | Duración | Uso |
| --- | --- | --- |
| Observación | 12 meses antes de t | Construcción de variables predictoras |
| Exclusión | 0 meses | La predicción se entrega en t, sin ventana muerta |
| Desempeño | 3 meses después de t | Etiqueta `churn_3m` |

Para entrenar se usarán varias fechas de corte mensuales (ventana deslizante), de modo que cada cliente aporta como máximo un registro por fecha de corte.

## 5. Campos adicionales requeridos a FinBank

La muestra actual (`data/sample_clientes.csv`) **no alcanza** para etiquetar churn real. A FinBank se le solicitan estos campos, que se agregarán al diccionario de datos cuando lleguen los extractos:

| Campo | Tipo | Descripción |
| --- | --- | --- |
| fecha_vinculacion | date | Fecha de apertura del primer producto |
| fecha_cancelacion | date | Fecha de cierre del último producto (nulo si sigue activo) |
| motivo_cancelacion | string | Voluntaria, fallecimiento, decisión del banco |
| productos_activos | int | Número de productos vigentes al cierre de mes |
| saldo_promedio_mes | float | Saldo promedio mensual en COP |
| ultima_transaccion | date | Fecha de la última transacción iniciada por el cliente |

## 6. Proxy para el pipeline con datos sintéticos

Mientras llegan los extractos reales, el pipeline usará un proxy **solo para pruebas técnicas, no para medir desempeño**: `churn_proxy = 1` si `activo = 'no'`. En la muestra sintética, los 8 clientes preferentes están activos, así que el proxy se calcula sobre toda la muestra (6 de 25 clientes inactivos). Este hallazgo se escaló al Product Owner como un impedimento del Sprint 3.

## 7. Criterios de aceptación de US-06.1

- [x] La definición de churn, la población y las exclusiones están documentadas y fueron aprobadas por el Product Owner.
- [x] Las ventanas de observación y desempeño son coherentes con el objetivo del Charter (anticipación de 3 meses).
- [x] La lista de campos adicionales que se le piden a FinBank es consistente con el diccionario de datos de US-03.
