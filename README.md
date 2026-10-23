# finbank-analytics

DMS Consulting desarrolla para FinBank S.A. un sistema predictivo de morosidad temprana y churn. Este repositorio contiene el pipeline de datos y modelado construido en los Sprints 2 y 3: validación de integridad y limpieza del conjunto de clientes (US-04), definición del objetivo de churn (US-06.1), variables y modelo base de morosidad temprana (US-05.1), el demo del Sprint Review, la suite de pruebas y la bitácora de prácticas XP del equipo.

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
├── appgmac.py                   # demo del Sprint Review (Streamlit)
├── data/
│   ├── sample_clientes.csv
│   └── processed/               # base limpia y tabla de variables
├── docs/
│   ├── data_dictionary.md       # US-03
│   ├── churn_target_definition.md   # US-06.1
│   └── sprint3/                 # backlog, dailies, burndown, review y retro
├── reports/                     # calidad de datos y modelo base
├── src/
│   └── finbank/
│       ├── __init__.py
│       ├── validators.py        # US-04.1
│       ├── cleaning.py          # US-04.2
│       ├── features.py          # US-05.1
│       └── baseline.py          # US-05.1
├── tests/
│   ├── test_validators.py
│   ├── test_cleaning.py
│   └── test_features_baseline.py
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
```

## Estado de pruebas

24/24 tests pasando (ver bitacora/pruebas.md).

## Bitácora

El registro de las prácticas XP del equipo (pair programming, pull requests, refactoring y evidencia de pruebas) está en [bitacora/](bitacora/).
