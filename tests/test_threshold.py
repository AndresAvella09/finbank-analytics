"""Acceptance tests for US-05.3: cost-based alert threshold agreed with FinBank."""

from pathlib import Path

import numpy as np
import pandas as pd

from finbank.threshold import (
    COSTO_FN,
    COSTO_FP,
    MAX_ALERT_RATE,
    best_threshold,
    confusion_at,
    cost_curve,
    expected_cost,
    out_of_fold_scores,
)

ROOT = Path(__file__).resolve().parent.parent
Y = pd.Series([1, 1, 0, 0, 0])
P = np.array([0.9, 0.2, 0.6, 0.1, 0.05])


def test_confusion_counts_at_threshold():
    assert confusion_at(Y, P, 0.5) == {"tp": 1, "fp": 1, "fn": 1, "tn": 2, "alert_rate": 0.4}


def test_expected_cost_weights_errors_by_business_cost():
    assert expected_cost(Y, P, 0.5) == COSTO_FN + COSTO_FP


def test_best_threshold_respects_collection_capacity():
    best = best_threshold(Y, P, max_alert_rate=0.4)
    assert best["alert_rate"] <= 0.4


def test_best_threshold_is_the_cheapest_feasible_point():
    curve = cost_curve(Y, P)
    best = best_threshold(Y, P, max_alert_rate=1.0)
    assert best["cost"] == curve["cost"].min()


def test_agreed_threshold_on_development_cohorts():
    y, p = out_of_fold_scores(pd.read_csv(ROOT / "data" / "extracto_finbank_sim.csv"))
    best = best_threshold(y, p)
    assert best["threshold"] == 0.09
    assert best["alert_rate"] <= MAX_ALERT_RATE
    assert best["saving_pct"] > 0.5
