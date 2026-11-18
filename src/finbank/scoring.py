"""Portfolio scoring and alert list delivered to FinBank (US-08).

One row per client of a cut-off cohort with the 60-day delinquency
probability and alert (agreed cost-based threshold, US-05.3) and, for active
preferred clients, the 3-month churn probability and a retention alert for
the top RETENTION_TOP_FRAC of risk (capacity of the retention campaign).
"""

import numpy as np
import pandas as pd

from finbank.models import (
    CHURN_FEATURES,
    MOROSIDAD_FEATURES,
    build_churn_features,
    build_delinquency_matrix,
    train_churn_model,
    train_delinquency_model,
)
from finbank.threshold import best_threshold, out_of_fold_scores

RETENTION_TOP_FRAC = 0.20

# Readable names for the main-driver column requested by FinBank at the Sprint 5 review
# (direction follows the sign of each model's coefficient).
NOMBRES_MORA = {
    "score_riesgo": "score de riesgo bajo", "ratio_mora_ingreso": "mora actual alta frente al ingreso",
    "productos_activos": "muchos productos", "antiguedad_meses": "poca antigüedad", "edad": "cliente joven",
    "es_preferente": "segmento", "log_ingreso": "ingreso bajo",
}
NOMBRES_CHURN = {
    "dias_sin_transaccion": "inactividad reciente", "productos_activos": "pocos productos",
    "saldo_bajo_ingreso": "saldo menor al ingreso", "antiguedad_meses": "poca antigüedad", "edad": "cliente joven",
    "inactividad_60d": "inactividad de 60 días", "log_saldo_promedio": "saldo promedio", "score_riesgo": "score de riesgo",
}


def main_driver(model, X: pd.DataFrame, features, names: dict) -> pd.Series:
    """Variable that pushes each client's risk up the most (coefficient x standardized value)."""
    scaler, logit = model.named_steps["scaler"], model.named_steps["logit"]
    contrib = scaler.transform(X[list(features)]) * logit.coef_[0]
    idx = np.argmax(contrib, axis=1)
    return pd.Series([names.get(features[i], features[i]) for i in idx], index=X.index)


def score_portfolio(df: pd.DataFrame, cohort: int | None = None) -> pd.DataFrame:
    """Score one cut-off cohort (the latest by default) with both models."""
    cohort = int(df["cohorte"].max()) if cohort is None else cohort
    target = df[df["cohorte"] == cohort].copy()
    mora_model = train_delinquency_model(df)["model"]
    churn_model = train_churn_model(df)["model"]
    threshold = best_threshold(*out_of_fold_scores(df))["threshold"]

    out = pd.DataFrame({
        "cliente_id": target["cliente_id"],
        "tipo_cliente": target["tipo_cliente"],
        "prob_mora_60d": mora_model.predict_proba(build_delinquency_matrix(target))[:, 1].round(4),
    })
    out["alerta_mora"] = (out["prob_mora_60d"] >= threshold).astype("int64")
    out["motivo_mora"] = main_driver(mora_model, build_delinquency_matrix(target), MOROSIDAD_FEATURES, NOMBRES_MORA)
    out.loc[out["alerta_mora"] == 0, "motivo_mora"] = ""

    pref = target[(target["tipo_cliente"] == "preferente") & (target["activo"] == "si")]
    out["prob_churn_3m"] = np.nan
    if len(pref):
        out.loc[pref.index, "prob_churn_3m"] = churn_model.predict_proba(build_churn_features(pref))[:, 1].round(4)
        cut = out.loc[pref.index, "prob_churn_3m"].quantile(1 - RETENTION_TOP_FRAC)
        out["alerta_churn"] = (out["prob_churn_3m"] >= cut).astype("int64")
        out["motivo_churn"] = ""
        out.loc[pref.index, "motivo_churn"] = main_driver(churn_model, build_churn_features(pref), CHURN_FEATURES, NOMBRES_CHURN)
        out.loc[out["alerta_churn"] == 0, "motivo_churn"] = ""
    else:
        out["alerta_churn"] = 0
        out["motivo_churn"] = ""
    out["prioridad"] = np.select(
        [(out["alerta_mora"] == 1) & (out["alerta_churn"] == 1), out["alerta_mora"] == 1, out["alerta_churn"] == 1],
        ["1-mora y churn", "2-mora", "3-churn"], default="4-sin alerta",
    )
    return out.sort_values(["prioridad", "prob_mora_60d"], ascending=[True, False]).reset_index(drop=True)


def alerts_by_driver(scored: pd.DataFrame) -> pd.DataFrame:
    """Committee summary: number of alerts by model and main driver."""
    parts = []
    for modelo, alerta, motivo in (("morosidad", "alerta_mora", "motivo_mora"), ("churn", "alerta_churn", "motivo_churn")):
        counts = scored.loc[scored[alerta] == 1, motivo].value_counts()
        parts.append(pd.DataFrame({"modelo": modelo, "motivo": counts.index, "alertas": counts.to_numpy()}))
    return pd.concat(parts, ignore_index=True)


def alert_summary(scored: pd.DataFrame) -> dict:
    pref = scored["tipo_cliente"] == "preferente"
    return {
        "clientes": int(len(scored)),
        "alertas_mora": int(scored["alerta_mora"].sum()),
        "tasa_alerta_mora": round(float(scored["alerta_mora"].mean()), 3),
        "preferentes": int(pref.sum()),
        "alertas_churn": int(scored["alerta_churn"].sum()),
        "por_prioridad": scored["prioridad"].value_counts().sort_index().to_dict(),
    }
