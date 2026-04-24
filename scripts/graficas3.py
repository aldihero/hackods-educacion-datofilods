#%% 
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ══════════════════════════════════════════════════════════════════════
# 1. CARGAR Y LIMPIAR DATOS
# ══════════════════════════════════════════════════════════════════════

# — Educacion_06: matrícula primaria + secundaria (ciclo 2022/2023) —
edu_raw = pd.read_csv("../datos/Educacion_06.csv", header=None, encoding="utf-8")
edu = edu_raw.iloc[9:41, [0, 2, 3]].copy()
edu.columns = ["estado", "primaria", "secundaria"]
edu["estado"] = edu["estado"].astype(str).str.strip()
for c in ["primaria", "secundaria"]:
    edu[c] = pd.to_numeric(edu[c].astype(str).str.replace(",", ""), errors="coerce")
edu["estudiantes"] = edu["primaria"] + edu["secundaria"]

# — cuadro4_6: población 5-17 y ocupados (ENTI 2022) —
# Columnas: 0=estado, 1=población 5-17, 3=total ocupados, 11=no ocupados
ocu_raw = pd.read_csv("../datos/cuadro4_6_pobSegun_condición_ocupación.csv",
                      header=None, encoding="utf-8")
ocu = ocu_raw.iloc[13:45, [0, 1, 3, 11]].copy()
ocu.columns = ["estado", "poblacion_5_17", "ocupados", "no_ocupados"]
ocu["estado"] = ocu["estado"].astype(str).str.strip()
for c in ["poblacion_5_17", "ocupados", "no_ocupados"]:
    ocu[c] = pd.to_numeric(ocu[c].astype(str).str.replace(",", ""), errors="coerce")

# — Merge —
df = pd.merge(edu, ocu, on="estado")
df["porc_ocupados"] = df["ocupados"] / df["poblacion_5_17"] * 100

# Abreviaciones
state_short = {
    'Aguascalientes':'AGS','Baja California':'BC','Baja California Sur':'BCS',
    'Campeche':'CAM','Chiapas':'CHIS','Chihuahua':'CHIH','Ciudad de México':'CDMX',
    'Coahuila de Zaragoza':'COAH','Colima':'COL','Durango':'DGO',
    'Guanajuato':'GTO','Guerrero':'GRO','Hidalgo':'HGO','Jalisco':'JAL',
    'México':'MEX','Michoacán de Ocampo':'MICH','Morelos':'MOR','Nayarit':'NAY',
    'Nuevo León':'NL','Oaxaca':'OAX','Puebla':'PUE','Querétaro':'QRO',
    'Quintana Roo':'QROO','San Luis Potosí':'SLP','Sinaloa':'SIN','Sonora':'SON',
    'Tabasco':'TAB','Tamaulipas':'TAMPS','Tlaxcala':'TLAX',
    'Veracruz de Ignacio de la Llave':'VER','Yucatán':'YUC','Zacatecas':'ZAC',
}
df["short"] = df["estado"].map(state_short).fillna(df["estado"])
df = df.sort_values("estudiantes", ascending=True)

# ══════════════════════════════════════════════════════════════════════
# 2. PALETA
# ══════════════════════════════════════════════════════════════════════
BG, PAPER, GRID, TEXT = "#0D1117", "#161B22", "#21262D", "#E6EDF3"
C_PRIM  = "#457B9D"   # primaria
C_SEC   = "#2EC4B6"   # secundaria
C_OCU   = "#E63946"   # ocupados
C_NOCU  = "#1a472a"   # no ocupados

# ══════════════════════════════════════════════════════════════════════
# 3. FIGURA — 3 paneles
# ══════════════════════════════════════════════════════════════════════
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        "Estudiantes (primaria + secundaria) vs Niños ocupados por estado",
        "Desglose: primaria vs secundaria por estado",
        "% Niños ocupados vs total estudiantes — scatter por estado",
        "Composición: ocupados vs no ocupados (top 10 estados con más ocupados)",
    ),
    specs=[[{"type": "bar"}, {"type": "bar"}],
           [{"type": "scatter"}, {"type": "bar"}]],
    vertical_spacing=0.16,
    horizontal_spacing=0.08,
)

# ── Panel 1: barras agrupadas estudiantes vs ocupados ────────────────
fig.add_trace(go.Bar(
    y=df["short"], x=df["estudiantes"],
    name="Estudiantes (prim+sec)", orientation="h",
    marker_color=C_PRIM, opacity=0.85,
    hovertemplate="<b>%{y}</b><br>Estudiantes: %{x:,.0f}<extra></extra>",
), row=1, col=1)

fig.add_trace(go.Bar(
    y=df["short"], x=df["ocupados"],
    name="Niños ocupados (5-17)", orientation="h",
    marker_color=C_OCU, opacity=0.85,
    hovertemplate="<b>%{y}</b><br>Ocupados: %{x:,.0f}<extra></extra>",
), row=1, col=1)

# ── Panel 2: desglose primaria vs secundaria ─────────────────────────
fig.add_trace(go.Bar(
    y=df["short"], x=df["primaria"],
    name="Primaria", orientation="h",
    marker_color=C_PRIM, opacity=0.9,
    hovertemplate="<b>%{y}</b><br>Primaria: %{x:,.0f}<extra></extra>",
), row=1, col=2)

fig.add_trace(go.Bar(
    y=df["short"], x=df["secundaria"],
    name="Secundaria", orientation="h",
    marker_color=C_SEC, opacity=0.9,
    hovertemplate="<b>%{y}</b><br>Secundaria: %{x:,.0f}<extra></extra>",
), row=1, col=2)

# ── Panel 3: scatter % ocupados vs total estudiantes ─────────────────
fig.add_trace(go.Scatter(
    x=df["estudiantes"], y=df["porc_ocupados"],
    mode="markers+text", text=df["short"],
    textposition="top center", textfont=dict(size=7.5, color=TEXT),
    marker=dict(
        size=df["ocupados"] / df["ocupados"].max() * 30 + 6,
        color=df["porc_ocupados"],
        colorscale=[[0, "#1a472a"], [0.5, "#f4d35e"], [1, C_OCU]],
        showscale=True,
        colorbar=dict(
            title=dict(text="% ocup.", font=dict(color=TEXT, size=9)),
            tickfont=dict(color=TEXT, size=8),
            len=0.38, x=0.47, y=0.18, thickness=12,
        ),
        line=dict(width=0.5, color=GRID),
    ),
    hovertemplate=(
        "<b>%{text}</b><br>"
        "Estudiantes: %{x:,.0f}<br>"
        "% ocupados: %{y:.1f}%<extra></extra>"
    ),
    showlegend=False, name="",
), row=2, col=1)

# línea de tendencia
x_arr = df["estudiantes"].values
y_arr = df["porc_ocupados"].values
mask = ~np.isnan(x_arr) & ~np.isnan(y_arr)
m, b = np.polyfit(x_arr[mask], y_arr[mask], 1)
xl = np.linspace(x_arr[mask].min(), x_arr[mask].max(), 100)
fig.add_trace(go.Scatter(
    x=xl, y=m*xl+b, mode="lines",
    line=dict(color=C_OCU, width=1.5, dash="dot"),
    showlegend=False, hoverinfo="skip",
), row=2, col=1)

# ── Panel 4: composición top-10 ocupados ─────────────────────────────
top10 = df.nlargest(10, "ocupados").sort_values("ocupados")
fig.add_trace(go.Bar(
    y=top10["short"], x=top10["no_ocupados"],
    name="No ocupados", orientation="h",
    marker_color="#1a472a", opacity=0.85,
    hovertemplate="<b>%{y}</b><br>No ocupados: %{x:,.0f}<extra></extra>",
), row=2, col=2)
fig.add_trace(go.Bar(
    y=top10["short"], x=top10["ocupados"],
    name="Ocupados", orientation="h",
    marker_color=C_OCU, opacity=0.85,
    hovertemplate="<b>%{y}</b><br>Ocupados: %{x:,.0f}<extra></extra>",
), row=2, col=2)

# ══════════════════════════════════════════════════════════════════════
# 4. LAYOUT
# ══════════════════════════════════════════════════════════════════════
fig.update_layout(
    title=dict(
        text="<b>Trabajo Infantil vs Matrícula Escolar — México 2022</b>",
        font=dict(size=17, color=TEXT), x=0.5,
    ),
    height=1000,
    paper_bgcolor=PAPER,
    plot_bgcolor=BG,
    font=dict(color=TEXT, size=10),
    barmode="group",
    legend=dict(bgcolor=PAPER, bordercolor=GRID, borderwidth=1,
                x=0.0, y=1.04, orientation="h", font=dict(size=9)),
    margin=dict(t=80, b=30, l=10, r=10),
)

for r, c in [(1,1),(1,2),(2,1),(2,2)]:
    fig.update_xaxes(gridcolor=GRID, zerolinecolor=GRID, row=r, col=c)
    fig.update_yaxes(gridcolor=GRID, zerolinecolor=GRID,
                     tickfont=dict(size=8), row=r, col=c)
fig.update_annotations(font=dict(color=TEXT, size=11))

fig.show()
# fig.write_html("trabajo_vs_educacion.html")
# %%
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ══════════════════════════════════════════════════════════════════════
# 1. CONSTRUIR DATASET
# ══════════════════════════════════════════════════════════════════════

# — Ocupados (ENTI 2022) —
ocu_raw = pd.read_csv("../datos/cuadro4_6_pobSegun_condición_ocupación.csv",
                      header=None, encoding="utf-8")
ocu = ocu_raw.iloc[13:45, [0, 1, 3]].copy()
ocu.columns = ["estado", "poblacion_5_17", "ocupados"]
ocu["estado"] = ocu["estado"].astype(str).str.strip()
for c in ["poblacion_5_17", "ocupados"]:
    ocu[c] = pd.to_numeric(ocu[c].astype(str).str.replace(",", ""), errors="coerce")
ocu["porc_ocupados"] = ocu["ocupados"] / ocu["poblacion_5_17"] * 100

# — Abandono (porcentajes_unificados, año 2022) —
aban = pd.read_csv("../datos/porcentajes_unificados.csv")
for col in aban.columns[2:]:
    aban[col] = pd.to_numeric(aban[col].astype(str).str.replace(",", ""), errors="coerce")
aban = aban[(aban["anio"] == 2022) & (~aban["estado"].str.contains("Estados Unidos"))]
aban = aban[["estado", "tasa_abandono_primaria", "tasa_abandono_secundaria"]].copy()

# — Merge —
df = pd.merge(ocu, aban, on="estado")
df["tasa_abandono_conjunta"] = (df["tasa_abandono_primaria"] + df["tasa_abandono_secundaria"]) / 2

state_short = {
    'Aguascalientes':'AGS','Baja California':'BC','Baja California Sur':'BCS',
    'Campeche':'CAM','Chiapas':'CHIS','Chihuahua':'CHIH','Ciudad de México':'CDMX',
    'Coahuila de Zaragoza':'COAH','Colima':'COL','Durango':'DGO',
    'Guanajuato':'GTO','Guerrero':'GRO','Hidalgo':'HGO','Jalisco':'JAL',
    'México':'MEX','Michoacán de Ocampo':'MICH','Morelos':'MOR','Nayarit':'NAY',
    'Nuevo León':'NL','Oaxaca':'OAX','Puebla':'PUE','Querétaro':'QRO',
    'Quintana Roo':'QROO','San Luis Potosí':'SLP','Sinaloa':'SIN','Sonora':'SON',
    'Tabasco':'TAB','Tamaulipas':'TAMPS','Tlaxcala':'TLAX',
    'Veracruz de Ignacio de la Llave':'VER','Yucatán':'YUC','Zacatecas':'ZAC',
}
df["short"] = df["estado"].map(state_short).fillna(df["estado"])

# ══════════════════════════════════════════════════════════════════════
# 2. PALETA
# ══════════════════════════════════════════════════════════════════════
BG, PAPER, GRID, TEXT = "#0D1117", "#161B22", "#21262D", "#E6EDF3"
C_OCU  = "#E63946"
C_PRIM = "#457B9D"
C_SEC  = "#2EC4B6"
C_CONJ = "#F4A261"

# ══════════════════════════════════════════════════════════════════════
# 3. FIGURA — 3 paneles
# ══════════════════════════════════════════════════════════════════════
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        "% Ocupados vs Tasa abandono primaria",
        "% Ocupados vs Tasa abandono secundaria",
        "% Ocupados vs Abandono conjunto (promedio prim+sec)",
        "Ranking: % Ocupados y abandono conjunto por estado",
    ),
    specs=[[{"type":"scatter"},{"type":"scatter"}],
           [{"type":"scatter"},{"type":"bar"}]],
    vertical_spacing=0.16,
    horizontal_spacing=0.10,
)

# helper: línea de tendencia
def add_trend(fig, x, y, color, row, col):
    mask = ~np.isnan(x) & ~np.isnan(y)
    if mask.sum() < 2:
        return
    m, b = np.polyfit(x[mask], y[mask], 1)
    xl = np.linspace(x[mask].min(), x[mask].max(), 100)
    fig.add_trace(go.Scatter(
        x=xl, y=m*xl+b, mode="lines",
        line=dict(color=color, width=1.5, dash="dot"),
        showlegend=False, hoverinfo="skip",
    ), row=row, col=col)
    # correlación
    r = np.corrcoef(x[mask], y[mask])[0,1]
    return r

# ── Panel 1: ocupados vs abandono primaria ────────────────────────────
r1 = add_trend(fig, df["porc_ocupados"].values, df["tasa_abandono_primaria"].values, C_PRIM, 1, 1)
fig.add_trace(go.Scatter(
    x=df["porc_ocupados"], y=df["tasa_abandono_primaria"],
    mode="markers+text", text=df["short"],
    textposition="top center", textfont=dict(size=7.5, color=TEXT),
    marker=dict(
        size=10, color=df["porc_ocupados"],
        colorscale=[[0,"#1a472a"],[0.5,"#f4d35e"],[1,C_OCU]],
        showscale=False, line=dict(width=0.5, color=GRID),
    ),
    hovertemplate="<b>%{text}</b><br>% Ocupados: %{x:.1f}%<br>Abandono prim: %{y:.1f}%<extra></extra>",
    name=f"r = {r1:.2f}",
), row=1, col=1)

# ── Panel 2: ocupados vs abandono secundaria ──────────────────────────
r2 = add_trend(fig, df["porc_ocupados"].values, df["tasa_abandono_secundaria"].values, C_SEC, 1, 2)
fig.add_trace(go.Scatter(
    x=df["porc_ocupados"], y=df["tasa_abandono_secundaria"],
    mode="markers+text", text=df["short"],
    textposition="top center", textfont=dict(size=7.5, color=TEXT),
    marker=dict(
        size=10, color=df["porc_ocupados"],
        colorscale=[[0,"#1a472a"],[0.5,"#f4d35e"],[1,C_OCU]],
        showscale=False, line=dict(width=0.5, color=GRID),
    ),
    hovertemplate="<b>%{text}</b><br>% Ocupados: %{x:.1f}%<br>Abandono sec: %{y:.1f}%<extra></extra>",
    name=f"r = {r2:.2f}",
), row=1, col=2)

# ── Panel 3: ocupados vs abandono conjunto ────────────────────────────
r3 = add_trend(fig, df["porc_ocupados"].values, df["tasa_abandono_conjunta"].values, C_CONJ, 2, 1)
fig.add_trace(go.Scatter(
    x=df["porc_ocupados"], y=df["tasa_abandono_conjunta"],
    mode="markers+text", text=df["short"],
    textposition="top center", textfont=dict(size=7.5, color=TEXT),
    marker=dict(
        size=df["ocupados"] / df["ocupados"].max() * 28 + 7,  # burbuja = volumen
        color=df["tasa_abandono_conjunta"],
        colorscale=[[0,"#0a3d62"],[0.5,"#60a3bc"],[1,C_CONJ]],
        showscale=True,
        colorbar=dict(
            title=dict(text="Abandono\nconjunto %", font=dict(color=TEXT, size=8)),
            tickfont=dict(color=TEXT, size=8),
            len=0.35, x=0.46, y=0.17, thickness=12,
        ),
        line=dict(width=0.5, color=GRID),
    ),
    hovertemplate=(
        "<b>%{text}</b><br>"
        "% Ocupados: %{x:.1f}%<br>"
        "Abandono conjunto: %{y:.2f}%<extra></extra>"
    ),
    name=f"r = {r3:.2f}",
), row=2, col=1)

# ── Panel 4: ranking barras dobles ────────────────────────────────────
df_rank = df.sort_values("porc_ocupados", ascending=True)
fig.add_trace(go.Bar(
    y=df_rank["short"], x=df_rank["porc_ocupados"],
    name="% Ocupados", orientation="h",
    marker_color=C_OCU, opacity=0.85,
    hovertemplate="<b>%{y}</b><br>% Ocupados: %{x:.1f}%<extra></extra>",
), row=2, col=2)
fig.add_trace(go.Bar(
    y=df_rank["short"], x=df_rank["tasa_abandono_conjunta"],
    name="Abandono conjunto %", orientation="h",
    marker_color=C_CONJ, opacity=0.85,
    hovertemplate="<b>%{y}</b><br>Abandono: %{x:.2f}%<extra></extra>",
), row=2, col=2)

# ══════════════════════════════════════════════════════════════════════
# 4. ANOTACIONES de correlación
# ══════════════════════════════════════════════════════════════════════
for row, col, r, label in [
    (1, 1, r1, "prim"), (1, 2, r2, "sec"), (2, 1, r3, "conjunta")
]:
    fig.add_annotation(
        text=f"r = {r:.2f}",
        xref=f"x{'' if (row==1 and col==1) else [None,'','2','3','4'][(row-1)*2+col]}",
        yref=f"y{'' if (row==1 and col==1) else [None,'','2','3','4'][(row-1)*2+col]}",
        x=0.95, y=0.95, xanchor="right", yanchor="top",
        showarrow=False,
        font=dict(color=TEXT, size=11),
        bgcolor=PAPER, bordercolor=GRID, borderwidth=1,
        row=row, col=col,
    )

# ══════════════════════════════════════════════════════════════════════
# 5. LAYOUT
# ══════════════════════════════════════════════════════════════════════
fig.update_layout(
    title=dict(
        text="<b>Trabajo Infantil (% Ocupados) vs Abandono Escolar — México 2022</b>",
        font=dict(size=17, color=TEXT), x=0.5,
    ),
    height=950,
    paper_bgcolor=PAPER,
    plot_bgcolor=BG,
    font=dict(color=TEXT, size=10),
    barmode="group",
    legend=dict(
        bgcolor=PAPER, bordercolor=GRID, borderwidth=1,
        x=0.0, y=1.05, orientation="h", font=dict(size=9),
    ),
    margin=dict(t=80, b=30, l=10, r=120),
)

for r, c in [(1,1),(1,2),(2,1),(2,2)]:
    fig.update_xaxes(gridcolor=GRID, zerolinecolor=GRID, row=r, col=c)
    fig.update_yaxes(gridcolor=GRID, zerolinecolor=GRID, row=r, col=c)
fig.update_xaxes(title_text="% Niños ocupados (5-17 años)", row=1, col=1)
fig.update_xaxes(title_text="% Niños ocupados (5-17 años)", row=1, col=2)
fig.update_xaxes(title_text="% Niños ocupados (5-17 años)", row=2, col=1)
fig.update_yaxes(title_text="Tasa abandono primaria (%)", row=1, col=1)
fig.update_yaxes(title_text="Tasa abandono secundaria (%)", row=1, col=2)
fig.update_yaxes(title_text="Abandono conjunto promedio (%)", row=2, col=1)
fig.update_yaxes(tickfont=dict(size=8.5), row=2, col=2)
fig.update_annotations(font=dict(color=TEXT, size=11))

fig.show()
# fig.write_html("ocupados_vs_abandono.html")
# %%
# Al final de tu código, después de fig.show(), agrega esto:

import numpy as np
from scipy import stats

# ── Calcular correlaciones de Pearson ────────────────────────────────
variables = [
    ("tasa_abandono_primaria",   "Abandono Primaria"),
    ("tasa_abandono_secundaria", "Abandono Secundaria"),
    ("tasa_abandono_conjunta",   "Abandono Conjunto"),
]

print("=" * 60)
print("  CORRELACIÓN DE PEARSON — % Ocupados vs Abandono Escolar")
print("=" * 60)
print()
print("  Fórmula:")
print()
print("         Σ [(xᵢ - x̄)(yᵢ - ȳ)]")
print("  r = ─────────────────────────────")
print("       √[Σ(xᵢ-x̄)²] · √[Σ(yᵢ-ȳ)²]")
print()
print("  Donde:")
print("    xᵢ = % ocupados del estado i")
print("    yᵢ = tasa de abandono del estado i")
print("    x̄  = promedio nacional de % ocupados")
print("    ȳ  = promedio nacional de tasa de abandono")
print()
print("-" * 60)
print(f"  {'Variable':<25} {'r':>6}  {'p-valor':>10}  {'Interpretación'}")
print("-" * 60)

x = df["porc_ocupados"].values

for col, label in variables:
    y = df[col].values
    mask = ~np.isnan(x) & ~np.isnan(y)
    r, p = stats.pearsonr(x[mask], y[mask])

    if abs(r) >= 0.7:
        interp = "Correlación fuerte"
    elif abs(r) >= 0.4:
        interp = "Correlación moderada"
    elif abs(r) >= 0.2:
        interp = "Correlación débil"
    else:
        interp = "Sin correlación"

    sig = "✓ significativo" if p < 0.05 else "✗ no significativo"
    print(f"  {label:<25} {r:>6.3f}  {p:>10.4f}  {interp} ({sig})")

print("-" * 60)
print()

# ── Desglose paso a paso para abandono conjunto ───────────────────────
y = df["tasa_abandono_conjunta"].values
mask = ~np.isnan(x) & ~np.isnan(y)
xm, ym = x[mask], y[mask]
x_bar, y_bar = xm.mean(), ym.mean()

numerador   = np.sum((xm - x_bar) * (ym - y_bar))
denom_x     = np.sqrt(np.sum((xm - x_bar)**2))
denom_y     = np.sqrt(np.sum((ym - y_bar)**2))
r_manual    = numerador / (denom_x * denom_y)

print("  Cálculo paso a paso — % Ocupados vs Abandono Conjunto:")
print()
print(f"    x̄  (media % ocupados)      = {x_bar:.4f}%")
print(f"    ȳ  (media abandono conj.)  = {y_bar:.4f}%")
print(f"    Σ[(xᵢ-x̄)(yᵢ-ȳ)]          = {numerador:.4f}")
print(f"    √Σ(xᵢ-x̄)²                 = {denom_x:.4f}")
print(f"    √Σ(yᵢ-ȳ)²                 = {denom_y:.4f}")
print(f"    r = {numerador:.4f} / ({denom_x:.4f} × {denom_y:.4f})")
print(f"    r = {numerador:.4f} / {denom_x * denom_y:.4f}")
print(f"    r = {r_manual:.4f}")
print()
print("  Escala de interpretación:")
print("    |r| ≥ 0.70  →  Fuerte    |  |r| 0.40–0.69  →  Moderada")
print("    |r| 0.20–0.39  →  Débil  |  |r| < 0.20     →  Sin correlación")
print("=" * 60)
# %%
