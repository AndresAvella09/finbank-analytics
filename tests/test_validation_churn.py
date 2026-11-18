"""Acceptance tests for US-07.2: out-of-time validation of the churn model."""

from pathlib import Path

import numpy as np
import pandas as pd

from finbank.validation import lift_at, psi, psi_label, validate_churn

ROOT = Path(__file__).resolve().parent.parent
RESULT = validate_churn(pd.read_csv(ROOT / "data" / "extracto_finbank_sim.csv"))


def test_psi_is_zero_for_identical_distributions():
    x = np.arange(1000)
    assert psi(x, x) < 0.001


def test_psi_detects_a_shift():
    rng = np.random.default_rng(0)
    base = rng.normal(0, 1, 2000)
    assert psi(base, base + 1.0) > 0.25
    assert psi_label(0.05) == "estable" and psi_label(0.15) == "monitorear" and psi_label(0.4) == "cambio mayor"


def test_lift_counts_positives_in_top_fraction():
    y = np.array([1, 0, 1, 0, 0, 0, 0, 0, 0, 0])
    p = np.array([0.9, 0.8, 0.7, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
    assert lift_at(y, p, 0.2) == {"top_frac": 0.2, "captured": 0.5, "lift": 2.5}


def test_churn_model_holds_out_of_time():
    assert RESULT["auc_oot"] >= 0.70
    assert all(auc >= 0.70 for auc in RESULT["auc_by_cohort"].values())
    assert RESULT["lift_top20"]["lift"] >= 2.0


def test_inactivity_drift_is_flagged_in_latest_cohort():
    by_cohort = RESULT["psi_inactivity_by_cohort"]
    assert by_cohort[11] < 0.10 < 0.25 < by_cohort[12]
