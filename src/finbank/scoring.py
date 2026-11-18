"""Portfolio scoring and alert list delivered to FinBank (US-08).

One row per client of a cut-off cohort with the 60-day delinquency
probability and alert (agreed cost-based threshold, US-05.3) and, for active
preferred clients, the 3-month churn probability and a retention alert for
the top RETENTION_TOP_FRAC of risk (capacity of the retention campaign).
"""

import numpy as np
import pandas as pd

from finbank.models import (
    build_churn_features,
    build_delinquency_matrix,
    train_churn_model,
    train_delinquency_model,
)
from finbank.threshold import best_threshold, out_of_fold_scores

RETENTION_TOP_FRAC = 0.20


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

    pref = target[(target["tipo_cliente"] == "preferente") & (target["activo"] == "si")]
    out["prob_churn_3m"] = np.nan
    if len(pref):
        out.loc[pref.index, "prob_churn_3m"] = churn_model.predict_proba(build_churn_features(pref))[:, 1].round(4)
        cut = out.loc[pref.index, "prob_churn_3m"].quantile(1 - RETENTION_TOP_FRAC)
        out["alerta_churn"] = (out["prob_churn_3m"] >= cut).astype("int64")
    else:
        out["alerta_churn"] = 0
    out["prioridad"] = np.select(
        [(out["alerta_mora"] == 1) & (out["alerta_churn"] == 1), out["alerta_mora"] == 1, out["alerta_churn"] == 1],
        ["1-mora y churn", "2-mora", "3-churn"], default="4-sin alerta",
    )
    return out.sort_values(["prioridad", "prob_mora_60d"], ascending=[True, False]).reset_index(drop=True)


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
