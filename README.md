# finbank-analytics

DMS Consulting desarrolla para FinBank S.A. un sistema predictivo de morosidad temprana y churn. Este repositorio contiene todo el sistema construido en los 5 Sprints del proyecto: contrato y limpieza de datos (US-03, US-04), definición de churn (US-06.1), modelos de morosidad a 60 días y churn a 3 meses (US-05, US-06), umbral de alerta por costo (US-05.3), validación fuera de tiempo (US-07), scoring con lista de alertas, fichas de los modelos y roadmap de despliegue (US-08), el acta de cierre, el demo del Sprint Review, la suite de pruebas y la bitácora de prácticas XP del equipo.

## Equipo y roles

| Integrante | Rol |
| --- | --- |
| Diego Avella | Product Owner / Project Lead |
| Miguel Hernández | Analista de negocio |
| Juan Sebastián Fajardo | Scrum Master |

## Estructura del repositorio

```text
finbank-analytics/
├── README.md
├── requirements.txt
├── conftest.py
├── run_pipeline.py              # validación -> limpieza -> variables -> modelo base
├── run_models.py                # modelos, umbral, validación, alertas y reportes
├── pytest.ini
├── scripts/
│   └── generar_extracto.py      # extracto simulado de FinBank (semilla fija)
├── appgmac.py                   # demo del Sprint Review (Streamlit)
├── data/
│   ├── sample_clientes.csv
│   ├── extracto_finbank_sim.csv
│   └── processed/               # base limpia y tabla de variables
├── docs/
│   ├── data_dictionary.md       # US-03
│   ├── churn_target_definition.md   # US-06.1
│   ├── sprint3/  sprint4/  sprint5/   # backlog, dailies, burndown, review y retro
│   ├── entrega/                 # fichas de los modelos y roadmap de despliegue
│   └── cierre/                  # acta de cierre
├── reports/                     # calidad, modelos, umbral, validaciones y alertas
├── src/
│   └── finbank/
│       ├── __init__.py
│       ├── validators.py        # US-04.1
│       ├── cleaning.py          # US-04.2
│       ├── features.py          # US-05.1
│       ├── baseline.py          # US-05.1
│       ├── models.py            # US-05.2, US-06.2, US-06.3
│       ├── threshold.py         # US-05.3
│       ├── validation.py        # US-07.1, US-07.2
│       └── scoring.py           # US-08
├── tests/
│   ├── test_validators.py
│   ├── test_cleaning.py
│   ├── test_features_baseline.py
│   ├── test_models.py
│   ├── test_threshold.py
│   ├── test_validation_churn.py
│   ├── test_validation_delinquency.py
│   ├── test_scoring.py
│   └── test_reserve_adjustments.py
└── bitacora/
    ├── pairing.md
    ├── prs.md
    ├── pruebas.md
    └── refactoring.md
```

## Cómo ejecutar

Desde la raíz del repositorio:

```bash
python -m venv .venv
.venv\Scripts\activate      # en Windows
pip install -r requirements.txt
python -m pytest -v
python run_pipeline.py
python run_models.py
```

## Estado de pruebas

53/53 tests pasando (ver bitacora/pruebas.md).

## Bitácora

El registro de las prácticas XP del equipo (pair programming, pull requests, refactoring y evidencia de pruebas) está en [bitacora/](bitacora/).
