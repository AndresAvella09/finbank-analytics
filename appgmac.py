"""Sprint Review & Demo Operacional - FinBank (DMS Consulting) - Cortes 2 y 3."""
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))
from finbank.cleaning import clean_dataset  # noqa: E402  (US-04.2)
from finbank.validators import validate_dataset  # noqa: E402  (US-04.1)

st.set_page_config(page_title="FinBank · Sprint Review", page_icon="🏦", layout="wide")
DATA = ROOT / "data" / "sample_clientes.csv"

# ---------- Datos del reporte de sprints ----------
SPRINTS = pd.DataFrame(
    {"Sprint": ["Sprint 1", "Sprint 2", "Sprint 3"], "Comprometidos": [11, 16, 10], "Completados": [8, 11, 10]}
)
# Burndown: puntos restantes por día hábil (según días de cierre del reporte)
BURNDOWN = {
    "Sprint 1": {"total": 11, "cierres": {6: 3, 8: 5}},
    "Sprint 2": {"total": 16, "cierres": {6: 3, 7: 5, 9: 3}},
    "Sprint 3": {"total": 10, "cierres": {4: 3, 5: 2, 6: 2, 9: 3}},
}


def burndown_df(total, cierres):
    rows, restante = [], total
    for dia in range(0, 11):
        restante -= cierres.get(dia, 0)
        rows.append({"Día": dia, "Ideal": total * (1 - dia / 10), "Real": restante})
    return pd.DataFrame(rows).set_index("Día")


# ---------- Contrato de datos (docs/data_dictionary.md) ----------
def validar(df: pd.DataFrame):
    """Devuelve (violaciones, imputaciones, base limpia) usando finbank.cleaning (US-04.2)."""
    res = clean_dataset(df)
    viol = pd.DataFrame(res["violations"]).rename(
        columns={"column": "campo", "rule": "regla", "value": "valor"})
    imp = pd.DataFrame(res["imputations"]).rename(columns={"column": "campo", "action": "acción"})
    return viol, imp, res["data"]


# ---------- Navegación ----------
st.sidebar.title("🏦 FinBank · DMS Consulting")
st.sidebar.caption("GMAC · Cortes 2 y 3")
pagina = st.sidebar.radio(
    "Sección",
    ["1. Resumen del Sprint Review", "2. Demo: pipeline de validación",
     "3. Definition of Done", "4. Lecciones y plan de mejora"],
)

# ---------- 1. Resumen ----------
if pagina.startswith("1"):
    st.title("Sprint Review · Sprints 1, 2 y 3")
    st.write("Incremento entregado a FinBank: diagnóstico, gobierno y Charter, tablero ágil, "
             "requisitos de datos, arquitectura y pipeline de validación de datos.")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Velocity Sprint 1", "8 pts", "de 11 comprometidos")
    c2.metric("Velocity Sprint 2", "11 pts", "de 16 comprometidos")
    c3.metric("Velocity Sprint 3", "10 pts", "de 10 comprometidos")
    c4.metric("Velocity promedio", "9.67 pts")
    st.subheader("Estimado vs. real")
    st.bar_chart(SPRINTS.set_index("Sprint"))
    st.subheader("Burndown")
    cols = st.columns(3)
    for col, (nombre, cfg) in zip(cols, BURNDOWN.items()):
        col.caption(nombre)
        col.line_chart(burndown_df(cfg["total"], cfg["cierres"]))
    st.info("Desvío clave: *Governance & Charter Approval* se planeó para el día 10 y cerró el día 16. "
            "Se trabajó en paralelo y el impacto fue de 1–2 días hábiles, absorbido por la reserva de "
            "contingencia (10 días).")

# ---------- 2. Demo ----------
elif pagina.startswith("2"):
    st.title("Demo operacional · validación de datos (US-04)")
    st.write("El pipeline aplica el contrato del diccionario de datos (US-03) a la base de clientes.")
    archivo = st.file_uploader("Sube un CSV de clientes (opcional)", type="csv")
    df = pd.read_csv(archivo) if archivo else pd.read_csv(DATA)
    st.caption("Fuente: " + (archivo.name if archivo else "data/sample_clientes.csv (datos sintéticos)"))
    st.dataframe(df, width="stretch", height=250)

    faltan = {"cliente_id", "edad", "ingreso_mensual", "saldo_mora_30d",
              "score_riesgo", "tipo_cliente", "activo"} - set(df.columns)
    if faltan:
        st.error(f"Faltan columnas del contrato: {sorted(faltan)}")
        st.stop()

    st.subheader("Reporte del pipeline · `finbank.validators.validate_dataset`")
    errores = validate_dataset(df)["errors"]
    if errores:
        st.error(f"{len(errores)} inconsistencias detectadas")
        st.dataframe(pd.DataFrame(errores), width="stretch", hide_index=True)
    else:
        st.success("Dataset íntegro: 0 inconsistencias.")
    st.caption("Debajo, el detalle por registro (qué filas fallan) según el diccionario de datos.")

    viol, imp, limpio = validar(df)
    filas_malas = viol["cliente_id"].nunique() if len(viol) else 0
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Registros", len(df))
    c2.metric("Violaciones", len(viol))
    c3.metric("Registros con error", filas_malas)
    c4.metric("Imputaciones", len(imp))

    st.subheader("Violaciones al contrato")
    if len(viol):
        st.dataframe(viol, width="stretch", hide_index=True)
    else:
        st.success("Sin violaciones.")
    if len(imp):
        st.subheader("Imputaciones aplicadas (política de nulos)")
        st.dataframe(imp, width="stretch", hide_index=True)

    st.subheader("Base limpia (sin registros inválidos)")
    st.write(f"{len(limpio)} de {len(df)} registros pasan a modelado.")
    st.download_button("Descargar CSV limpio", limpio.to_csv(index=False).encode(), "clientes_limpio.csv")

    st.subheader("Distribución de score de riesgo")
    st.bar_chart(pd.cut(df["score_riesgo"], bins=range(300, 900, 50)).value_counts().sort_index()
                 .rename(lambda x: f"{x.left}-{x.right}"))

# ---------- 3. DoD ----------
elif pagina.startswith("3"):
    st.title("Definition of Done")
    st.write("Una historia está *Done* cuando: (1) su checklist de 3 ítems está completo, "
             "(2) pasó por un Pull Request revisado y mezclado por un integrante distinto al autor, (3) las pruebas pasan sin errores y "
             "(4) la tarjeta está en la columna Done.")
    hist = pd.DataFrame([
        ["US-03 Requisitos de datos", "Diccionario de datos", "PR #6", "—", "✅"],
        ["US-04 Datos de muestra", "Dataset sintético", "PR #5", "—", "✅"],
        ["US-04.1 Validadores", "feat → test (red) → fix (green) → refactor",
         "PR #4 · #7 · #8", "TDD: 089febe · ccf0bd0 · ceaa33b", "✅"],
        ["US-06.1 Definición de churn", "docs/churn_target_definition.md", "PR #10", "—", "✅"],
        ["US-04.2 Limpieza", "src/finbank/cleaning.py + reporte de calidad", "PR #11", "9 pruebas (red → green)", "✅"],
        ["US-05.1 Variables y modelo base", "features.py · baseline.py · run_pipeline.py", "PR #12",
         "7 pruebas (red → green)", "✅"],
    ], columns=["Historia", "Artefacto", "Pull Request", "Evidencia TDD (commits)", "DoD"])
    st.dataframe(hist, width="stretch", hide_index=True)
    st.caption("Repo: github.com/AndresAvella09/finbank-analytics")
    st.markdown("**Prácticas XP aplicadas:** pair programming (piloto/copiloto), TDD, "
                "integración continua con ramas por funcionalidad y refactorización de validadores "
                "en funciones de responsabilidad única.")

# ---------- 4. Lecciones ----------
else:
    st.title("Lecciones aprendidas y plan de mejora")
    c1, c2, c3 = st.columns(3)
    c1.subheader("Start")
    c1.markdown("- Comprometer puntos según velocity real (8–11)\n- Dividir historias en tareas ≤ 3 pts\n"
                "- Trabajo en paralelo con criterios de aceptación acordados\n- Commits con *Co-authored-by*")
    c2.subheader("Stop")
    c2.markdown("- Comprometer más puntos de los que permite la velocity\n"
                "- Dejar tarjetas para la segunda semana\n- Esperar aprobaciones sin plan B")
    c3.subheader("Continue")
    c3.markdown("- Tablero Kanban con checklist de 3 ítems\n- Revisión por pares antes de Done\n"
                "- Dailies cortas\n- Etiquetas por fase del Charter")
    st.success("Sprint 3: se comprometieron 10 puntos y se completaron 10 (100 %), con 5 puntos cerrados "
               "en la primera semana. Sprint 4: 9–10 puntos con US-05.2 y US-06.2, sujetos a la entrega "
               "del extracto real de FinBank.")
