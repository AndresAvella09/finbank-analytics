"""Delinquency (US-05.2) and churn (US-06.2, US-06.3) models.

Both models are logistic regressions on standardized features: transparent,
explainable to FinBank's risk committee and enough to beat the US-05.1
baseline. Cohorts 1-10 are used for training; cohorts 11-12 are held out for
the out-of-time validation of Sprint 5 (US-07).
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from finbank.features import build_features

SEED = 42
OOT_FROM_COHORT = 11

MOROSIDAD_FEATURES = (
    "edad", "log_ingreso", "score_riesgo", "ratio_mora_ingreso",
    "es_preferente", "antiguedad_meses", "productos_activos",
)
CHURN_FEATURES = (
    "edad", "antiguedad_meses", "productos_activos", "log_saldo_promedio",
    "dias_sin_transaccion", "inactividad_60d", "saldo_bajo_ingreso", "score_riesgo",
)


def split_out_of_time(df: pd.DataFrame, oot_from: int = OOT_FROM_COHORT) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split by cut-off cohort: development (< oot_from) and out-of-time (>= oot_from)."""
    return df[df["cohorte"] < oot_from].copy(), df[df["cohorte"] >= oot_from].copy()


def build_delinquency_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """US-05.1 features plus tenure and products, ready for the 60-day model.

    ratio_mora_ingreso is measured at the cut-off date and the label 60 days
    later, so it is a valid predictor here (it only leaks the 30-day proxy).
    """
    base = build_features(df)
    return pd.DataFrame({
        "edad": base["edad"],
        "log_ingreso": np.log1p(base["ingreso_mensual"]),
        "score_riesgo": base["score_riesgo"],
        "ratio_mora_ingreso": base["ratio_mora_ingreso"],
        "es_preferente": base["es_preferente"],
        "antiguedad_meses": df["antiguedad_meses"].astype("int64"),
        "productos_activos": df["productos_activos"].astype("int64"),
    }, index=df.index)[list(MOROSIDAD_FEATURES)]


def build_churn_features(df: pd.DataFrame) -> pd.DataFrame:
    """US-06.2: churn predictors from the observation window (docs/churn_target_definition.md)."""
    return pd.DataFrame({
        "edad": df["edad"].astype("int64"),
        "antiguedad_meses": df["antiguedad_meses"].astype("int64"),
        "productos_activos": df["productos_activos"].astype("int64"),
        "log_saldo_promedio": np.log1p(df["saldo_promedio_mes"]),
        "dias_sin_transaccion": df["dias_sin_transaccion"].astype("int64"),
        "inactividad_60d": (df["dias_sin_transaccion"] >= 60).astype("int64"),
        "saldo_bajo_ingreso": (df["saldo_promedio_mes"] < df["ingreso_mensual"]).astype("int64"),
        "score_riesgo": df["score_riesgo"].astype("int64"),
    }, index=df.index)[list(CHURN_FEATURES)]


def churn_population(df: pd.DataFrame) -> pd.DataFrame:
    """Target population of US-06.1: active preferred clients with a churn label."""
    mask = (df["tipo_cliente"] == "preferente") & (df["activo"] == "si") & df["churn_3m"].notna()
    return df[mask].copy()


def make_model() -> Pipeline:
    return Pipeline([
        ("scaler", StandardScaler()),
        ("logit", LogisticRegression(max_iter=1000, random_state=SEED)),
    ])


def fit_with_cv(X: pd.DataFrame, y: pd.Series) -> dict:
    """Fit on the full development sample and report 5-fold stratified CV AUC."""
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
    cv_auc = cross_val_score(make_model(), X, y, cv=cv, scoring="roc_auc")
    model = make_model().fit(X, y)
    return {
        "model": model,
        "auc_train": round(float(roc_auc_score(y, model.predict_proba(X)[:, 1])), 3),
        "auc_cv_mean": round(float(cv_auc.mean()), 3),
        "auc_cv_std": round(float(cv_auc.std()), 3),
        "n": int(len(y)),
        "positives": int(y.sum()),
    }


def train_delinquency_model(df: pd.DataFrame) -> dict:
    """US-05.2: 60-day delinquency model on the development cohorts."""
    dev, _ = split_out_of_time(df)
    return fit_with_cv(build_delinquency_matrix(dev), dev["mora_60d"].astype(int))


def train_churn_model(df: pd.DataFrame) -> dict:
    """US-06.3: 3-month churn model on the development cohorts of the target population."""
    dev, _ = split_out_of_time(churn_population(df))
    return fit_with_cv(build_churn_features(dev), dev["churn_3m"].astype(int))


def coefficients(result: dict, features) -> pd.DataFrame:
    """Standardized coefficients, sorted by absolute weight (model explainability)."""
    coefs = result["model"].named_steps["logit"].coef_[0]
    out = pd.DataFrame({"variable": list(features), "coeficiente": np.round(coefs, 3)})
    return out.reindex(out["coeficiente"].abs().sort_values(ascending=False).index).reset_index(drop=True)
