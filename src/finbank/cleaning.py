"""Data cleaning for the FinBank clients dataset (US-04.2).

Applies the null policy and the row-level rules of the data contract
(docs/data_dictionary.md, US-03) and returns the analytical dataset that feeds
the modeling stories (US-05 and US-06), together with a data quality report.

Usage from the repository root:

    PYTHONPATH=src python -m finbank.cleaning data/sample_clientes.csv
"""

import re
import sys
from pathlib import Path

import pandas as pd

from finbank.validators import SCORE_MAX, SCORE_MIN

EDAD_MIN = 18
EDAD_MAX = 75
ID_PATTERN = re.compile(r"C-\d{4}")
TIPOS_CLIENTE = ("preferente", "regular")
VALORES_ACTIVO = ("si", "no")

# Columns whose nulls the data contract allows to impute with 0.
IMPUTE_WITH_ZERO = ("saldo_mora_30d",)

DEFAULT_OUTPUT = Path("data/processed/clientes_limpio.csv")
DEFAULT_REPORT = Path("reports/calidad_datos.md")


def _violation(cliente_id, column: str, rule: str, value) -> dict:
    """Build a uniform row-level violation entry."""
    shown = "(vacío)" if pd.isna(value) else str(value)
    return {"cliente_id": cliente_id, "column": column, "rule": rule, "value": shown}


def impute_nulls(df: pd.DataFrame) -> tuple[pd.DataFrame, list[dict]]:
    """Impute the nulls the contract allows and log every imputation."""
    out = df.copy()
    log = []
    for column in IMPUTE_WITH_ZERO:
        if column not in out.columns:
            continue
        for cliente_id in out.loc[out[column].isna(), "cliente_id"]:
            log.append({"cliente_id": cliente_id, "column": column, "action": "nulo imputado a 0"})
        out[column] = out[column].fillna(0.0)
    return out, log


def _check_range(value, low, high) -> str | None:
    """Return the rule broken by a numeric value, or None if it is valid."""
    if pd.isna(value):
        return "no admite nulos"
    if not low <= value <= high:
        return "rango " + str(low) + "-" + str(high)
    return None


def find_invalid_records(df: pd.DataFrame) -> list[dict]:
    """Report every row-level violation of the data contract."""
    violations = []
    duplicated = df["cliente_id"].duplicated(keep=False)
    for i, row in df.iterrows():
        cid = row["cliente_id"]
        if pd.isna(cid) or not ID_PATTERN.fullmatch(str(cid)):
            violations.append(_violation(cid, "cliente_id", "formato C-XXXX", cid))
        elif duplicated[i]:
            violations.append(_violation(cid, "cliente_id", "debe ser único", cid))

        for column, low, high in (
            ("edad", EDAD_MIN, EDAD_MAX),
            ("score_riesgo", SCORE_MIN, SCORE_MAX),
        ):
            rule = _check_range(row[column], low, high)
            if rule:
                violations.append(_violation(cid, column, rule, row[column]))

        for column in ("ingreso_mensual", "saldo_mora_30d"):
            if pd.isna(row[column]):
                violations.append(_violation(cid, column, "no admite nulos", row[column]))
            elif row[column] < 0:
                violations.append(_violation(cid, column, "debe ser >= 0", row[column]))

        if row["tipo_cliente"] not in TIPOS_CLIENTE:
            violations.append(_violation(cid, "tipo_cliente", "'preferente' o 'regular'", row["tipo_cliente"]))
        if row["activo"] not in VALORES_ACTIVO:
            violations.append(_violation(cid, "activo", "'si' o 'no'", row["activo"]))
    return violations


def clean_dataset(df: pd.DataFrame) -> dict:
    """Impute allowed nulls, drop invalid records and summarize the run.

    Returns {"data", "imputations", "violations", "summary"}. Every record with
    at least one violation is excluded from the analytical dataset.
    """
    imputed, imputations = impute_nulls(df)
    violations = find_invalid_records(imputed)
    invalid_ids = {v["cliente_id"] for v in violations}
    clean = imputed[~imputed["cliente_id"].isin(invalid_ids)].reset_index(drop=True)
    clean["edad"] = clean["edad"].astype("int64")
    clean["score_riesgo"] = clean["score_riesgo"].astype("int64")
    summary = {
        "input_rows": len(df),
        "output_rows": len(clean),
        "removed_rows": len(df) - len(clean),
        "imputed_values": len(imputations),
        "violations": len(violations),
    }
    return {"data": clean, "imputations": imputations, "violations": violations, "summary": summary}


def build_quality_report(result: dict, source: str) -> str:
    """Render the cleaning result as a Markdown data quality report."""
    s = result["summary"]
    lines = [
        "# Reporte de calidad de datos (US-04.2)",
        "",
        "Fuente: `" + source + "`. Generado con `PYTHONPATH=src python -m finbank.cleaning`.",
        "",
        "| Métrica | Valor |",
        "| --- | --- |",
        "| Registros de entrada | " + str(s["input_rows"]) + " |",
        "| Registros válidos (pasan a modelado) | " + str(s["output_rows"]) + " |",
        "| Registros excluidos | " + str(s["removed_rows"]) + " |",
        "| Valores imputados | " + str(s["imputed_values"]) + " |",
        "",
        "## Violaciones al contrato de datos",
        "",
    ]
    if result["violations"]:
        lines += ["| cliente_id | Campo | Regla | Valor |", "| --- | --- | --- | --- |"]
        lines += [
            "| " + " | ".join(str(v[k]) for k in ("cliente_id", "column", "rule", "value")) + " |"
            for v in result["violations"]
        ]
    else:
        lines.append("Sin violaciones.")
    lines += ["", "## Imputaciones", ""]
    if result["imputations"]:
        lines += ["| cliente_id | Campo | Acción |", "| --- | --- | --- |"]
        lines += [
            "| " + " | ".join(str(v[k]) for k in ("cliente_id", "column", "action")) + " |"
            for v in result["imputations"]
        ]
    else:
        lines.append("Sin imputaciones.")
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    source = argv[1] if len(argv) > 1 else "data/sample_clientes.csv"
    result = clean_dataset(pd.read_csv(source))
    DEFAULT_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    DEFAULT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    result["data"].to_csv(DEFAULT_OUTPUT, index=False)
    DEFAULT_REPORT.write_text(build_quality_report(result, source), encoding="utf-8")
    s = result["summary"]
    print(f"{s['output_rows']} de {s['input_rows']} registros validos -> {DEFAULT_OUTPUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
