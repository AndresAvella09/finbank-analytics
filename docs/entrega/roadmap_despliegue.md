# Roadmap de despliegue — Sistema predictivo de morosidad y churn (US-08)

El Charter excluye la puesta en producción del alcance de este proyecto. Este documento entrega a FinBank la hoja de ruta para hacerla, con todo lo que se construyó en las 12 semanas como punto de partida.

## Qué se entrega

| Activo | Ubicación |
| --- | --- |
| Contrato de datos y su validación | `docs/data_dictionary.md`, `src/finbank/validators.py`, `src/finbank/cleaning.py` |
| Definición de churn | `docs/churn_target_definition.md` |
| Modelos de morosidad a 60 días y churn a 3 meses | `src/finbank/models.py` |
| Umbral de alerta por costo | `src/finbank/threshold.py`, `reports/umbral_morosidad.md` |
| Validación fuera de tiempo y estabilidad | `src/finbank/validation.py`, `reports/validacion_*.md` |
| Scoring y lista de alertas priorizada | `src/finbank/scoring.py`, `reports/alertas_cohorte_12.csv` |
| Fichas de los modelos | `docs/entrega/ficha_modelo_*.md` |
| Ejecución reproducible | `python run_pipeline.py`, `python run_models.py` y `python -m pytest` |

## Fases propuestas

| Fase | Duración estimada | Objetivo | Criterio para avanzar |
| --- | --- | --- | --- |
| 1. Reentrenamiento con datos productivos | 3 semanas | Repetir el desarrollo y la validación con el extracto real, dentro de la infraestructura de FinBank | AUC fuera de tiempo ≥ 0,80 en morosidad y ≥ 0,70 en churn; PSI < 0,10 |
| 2. Piloto controlado | 8 semanas | Aplicar las alertas en una regional, con un grupo de control sin alertas | Reducción de la mora a 60 días y del churn de preferentes frente al grupo de control |
| 3. Integración | 6 semanas | Scoring mensual automático conectado al core bancario y al CRM de cobranza y retención | Lista de alertas disponible el día 1 de cada mes, sin intervención manual |
| 4. Operación y gobierno | Continuo | Monitoreo mensual del PSI, recalibración trimestral y revisión anual en el comité de riesgo | Ningún PSI > 0,25 sin un plan de acción |

## Gobierno del modelo

- **Dueños:** Gerencia de Riesgo (modelo de morosidad) y Gerencia de Clientes Preferentes (modelo de churn).
- **Cambios de umbral:** requieren actualizar los costos y la capacidad de gestión, y volver a correr `best_threshold` con aprobación del comité de riesgo.
- **Datos:** formalizar el acuerdo de entrega de datos (campos, frecuencia y responsable), que fue el impedimento externo más costoso del proyecto (I-2).
- **Cumplimiento:** documentar los modelos según los requisitos internos y regulatorios de gestión del riesgo de crédito antes de usarlos en decisiones.

## Riesgos del despliegue

| Riesgo | Mitigación |
| --- | --- |
| Deriva de las variables de comportamiento (ya observada en la cohorte 12) | Monitoreo mensual del PSI y recalibración trimestral |
| La capacidad de cobranza no alcanza para todas las alertas | El umbral se recalcula con la capacidad real; la prioridad "mora y churn" va primero |
| Uso del puntaje en decisiones de crédito no previstas | La ficha de cada modelo limita su uso a la gestión preventiva y la retención |
