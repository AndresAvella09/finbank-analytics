"""End-to-end pipeline: validate -> clean -> features -> baseline (US-04 + US-05.1).

Run from the repository root:

    python run_pipeline.py [data/sample_clientes.csv]

Writes data/processed/clientes_limpio.csv, data/processed/features_morosidad.csv,
reports/calidad_datos.md and reports/baseline_morosidad.md.
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from finbank.baseline import build_baseline_report, run_baseline  # noqa: E402
from finbank.cleaning import build_quality_report, clean_dataset  # noqa: E402
from finbank.features import build_delinquency_target, build_features  # noqa: E402
from finbank.validators import validate_dataset  # noqa: E402

PROCESSED = Path("data/processed")
REPORTS = Path("reports")


def main(source: str) -> int:
    raw = pd.read_csv(source)
    issues = validate_dataset(raw)["errors"]
    print(f"[1/4] validacion: {len(issues)} inconsistencias a nivel de dataset")

    cleaned = clean_dataset(raw)
    s = cleaned["summary"]
    print(f"[2/4] limpieza: {s['output_rows']} de {s['input_rows']} registros validos, "
          f"{s['imputed_values']} imputados")

    clean = cleaned["data"]
    features = build_features(clean)
    target = build_delinquency_target(clean)
    print(f"[3/4] features: {features.shape[1] - 1} variables, {int(target.sum())} clientes en mora 30d")

    rows = run_baseline(features, target)
    best = max(rows, key=lambda r: r["f1"])
    print(f"[4/4] baseline: mejor F1 {best['f1']:.3f} con umbral {best['threshold']}")

    PROCESSED.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    clean.to_csv(PROCESSED / "clientes_limpio.csv", index=False)
    features.assign(en_mora_30d=target).to_csv(PROCESSED / "features_morosidad.csv", index=False)
    (REPORTS / "calidad_datos.md").write_text(build_quality_report(cleaned, source), encoding="utf-8")
    (REPORTS / "baseline_morosidad.md").write_text(
        build_baseline_report(rows, len(clean), int(target.sum())), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "data/sample_clientes.csv"))
