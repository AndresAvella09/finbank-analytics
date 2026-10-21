"""Feature engineering for the early-delinquency model (US-05.1).

Input: the analytical dataset produced by finbank.cleaning (US-04.2), which
already satisfies the data contract (no nulls, valid ranges and categories).
"""

import pandas as pd

# FICO-style bands over the 300-850 score range of the data contract.
SCORE_BINS = (300, 580, 670, 740, 800, 851)
SCORE_LABELS = ("deficiente", "regular", "bueno", "muy_bueno", "excepcional")

# Built from saldo_mora_30d, so it leaks the 30-day proxy target. It is valid
# only as a predictor of the 60-day label (measured after the cut-off date).
LEAKY_FOR_30D_PROXY = ("ratio_mora_ingreso",)


def build_delinquency_target(df: pd.DataFrame) -> pd.Series:
    """Target proxy: 1 if the client carries any 30-day delinquent balance.

    The 60-day label requires FinBank's monthly delinquency history, which is
    not in the synthetic sample yet (see the Sprint 3 impediment log).
    """
    return (df["saldo_mora_30d"] > 0).astype("int64").rename("en_mora_30d")


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """Return the model-ready feature table, one row per client."""
    ingreso = df["ingreso_mensual"].astype("float64")
    features = pd.DataFrame(
        {
            "cliente_id": df["cliente_id"],
            "edad": df["edad"].astype("int64"),
            "ingreso_mensual": ingreso,
            "score_riesgo": df["score_riesgo"].astype("int64"),
            "ratio_mora_ingreso": (df["saldo_mora_30d"] / ingreso.where(ingreso > 0)).fillna(0.0),
            "es_preferente": (df["tipo_cliente"] == "preferente").astype("int64"),
            "es_activo": (df["activo"] == "si").astype("int64"),
        }
    )
    features["banda_score"] = pd.cut(
        df["score_riesgo"], bins=SCORE_BINS, labels=SCORE_LABELS, right=False
    ).astype(str)
    return features
