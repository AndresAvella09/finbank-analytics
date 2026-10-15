# finbank-analytics

DMS Consulting desarrolla para FinBank S.A. un sistema predictivo de morosidad temprana y churn. Este repositorio corresponde a la historia de usuario US-04 (recolección y limpieza de datos) y contiene el pipeline de validación de datos: validadores de integridad del conjunto de clientes, diccionario de datos, dataset sintético de ejemplo, suite de pruebas y la bitácora de prácticas XP del equipo.

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
├── data/
│   └── sample_clientes.csv
├── docs/
│   └── data_dictionary.md
├── src/
│   └── finbank/
│       ├── __init__.py
│       └── validators.py
├── tests/
│   └── test_validators.py
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
```

## Estado de pruebas

8/8 tests pasando (ver bitacora/pruebas.md).

## Bitácora

El registro de las prácticas XP del equipo (pair programming, pull requests, refactoring y evidencia de pruebas) está en [bitacora/](bitacora/).
