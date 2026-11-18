"""Cost-based alert threshold for the delinquency model (US-05.3).

Agreed with FinBank at the modeling risk checkpoint (Charter risk: misalignment
on model thresholds). A missed delinquent client (false negative) costs the
expected loss of an unmanaged 60-day delinquency; a false alarm (false
positive) costs one preventive collection contact. The collection team can
contact at most MAX_ALERT_RATE of the portfolio per month, so the threshold
minimizes expected cost subject to that capacity.

The threshold is chosen on out-of-fold predictions of the development cohorts,
never on the out-of-time cohorts used to validate it (US-07.1).
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold, cross_val_predict

from finbank.models import SEED, build_delinquency_matrix, make_model, split_out_of_time

COSTO_FN = 950_000   # COP, expected loss of an unmanaged 60-day delinquency
COSTO_FP = 85_000    # COP, one preventive collection contact
MAX_ALERT_RATE = 0.15
GRID = np.round(np.arange(0.02, 0.61, 0.01), 2)


def confusion_at(y: pd.Series, p: np.ndarray, threshold: float) -> dict:
    pred = p >= threshold
    y = np.asarray(y).astype(bool)
    return {
        "tp": int((pred & y).sum()), "fp": int((pred & ~y).sum()),
        "fn": int((~pred & y).sum()), "tn": int((~pred & ~y).sum()),
        "alert_rate": round(float(pred.mean()), 3),
    }


def expected_cost(y, p, threshold, costo_fn=COSTO_FN, costo_fp=COSTO_FP) -> float:
    c = confusion_at(y, p, threshold)
    return float(c["fn"] * costo_fn + c["fp"] * costo_fp)


def cost_curve(y, p, grid=GRID, costo_fn=COSTO_FN, costo_fp=COSTO_FP) -> pd.DataFrame:
    rows = []
    for t in grid:
        c = confusion_at(y, p, t)
        rows.append({"threshold": float(t), **c, "cost": expected_cost(y, p, t, costo_fn, costo_fp)})
    return pd.DataFrame(rows)


def best_threshold(y, p, max_alert_rate=MAX_ALERT_RATE, grid=GRID, costo_fn=COSTO_FN, costo_fp=COSTO_FP) -> dict:
    """Cheapest threshold whose alert rate fits the collection capacity."""
    curve = cost_curve(y, p, grid, costo_fn, costo_fp)
    feasible = curve[curve["alert_rate"] <= max_alert_rate]
    if feasible.empty:
        raise ValueError("no threshold in the grid fits the alert capacity")
    best = feasible.loc[feasible["cost"].idxmin()]
    no_model_cost = float(np.asarray(y).sum() * costo_fn)  # nobody contacted
    return {**best.to_dict(), "cost_without_model": no_model_cost,
            "saving_pct": round(1 - best["cost"] / no_model_cost, 3)}


def out_of_fold_scores(df: pd.DataFrame) -> tuple[pd.Series, np.ndarray]:
    """Out-of-fold probabilities of the 60-day model on the development cohorts."""
    dev, _ = split_out_of_time(df)
    X, y = build_delinquency_matrix(dev), dev["mora_60d"].astype(int)
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
    return y, cross_val_predict(make_model(), X, y, cv=cv, method="predict_proba")[:, 1]
