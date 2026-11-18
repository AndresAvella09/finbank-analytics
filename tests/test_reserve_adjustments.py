"""Acceptance tests for the work done in the contingency reserve (weeks 11-12).

FinBank's acceptance requests after the Sprint 5 review: investigate the
inactivity drift of cohort 12 (impediment I-5) and explain each alert with its
main driver for the committee.
"""

from pathlib import Path

import pandas as pd

from finbank.scoring import alert_summary, alerts_by_driver, score_portfolio
from finbank.validation import drift_investigation

ROOT = Path(__file__).resolve().parent.parent
EXTRACT = pd.read_csv(ROOT / "data" / "extracto_finbank_sim.csv")
DRIFT = drift_investigation(EXTRACT)
SCORED = score_portfolio(EXTRACT)


def test_drift_is_isolated_in_the_latest_cohort():
    assert len(DRIFT) == 12
    assert (DRIFT.loc[DRIFT["cohorte"] < 12, "psi_inactividad"] < 0.10).all()
    assert DRIFT.loc[DRIFT["cohorte"] == 12, "psi_inactividad"].item() > 0.25


def test_model_stays_calibrated_where_the_drift_happens():
    latest = DRIFT[DRIFT["cohorte"] == 12].iloc[0]
    assert abs(latest["brecha_calibracion"]) < 0.03
    assert latest["churn_observado"] > DRIFT.loc[DRIFT["cohorte"] < 12, "churn_observado"].mean()


def test_every_alert_has_a_main_driver_and_non_alerts_have_none():
    for alerta, motivo in (("alerta_mora", "motivo_mora"), ("alerta_churn", "motivo_churn")):
        assert (SCORED.loc[SCORED[alerta] == 1, motivo] != "").all()
        assert (SCORED.loc[SCORED[alerta] == 0, motivo] == "").all()


def test_committee_summary_adds_up_to_the_alerts():
    summary = alerts_by_driver(SCORED)
    totals = alert_summary(SCORED)
    assert summary.loc[summary["modelo"] == "morosidad", "alertas"].sum() == totals["alertas_mora"]
    assert summary.loc[summary["modelo"] == "churn", "alertas"].sum() == totals["alertas_churn"]
