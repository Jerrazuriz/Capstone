"""Sensibilidades de la entrega final (Informe final, Grupo 13).

Reutiliza EXACTAMENTE el modelo de `Modelo_Final_Maule_C2_corregido.ipynb`: lee las
celdas de código del notebook (datos, red, restricciones, verificación, indicadores)
y las ejecuta en este proceso, sin copiar ni modificar el modelo. Luego corre:

  1. Caso base miope con la misma condición terminal  V_final >= V_inicial.
  2. Modelo optimizado sin condición terminal (a) puro y (b) con valor del agua al final.
  3. Volumen inicial de la Laguna del Maule bajo y alto.
  4. Con y sin filtración de La Invernada (11,84 m3/s vs. 0).
  5. Uso previo de la cuota 2026 de 0, 125 y 250 hm3 (saldo de cuota).

Uso (desde la carpeta raíz del repositorio):
    python sensibilidades_final/correr_sensibilidades.py

Solver: usa Gurobi si hay una licencia completa (gurobi.lic / GRB_LICENSE_FILE).
Si solo está la licencia restringida de pip (2.000 variables), arma el mismo modelo con
gurobipy, lo exporta a MPS y lo resuelve con HiGHS (pip install highspy). Se puede
forzar con la variable de entorno SOLVER=gurobi o SOLVER=highs.

Salidas en sensibilidades_final/resultados/ (ver README.md de esta carpeta).
"""
import json
import os
import sys
import tempfile
import time

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RAIZ)                                  # el notebook busca data/ en la carpeta actual
SALIDA = os.path.join(RAIZ, "sensibilidades_final", "resultados")
os.makedirs(os.path.join(SALIDA, "figuras"), exist_ok=True)

import matplotlib
matplotlib.use("Agg")

# --------------------------------------------------------------------------------------
# 1. Cargar el modelo desde el notebook (solo definiciones y datos, sin las corridas)
# --------------------------------------------------------------------------------------
NB_PATH = os.path.join(RAIZ, "Modelo_Final_Maule_C2_corregido.ipynb")
CELDAS = json.load(open(NB_PATH, encoding="utf-8"))["cells"]
codigo = ["".join(c["source"]) for c in CELDAS if c["cell_type"] == "code"]


def celda_que_contiene(texto):
    return next(c for c in codigo if texto in c)


def hasta(c, marca):
    return c.split(marca)[0]


PARTES = [
    celda_que_contiene("import gurobipy as gp").replace("!pip install -q gurobipy", ""),
    "ENV = None",
    celda_que_contiene('DATA = "data/"'),
    celda_que_contiene("NT, NB = 48, 5"),
    celda_que_contiene("def leer_plp"),
    celda_que_contiene("def leer_horas"),
    celda_que_contiene("def leer_historicos"),
    celda_que_contiene("def leer_filtracion"),
    celda_que_contiene("def crear_variables"),
    celda_que_contiene("def agregar_balances"),
    celda_que_contiene("def riego_canales"),
    celda_que_contiene("def agregar_convenio"),
    celda_que_contiene("def definir_objetivo"),
    celda_que_contiene("def construir_modelo"),
    celda_que_contiene("def verificar"),
    celda_que_contiene("def resumen"),
    hasta(celda_que_contiene("def caso_base_miope"), "\nBASE = {}"),
    hasta(celda_que_contiene("def construir_sin_convenio"), "\nif CORRER_SENSIBILIDADES"),
]
NS = {"__name__": "modelo_maule", "display": print}
for p in PARTES:
    exec(compile(p, NB_PATH, "exec"), NS)

gp, GRB, np, pd, plt = NS["gp"], NS["GRB"], NS["np"], NS["pd"], NS["plt"]
RED, H, KAPPA, NT, NB = NS["RED"], NS["H"], NS["KAPPA"], NS["NT"], NS["NB"]
LAGUNA, EMBALSES, NODOS, CENTRALES = NS["LAGUNA"], NS["EMBALSES"], NS["NODOS"], NS["CENTRALES"]
ESCENARIOS, AFL, etiqueta = NS["ESCENARIOS"], NS["AFL"], NS["etiqueta"]

# --------------------------------------------------------------------------------------
# 2. Solver: Gurobi (licencia completa) o HiGHS sobre el mismo modelo exportado a MPS
# --------------------------------------------------------------------------------------


def licencia_completa():
    try:
        m = gp.Model()
        m.Params.OutputFlag = 0
        x = m.addVars(2100)
        m.addConstr(gp.quicksum(x.values()) <= 1)
        m.setObjective(gp.quicksum(x.values()), GRB.MAXIMIZE)
        m.optimize()
        return True
    except gp.GurobiError:
        return False


SOLVER = os.environ.get("SOLVER") or ("gurobi" if licencia_completa() else "highs")
if SOLVER == "highs":
    import highspy
print(f"gurobipy {gp.gurobi.version()} | solver: {SOLVER}")


class Solucion:
    def __init__(self, valores, gap):
        self.valores, self.gap = valores, gap

    def __call__(self, v):
        return self.valores[v.index]


def optimizar(m):
    """Resuelve m y devuelve una función var -> valor (equivale a var.X)."""
    tl, gap = float(NS["TIEMPO_MAX"]), float(NS["GAP_MIP"])
    if SOLVER == "gurobi":
        m.Params.TimeLimit, m.Params.MIPGap, m.Params.OutputFlag = tl, gap, 0
        m.optimize()
        if m.SolCount == 0:
            raise RuntimeError(f"Gurobi sin solución (estado {m.Status})")
        x = m.getAttr("X", m.getVars())
        return Solucion(x, m.MIPGap if m.IsMIP else 0.0)
    m.update()
    with tempfile.TemporaryDirectory() as d:
        f = os.path.join(d, "m.mps")
        m.write(f)
        h = highspy.Highs()
        h.setOptionValue("output_flag", False)
        h.setOptionValue("mip_rel_gap", gap)
        h.setOptionValue("time_limit", tl)
        h.readModel(f)
        h.run()
    st = h.getModelStatus()
    if st not in (highspy.HighsModelStatus.kOptimal, highspy.HighsModelStatus.kTimeLimit):
        raise RuntimeError(f"HiGHS sin solución ({h.modelStatusToString(st)})")
    info = h.getInfo()
    return Solucion(list(h.getSolution().col_value), float(getattr(info, "mip_gap", 0.0) or 0.0))


def extraer(M, X):
    q, s, V = M["q"], M["s"], M["V"]
    T, B = range(NT), range(NB)
    M["Q"] = {n: np.array([[X(q[n, t, b]) for b in B] for t in T]) for n in NODOS}
    M["S"] = {n: np.array([[X(s[n, t, b]) for b in B] for t in T]) for n in NODOS}
    M["Vx"] = {e: np.array([X(V[e, t]) for t in T]) for e in EMBALSES}
    M["DEF"] = np.array([[X(M["deficit"][t, b]) for b in B] for t in T])
    M["F"] = np.array([X(M["f"][t]) for t in T])
    M["R"] = np.array([[X(M["r"][t, b]) for b in B] for t in T])
    M["G"] = np.array([[X(M["g"][t, b]) for b in B] for t in T])
    M["Y"] = np.array([round(X(M["y"][t])) for t in T])
    M["gap"] = X.gap
    return M


def resolver(M):
    """Igual que resolver() del notebook, pero con el solver elegido."""
    t0 = time.time()
    M = extraer(M, optimizar(M["m"]))
    M["seg"] = time.time() - t0
    return M


def caso_base_miope(afl, condicion_terminal=False, pi=None, conv=None):
    """Igual que caso_base_miope() del notebook (semana a semana, solo el ingreso de la semana).
    condicion_terminal=True mantiene V_final >= V_inicial en todos los embalses: el miope sigue
    mirando una semana, pero cada decisión debe dejar factible terminar el año con V0."""
    PEN, DES, FILT = NS["PEN_DEFICIT"], NS["DESEMPATE"], NS["FILT"]
    M = NS["construir_modelo"](afl, pi, conv)
    m, q, s, pi_ = M["m"], M["q"], M["s"], M["pi"]
    if not condicion_terminal:
        for e in EMBALSES:
            M["V"][e, NT - 1].LB = NS["V_INFERIOR"] if e == LAGUNA else float(RED.at[e, "Vmin"])
    t0 = time.time()
    for t in range(NT):
        B = range(NB)
        ingreso_t = gp.quicksum(float(pi_[RED.at[n, "barra"]][t, b] * RED.at[n, "eta"] * H[t, b]) * q[n, t, b]
                                for n in CENTRALES for b in B)
        castigo_t = gp.quicksum(PEN * float(H[t, b]) * M["deficit"][t, b] for b in B) \
            + PEN * float(H[t].sum()) * (FILT - M["f"][t])
        desempate_t = gp.quicksum(DES * float(H[t, b]) * s[n, t, b] for n in CENTRALES for b in B)
        m.setObjective(ingreso_t - castigo_t - desempate_t, GRB.MAXIMIZE)
        X = optimizar(m)
        continuas = [q[n, t, b] for n in NODOS for b in B] + [s[n, t, b] for n in NODOS for b in B] \
            + [M["V"][e, t] for e in EMBALSES] + [M["deficit"][t, b] for b in B] + [M["f"][t]] \
            + [M["r"][t, b] for b in B] + [M["g"][t, b] for b in B] + [M["g_ro"][t], M["r_ro"][t]]
        binarias = [M["y"][t]] + [M["on"][t, b] for b in B]
        valores = [X(v) for v in continuas] + [round(X(v)) for v in binarias]
        for v, x in zip(continuas + binarias, valores):
            v.LB, v.UB = x, x
    M = resolver(M)
    M["seg"] = time.time() - t0
    return M


def sin_condicion_terminal(M):
    for e in EMBALSES:
        M["V"][e, NT - 1].LB = NS["V_INFERIOR"] if e == LAGUNA else float(RED.at[e, "Vmin"])
    return M


def valor_agua_hm3():
    """Valor del agua al final del horizonte [USD/hm3] para cada embalse: energía que daría
    1 hm3 bajando por todas las centrales aguas abajo (suma de rendimientos, por la ruta
    turbinada) x CMg medio anual de esas barras. 1 hm3 = 1e6/3600 (m3/s)·h."""
    out = {}
    for e in EMBALSES:
        n, usd_por_m3s_h = e, 0.0
        while n is not None:
            if RED.at[n, "genera"]:
                pi = NS["PI"][RED.at[n, "barra"]]
                usd_por_m3s_h += RED.at[n, "eta"] * (pi * H).sum() / H.sum()
            n = RED.at[n, "abajo_q"]
        out[e] = usd_por_m3s_h / KAPPA
    return out


def con_valor_agua(M):
    """Sin condición terminal y con el agua final valorizada (reemplaza V_final >= V0)."""
    sin_condicion_terminal(M)
    va = valor_agua_hm3()
    m = M["m"]
    m.setObjective(m.getObjective() + gp.quicksum(va[e] * M["V"][e, NT - 1] for e in EMBALSES), GRB.MAXIMIZE)
    M["valor_agua"] = va
    return M


# --------------------------------------------------------------------------------------
# 3. Corridas
# --------------------------------------------------------------------------------------
KPI = ["Q medio en B_Maule [m3/s]", "Q50 [m3/s]", "Q90 [m3/s]", "Q mínimo semanal [m3/s]",
       "Déficit de riego [hm3]", "Generación desde la Laguna [hm3]", "Semanas en reserva ordinaria",
       "V final LMAULE [hm3]", "V final CIPRESES [hm3]", "V final COLBUN [hm3]",
       "Energía [GWh]", "Ingreso [MUSD]"]
FILAS, TRAYECTORIAS = [], {}
V0_LAGUNA = float(RED.at[LAGUNA, "V0"])
FILT0 = float(NS["FILT"])
CUOTA0 = dict(NS["CUOTA_DISPONIBLE"])


def registrar(grupo, caso, nombre, M, sin_vf=False):
    """sin_vf=True: el caso no exige V_final >= V0, así que ese chequeo no cuenta como error."""
    errores = NS["verificar"](M)
    if sin_vf:
        errores = [e for e in errores if not e.startswith("volumen final")]
    r = NS["resumen"](M, nombre, ESCENARIOS[nombre])
    fila = {"grupo": grupo, "caso": caso, "escenario": nombre, "año": etiqueta(ESCENARIOS[nombre])}
    fila.update({k: r[k] for k in KPI})
    fila["V inicial LMAULE [hm3]"] = float(RED.at[LAGUNA, "V0"])
    fila["Filtración [m3/s]"] = float(NS["FILT"])
    fila["Cuota 2026 disponible [hm3]"] = NS["CUOTA_DISPONIBLE"][2026]
    fila["Gap MIP"] = r["Gap MIP"]
    fila["Verificación"] = "OK" if not errores else "; ".join(errores[:5])
    FILAS.append(fila)
    TRAYECTORIAS[(grupo, caso, nombre)] = dict(
        Q=NS["prom_semana"](NS["caudal_punto"](M)), V=M["Vx"][LAGUNA].copy())
    print(f"  {caso:42s} {nombre:7s} Q={fila['Q medio en B_Maule [m3/s]']:6.1f}  Q90={fila['Q90 [m3/s]']:5.1f}"
          f"  Qmin={fila['Q mínimo semanal [m3/s]']:5.1f}  Vf={fila['V final LMAULE [hm3]']:6.1f}  {fila['Verificación']}")


def correr_todo():
    construir = NS["construir_modelo"]
    print("0. Modelo base (debe reproducir la corrida del 18-10: 135,9 / 98,1 / 68,2)")
    for k, a in ESCENARIOS.items():
        registrar("0. Base", "Modelo optimizado (base)", k, resolver(construir(AFL[a])))

    print("1. Caso base miope")
    for k, a in ESCENARIOS.items():
        registrar("1. Caso base miope", "Miope (notebook, sin condición terminal)", k, caso_base_miope(AFL[a]), sin_vf=True)
        registrar("1. Caso base miope", "Miope con V_final >= V_inicial", k,
                  caso_base_miope(AFL[a], condicion_terminal=True))

    print("2. Condición terminal")
    for k, a in ESCENARIOS.items():
        registrar("2. Condición terminal", "Sin condición terminal", k,
                  resolver(sin_condicion_terminal(construir(AFL[a]))), sin_vf=True)
        registrar("2. Condición terminal", "Sin condición terminal, con valor del agua", k,
                  resolver(con_valor_agua(construir(AFL[a]))), sin_vf=True)

    print("3. Volumen inicial de la Laguna (la condición terminal sigue siendo V_final >= V_inicial)")
    for v0 in (400.0, 510.0, 900.0):
        RED.at[LAGUNA, "V0"] = v0
        try:
            for k, a in ESCENARIOS.items():
                registrar("3. Volumen inicial Laguna", f"V inicial Laguna = {v0:.0f} hm3", k,
                          resolver(construir(AFL[a])))
        finally:
            RED.at[LAGUNA, "V0"] = V0_LAGUNA

    print("4. Filtración de La Invernada")
    NS["FILT"] = 0.0
    try:
        for k, a in ESCENARIOS.items():
            registrar("4. Filtración", "Sin filtración (0 m3/s)", k, resolver(construir(AFL[a])))
    finally:
        NS["FILT"] = FILT0

    print("5. Uso previo de la cuota 2026")
    for usado in (0.0, 250.0):
        NS["CUOTA_DISPONIBLE"][2026] = max(0.0, NS["CUOTA_GENERACION"] - usado)
        try:
            for k, a in ESCENARIOS.items():
                registrar("5. Saldo de cuota", f"Uso previo {usado:.0f} hm3", k, resolver(construir(AFL[a])))
        finally:
            NS["CUOTA_DISPONIBLE"].update(CUOTA0)


# --------------------------------------------------------------------------------------
# 4. Tablas y figuras
# --------------------------------------------------------------------------------------
COLOR = {"Húmedo": "#2a78d6", "Medio": "#1baf7a", "Seco": "#eb6834"}


def exportar():
    df = pd.DataFrame(FILAS)
    base = df[df.grupo == "0. Base"].set_index("escenario")
    for c in ("Q medio en B_Maule [m3/s]", "Q90 [m3/s]", "Q mínimo semanal [m3/s]", "V final LMAULE [hm3]"):
        df["Δ " + c + " vs base"] = df[c] - df.escenario.map(base[c])
    df.to_csv(os.path.join(SALIDA, "sensibilidades.csv"), index=False, encoding="utf-8-sig")

    # Tabla compacta para el informe: Q medio / Q50 / Q90 / Q min / V final por caso y escenario
    cols = ["Q medio en B_Maule [m3/s]", "Q50 [m3/s]", "Q90 [m3/s]", "Q mínimo semanal [m3/s]", "V final LMAULE [hm3]"]
    tabla = df.pivot_table(index=["grupo", "caso"], columns="escenario", values=cols, sort=False)
    tabla = tabla.reindex(columns=pd.MultiIndex.from_product([cols, list(ESCENARIOS)]))
    with pd.ExcelWriter(os.path.join(SALIDA, "sensibilidades.xlsx")) as xw:
        df.to_excel(xw, sheet_name="todas", index=False)
        tabla.round(1).to_excel(xw, sheet_name="tabla_informe")
        semanal = pd.DataFrame({f"{g} | {c} | {e} | {var}": v[var]
                                for (g, c, e), v in TRAYECTORIAS.items() for var in ("Q", "V")})
        semanal.index = np.arange(1, NT + 1)
        semanal.index.name = "semana"
        semanal.to_excel(xw, sheet_name="semanal")
    open(os.path.join(SALIDA, "tabla_informe.md"), "w", encoding="utf-8").write(tabla.round(1).to_markdown())

    # Figura A: Q medio y Q90 en B_Maule por sensibilidad (puntos), con la base como línea
    casos = [(g, c) for g, c in dict.fromkeys(zip(df.grupo, df.caso)) if g != "0. Base"]
    fig, axs = plt.subplots(1, 2, figsize=(11, 0.42 * len(casos) + 1.6), sharey=True)
    for ax, kpi, tit in zip(axs, ("Q medio en B_Maule [m3/s]", "Q90 [m3/s]"),
                            ("Caudal medio en B_Maule [m³/s]", "Q90 en B_Maule [m³/s]")):
        for k in ESCENARIOS:
            ax.axvline(base.at[k, kpi], color=COLOR[k], lw=1, ls=":")
            vals = [df[(df.grupo == g) & (df.caso == c) & (df.escenario == k)][kpi].iloc[0] for g, c in casos]
            ax.scatter(vals, range(len(casos)), color=COLOR[k], s=28, label=k, zorder=3)
        ax.set_title(tit, fontsize=10)
        ax.grid(axis="x", alpha=.3)
    axs[0].set_yticks(range(len(casos)))
    axs[0].set_yticklabels([c for _, c in casos], fontsize=8)
    axs[0].invert_yaxis()
    h_, l_ = axs[1].get_legend_handles_labels()
    fig.legend(h_, l_, fontsize=8, loc="lower center", ncol=3, frameon=False)
    fig.text(0.99, 0.01, "Línea punteada: modelo base de cada escenario", ha="right", fontsize=7, color="#555")
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.savefig(os.path.join(SALIDA, "figuras", "e3_sensibilidades.pdf"))
    fig.savefig(os.path.join(SALIDA, "figuras", "e3_sensibilidades.png"), dpi=200)
    plt.close(fig)

    # Figura B: año seco, volumen de la Laguna y caudal semanal: modelo, miope y miope con V_final >= V0
    x = np.arange(1, NT + 1)
    curvas = [(("0. Base", "Modelo optimizado (base)"), "Modelo", "#222", "-"),
              (("1. Caso base miope", "Miope (notebook, sin condición terminal)"), "Miope", "#eb6834", "--"),
              (("1. Caso base miope", "Miope con V_final >= V_inicial"), "Miope con $V_f \\geq V_0$", "#7a4fd6", "-.")]
    fig, axs = plt.subplots(1, 2, figsize=(12, 3.8))
    for (g, c), lab, col, ls in curvas:
        tr = TRAYECTORIAS[(g, c, "Seco")]
        axs[0].plot(x, tr["Q"], color=col, ls=ls, lw=1.8, label=lab)
        axs[1].plot(x, tr["V"], color=col, ls=ls, lw=1.8, label=lab)
    axs[0].set(xlabel="Semana (jul-2026 a jun-2027)", ylabel="m³/s", title="Caudal semanal en B_Maule, año seco")
    axs[1].axhline(NS["CONV"]["V_superior"], color="#999", lw=.8)
    axs[1].axhline(NS["V_INFERIOR"], color="#999", lw=.8)
    axs[1].set(xlabel="Semana (jul-2026 a jun-2027)", ylabel="hm³", title="Volumen de la Laguna del Maule, año seco")
    for ax in axs:
        ax.grid(alpha=.3)
        ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(SALIDA, "figuras", "e3_miope_terminal.pdf"))
    fig.savefig(os.path.join(SALIDA, "figuras", "e3_miope_terminal.png"), dpi=200)
    plt.close(fig)
    return df, tabla


if __name__ == "__main__":
    t0 = time.time()
    correr_todo()
    df, tabla = exportar()
    print(f"\nListo en {time.time() - t0:.0f} s. Resultados en {SALIDA}")
    print(f"Valor del agua usado en 2b [USD/hm3]: { {k: round(v) for k, v in valor_agua_hm3().items()} }")
