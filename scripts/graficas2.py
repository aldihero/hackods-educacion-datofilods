import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

df = pd.read_csv("../datos/percepcion-inseguridad.csv")

# ── 1. Nacional promedio por año ──────────────────────────────────────────────
national = (
    df.groupby("anio")[["prct_Total", "prct_Hombres", "prct_Mujeres"]]
    .mean()
    .reset_index()
)

# ── 2. Últimos datos disponibles por estado (2024) ────────────────────────────
latest = df[df["anio"] == df["anio"].max()].sort_values("prct_Total", ascending=True)

# ── 3. Brecha de género (Mujeres − Hombres) por año ───────────────────────────
df["brecha"] = df["prct_Mujeres"] - df["prct_Hombres"]
brecha_nacional = df.groupby("anio")["brecha"].mean().reset_index()

# ── Paleta ────────────────────────────────────────────────────────────────────
COLOR_TOTAL    = "#E63946"
COLOR_HOMBRES  = "#457B9D"
COLOR_MUJERES  = "#F4A261"
BG             = "#0D1117"
PAPER          = "#161B22"
GRID           = "#21262D"
TEXT           = "#E6EDF3"

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        "Percepción de inseguridad nacional promedio (2011–2024)",
        "Percepción de inseguridad por estado — último año disponible (2024)",
        "Brecha de género en percepción de inseguridad (Mujeres − Hombres, pts %)",
        "",   # espacio vacío
    ),
    column_widths=[0.45, 0.55],
    row_heights=[0.5, 0.5],
    specs=[[{}, {}], [{}, {}]],
)

# ── Panel 1: líneas nacionales ────────────────────────────────────────────────
for col, color, name in [
    ("prct_Total",    COLOR_TOTAL,   "Total"),
    ("prct_Hombres",  COLOR_HOMBRES, "Hombres"),
    ("prct_Mujeres",  COLOR_MUJERES, "Mujeres"),
]:
    fig.add_trace(
        go.Scatter(
            x=national["anio"], y=national[col],
            mode="lines+markers",
            name=name,
            line=dict(color=color, width=2.5),
            marker=dict(size=6),
            hovertemplate="%{y:.1f}%<extra>" + name + "</extra>",
        ),
        row=1, col=1,
    )

# ── Panel 2: barras horizontales por estado ───────────────────────────────────
### esta hay que guardarla 
fig.add_trace(
    go.Bar(
        x=latest["prct_Hombres"],
        y=latest["entidad_etiqueta"],
        orientation="h",
        name="Hombres 2024",
        marker_color=COLOR_HOMBRES,
        opacity=0.85,
        hovertemplate="%{y}: %{x:.1f}%<extra>Hombres</extra>",
    ),
    row=1, col=2,
)
fig.add_trace(
    go.Bar(
        x=latest["prct_Mujeres"],
        y=latest["entidad_etiqueta"],
        orientation="h",
        name="Mujeres 2024",
        marker_color=COLOR_MUJERES,
        opacity=0.85,
        hovertemplate="%{y}: %{x:.1f}%<extra>Mujeres</extra>",
    ),
    row=1, col=2,
)

# ── Panel 3: brecha de género ─────────────────────────────────────────────────
fig.add_trace(
    go.Bar(
        x=brecha_nacional["anio"],
        y=brecha_nacional["brecha"],
        name="Brecha (M−H)",
        marker_color=[COLOR_MUJERES if v >= 0 else COLOR_HOMBRES for v in brecha_nacional["brecha"]],
        hovertemplate="Año %{x}: +%{y:.1f} pts<extra></extra>",
    ),
    row=2, col=1,
)
fig.add_hline(y=0, line_dash="dot", line_color=GRID, row=2, col=1)

# ── Panel 4: heatmap estado × año ────────────────────────────────────────────
pivot = df.pivot_table(index="entidad_etiqueta", columns="anio", values="prct_Total")
pivot = pivot.sort_values(pivot.columns[-1], ascending=False)

fig.add_trace(
    go.Heatmap(
        z=pivot.values,
        x=pivot.columns.tolist(),
        y=pivot.index.tolist(),
        colorscale=[
            [0.0, "#1a472a"],
            [0.4, "#f4d35e"],
            [1.0, "#e63946"],
        ],
        colorbar=dict(
            title=dict(text="% inseg.", font=dict(color=TEXT, size=11)),  # ← correcto
            tickfont=dict(color=TEXT, size=10),
            x=1.01,
        ),
        hovertemplate="%{y} %{x}: %{z:.1f}%<extra></extra>",
        name="",
    ),
    row=2, col=2,
)

# ── Estilo global ─────────────────────────────────────────────────────────────
fig.update_layout(
    title=dict(
        text="<b>Percepción de Inseguridad en México — ENVIPE</b>",
        font=dict(size=20, color=TEXT),
        x=0.5,
    ),
    barmode="group",
    height=900,
    paper_bgcolor=PAPER,
    plot_bgcolor=BG,
    font=dict(color=TEXT, size=11),
    legend=dict(
        bgcolor=PAPER,
        bordercolor=GRID,
        borderwidth=1,
    ),
    margin=dict(t=80, b=40, l=20, r=20),
)

# ejes
for row, col in [(1,1),(2,1)]:
    fig.update_xaxes(gridcolor=GRID, zerolinecolor=GRID, row=row, col=col)
    fig.update_yaxes(gridcolor=GRID, zerolinecolor=GRID, row=row, col=col)

fig.update_xaxes(gridcolor=GRID, row=1, col=2)
fig.update_yaxes(gridcolor=GRID, tickfont=dict(size=9), row=1, col=2)
fig.update_xaxes(gridcolor=GRID, row=2, col=2)
fig.update_yaxes(gridcolor=GRID, tickfont=dict(size=9), row=2, col=2)

fig.update_annotations(font=dict(color=TEXT, size=12))

fig.show()
# fig.write_html("percepcion_inseguridad.html")  # para guardar

#%%
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Carga y limpieza ──────────────────────────────────────────────────────────
df = pd.read_csv("../datos/porcentajes_unificados.csv")

# Quitar filas que son el nacional y el año 2021 (mayormente vacío)
df = df[~df["estado"].str.contains("Estados Unidos Mexicanos")]
df = df[df["anio"] != 2021]

# Limpiar columnas numéricas con comas (p.ej. "1,532.4")
for col in df.columns[2:]:
    df[col] = pd.to_numeric(
        df[col].astype(str).str.replace(",", ""), errors="coerce"
    )

# ── Paleta ────────────────────────────────────────────────────────────────────
BG       = "#0D1117"
PAPER    = "#161B22"
GRID     = "#21262D"
TEXT     = "#E6EDF3"
C1       = "#E63946"   # rojo  — pobreza/inseg alimentaria
C2       = "#457B9D"   # azul  — sin primaria
C3       = "#2EC4B6"   # verde — inasistencia
C4       = "#F4A261"   # naranja — sin secundaria
C5       = "#A8DADC"   # celeste — abandono

AÑOS     = sorted(df["anio"].unique())
MARKERS  = ["circle", "square", "diamond", "cross"]

# ── Figura ────────────────────────────────────────────────────────────────────
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        "Scatter: % Sin primaria vs Inseguridad alimentaria severa (por estado, 2022)",
        "Heatmap: Inasistencia escolar 3-15 años por estado y año",
        "Líneas: Evolución nacional promedio — educación y pobreza alimentaria",
        "Burbujas: Sin secundaria vs Abandono secundaria vs Inseg. alim. severa (2022)",
    ),
    column_widths=[0.5, 0.5],
    row_heights=[0.48, 0.52],
    specs=[[{"type": "scatter"}, {"type": "heatmap"}],
           [{"type": "scatter"}, {"type": "scatter"}]],
)

# ══════════════════════════════════════════════════════════════════════════════
# PANEL 1 — Scatter: % sin primaria vs inseg. alimentaria severa (2022)
# ══════════════════════════════════════════════════════════════════════════════
d22 = df[df["anio"] == 2022].dropna(subset=["porc_pob_16mas_sin_prim", "porc_inseg_aliment_seve"])

fig.add_trace(
    go.Scatter(
        x=d22["porc_pob_16mas_sin_prim"],
        y=d22["porc_inseg_aliment_seve"],
        mode="markers+text",
        text=d22["estado"].str.replace(" de Ignacio de la Llave", "")
                          .str.replace(" de Ocampo", "")
                          .str.replace(" de Zaragoza", ""),
        textposition="top center",
        textfont=dict(size=8, color=TEXT),
        marker=dict(
            size=10,
            color=d22["porc_inseg_aliment_seve"],
            colorscale=[[0, "#1a472a"], [0.5, "#f4d35e"], [1, C1]],
            showscale=False,
            line=dict(width=0.5, color=GRID),
        ),
        hovertemplate="<b>%{text}</b><br>Sin primaria: %{x:.1f}%<br>Inseg. severa: %{y:.1f}%<extra></extra>",
        name="",
        showlegend=False,
    ),
    row=1, col=1,
)

# Línea de tendencia simple (regresión lineal manual)
import numpy as np
x_vals = d22["porc_pob_16mas_sin_prim"].values
y_vals = d22["porc_inseg_aliment_seve"].values
mask   = ~np.isnan(x_vals) & ~np.isnan(y_vals)
m, b   = np.polyfit(x_vals[mask], y_vals[mask], 1)
x_line = np.linspace(x_vals[mask].min(), x_vals[mask].max(), 100)
fig.add_trace(
    go.Scatter(
        x=x_line, y=m * x_line + b,
        mode="lines",
        line=dict(color=C1, width=1.5, dash="dot"),
        showlegend=False,
        hoverinfo="skip",
    ),
    row=1, col=1,
)

# ══════════════════════════════════════════════════════════════════════════════
# PANEL 2 — Heatmap: inasistencia escolar 3-15 por estado y año
# ══════════════════════════════════════════════════════════════════════════════
pivot = df.pivot_table(
    index="estado", columns="anio", values="porc_tasa_inasistencia_3_15"
)
pivot.index = (pivot.index
               .str.replace(" de Ignacio de la Llave", "")
               .str.replace(" de Ocampo", "")
               .str.replace(" de Zaragoza", ""))
pivot = pivot.sort_values(2022, ascending=False)

fig.add_trace(
    go.Heatmap(
        z=pivot.values,
        x=[str(c) for c in pivot.columns],
        y=pivot.index.tolist(),
        colorscale=[[0, "#1a472a"], [0.5, "#f4d35e"], [1, C1]],
        colorbar=dict(
            title=dict(text="% inasist.", font=dict(color=TEXT, size=10)),
            tickfont=dict(color=TEXT, size=9),
            x=1.01,
        ),
        hovertemplate="%{y} %{x}: %{z:.1f}%<extra></extra>",
        name="",
    ),
    row=1, col=2,
)

# ══════════════════════════════════════════════════════════════════════════════
# PANEL 3 — Líneas: evolución promedio nacional
# ══════════════════════════════════════════════════════════════════════════════
nacional = (
    df.groupby("anio")[
        ["porc_pob_16mas_sin_prim", "porc_pob_16mas_sin_secu",
         "porc_inseg_aliment_seve", "porc_tasa_inasistencia_3_15",
         "tasa_abandono_secundaria"]
    ].mean().reset_index()
)

series = [
    ("porc_pob_16mas_sin_prim",      C2,  "Sin primaria (16+)"),
    ("porc_pob_16mas_sin_secu",      C4,  "Sin secundaria (16+)"),
    ("porc_inseg_aliment_seve",      C1,  "Inseg. alim. severa"),
    ("porc_tasa_inasistencia_3_15",  C3,  "Inasistencia 3-15 años"),
    ("tasa_abandono_secundaria",     C5,  "Abandono secundaria"),
]

for col, color, label in series:
    fig.add_trace(
        go.Scatter(
            x=nacional["anio"], y=nacional[col],
            mode="lines+markers",
            name=label,
            line=dict(color=color, width=2.2),
            marker=dict(size=7),
            hovertemplate=f"{label}: %{{y:.1f}}%<extra></extra>",
        ),
        row=2, col=1,
    )

# ══════════════════════════════════════════════════════════════════════════════
# PANEL 4 — Burbujas: sin secundaria vs abandono secundaria, burbuja = inseg severa
# ══════════════════════════════════════════════════════════════════════════════
d22b = df[df["anio"] == 2022].dropna(
    subset=["porc_pob_16mas_sin_secu", "tasa_abandono_secundaria", "porc_inseg_aliment_seve"]
)

fig.add_trace(
    go.Scatter(
        x=d22b["porc_pob_16mas_sin_secu"],
        y=d22b["tasa_abandono_secundaria"],
        mode="markers+text",
        text=d22b["estado"].str.replace(" de Ignacio de la Llave", "")
                           .str.replace(" de Ocampo", "")
                           .str.replace(" de Zaragoza", ""),
        textposition="top center",
        textfont=dict(size=8, color=TEXT),
        marker=dict(
            size=d22b["porc_inseg_aliment_seve"] * 3.5,
            color=d22b["porc_inseg_aliment_seve"],
            colorscale=[[0, C3], [0.5, C4], [1, C1]],
            showscale=True,
            colorbar=dict(
                title=dict(text="Inseg.\nsevera %", font=dict(color=TEXT, size=9)),
                tickfont=dict(color=TEXT, size=8),
                x=1.14,
                len=0.45,
                y=0.2,
            ),
            line=dict(width=0.5, color=GRID),
            opacity=0.85,
        ),
        hovertemplate=(
            "<b>%{text}</b><br>"
            "Sin secundaria: %{x:.1f}%<br>"
            "Abandono sec.: %{y:.1f}%<br>"
            "Inseg. severa: %{marker.color:.1f}%<extra></extra>"
        ),
        showlegend=False,
        name="",
    ),
    row=2, col=2,
)

# ══════════════════════════════════════════════════════════════════════════════
# Estilo global
# ══════════════════════════════════════════════════════════════════════════════
fig.update_layout(
    title=dict(
        text="<b>Pobreza Educativa vs Inseguridad Alimentaria — México (2016–2022)</b>",
        font=dict(size=19, color=TEXT),
        x=0.5,
    ),
    height=950,
    paper_bgcolor=PAPER,
    plot_bgcolor=BG,
    font=dict(color=TEXT, size=10),
    legend=dict(
        bgcolor=PAPER, bordercolor=GRID, borderwidth=1,
        x=0.01, y=0.44, font=dict(size=9),
    ),
    margin=dict(t=80, b=40, l=10, r=120),
)

for r, c in [(1,1),(2,1),(2,2)]:
    fig.update_xaxes(gridcolor=GRID, zerolinecolor=GRID, row=r, col=c)
    fig.update_yaxes(gridcolor=GRID, zerolinecolor=GRID, row=r, col=c)

fig.update_xaxes(title_text="% Pob. 16+ sin primaria", row=1, col=1)
fig.update_yaxes(title_text="% Inseg. alim. severa",   row=1, col=1)
fig.update_xaxes(title_text="% Pob. 16+ sin secundaria", row=2, col=2)
fig.update_yaxes(title_text="Tasa abandono secundaria (%)", row=2, col=2)

fig.update_xaxes(gridcolor=GRID, tickfont=dict(size=9), row=1, col=2)
fig.update_yaxes(gridcolor=GRID, tickfont=dict(size=8), row=1, col=2)
fig.update_annotations(font=dict(color=TEXT, size=11))

fig.show()
# fig.write_html("pobreza_educacion.html")

# %%
import json, pandas as pd, numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Cargar datos ──────────────────────────────────────────────────────────────
df = pd.read_csv("../datos/porcentajes_unificados.csv")
for col in df.columns[2:]:
    df[col] = pd.to_numeric(df[col].astype(str).str.replace(",", ""), errors="coerce")
df = df[~df["estado"].str.contains("Estados Unidos")]

# ── Mapeo a ISO y abreviaciones ───────────────────────────────────────────────
state_iso = {
    'Aguascalientes':'MX-AGU','Baja California':'MX-BCN','Baja California Sur':'MX-BCS',
    'Campeche':'MX-CAM','Chiapas':'MX-CHP','Chihuahua':'MX-CHH','Ciudad de México':'MX-CMX',
    'Coahuila de Zaragoza':'MX-COA','Colima':'MX-COL','Durango':'MX-DUR',
    'Guanajuato':'MX-GUA','Guerrero':'MX-GRO','Hidalgo':'MX-HID','Jalisco':'MX-JAL',
    'México':'MX-MEX','Michoacán de Ocampo':'MX-MIC','Morelos':'MX-MOR','Nayarit':'MX-NAY',
    'Nuevo León':'MX-NLE','Oaxaca':'MX-OAX','Puebla':'MX-PUE','Querétaro':'MX-QUE',
    'Quintana Roo':'MX-ROO','San Luis Potosí':'MX-SLP','Sinaloa':'MX-SIN','Sonora':'MX-SON',
    'Tabasco':'MX-TAB','Tamaulipas':'MX-TAM','Tlaxcala':'MX-TLA',
    'Veracruz de Ignacio de la Llave':'MX-VER','Yucatán':'MX-YUC','Zacatecas':'MX-ZAC',
}
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

df["iso"]   = df["estado"].map(state_iso)
df["short"] = df["estado"].map(state_short)
d22 = df[df["anio"] == 2022].dropna(subset=["iso"])

# ── GeoJSON México estados (simplificado) ─────────────────────────────────────
# Requiere el archivo states_simple.geojson con featureidkey="id"
# donde cada feature tiene "id": "MX-XXX"
# Si usas el archivo propio del usuario, asegúrate que los ids sean tipo "MX-AGU" etc.
# Aquí cargamos el archivo que tengas:
with open("../datos/states_simple.geojson") as f:
    geojson = json.load(f)

# ── Paleta ────────────────────────────────────────────────────────────────────
BG, PAPER, GRID, TEXT = "#0D1117", "#161B22", "#21262D", "#E6EDF3"
SCALES = {
    "car":  [[0,"#1a472a"],[0.5,"#f4d35e"],[1,"#E63946"]],
    "aban": [[0,"#0a3d62"],[0.5,"#60a3bc"],[1,"#fbc531"]],
}
VARS = [
    ("porc_carencia_6_11_y",      "car",  "Carencia educativa 6-11 años (%)"),
    ("porc_carencia_12_17_x",     "car",  "Carencia educativa 12-17 años (%)"),
    ("tasa_abandono_primaria",    "aban", "Tasa abandono primaria (%)"),
    ("tasa_abandono_secundaria",  "aban", "Tasa abandono secundaria (%)"),
]

# ══════════════════════════════════════════════════════════════════════════════
# FIGURA 1 — Cuatro mapas coropléticos (2022)
# ══════════════════════════════════════════════════════════════════════════════
fig1 = make_subplots(
    rows=2, cols=2,
    subplot_titles=[v[2] for v in VARS],
    specs=[[{"type":"choropleth"},{"type":"choropleth"}],
           [{"type":"choropleth"},{"type":"choropleth"}]],
    vertical_spacing=0.06, horizontal_spacing=0.04,
)
cb_x = [0.46, 1.01, 0.46, 1.01]
cb_y = [0.76, 0.76, 0.24, 0.24]

for i, (col, scale_key, label) in enumerate(VARS):
    r, c = (i//2)+1, (i%2)+1
    sub = d22.dropna(subset=[col])
    fig1.add_trace(
        go.Choropleth(
            geojson=geojson, locations=sub["iso"], z=sub[col],
            text=sub["short"], featureidkey='properties.NOMGEO',
            colorscale=SCALES[scale_key],
            colorbar=dict(
                title=dict(text="%", font=dict(color=TEXT, size=9)),
                tickfont=dict(color=TEXT, size=8),
                len=0.38, x=cb_x[i], y=cb_y[i], thickness=12,
            ),
            hovertemplate="<b>%{text}</b><br>" + label + ": %{z:.1f}%<extra></extra>",
            name=label,
        ),
        row=r, col=c,
    )
    fig1.update_geos(fitbounds="locations", visible=False, bgcolor=BG, row=r, col=c)

fig1.update_layout(
    title=dict(
        text="<b>Carencia Educativa y Abandono Escolar por Estado — 2022</b>",
        font=dict(size=17, color=TEXT), x=0.5,
    ),
    height=820, paper_bgcolor=PAPER, plot_bgcolor=BG,
    font=dict(color=TEXT, size=10),
    margin=dict(t=70, b=20, l=10, r=10),
)
fig1.update_annotations(font=dict(color=TEXT, size=11))

# ══════════════════════════════════════════════════════════════════════════════
# FIGURA 2 — Evolución + ranking + scatters comparativos
# ══════════════════════════════════════════════════════════════════════════════
fig2 = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        "Evolución nacional promedio por año",
        "Ranking top 10 — Carencia educativa 2022",
        "Scatter: Carencia 6-11 vs Abandono primaria",
        "Scatter: Carencia 12-17 vs Abandono secundaria",
    ),
    specs=[[{"type":"scatter"},{"type":"bar"}],
           [{"type":"scatter"},{"type":"scatter"}]],
    vertical_spacing=0.14, horizontal_spacing=0.12,
)

# Panel 1 — líneas
nacional = (df[df["anio"]!=2021].groupby("anio")
            [["porc_carencia_6_11_y","porc_carencia_12_17_y",
              "tasa_abandono_primaria","tasa_abandono_secundaria"]]
            .mean().reset_index())
for col, color, lab in zip(
    ["porc_carencia_6_11_y","porc_carencia_12_17_y","tasa_abandono_primaria","tasa_abandono_secundaria"],
    ["#E63946","#F4A261","#457B9D","#2EC4B6"],
    ["Carencia 6-11 años","Carencia 12-17 años","Abandono primaria","Abandono secundaria"],
):
    fig2.add_trace(go.Scatter(
        x=nacional["anio"], y=nacional[col], mode="lines+markers", name=lab,
        line=dict(color=color, width=2.3), marker=dict(size=7),
        hovertemplate=f"{lab}: %{{y:.1f}}%<extra></extra>",
    ), row=1, col=1)

# Panel 2 — ranking barras agrupadas
top10 = d22.nlargest(10, "porc_carencia_6_11_y").sort_values("porc_carencia_6_11_y")
for col, color, lab in [
    ("porc_carencia_6_11_y",  "#E63946", "Carencia 6-11"),
    ("porc_carencia_12_17_y", "#F4A261", "Carencia 12-17"),
]:
    fig2.add_trace(go.Bar(
        x=top10[col], y=top10["short"], orientation="h",
        name=lab, marker_color=color, opacity=0.85,
        hovertemplate="%{y}: %{x:.1f}%<extra></extra>",
    ), row=1, col=2)

# Panel 3 — scatter + tendencia
def scatter_with_trend(fig, xcol, ycol, row, col, color):
    sub = d22.dropna(subset=[xcol, ycol])
    fig.add_trace(go.Scatter(
        x=sub[xcol], y=sub[ycol], mode="markers+text", text=sub["short"],
        textposition="top center", textfont=dict(size=7.5, color=TEXT),
        marker=dict(size=9, color=sub[ycol], colorscale=SCALES["aban"],
                    showscale=False, line=dict(width=0.5, color=GRID)),
        hovertemplate="<b>%{text}</b><br>X: %{x:.1f}%<br>Y: %{y:.1f}%<extra></extra>",
        showlegend=False, name="",
    ), row=row, col=col)
    x, y = sub[xcol].values, sub[ycol].values
    mask = ~np.isnan(x) & ~np.isnan(y)
    if mask.sum() > 1:
        m, b = np.polyfit(x[mask], y[mask], 1)
        xl = np.linspace(x[mask].min(), x[mask].max(), 100)
        fig.add_trace(go.Scatter(x=xl, y=m*xl+b, mode="lines",
            line=dict(color=color, width=1.5, dash="dot"),
            showlegend=False, hoverinfo="skip"), row=row, col=col)

scatter_with_trend(fig2, "porc_carencia_6_11_y",  "tasa_abandono_primaria",    2, 1, "#E63946")
scatter_with_trend(fig2, "porc_carencia_12_17_y", "tasa_abandono_secundaria",  2, 2, "#457B9D")

fig2.update_layout(
    title=dict(
        text="<b>Análisis Comparativo: Carencia Educativa vs Abandono Escolar</b>",
        font=dict(size=17, color=TEXT), x=0.5,
    ),
    height=850, paper_bgcolor=PAPER, plot_bgcolor=BG,
    font=dict(color=TEXT, size=10), barmode="group",
    legend=dict(bgcolor=PAPER, bordercolor=GRID, borderwidth=1, font=dict(size=9)),
    margin=dict(t=70, b=30, l=10, r=10),
)
for r, c in [(1,1),(2,1),(2,2)]:
    fig2.update_xaxes(gridcolor=GRID, zerolinecolor=GRID, row=r, col=c)
    fig2.update_yaxes(gridcolor=GRID, zerolinecolor=GRID, row=r, col=c)
fig2.update_xaxes(gridcolor=GRID, row=1, col=2)
fig2.update_yaxes(gridcolor=GRID, tickfont=dict(size=8.5), row=1, col=2)
fig2.update_annotations(font=dict(color=TEXT, size=11))

fig1.show()
fig2.show()
# fig1.write_html("mapas_educacion.html")
# fig2.write_html("comparativas_educacion.html")
# %%
import json, pandas as pd, numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Cargar datos ──────────────────────────────────────────────────────────────
df = pd.read_csv("../datos/porcentajes_unificados.csv")
for col in df.columns[2:]:
    df[col] = pd.to_numeric(df[col].astype(str).str.replace(",", ""), errors="coerce")
df = df[~df["estado"].str.contains("Estados Unidos")]

# ── Mapeo a códigos INEGI (CVE_ENT) ──────────────────────────────────────────
# Tu GeoJSON usa "01", "02"... en properties.CVE_ENT
state_cve = {
    'Aguascalientes':'01',          'Baja California':'02',
    'Baja California Sur':'03',     'Campeche':'04',
    'Coahuila de Zaragoza':'05',    'Colima':'06',
    'Chiapas':'07',                 'Chihuahua':'08',
    'Ciudad de México':'09',        'Durango':'10',
    'Guanajuato':'11',              'Guerrero':'12',
    'Hidalgo':'13',                 'Jalisco':'14',
    'México':'15',                  'Michoacán de Ocampo':'16',
    'Morelos':'17',                 'Nayarit':'18',
    'Nuevo León':'19',              'Oaxaca':'20',
    'Puebla':'21',                  'Querétaro':'22',
    'Quintana Roo':'23',            'San Luis Potosí':'24',
    'Sinaloa':'25',                 'Sonora':'26',
    'Tabasco':'27',                 'Tamaulipas':'28',
    'Tlaxcala':'29',                'Veracruz de Ignacio de la Llave':'30',
    'Yucatán':'31',                 'Zacatecas':'32',
}
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

df["iso"]   = df["estado"].map(state_cve)   # ← ahora son "01", "02"...
df["short"] = df["estado"].map(state_short)
d22 = df[df["anio"] == 2022].dropna(subset=["iso"])

# ── Cargar GeoJSON ────────────────────────────────────────────────────────────
with open("../datos/states_simple.geojson") as f:
    geojson = json.load(f)

# ── Paleta ────────────────────────────────────────────────────────────────────
BG, PAPER, GRID, TEXT = "#0D1117", "#161B22", "#21262D", "#E6EDF3"
SCALES = {
    "car":  [[0,"#1a472a"],[0.5,"#f4d35e"],[1,"#E63946"]],
    "aban": [[0,"#0a3d62"],[0.5,"#60a3bc"],[1,"#fbc531"]],
}
VARS = [
    ("porc_carencia_6_11_y",      "car",  "Carencia educativa 6-11 años (%)"),
    ("porc_carencia_12_17_x",     "car",  "Carencia educativa 12-17 años (%)"),
    ("tasa_abandono_primaria",    "aban", "Tasa abandono primaria (%)"),
    ("tasa_abandono_secundaria",  "aban", "Tasa abandono secundaria (%)"),
]

# ══════════════════════════════════════════════════════════════════════════════
# FIGURA 1 — Cuatro mapas coropléticos (2022)
# ══════════════════════════════════════════════════════════════════════════════
fig1 = make_subplots(
    rows=2, cols=2,
    subplot_titles=[v[2] for v in VARS],
    specs=[[{"type":"choropleth"},{"type":"choropleth"}],
           [{"type":"choropleth"},{"type":"choropleth"}]],
    vertical_spacing=0.06, horizontal_spacing=0.04,
)
cb_x = [0.46, 1.01, 0.46, 1.01]
cb_y = [0.76, 0.76, 0.24, 0.24]

for i, (col, scale_key, label) in enumerate(VARS):
    r, c = (i//2)+1, (i%2)+1
    sub = d22.dropna(subset=[col])
    fig1.add_trace(
        go.Choropleth(
            geojson=geojson,
            locations=sub["iso"],
            z=sub[col],
            text=sub["short"],
            featureidkey="properties.CVE_ENT",   # ← CLAVE: apunta al campo correcto
            colorscale=SCALES[scale_key],
            colorbar=dict(
                title=dict(text="%", font=dict(color=TEXT, size=9)),
                tickfont=dict(color=TEXT, size=8),
                len=0.38, x=cb_x[i], y=cb_y[i], thickness=12,
            ),
            hovertemplate="<b>%{text}</b><br>" + label + ": %{z:.1f}%<extra></extra>",
            name=label,
        ),
        row=r, col=c,
    )
    fig1.update_geos(fitbounds="locations", visible=False, bgcolor=BG, row=r, col=c)

fig1.update_layout(
    title=dict(
        text="<b>Carencia Educativa y Abandono Escolar por Estado — 2022</b>",
        font=dict(size=17, color=TEXT), x=0.5,
    ),
    height=820, paper_bgcolor=PAPER, plot_bgcolor=BG,
    font=dict(color=TEXT, size=10),
    margin=dict(t=70, b=20, l=10, r=10),
)
fig1.update_annotations(font=dict(color=TEXT, size=11))
fig1.show()
# %%
