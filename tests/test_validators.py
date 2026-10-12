"""Quality gates for the US-04 data validation module.

These tests encode the acceptance contract of the validators: a US-04 task
is only marked as done when this whole suite passes. They are deterministic
(no randomness) and build their inputs inline as plain pandas DataFrames.
"""

import numpy as np
import pandas as pd

from finbank.validators import validate_dataset

BASE_ROW = {
    "cliente_id": "C-0001",
    "edad": 34,
    "ingreso_mensual": 4500000.0,
    "saldo_mora_30d": 0.0,
    "score_riesgo": 720,
    "tipo_cliente": "regular",
    "activo": "si",
}


def make_df(**overrides):
    """Return a one-row DataFrame built from the valid base row plus overrides."""
    row = dict(BASE_ROW)
    row.update(overrides)
    return pd.DataFrame([row])


def _reported_issue_count(result):
    """Count reported issues regardless of the internal result shape."""
    total = 0
    for value in result.values():
        if isinstance(value, list):
            total += len(value)
        elif isinstance(value, int):
            total += value
    return total


def _issue_texts(result):
    """Flatten the result into searchable text so the behavioral tests do not
    depend on the exact shape of the report."""
    texts = []
    for key, value in result.items():
        texts.append(str(key))
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    texts.append(" ".join(str(part) for part in item.values()))
                else:
                    texts.append(str(item))
        else:
            texts.append(str(value))
    return texts


def test_clean_dataset_passes():
    result = validate_dataset(make_df())
    assert _reported_issue_count(result) == 0


def test_nulls_in_tracked_columns_are_reported():
    result = validate_dataset(make_df(edad=np.nan))
    assert _reported_issue_count(result) >= 1
    assert any("edad" in text for text in _issue_texts(result))


def test_nulls_in_all_columns_are_reported():
    result = validate_dataset(make_df(tipo_cliente=None))
    assert _reported_issue_count(result) >= 1
    assert any("tipo_cliente" in text for text in _issue_texts(result))


def test_score_range_bounds_are_inclusive():
    upper = validate_dataset(make_df(score_riesgo=850))
    lower = validate_dataset(make_df(score_riesgo=300))
    assert _reported_issue_count(upper) == 0
    assert _reported_issue_count(lower) == 0


def test_score_out_of_range_is_reported():
    result = validate_dataset(make_df(score_riesgo=287))
    assert _reported_issue_count(result) >= 1
    assert any("score" in text for text in _issue_texts(result))


def test_ingreso_mensual_accepts_int_and_float():
    as_int = validate_dataset(make_df(ingreso_mensual=4500000))
    as_float = validate_dataset(make_df(ingreso_mensual=4500000.0))
    assert _reported_issue_count(as_int) == 0
    assert _reported_issue_count(as_float) == 0


def test_missing_column_is_reported_not_crash():
    df = make_df().drop(columns=["score_riesgo"])
    result = validate_dataset(df)
    assert _reported_issue_count(result) >= 1
    assert any("score_riesgo" in text for text in _issue_texts(result))


def test_result_shape_is_consistent():
    result = validate_dataset(make_df(edad=np.nan))
    assert isinstance(result, dict)
    assert "errors" in result
    errors = result["errors"]
    assert isinstance(errors, list)
    assert all(isinstance(item, dict) for item in errors)
    assert all({"type", "column"} <= set(item) for item in errors)
