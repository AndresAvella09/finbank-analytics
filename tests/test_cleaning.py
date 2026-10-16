"""Acceptance tests for the US-04.2 cleaning module.

They encode the null policy and the row-level rules of the data dictionary
(US-03). US-04.2 is only done when this suite and tests/test_validators.py pass.
"""

from pathlib import Path

import numpy as np
import pandas as pd

from finbank.cleaning import build_quality_report, clean_dataset

SAMPLE = Path(__file__).resolve().parent.parent / "data" / "sample_clientes.csv"

BASE_ROW = {
    "cliente_id": "C-0001",
    "edad": 34,
    "ingreso_mensual": 4500000.0,
    "saldo_mora_30d": 0.0,
    "score_riesgo": 720,
    "tipo_cliente": "regular",
    "activo": "si",
}


def make_df(*overrides):
    """Build a DataFrame with one valid row per override dict (ids made unique)."""
    rows = []
    for i, override in enumerate(overrides or ({},), start=1):
        row = dict(BASE_ROW, cliente_id=f"C-{i:04d}")
        row.update(override)
        rows.append(row)
    return pd.DataFrame(rows)


def test_valid_record_is_kept():
    result = clean_dataset(make_df())
    assert result["summary"]["output_rows"] == 1
    assert result["violations"] == []


def test_null_saldo_mora_is_imputed_to_zero_and_logged():
    result = clean_dataset(make_df({"saldo_mora_30d": np.nan}))
    assert result["data"].loc[0, "saldo_mora_30d"] == 0.0
    assert result["imputations"][0]["column"] == "saldo_mora_30d"


def test_null_in_non_imputable_column_drops_the_record():
    result = clean_dataset(make_df({"edad": np.nan}, {}))
    assert list(result["data"]["cliente_id"]) == ["C-0002"]
    assert result["violations"][0]["rule"] == "no admite nulos"


def test_score_bounds_are_inclusive():
    result = clean_dataset(make_df({"score_riesgo": 300}, {"score_riesgo": 850}, {"score_riesgo": 299}))
    assert list(result["data"]["score_riesgo"]) == [300, 850]


def test_age_outside_contract_range_is_dropped():
    result = clean_dataset(make_df({"edad": 17}, {"edad": 76}, {"edad": 75}))
    assert list(result["data"]["edad"]) == [75]


def test_invalid_categories_and_id_format_are_dropped():
    result = clean_dataset(make_df({"tipo_cliente": "vip"}, {"activo": "x"}, {"cliente_id": "0003"}))
    assert result["summary"]["output_rows"] == 0
    assert result["summary"]["violations"] == 3


def test_duplicated_ids_are_reported():
    df = pd.concat([make_df(), make_df()], ignore_index=True)
    result = clean_dataset(df)
    assert {v["rule"] for v in result["violations"]} == {"debe ser único"}


def test_sample_dataset_end_to_end():
    result = clean_dataset(pd.read_csv(SAMPLE))
    s = result["summary"]
    assert (s["input_rows"], s["output_rows"], s["removed_rows"], s["imputed_values"]) == (25, 22, 3, 1)
    assert result["data"]["saldo_mora_30d"].isna().sum() == 0


def test_quality_report_lists_violations_and_imputations():
    report = build_quality_report(clean_dataset(pd.read_csv(SAMPLE)), "data/sample_clientes.csv")
    assert "| Registros válidos (pasan a modelado) | 22 |" in report
    assert "C-0007" in report and "C-0018" in report
