#%%
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
# %%
df = pd.read_csv('../datos/porcentajes.csv')
df = df[df['estado'] != 'Estados Unidos Mexicanos']
#%%
# Grafica 1
años = sorted(df['anio'].unique())

# 2. Crear la figura base de Plotly (Graph Objects permite más control)
fig = go.Figure()

# 3. Añadir trazas (barras) para cada año
# Cada año tendrá dos trazas: una para 3-15 años y otra para 16-21 años
for año in años:
    df_anio = df[df['anio'] == año].sort_values('porc_tasa_inasistencia_3_15', ascending=True)
    
    # Barra de Niñez (3-15 años)
    fig.add_trace(go.Bar(
        y=df_anio['estado'],
        x=df_anio['porc_tasa_inasistencia_3_15'],
        name='Infancias (3-15 años)',
        orientation='h',
        marker_color="#0860ED", 
        visible=(año == años[-1]) # Solo el año más reciente (2022) visible al inicio
    ))
    
    # Barra de Adolescencia/Juventud (16-21 años)
    fig.add_trace(go.Bar(
        y=df_anio['estado'],
        x=df_anio['porc_tasa_inasistencia_16_21'],
        name='Juventud (16-21 años)',
        orientation='h',
        marker_color="#F3487E", 
        visible=(año == años[-1])
    ))

# 4. Crear los botones para el menú desplegable
botones = []
for i, año in enumerate(años):
    # Definir qué trazas son visibles para este año
    # Como agregamos 2 trazas por año, calculamos su visibilidad:
    visibilidad = [False] * (len(años) * 2)
    visibilidad[i*2] = True      # Barra 3-15
    visibilidad[i*2 + 1] = True  # Barra 16-21
    
    boton = dict(
        label=str(año),
        method="update",
        args=[{"visible": visibilidad},
              {"title": f"<b>Inasistencia Escolar en {año}</b>"}]
    )
    botones.append(boton)

# 5. Configurar el diseño final y el menú
fig.update_layout(
    updatemenus=[dict(
        active=len(años)-1, # Por defecto selecciona el último año
        buttons=botones,
        direction="down",
        showactive=True,
        x=1,
        xanchor="right",
        y=1.1,
        yanchor="top"
    )],
    barmode='group',
    title=f"<b>Inasistencia Escolar en {años[-1]}</b>",
    height=900,
    template="plotly_white",
    xaxis=dict(title="Porcentaje de Inasistencia (%)", range=[0, 75]), # Rango fijo para notar el cambio
    yaxis=dict(title=""),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    margin=dict(l=150, r=20, t=100, b=50)
)

fig.show()

 
# %%
# Grafica 2
años = sorted(df['anio'].unique())
fig = go.Figure()

# Definir categorías y colores (de lo más estable a lo más crítico)
categorias = {
    'porc_seg_aliment': {'nombre': 'Seguridad Alimentaria', 'color': '#2E7D32'}, # Verde
    'porc_inseg_aliment_leve': {'nombre': 'Inseguridad Leve', 'color': '#FBC02D'}, # Amarillo
    'porc_inseg_aliment_mode': {'nombre': 'Inseguridad Moderada', 'color': '#EF6C00'}, # Naranja
    'porc_inseg_aliment_seve': {'nombre': 'Inseguridad Severa (Hambre)', 'color': '#C62828'} # Rojo
}

# 2. Generar trazas por cada año y categoría
for año in años:
    # Ordenar estados por Inseguridad Severa para que los más críticos queden arriba
    df_anio = df[df['anio'] == año].sort_values('porc_inseg_aliment_seve', ascending=True)
    
    for col, info in categorias.items():
        fig.add_trace(go.Bar(
            y=df_anio['estado'],
            x=df_anio[col],
            name=info['nombre'],
            orientation='h',
            marker_color=info['color'],
            visible=(año == años[-1]), # Solo mostrar el año más reciente al inicio
            hovertemplate=f"<b>%{{y}}</b><br>{info['nombre']}: %{{x}}%<extra></extra>"
        ))

# 3. Crear el menú de años
# Cada año tiene 4 trazas (Seguridad + 3 niveles de Inseguridad)
botones_anio = []
for i, año in enumerate(años):
    visibilidad = [False] * (len(años) * 4)
    # Activar las 4 trazas correspondientes a este año
    inicio = i * 4
    visibilidad[inicio : inicio + 4] = [True] * 4
    
    botones_anio.append(dict(
        label=f"Año {año}",
        method="update",
        args=[{"visible": visibilidad},
              {"title": f"<b>Distribución Alimentaria en {año}: ¿Quiénes pueden comer hoy?</b>"}]
    ))

# 4. Diseño de la gráfica
fig.update_layout(
    updatemenus=[dict(
        buttons=botones_anio,
        direction="down",
        showactive=True,
        x=1, xanchor="right", y=1.1
    )],
    barmode='stack', 
    title=f"<b>¿Quiénes pueden comer hoy?  {años[-1]}</b><br><sup>Los estados arriba tienen los niveles más altos de hambre severa.</sup>",
    height=900,
    template="plotly_white",
    xaxis=dict(title="Porcentaje de la Población (%)", range=[0, 100]),
    yaxis=dict(title=""),
    legend=dict(
        orientation="h",
        yanchor="bottom", y=1.02,
        xanchor="center", x=0.5
    ),
    margin=dict(l=150, r=20, t=100, b=50)
)

fig.show()
# %%
## Grafica 3
# 2. Cargar el GeoJSON local
with open('../Datos/states_simple.geojson', 'r', encoding='utf-8') as f:
    mexico_geojson = json.load(f)

# 4. Crear el mapa
fig = px.choropleth(
    df,
    geojson=mexico_geojson,
    locations='estado',       # Columna en tu DataFrame
    featureidkey='properties.NOMGEO',  # ¡OJO! Verifica si en tu archivo es 'name' o 'NOM_ENT'
    color='porc_inseg_aliment_seve',
    animation_frame='anio',        # El slider de años
    color_continuous_scale="Reds",
    range_color=[0, 25],           # Ajustado basado en tus datos (Tabasco ~21%)
    labels={'porc_inseg_aliment_seve': 'Hambre Severa (%)', 'estado': 'Estado'},
    title='<b>Población con Inseguridad Alimentaria Severa</b>'
)

fig.update_geos(
    fitbounds="locations", # Esto obliga al mapa a hacer zoom solo a los estados
    visible=False          # Oculta el resto del mundo y líneas innecesarias
)

fig.update_layout(
    height=600,             # Ajusta la altura
    margin={"r":0,"t":50,"l":0,"b":0}, # Elimina márgenes extra
    coloraxis_colorbar=dict(
        title="Hambre (%)",
        thicknessmode="pixels", thickness=15, # Barra más delgada
        lenmode="fraction", len=0.6,          # Reducimos el largo al 60% de la altura del cuadro
        yanchor="middle", y=0.5,              # Centramos la barra verticalmente
        xanchor="left", x=1.02                # La pegamos un poco más al mapa
    )
)

fig.show()
# %%
