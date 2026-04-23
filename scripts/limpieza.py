#Script evaluado en: cuadro 26A 
#Porcentaje y número de personas en los componentes de rezago educativo, según entidad federativa, 2016 - 2022
#%%
import pandas as pd
import numpy as np 
from functools import reduce
#%%
def limpiar(archivoCSV, cabecera, tail, quitar=False, cols=[7]):
    df = pd.read_csv(archivoCSV, encoding='utf-8',skip_blank_lines=True)
    df = df.iloc[cabecera:].copy()
    df = df.head(-tail)
    if quitar: 
        df = df.drop(df.columns[cols], axis=1)
    df = df.dropna(axis=1, how='all')
    df.columns =['col' + str(i) for i in range(len(df.columns))]
    df = df.rename(columns={'col0':'estado'})
    return df

# %%
def formatearIndicador(datos, cols, valor='valor'):
    df_long = datos.melt(id_vars=['estado'],
                      value_vars=cols,
                      var_name='anio',
                      value_name=valor)
    anios = ['2016', '2018', '2020', '2022']
    mapeo = {}
    for i, col in enumerate(cols):
        mapeo[col] = anios[i % 4]
    df_long['anio'] = df_long['anio'].map(mapeo)
    return df_long
#%%
"""Datos de rezago educativo"""

cuadro26A = limpiar("../datos/cuadro26A_rezago_educativo.csv", 9,7, True)

cols = [f'col{i}' for i in range(1, 5)]
tmp1 = formatearIndicador(cuadro26A, cols, 'porc_pob_3_21_no_asist_sin_oblig')

cols = [f'col{i}' for i in range(5, 9)]
tmp2 = formatearIndicador(cuadro26A, cols, 'porc_pob_16mas_sin_secu')

cols = [f'col{i}' for i in range(9, 13)]
tmp3 = formatearIndicador(cuadro26A, cols, 'porc_pob_16mas_sin_prim')

# sin educacion obligatoria
cols = [f'col{i}' for i in range(13, 17)]
tmp4 = formatearIndicador(cuadro26A, cols, 'porc_tasa_inasistencia_3_15')

cols = [f'col{i}' for i in range(17, 21)]
tmp5 = formatearIndicador(cuadro26A, cols, 'porc_tasa_inasistencia_16_21')
# %%
dfs = [tmp1, tmp2, tmp3, tmp4, tmp5] 
datosCompletos = reduce(lambda left, right: pd.merge(left, right, on=['estado', 'anio'], how='outer'), dfs)

# %%
"""Datos de carencia alimentaria"""

cuadro26F = limpiar("../datos/cuadro26F_carencia_alimentacion.csv", 8,6, False )
cols = [f'col{i}' for i in range(1, 5)]
tmp1 = formatearIndicador(cuadro26F, cols, 'porc_seg_aliment')

cols = [f'col{i}' for i in range(5, 9)]
tmp2 = formatearIndicador(cuadro26F, cols, 'porc_inseg_aliment_leve')

cols = [f'col{i}' for i in range(9, 13)]
tmp3 = formatearIndicador(cuadro26F, cols, 'porc_inseg_aliment_mode')

cols = [f'col{i}' for i in range(13, 17)]
tmp4 = formatearIndicador(cuadro26F, cols, 'porc_inseg_aliment_seve')

cols = [f'col{i}' for i in range(17, 21)]
tmp5 = formatearIndicador(cuadro26F, cols, 'porc_limit_consumo')

dfs = [tmp1, tmp2, tmp3, tmp4, tmp5] 
dfsTemp = reduce(lambda left, right: pd.merge(left, right, on=['estado', 'anio'], how='outer'), dfs)

# %%
datosCompletos = pd.merge(datosCompletos, dfsTemp, on=['estado', 'anio'], how='outer')
# %%

"""Datos de carencias"""
cuadro27 = limpiar("../datos/cuadro27_pobreza_porgrupo_etarios.csv", 8,6, False )
cols = [f'col{i}' for i in range(25, 29)]
tmp1 = formatearIndicador(cuadro26F, cols, 'porc_carencia_menor18')

cuadro28 = limpiar("../datos/cuadro28_pobreza_porgrupo_etarios_parte2.csv", 7,6, False )
cols = [f'col{i}' for i in range(13, 17)]
tmp2 = formatearIndicador(cuadro26F, cols, 'porc_carencia_6_11')

cols = [f'col{i}' for i in range(25, 29)]
tmp3 = formatearIndicador(cuadro26F, cols, 'porc_carencia_12_17')
dfs = [tmp1, tmp2, tmp3] 
dfsTemp = reduce(lambda left, right: pd.merge(left, right, on=['estado', 'anio'], how='outer'), dfs)
# %%
datosCompletos = pd.merge(datosCompletos, dfsTemp, on=['estado', 'anio'], how='outer')

# %%
# Datos de ocupación infantil 

# 1. Cargar los archivos originales
# Nota: Asegúrate de que los nombres de los archivos coincidan con los tuyos
df_edu_raw = pd.read_csv('../datos/Tasa_abandono_escolar_entidad_federativa.csv', skiprows=5)

# 2. Limpieza inicial del archivo de Educación (INEGI)
# Limpiar espacios en blanco en los nombres de las columnas
df_edu_raw.columns = [c.strip() for c in df_edu_raw.columns]

# Renombrar columnas clave para facilitar el manejo
df_edu = df_edu_raw.rename(columns={
    'Entidad federativa': 'estado', 
    'Nivel educativo': 'nivel'
})

# 3. Transformar la tabla de formato ancho a largo (Melt)
# Esto pasa los años de columnas a una sola columna llamada 'ciclo'
df_melted = df_edu.melt(
    id_vars=['estado', 'nivel'], 
    value_vars=['2015/2016', '2020/2021', '2021/2022'],
    var_name='ciclo', 
    value_name='tasa_abandono'
)

# 4. Convertir Ciclo Escolar a Año numérico
# Ejemplo: '2015/2016' -> 2016 (para que coincida con tus datos de hambre)
def extraer_anio(ciclo):
    try:
        return int(ciclo.split('/')[1])
    except:
        return None

df_melted['anio'] = df_melted['ciclo'].apply(extraer_anio)

# 5. Pivotar los niveles educativos a columnas
# Queremos que cada nivel (Primaria, Secundaria, etc.) sea una columna propia
df_pivoted = df_melted.pivot_table(
    index=['estado', 'anio'], 
    columns='nivel', 
    values='tasa_abandono'
).reset_index()

# Limpiar los nombres de las nuevas columnas
df_pivoted.columns.name = None
df_pivoted = df_pivoted.rename(columns={
    'Primaria': 'tasa_abandono_primaria',
    'Secundaria': 'tasa_abandono_secundaria',
    'Media superior': 'tasa_abandono_media_superior',
    'Superior': 'tasa_abandono_superior'
})

# 6. Unificar con el archivo de porcentajes original
# Eliminamos la columna 'Unnamed: 0' si existe para que no estorbe
if 'Unnamed: 0' in datosCompletos.columns:
    datosCompletos = datosCompletos.drop(columns=['Unnamed: 0'])

#%%
# Merge usando 'estado' y 'anio' como llaves
datosCompletos = pd.merge(datosCompletos, df_pivoted, on=['estado', 'anio'], how='outer')

# 7. Guardar el resultado final
datosCompletos.to_csv("../datos/porcentajes.csv")
# df_final.to_csv('porcentajes_unificados.csv', index=False)

#%%


