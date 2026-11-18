"""Acceptance tests for the Sprint 4 models (US-05.2, US-06.2, US-06.3)."""

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from generar_extracto import generar_extracto  # noqa: E402

from finbank.models import (  # noqa: E402
    CHURN_FEATURES,
    MOROSIDAD_FEATURES,
    build_churn_features,
    build_delinquency_matrix,
    churn_population,
    split_out_of_time,
    train_churn_model,
    train_delinquency_model,
)

EXTRACT = generar_extracto()


def test_extract_is_reproducible_and_matches_committed_csv():
    committed = pd.read_csv(ROOT / "data" / "extracto_finbank_sim.csv")
    assert len(committed) == len(EXTRACT) == 5000
    pd.testing.assert_series_equal(committed["mora_60d"], EXTRACT["mora_60d"])


def test_out_of_time_split_keeps_latest_cohorts_apart():
    dev, oot = split_out_of_time(EXTRACT)
    assert dev["cohorte"].max() == 10 and oot["cohorte"].min() == 11
    assert len(dev) + len(oot) == len(EXTRACT)


def test_feature_matrices_have_no_nulls_and_expected_columns():
    X_mora = build_delinquency_matrix(EXTRACT)
    X_churn = build_churn_features(churn_population(EXTRACT))
    assert tuple(X_mora.columns) == MOROSIDAD_FEATURES and not X_mora.isna().any().any()
    assert tuple(X_churn.columns) == CHURN_FEATURES and not X_churn.isna().any().any()


def test_churn_population_is_active_preferred_clients_only():
    pop = churn_population(EXTRACT)
    assert set(pop["tipo_cliente"]) == {"preferente"} and set(pop["activo"]) == {"si"}


def test_delinquency_model_beats_score_baseline():
    result = train_delinquency_model(EXTRACT)
    assert result["auc_cv_mean"] >= 0.70


def test_churn_model_is_better_than_random():
    result = train_churn_model(EXTRACT)
    assert result["auc_cv_mean"] >= 0.70
