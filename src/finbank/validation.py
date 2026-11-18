"""Out-of-time validation of the delinquency and churn models (US-07).

The models are trained on cohorts 1-10 and evaluated on cohorts 11-12, which
they never saw. Stability is measured with the Population Stability Index
(PSI): < 0.10 stable, 0.10-0.25 moderate shift (monitor), > 0.25 major shift.
"""

import numpy as np
import pandas as pd
from sklearn.metrics import brier_score_loss, roc_auc_score

from finbank.models import (
    CHURN_FEATURES,
    MOROSIDAD_FEATURES,
    build_churn_features,
    build_delinquency_matrix,
    churn_population,
    split_out_of_time,
    train_churn_model,
    train_delinquency_model,
)
from finbank.threshold import COSTO_FN, best_threshold, confusion_at, expected_cost, out_of_fold_scores

PSI_STABLE = 0.10
PSI_MAJOR = 0.25


def psi(expected, actual, bins: int = 10) -> float:
    """Population Stability Index of `actual` against the `expected` distribution."""
    expected = np.asarray(expected, dtype=float)
    actual = np.asarray(actual, dtype=float)
    edges = np.unique(np.quantile(expected, np.linspace(0, 1, bins + 1)))
    if len(edges) < 3:  # (near) constant variable: compare category shares instead
        values = np.union1d(expected, actual)
        e = np.array([(expected == v).mean() for v in values])
        a = np.array([(actual == v).mean() for v in values])
    else:
        edges[0], edges[-1] = -np.inf, np.inf
        # Laplace smoothing (+0.5 per bin) keeps empty bins of small samples finite.
        e_counts = np.histogram(expected, edges)[0] + 0.5
        a_counts = np.histogram(actual, edges)[0] + 0.5
        e, a = e_counts / e_counts.sum(), a_counts / a_counts.sum()
        return round(float(np.sum((a - e) * np.log(a / e))), 4)
    e, a = np.clip(e, 1e-4, None), np.clip(a, 1e-4, None)
    return round(float(np.sum((a - e) * np.log(a / e))), 4)


def psi_label(value: float) -> str:
    if value < PSI_STABLE:
        return "estable"
    return "monitorear" if value < PSI_MAJOR else "cambio mayor"


def lift_at(y, p, top_frac: float = 0.2) -> dict:
    """Share of positives captured in the top `top_frac` of scores, and the lift."""
    y = np.asarray(y)
    order = np.argsort(-np.asarray(p))
    k = max(1, int(round(top_frac * len(y))))
    captured = y[order[:k]].sum() / max(1, y.sum())
    return {"top_frac": top_frac, "captured": round(float(captured), 3), "lift": round(float(captured / top_frac), 2)}


def psi_table(dev: pd.DataFrame, oot: pd.DataFrame, features) -> pd.DataFrame:
    rows = [{"variable": f, "psi": psi(dev[f], oot[f])} for f in features]
    out = pd.DataFrame(rows)
    out["estado"] = out["psi"].map(psi_label)
    return out.sort_values("psi", ascending=False).reset_index(drop=True)


def validate_churn(df: pd.DataFrame) -> dict:
    """US-07.2: out-of-time discrimination, campaign lift and stability of the churn model."""
    pop = churn_population(df)
    dev, oot = split_out_of_time(pop)
    model = train_churn_model(df)["model"]
    X_dev, X_oot = build_churn_features(dev), build_churn_features(oot)
    p_dev, p_oot = model.predict_proba(X_dev)[:, 1], model.predict_proba(X_oot)[:, 1]
    y_oot = oot["churn_3m"].astype(int)
    by_cohort = {
        int(c): round(float(roc_auc_score(y_oot[oot["cohorte"] == c], p_oot[(oot["cohorte"] == c).to_numpy()])), 3)
        for c in sorted(oot["cohorte"].unique())
    }
    return {
        "n_oot": int(len(oot)),
        "positives_oot": int(y_oot.sum()),
        "auc_oot": round(float(roc_auc_score(y_oot, p_oot)), 3),
        "auc_by_cohort": by_cohort,
        "lift_top20": lift_at(y_oot, p_oot, 0.2),
        "psi_score": psi(p_dev, p_oot),
        "psi_features": psi_table(X_dev, X_oot, CHURN_FEATURES),
        "psi_inactivity_by_cohort": {
            int(c): psi(X_dev["dias_sin_transaccion"], X_oot.loc[(oot["cohorte"] == c).to_numpy(), "dias_sin_transaccion"], bins=5)
            for c in sorted(oot["cohorte"].unique())
        },
    }


def ks_statistic(y, p) -> float:
    """Kolmogorov-Smirnov: max distance between the score CDFs of positives and negatives."""
    y = np.asarray(y).astype(bool)
    p = np.asarray(p)
    grid = np.unique(p)
    cdf_pos = np.searchsorted(np.sort(p[y]), grid, side="right") / max(1, y.sum())
    cdf_neg = np.searchsorted(np.sort(p[~y]), grid, side="right") / max(1, (~y).sum())
    return round(float(np.max(np.abs(cdf_pos - cdf_neg))), 3)


def calibration_table(y, p, bins: int = 5) -> pd.DataFrame:
    """Mean predicted vs observed rate by score quantile (highest risk last)."""
    df = pd.DataFrame({"y": np.asarray(y), "p": np.asarray(p)})
    df["grupo"] = pd.qcut(df["p"].rank(method="first"), bins, labels=range(1, bins + 1))
    out = df.groupby("grupo", observed=True).agg(n=("y", "size"), predicha=("p", "mean"), observada=("y", "mean"))
    return out.round(3).reset_index()


def validate_delinquency(df: pd.DataFrame) -> dict:
    """US-07.1: out-of-time discrimination, calibration, stability and business cost."""
    dev, oot = split_out_of_time(df)
    model = train_delinquency_model(df)["model"]
    X_dev, X_oot = build_delinquency_matrix(dev), build_delinquency_matrix(oot)
    p_dev, p_oot = model.predict_proba(X_dev)[:, 1], model.predict_proba(X_oot)[:, 1]
    y_oot = oot["mora_60d"].astype(int)
    threshold = best_threshold(*out_of_fold_scores(df))["threshold"]
    conf = confusion_at(y_oot, p_oot, threshold)
    auc = roc_auc_score(y_oot, p_oot)
    return {
        "n_oot": int(len(oot)),
        "positives_oot": int(y_oot.sum()),
        "auc_oot": round(float(auc), 3),
        "gini_oot": round(float(2 * auc - 1), 3),
        "ks_oot": ks_statistic(y_oot, p_oot),
        "brier_oot": round(float(brier_score_loss(y_oot, p_oot)), 4),
        "auc_score_only_oot": round(float(roc_auc_score(y_oot, -oot["score_riesgo"])), 3),
        "calibration": calibration_table(y_oot, p_oot),
        "psi_score": psi(p_dev, p_oot),
        "psi_features": psi_table(X_dev, X_oot, MOROSIDAD_FEATURES),
        "threshold": threshold,
        "confusion_oot": conf,
        "recall_oot": round(conf["tp"] / max(1, conf["tp"] + conf["fn"]), 3),
        "saving_oot": round(1 - expected_cost(y_oot, p_oot, threshold) / (y_oot.sum() * COSTO_FN), 3),
    }
