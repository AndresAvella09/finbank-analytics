"""Acceptance tests for US-07.1: out-of-time validation of the delinquency model."""

from pathlib import Path

import numpy as np
import pandas as pd

from finbank.threshold import MAX_ALERT_RATE
from finbank.validation import calibration_table, ks_statistic, validate_delinquency

ROOT = Path(__file__).resolve().parent.parent
RESULT = validate_delinquency(pd.read_csv(ROOT / "data" / "extracto_finbank_sim.csv"))


def test_ks_is_one_for_perfect_separation_and_zero_for_identical_scores():
    y = np.array([0, 0, 1, 1])
    assert ks_statistic(y, np.array([0.1, 0.2, 0.8, 0.9])) == 1.0
    assert ks_statistic(y, np.array([0.5, 0.5, 0.5, 0.5])) == 0.0


def test_calibration_table_has_one_row_per_group():
    y = np.array([0, 1] * 50)
    p = np.linspace(0, 1, 100)
    table = calibration_table(y, p, bins=5)
    assert len(table) == 5 and table["n"].sum() == 100


def test_model_beats_score_rule_out_of_time():
    assert RESULT["auc_oot"] >= 0.80
    assert RESULT["auc_oot"] > RESULT["auc_score_only_oot"]
    assert RESULT["ks_oot"] >= 0.40


def test_model_is_calibrated_by_quintile():
    cal = RESULT["calibration"]
    assert (abs(cal["predicha"] - cal["observada"]) < 0.05).all()
    assert cal["observada"].iloc[-1] == cal["observada"].max()


def test_agreed_threshold_holds_out_of_time():
    assert RESULT["threshold"] == 0.09
    assert RESULT["confusion_oot"]["alert_rate"] <= MAX_ALERT_RATE
    assert RESULT["saving_oot"] > 0.4
    assert RESULT["psi_score"] < 0.10
