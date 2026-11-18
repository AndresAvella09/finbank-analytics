"""Simulated FinBank extract for the modeling sprints (US-05.2, US-06.2, US-06.3).

FinBank's real extract cannot leave the bank, so the team trains and validates
on a synthetic extract with the same contract: the clients dataset of US-03
plus the extra fields requested in docs/churn_target_definition.md and the two
labels (60-day delinquency and 3-month churn). It is fully reproducible
(fixed seed) and includes one deliberate data-drift effect in the latest
cohort, so the validation sprint can test stability (PSI).

Usage from the repository root:

    python scripts/generar_extracto.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

SEED = 42
N_CLIENTES = 5000
N_COHORTES = 12  # monthly cut-off dates; 11 and 12 are kept for out-of-time validation
OUTPUT = Path("data/extracto_finbank_sim.csv")


def _sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


def generar_extracto(n: int = N_CLIENTES, seed: int = SEED) -> pd.DataFrame:
    """Return the simulated extract, one row per client and cut-off cohort."""
    rng = np.random.default_rng(seed)
    cohorte = rng.integers(1, N_COHORTES + 1, size=n)
    edad = rng.integers(18, 76, size=n)
    preferente = rng.random(n) < 0.25
    ingreso = np.round(rng.lognormal(np.log(4_200_000), 0.55, size=n) * np.where(preferente, 1.8, 1.0), -3)
    score = np.clip(np.round(rng.normal(670, 75, size=n) + np.where(preferente, 35, 0)), 300, 850).astype(int)
    antiguedad = rng.integers(6, 181, size=n)
    productos = np.clip(rng.poisson(np.where(preferente, 3.2, 1.8)), 1, 8)
    saldo_prom = np.round(ingreso * rng.uniform(0.3, 2.5, size=n), -3)

    # Inactivity: the latest cohort drifts upwards (the drift validation must catch).
    dias_sin_tx = np.round(rng.gamma(2.0, 9.0, size=n) + np.where(cohorte == N_COHORTES, 12, 0)).astype(int)

    # Current 30-day delinquency depends on the score.
    p_mora30 = _sigmoid(-2.9 - 0.018 * (score - 650))
    en_mora30 = rng.random(n) < p_mora30
    saldo_mora_30d = np.where(en_mora30, np.round(ingreso * rng.uniform(0.05, 0.6, size=n), 2), 0.0)
    ratio = saldo_mora_30d / ingreso

    # Labels
    logit_mora60 = -3.0 - 0.016 * (score - 650) + 6.5 * ratio - 0.004 * antiguedad + 0.012 * (35 - np.minimum(edad, 35))
    mora_60d = (rng.random(n) < _sigmoid(logit_mora60)).astype(int)

    logit_churn = -1.9 + 0.055 * (dias_sin_tx - 18) - 0.35 * (productos - 3) - 0.006 * antiguedad + 0.25 * (saldo_prom < ingreso)
    churn = (rng.random(n) < _sigmoid(logit_churn)).astype(int)
    churn_3m = np.where(preferente, churn, np.nan)  # defined only for preferred clients (US-06.1)

    return pd.DataFrame({
        "cliente_id": [f"C-{i:04d}" for i in range(1, n + 1)],
        "cohorte": cohorte.astype("int64"),
        "edad": edad.astype("int64"),
        "ingreso_mensual": ingreso.astype("int64"),
        "saldo_mora_30d": saldo_mora_30d,
        "score_riesgo": score.astype("int64"),
        "tipo_cliente": np.where(preferente, "preferente", "regular"),
        "activo": "si",
        "antiguedad_meses": antiguedad.astype("int64"),
        "productos_activos": productos.astype("int64"),
        "saldo_promedio_mes": saldo_prom.astype("int64"),
        "dias_sin_transaccion": dias_sin_tx.astype("int64"),
        "mora_60d": mora_60d.astype("int64"),
        "churn_3m": churn_3m,
    })


if __name__ == "__main__":
    df = generar_extracto()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT, index=False)
    pref = df[df["tipo_cliente"] == "preferente"]
    print(f"{len(df)} clientes -> {OUTPUT} | mora_60d {df['mora_60d'].mean():.1%} | "
          f"preferentes {len(pref)} | churn_3m {pref['churn_3m'].mean():.1%}")
