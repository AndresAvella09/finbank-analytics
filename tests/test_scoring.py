"""Acceptance tests for US-08: portfolio scoring and alert list delivered to FinBank."""

from pathlib import Path

import pandas as pd

from finbank.scoring import RETENTION_TOP_FRAC, alert_summary, score_portfolio
from finbank.threshold import MAX_ALERT_RATE

ROOT = Path(__file__).resolve().parent.parent
EXTRACT = pd.read_csv(ROOT / "data" / "extracto_finbank_sim.csv")
SCORED = score_portfolio(EXTRACT)


def test_one_row_per_client_of_the_latest_cohort():
    latest = EXTRACT[EXTRACT["cohorte"] == EXTRACT["cohorte"].max()]
    assert len(SCORED) == len(latest)
    assert set(SCORED["cliente_id"]) == set(latest["cliente_id"])


def test_delinquency_alerts_fit_collection_capacity():
    assert alert_summary(SCORED)["tasa_alerta_mora"] <= MAX_ALERT_RATE


def test_churn_scores_only_for_preferred_clients():
    regular = SCORED[SCORED["tipo_cliente"] == "regular"]
    preferred = SCORED[SCORED["tipo_cliente"] == "preferente"]
    assert regular["prob_churn_3m"].isna().all() and regular["alerta_churn"].eq(0).all()
    assert preferred["prob_churn_3m"].notna().all()
    assert preferred["alerta_churn"].mean() <= RETENTION_TOP_FRAC + 0.02


def test_priorities_are_sorted_with_double_alerts_first():
    assert SCORED["prioridad"].is_monotonic_increasing
    assert SCORED["prioridad"].iloc[0] == "1-mora y churn"
