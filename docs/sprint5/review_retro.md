# Sprint 5 — Sprint Review y retrospectiva final del proyecto

Día 50 del proyecto. Asistentes: Diego Avella (PO), Miguel Hernández y Juan Sebastián Fajardo (SM, facilitador). En la Review también participaron el comité de riesgo y la gerencia de clientes preferentes de FinBank.

## Sprint Review

| Métrica | Sprint 1 | Sprint 2 | Sprint 3 | Sprint 4 | Sprint 5 |
| --- | --- | --- | --- | --- | --- |
| Comprometido | 11 | 16 | 10 | 9 | 10 |
| Completado (velocidad) | 8 | 11 | 10 | 9 | 10 |
| Cumplimiento | 73 % | 69 % | 100 % | 100 % | 100 % |

Velocidad promedio: **9,6 pts**. Se completaron 48 de 56 puntos comprometidos (86 %), y esos 48 puntos son **el 100 % del backlog**: los 8 puntos de diferencia fueron arrastres de los Sprints 1 y 2 que se terminaron en el Sprint siguiente.

**Incremento mostrado:** umbral por costo, validación fuera de tiempo de los dos modelos, lista de alertas de la cohorte 12, fichas de los modelos y roadmap de despliegue. La suite tiene 49 pruebas en verde.

**Decisión de FinBank:** acepta los 4 incrementos con 2 solicitudes antes del cierre, que se cargan a la reserva de contingencia:

1. Confirmar si la deriva de inactividad (I-5) es un error de datos antes de desplegar el modelo de churn (4 días).
2. Explicar cada alerta con su motivo principal y entregar un resumen para el comité (2 días).

## Cumplimiento de los acuerdos de la retrospectiva del Sprint 3

| Acuerdo | Resultado |
| --- | --- |
| Proteger `main` con 1 aprobación obligatoria | Activo desde el Sprint 4. #15, #16, #19 y #21 tienen Approve; #17, #18 y #20 entraron apilados dentro del #19 y el #21 (ver `bitacora/prs.md`) |
| Pedir los datos con un Sprint de anticipación | El extracto se pidió en el Sprint 3 y llegó el día 33, 2 días tarde, sin frenar el Sprint 4 |
| Registrar los impedimentos externos con su fecha | I-2, I-4 e I-5 quedaron registrados con su día de detección |
| Comprometer según la velocidad, con historias de 3 pts o menos | Sprints 4 y 5: 9 y 10 pts, historias de 2–3 pts y 100 % de cumplimiento |

## Retrospectiva final del proyecto

**Lo que funcionó**
- Planear con la velocidad real: desde el Sprint 3, el compromiso coincidió con la capacidad (100 % en tres Sprints seguidos).
- Automatizar temprano: el pipeline y las pruebas de los Sprints 2 y 3 hicieron que la validación tomara 6 días en lugar de 10, y con eso se recuperaron los desvíos acumulados.
- Los checkpoints de riesgo con el cliente: el de umbrales evitó entregar un punto de corte que FinBank no iba a usar.
- La reserva de contingencia se usó para lo que fue diseñada, riesgos ya identificados, sin mover la fecha de cierre.

**Lo que mejoraríamos**
- Formalizar desde el día 1 el acuerdo de entrega de datos con el cliente: los dos impedimentos externos (I-2 e I-5) vinieron de los datos.
- Activar la protección de la rama desde el primer Sprint, y no después de una desviación.
- Medir la estabilidad (PSI) desde el primer modelo, no solo en la validación.

**Recomendaciones para la implementación:** ver `docs/entrega/roadmap_despliegue.md`.
