"""Acceptance tests for US-05.1: delinquency features and reference baseline."""

from pathlib import Path

import pandas as pd

from finbank.baseline import evaluate, run_baseline, score_rule_predict
from finbank.cleaning import clean_dataset
from finbank.features import build_delinquency_target, build_features

SAMPLE = Path(__file__).resolve().parent.parent / "data" / "sample_clientes.csv"


def make_clean(**overrides):
    row = {
        "cliente_id": "C-0001",
        "edad": 40,
        "ingreso_mensual": 5000000,
        "saldo_mora_30d": 0.0,
        "score_riesgo": 700,
        "tipo_cliente": "regular",
        "activo": "si",
    }
    row.update(overrides)
    return pd.DataFrame([row])


def test_target_flags_any_delinquent_balance():
    df = pd.concat([make_clean(), make_clean(cliente_id="C-0002", saldo_mora_30d=1.0)])
    assert list(build_delinquency_target(df)) == [0, 1]


def test_ratio_mora_ingreso_handles_zero_income():
    features = build_features(make_clean(ingreso_mensual=0, saldo_mora_30d=500.0))
    assert features.loc[0, "ratio_mora_ingreso"] == 0.0


def test_binary_flags_and_score_band():
    features = build_features(make_clean(tipo_cliente="preferente", activo="no", score_riesgo=850))
    row = features.iloc[0]
    assert (row["es_preferente"], row["es_activo"], row["banda_score"]) == (1, 0, "excepcional")


def test_score_band_edges_follow_fico_cuts():
    df = pd.concat([make_clean(cliente_id=f"C-{i:04d}", score_riesgo=s) for i, s in enumerate((300, 579, 580, 800))])
    assert list(build_features(df)["banda_score"]) == ["deficiente", "deficiente", "regular", "excepcional"]


def test_rule_threshold_is_strict():
    df = pd.concat([make_clean(score_riesgo=649), make_clean(score_riesgo=650)])
    assert list(score_rule_predict(df, 650)) == [1, 0]


def test_evaluate_confusion_matrix():
    m = evaluate(pd.Series([1, 1, 0, 0]), pd.Series([1, 0, 1, 0]))
    assert (m["tp"], m["fn"], m["fp"], m["tn"]) == (1, 1, 1, 1)
    assert m["precision"] == m["recall"] == m["f1"] == 0.5


def test_pipeline_on_sample_is_reproducible():
    clean = clean_dataset(pd.read_csv(SAMPLE))["data"]
    features, target = build_features(clean), build_delinquency_target(clean)
    assert len(features) == 22 and int(target.sum()) == 3
    rows = run_baseline(features, target)
    assert [r["threshold"] for r in rows] == [600, 650, 700]
    assert all(r["tp"] + r["fp"] + r["fn"] + r["tn"] == 22 for r in rows)
