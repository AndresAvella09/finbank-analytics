"""Reference baseline for the early-delinquency model (US-05.1).

A transparent score-threshold rule: flag a client as at-risk when the credit
risk score is below the threshold. It is not the final model; it sets the bar
the US-05.2 model must beat once FinBank's real data is available. The
threshold itself is a business decision to be agreed with FinBank (Charter
risk: misalignment on model thresholds).
"""

import pandas as pd

DEFAULT_THRESHOLD = 650
SENSITIVITY_THRESHOLDS = (600, 650, 700)


def score_rule_predict(features: pd.DataFrame, threshold: int = DEFAULT_THRESHOLD) -> pd.Series:
    """Predict 1 (at risk) when score_riesgo is strictly below the threshold."""
    return (features["score_riesgo"] < threshold).astype("int64").rename("pred_mora")


def evaluate(y_true: pd.Series, y_pred: pd.Series) -> dict:
    """Confusion matrix and classification metrics, without external deps."""
    y_true = y_true.reset_index(drop=True)
    y_pred = y_pred.reset_index(drop=True)
    tp = int(((y_true == 1) & (y_pred == 1)).sum())
    fp = int(((y_true == 0) & (y_pred == 1)).sum())
    fn = int(((y_true == 1) & (y_pred == 0)).sum())
    tn = int(((y_true == 0) & (y_pred == 0)).sum())
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "tp": tp, "fp": fp, "fn": fn, "tn": tn,
        "precision": round(precision, 3),
        "recall": round(recall, 3),
        "f1": round(f1, 3),
        "accuracy": round((tp + tn) / len(y_true), 3) if len(y_true) else 0.0,
    }


def run_baseline(features: pd.DataFrame, target: pd.Series, thresholds=SENSITIVITY_THRESHOLDS) -> list[dict]:
    """Evaluate the score rule for each threshold in the sensitivity table."""
    return [
        {"threshold": t, **evaluate(target, score_rule_predict(features, t))}
        for t in thresholds
    ]


def build_baseline_report(rows: list[dict], n_clients: int, positives: int) -> str:
    """Render the sensitivity table as a Markdown report."""
    lines = [
        "# Modelo base de morosidad temprana (US-05.1)",
        "",
        "Regla de referencia: `score_riesgo < umbral` => cliente en riesgo. "
        "Objetivo proxy: `en_mora_30d` (saldo en mora a 30 días > 0).",
        "",
        f"Base analítica: {n_clients} clientes válidos, {positives} con mora a 30 días.",
        "",
        "| Umbral | TP | FP | FN | TN | Precisión | Recall | F1 |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for r in rows:
        lines.append(
            f"| {r['threshold']} | {r['tp']} | {r['fp']} | {r['fn']} | {r['tn']} "
            f"| {r['precision']:.3f} | {r['recall']:.3f} | {r['f1']:.3f} |"
        )
    lines += [
        "",
        "Lectura: con la muestra sintética el score por sí solo separa mal a los clientes en mora; "
        "es la línea base que el modelo de US-05.2 debe superar con los extractos reales de FinBank. "
        "El umbral definitivo se acuerda con FinBank en el checkpoint de riesgo de la fase de modelado.",
    ]
    return "\n".join(lines) + "\n"
