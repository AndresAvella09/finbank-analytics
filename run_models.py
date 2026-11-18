"""Train the delinquency and churn models on the simulated FinBank extract.

Run from the repository root:

    python run_models.py

Writes the model reports under reports/.
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
from finbank.validation import psi_label, validate_churn, validate_delinquency  # noqa: E402
from finbank.scoring import alert_summary, score_portfolio  # noqa: E402
from finbank.threshold import (  # noqa: E402
    COSTO_FN,
    COSTO_FP,
    MAX_ALERT_RATE,
    best_threshold,
    out_of_fold_scores,
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


def report_threshold(best: dict) -> str:
    lines = [
        "# Umbral de alerta del modelo de morosidad (US-05.3)",
        "",
        "Acordado con FinBank en el checkpoint de umbrales. Se elige sobre las predicciones "
        "fuera de pliegue de las cohortes de desarrollo (1-10) y se valida fuera de tiempo en US-07.1.",
        "",
        "| Supuesto de negocio | Valor |",
        "| --- | --- |",
        f"| Costo de un falso negativo (mora no gestionada) | COP {COSTO_FN:,.0f} |",
        f"| Costo de un falso positivo (contacto preventivo) | COP {COSTO_FP:,.0f} |",
        f"| Capacidad del equipo de cobranza | {MAX_ALERT_RATE:.0%} de la cartera por mes |",
        "",
        "| Resultado | Valor |",
        "| --- | --- |",
        f"| Umbral de probabilidad | {best['threshold']:.2f} |",
        f"| Tasa de alertas | {best['alert_rate']:.1%} |",
        f"| Morosos detectados (TP / TP+FN) | {int(best['tp'])} / {int(best['tp'] + best['fn'])} |",
        f"| Costo esperado con el modelo | COP {best['cost']:,.0f} |",
        f"| Costo esperado sin modelo | COP {best['cost_without_model']:,.0f} |",
        f"| Ahorro | {best['saving_pct']:.1%} |",
    ]
    return "\n".join(lines).replace(",", ".") + "\n"


def report_churn_validation(r: dict) -> str:
    lines = [
        "# Validación fuera de tiempo del modelo de churn (US-07.2)",
        "",
        "Modelo entrenado con las cohortes 1-10 y evaluado sobre las cohortes 11-12 (preferentes activos).",
        "",
        "| Métrica | Valor |",
        "| --- | --- |",
        f"| Clientes fuera de tiempo / churn observados | {r['n_oot']} / {r['positives_oot']} |",
        f"| AUC fuera de tiempo | {r['auc_oot']:.3f} |",
        *[f"| AUC cohorte {c} | {a:.3f} |" for c, a in r["auc_by_cohort"].items()],
        f"| Churn capturado en el 20 % de mayor riesgo | {r['lift_top20']['captured']:.0%} (lift {r['lift_top20']['lift']:.1f}) |",
        f"| PSI del puntaje (desarrollo vs. fuera de tiempo) | {r['psi_score']:.3f} ({psi_label(r['psi_score'])}) |",
        "",
        "## Estabilidad de las variables (PSI)",
        "",
        "| Variable | PSI | Estado |",
        "| --- | --- | --- |",
        *[f"| {x.variable} | {x.psi:.3f} | {x.estado} |" for x in r["psi_features"].itertuples()],
        "",
        "PSI de `dias_sin_transaccion` por cohorte: "
        + ", ".join(f"cohorte {c}: {v:.2f}" for c, v in r["psi_inactivity_by_cohort"].items()) + ".",
        "",
        "Lectura: el modelo discrimina bien fuera de tiempo, pero la inactividad de la cohorte 12 cambió "
        "(impedimento I-5). Antes de desplegar se recomienda recalibrar con las cohortes recientes y "
        "monitorear el PSI mensualmente (umbral de alerta 0,10).",
    ]
    return "\n".join(lines) + "\n"


def report_delinquency_validation(r: dict) -> str:
    c = r["confusion_oot"]
    lines = [
        "# Validación fuera de tiempo del modelo de morosidad (US-07.1)",
        "",
        "Modelo entrenado con las cohortes 1-10 y evaluado sobre las cohortes 11-12, que no vio en el entrenamiento.",
        "",
        "| Métrica | Valor |",
        "| --- | --- |",
        f"| Clientes fuera de tiempo / morosos a 60 días | {r['n_oot']} / {r['positives_oot']} |",
        f"| AUC fuera de tiempo | {r['auc_oot']:.3f} (regla de solo score: {r['auc_score_only_oot']:.3f}) |",
        f"| Gini | {r['gini_oot']:.3f} |",
        f"| KS | {r['ks_oot']:.3f} |",
        f"| Brier | {r['brier_oot']:.4f} |",
        f"| PSI del puntaje | {r['psi_score']:.3f} ({psi_label(r['psi_score'])}) |",
        f"| Umbral acordado (US-05.3) | {r['threshold']:.2f} |",
        f"| Tasa de alertas fuera de tiempo | {c['alert_rate']:.1%} |",
        f"| Morosos detectados | {c['tp']} de {c['tp'] + c['fn']} ({r['recall_oot']:.1%}) |",
        f"| Ahorro de costo esperado frente a no usar modelo | {r['saving_oot']:.1%} |",
        "",
        "## Calibración por quintil de riesgo",
        "",
        "| Quintil | Clientes | Tasa predicha | Tasa observada |",
        "| --- | --- | --- | --- |",
        *[f"| {x.grupo} | {x.n} | {x.predicha:.3f} | {x.observada:.3f} |" for x in r["calibration"].itertuples()],
        "",
        "## Estabilidad de las variables (PSI)",
        "",
        "| Variable | PSI | Estado |",
        "| --- | --- | --- |",
        *[f"| {x.variable} | {x.psi:.3f} | {x.estado} |" for x in r["psi_features"].itertuples()],
        "",
        "Lectura: el modelo mantiene su capacidad de discriminación fuera de tiempo, está calibrado por "
        "quintiles y el umbral acordado respeta la capacidad de cobranza. La razón mora/ingreso queda en "
        "monitoreo (PSI entre 0,10 y 0,25).",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    df = pd.read_csv(EXTRACT)
    mora = train_delinquency_model(df)
    churn = train_churn_model(df)
    print(f"morosidad 60d: AUC CV {mora['auc_cv_mean']:.3f} | churn 3m: AUC CV {churn['auc_cv_mean']:.3f}")
    best = best_threshold(*out_of_fold_scores(df))
    print(f"umbral morosidad: {best['threshold']:.2f} | alertas {best['alert_rate']:.1%} | ahorro {best['saving_pct']:.1%}")
    churn_val = validate_churn(df)
    print(f"churn fuera de tiempo: AUC {churn_val['auc_oot']:.3f} | PSI inactividad {churn_val['psi_inactivity_by_cohort']}")
    mora_val = validate_delinquency(df)
    print(f"morosidad fuera de tiempo: AUC {mora_val['auc_oot']:.3f} | KS {mora_val['ks_oot']:.3f} | recall {mora_val['recall_oot']:.1%}")
    scored = score_portfolio(df)
    resumen = alert_summary(scored)
    print(f"alertas cohorte {int(df['cohorte'].max())}: mora {resumen['alertas_mora']} | churn {resumen['alertas_churn']}")
    REPORTS.mkdir(exist_ok=True)
    scored.to_csv(REPORTS / f"alertas_cohorte_{int(df['cohorte'].max())}.csv", index=False)
    (REPORTS / "validacion_morosidad.md").write_text(report_delinquency_validation(mora_val), encoding="utf-8")
    (REPORTS / "validacion_churn.md").write_text(report_churn_validation(churn_val), encoding="utf-8")
    (REPORTS / "modelos_sprint4.md").write_text(report_sprint4(df, mora, churn), encoding="utf-8")
    (REPORTS / "umbral_morosidad.md").write_text(report_threshold(best), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
