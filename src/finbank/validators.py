"""Data integrity validators for the FinBank clients dataset.

Implements the data contract defined in docs/data_dictionary.md (US-03):
null checks, credit-risk score range and variable type checks.
"""

import pandas as pd

SCORE_MIN = 300
SCORE_MAX = 850

REQUIRED_COLUMNS = (
    "cliente_id",
    "edad",
    "ingreso_mensual",
    "saldo_mora_30d",
    "score_riesgo",
    "tipo_cliente",
    "activo",
)

EXPECTED_TYPES = {
    "edad": ("int64",),
    "ingreso_mensual": ("int64", "float64"),
    "saldo_mora_30d": ("float64",),
}


def _issue(issue_type: str, column: str, message: str) -> dict:
    """Build a uniform issue report entry."""
    return {"type": issue_type, "column": column, "message": message}


def check_missing_columns(df: pd.DataFrame) -> list[dict]:
    """Report required columns that are absent from the dataset."""
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    return [_issue("missing_column", c, "columna faltante: " + c) for c in missing]


def check_nulls(df: pd.DataFrame) -> list[dict]:
    """Report null values for every column present in the dataset."""
    issues = []
    for col in df.columns:
        n = int(df[col].isnull().sum())
        if n > 0:
            issues.append(_issue("nulls", col, "nulos en " + col + ": " + str(n)))
    return issues


def check_score_range(
    df: pd.DataFrame,
    min_score: int = SCORE_MIN,
    max_score: int = SCORE_MAX,
) -> list[dict]:
    """Report credit-risk scores outside the inclusive [min_score, max_score] range."""
    if "score_riesgo" not in df.columns:
        return []
    out_of_range = df[(df["score_riesgo"] < min_score) | (df["score_riesgo"] > max_score)]
    if out_of_range.empty:
        return []
    message = "score fuera de rango, debe estar entre " + str(min_score) + " y " + str(max_score)
    return [_issue("score_range", "score_riesgo", message)]


def check_variable_types(
    df: pd.DataFrame,
    expected_types: dict = EXPECTED_TYPES,
) -> list[dict]:
    """Report columns whose dtype is not one of the accepted dtypes."""
    issues = []
    for column, accepted in expected_types.items():
        if column not in df.columns:
            continue
        if str(df[column].dtype) not in accepted:
            message = column + " deberia ser " + " o ".join(accepted)
            issues.append(_issue("wrong_type", column, message))
    return issues


def validate_dataset(df: pd.DataFrame) -> dict:
    """Run all integrity checks and return a uniform report.

    Returns {"errors": [...]} where each error is a dict with keys
    'type', 'column' and 'message'.
    """
    errors = []
    errors.extend(check_missing_columns(df))
    errors.extend(check_nulls(df))
    errors.extend(check_score_range(df))
    errors.extend(check_variable_types(df))
    return {"errors": errors}
