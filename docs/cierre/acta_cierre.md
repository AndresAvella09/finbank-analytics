# Acta de cierre del proyecto

**Proyecto:** Sistema predictivo de morosidad temprana y churn — FinBank S.A.
**Consultor:** DMS Consulting (Diego Avella, Miguel Hernández, Juan Sebastián Fajardo)
**Cierre:** día 56 del proyecto (semana 12 de 12)

## 1. Entregables aceptados

| Entregable | Historias | Evidencia |
| --- | --- | --- |
| Diagnóstico, gobernanza y Charter aprobado | US-01, US-02 | Corte 1 |
| Tablero ágil y backlog | US-09 | Tablero del proyecto |
| Contrato de datos, validación y limpieza | US-03, US-04 | PR #4 a #11 |
| Arquitectura de la solución | US-10 | Corte 2 |
| Modelo de morosidad a 60 días con umbral por costo | US-05.1 a US-05.3 | PR #12, #15, #16 |
| Definición y modelo de churn a 3 meses | US-06.1 a US-06.3 | PR #10, #15 |
| Validación fuera de tiempo de los dos modelos | US-07.1, US-07.2 | PR #17, #18 |
| Lista de alertas, fichas de los modelos y roadmap de despliegue | US-08 | PR #19, #20 |
| Presentación ejecutiva a FinBank (tarea K) | — | Día 56 |

## 2. Cronograma

| | Línea base (Charter) | Real |
| --- | --- | --- |
| Tareas A–H (trabajo) | Días 1–50 | Días 1–49 |
| Reserva de contingencia (tarea L) | Días 51–60 (10 días) | 6 días usados (51–56) |
| Cierre | Semana 12 | Día 56, semana 12 |

Uso de la reserva: 4 días para investigar la deriva del modelo de churn (I-5) y 2 días para ajustar el reporte de alertas. Ambas fueron solicitudes de FinBank en la Sprint Review del Sprint 5 y corresponden a riesgos identificados en el Charter: calidad de datos y alineación con el cliente.

## 3. Presupuesto

| Concepto | Presupuesto | Ejecutado | Variación |
| --- | --- | --- | --- |
| Fase 1. Diagnóstico y gobernanza | $27,0M | $29,5M | +$2,5M |
| Fase 2. Requisitos y datos | $63,0M | $64,0M | +$1,0M |
| Fase 3. Modelado y validación | $63,0M | $61,5M | −$1,5M |
| Fase 4. Entrega (tarea H) | $9,0M | $9,3M | +$0,3M |
| Fase 4. Reserva de contingencia (tarea L) | $18,0M | $10,8M | −$7,2M |
| **Total** | **$180,0M** | **$175,1M** | **−$4,9M (−2,7 %)** |

Sin contar la reserva, el trabajo A–H costó $164,3M frente a $162,0M planeados (+1,4 %; CPI 0,986).

## 4. Pendientes que se transfieren a FinBank

- Reentrenar y validar los modelos con los datos productivos dentro de la infraestructura del banco (fase 1 del roadmap).
- Monitorear mensualmente el PSI del modelo de churn y reentrenarlo si la brecha de calibración supera 3 puntos.
- Formalizar el acuerdo de entrega de datos (campos, frecuencia y responsable).

## 5. Aceptación

El comité de FinBank acepta los entregables el día 56, con los pendientes de la sección 4 a su cargo. El proyecto queda formalmente cerrado.
