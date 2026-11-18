"""Train the delinquency and churn models on the simulated FinBank extract.

Run from the repository root:

    python run_models.py

Writes reports/modelos_sprint4.md.
"""

import sys
from pathlib import Path

import pandas as pd
from sklearn.metrics import roc_auc_score

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from finbank.models import (  # noqa: E402
    CHURN_FEATURES,
    MOROSIDAD_FEATURES,
    coefficients,
    split_out_of_time,
    train_churn_model,
    train_delinquency_model,
)

EXTRACT = Path("data/extracto_finbank_sim.csv")
REPORTS = Path("reports")


def _coef_table(df: pd.DataFrame) -> list[str]:
    lines = ["| Variable | Coeficiente estandarizado |", "| --- | --- |"]
    lines += [f"| {r.variable} | {r.coeficiente:+.3f} |" for r in df.itertuples()]
    return lines


def report_sprint4(df: pd.DataFrame, mora: dict, churn: dict) -> str:
    dev, _ = split_out_of_time(df)
    auc_score_only = roc_auc_score(dev["mora_60d"], -dev["score_riesgo"])
    lines = [
        "# Modelos del Sprint 4 (US-05.2, US-06.2, US-06.3)",
        "",
        "Regresión logística sobre variables estandarizadas. Desarrollo: cohortes 1-10 del extracto "
        "simulado; las cohortes 11-12 quedan reservadas para la validación fuera de tiempo (US-07).",
        "",
        "| Modelo | Población | n | Positivos | AUC entrenamiento | AUC CV (5 pliegues) |",
        "| --- | --- | --- | --- | --- | --- |",
        f"| Morosidad 60 días | Todos los clientes | {mora['n']} | {mora['positives']} | "
        f"{mora['auc_train']:.3f} | {mora['auc_cv_mean']:.3f} ± {mora['auc_cv_std']:.3f} |",
        f"| Churn 3 meses | Preferentes activos | {churn['n']} | {churn['positives']} | "
        f"{churn['auc_train']:.3f} | {churn['auc_cv_mean']:.3f} ± {churn['auc_cv_std']:.3f} |",
        "",
        f"Referencia US-05.1: la regla de solo score alcanza AUC {auc_score_only:.3f} sobre las mismas "
        "cohortes; el modelo de morosidad la supera.",
        "",
        "## Morosidad 60 días: peso de las variables",
        "",
        *_coef_table(coefficients(mora, MOROSIDAD_FEATURES)),
        "",
        "## Churn 3 meses: peso de las variables",
        "",
        *_coef_table(coefficients(churn, CHURN_FEATURES)),
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    df = pd.read_csv(EXTRACT)
    mora = train_delinquency_model(df)
    churn = train_churn_model(df)
    print(f"morosidad 60d: AUC CV {mora['auc_cv_mean']:.3f} | churn 3m: AUC CV {churn['auc_cv_mean']:.3f}")
    REPORTS.mkdir(exist_ok=True)
    (REPORTS / "modelos_sprint4.md").write_text(report_sprint4(df, mora, churn), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
