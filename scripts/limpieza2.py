
#%%
import pandas as pd
import numpy as np 
from functools import reduce

def limpiar(archivoCSV, cabecera, tail, quitar=False, cols=[7]):
    df = pd.read_csv(archivoCSV, encoding='utf-8', skip_blank_lines=True)
    df = df.iloc[cabecera:].copy()
    df = df.head(-tail)
    if quitar: 
        df = df.drop(df.columns[cols], axis=1)
    df = df.dropna(axis=1, how='all')
    df.columns = ['col' + str(i) for i in range(len(df.columns))]
    df = df.rename(columns={'col0':'estado'})
    return df

def formatearIndicador(datos, cols, valor='valor'):
    df_long = datos.melt(id_vars=['estado'],
                         value_vars=cols,
                         var_name='anio',
                         value_name=valor)
    # AJUSTE 1: Años como enteros para coincidir con el resto de los datos
    anios = [2016, 2018, 2020, 2022]
    mapeo = {}
    for i, col in enumerate(cols):
        mapeo[col] = anios[i % 4]
    df_long['anio'] = df_long['anio'].map(mapeo)
    return df_long

#%%
# --- Datos de rezago educativo ---
cuadro26A = limpiar("../datos/cuadro26A_rezago_educativo.csv", 9, 7, True)

tmp1 = formatearIndicador(cuadro26A, [f'col{i}' for i in range(1, 5)], 'porc_pob_3_21_no_asist_sin_oblig')
tmp2 = formatearIndicador(cuadro26A, [f'col{i}' for i in range(5, 9)], 'porc_pob_16mas_sin_secu')
tmp3 = formatearIndicador(cuadro26A, [f'col{i}' for i in range(9, 13)], 'porc_pob_16mas_sin_prim')
tmp4 = formatearIndicador(cuadro26A, [f'col{i}' for i in range(13, 17)], 'porc_tasa_inasistencia_3_15')
tmp5 = formatearIndicador(cuadro26A, [f'col{i}' for i in range(17, 21)], 'porc_tasa_inasistencia_16_21')

dfs = [tmp1, tmp2, tmp3, tmp4, tmp5] 
datosCompletos = reduce(lambda left, right: pd.merge(left, right, on=['estado', 'anio'], how='outer'), dfs)

#%%
# --- Datos de carencia alimentaria ---
cuadro26F = limpiar("../datos/cuadro26F_carencia_alimentacion.csv", 8, 6, False)
tmp_a1 = formatearIndicador(cuadro26F, [f'col{i}' for i in range(1, 5)], 'porc_seg_aliment')
tmp_a2 = formatearIndicador(cuadro26F, [f'col{i}' for i in range(5, 9)], 'porc_inseg_aliment_leve')
tmp_a3 = formatearIndicador(cuadro26F, [f'col{i}' for i in range(9, 13)], 'porc_inseg_aliment_mode')
tmp_a4 = formatearIndicador(cuadro26F, [f'col{i}' for i in range(13, 17)], 'porc_inseg_aliment_seve')
tmp_a5 = formatearIndicador(cuadro26F, [f'col{i}' for i in range(17, 21)], 'porc_limit_consumo')

dfs_alim = [tmp_a1, tmp_a2, tmp_a3, tmp_a4, tmp_a5] 
dfsAlim = reduce(lambda left, right: pd.merge(left, right, on=['estado', 'anio'], how='outer'), dfs_alim)
datosCompletos = pd.merge(datosCompletos, dfsAlim, on=['estado', 'anio'], how='outer')

#%%
# --- Datos de carencias (AJUSTE 2: Variables corregidas) ---
cuadro27 = limpiar("../datos/cuadro27_pobreza_porgrupo_etarios.csv", 8, 6, False)
tmp_c1 = formatearIndicador(cuadro27, [f'col{i}' for i in range(25, 29)], 'porc_carencia_menor18')

cuadro28 = limpiar("../datos/cuadro28_pobreza_porgrupo_etarios_parte2.csv", 7, 6, False)
tmp_c2 = formatearIndicador(cuadro28, [f'col{i}' for i in range(13, 17)], 'porc_carencia_6_11')
tmp_c3 = formatearIndicador(cuadro28, [f'col{i}' for i in range(25, 29)], 'porc_carencia_12_17')

dfs_car = [tmp_c1, tmp_c2, tmp_c3] 
dfsCar = reduce(lambda left, right: pd.merge(left, right, on=['estado', 'anio'], how='outer'), dfs_car)
datosCompletos = pd.merge(datosCompletos, dfsCar, on=['estado', 'anio'], how='outer')

#%%
# --- Datos de abandono escolar (INEGI) ---
df_edu_raw = pd.read_csv('../datos/Tasa_abandono_escolar_entidad_federativa.csv', skiprows=5)
df_edu_raw.columns = [c.strip() for c in df_edu_raw.columns]
df_edu = df_edu_raw.rename(columns={'Entidad federativa': 'estado', 'Nivel educativo': 'nivel'})

df_melted = df_edu.melt(
    id_vars=['estado', 'nivel'], 
    value_vars=['2015/2016', '2020/2021', '2021/2022'],
    var_name='ciclo', 
    value_name='tasa_abandono'
)

def extraer_anio(ciclo):
    try:
        return int(ciclo.split('/')[1])
    except:
        return None

df_melted['anio'] = df_melted['ciclo'].apply(extraer_anio)

df_pivoted = df_melted.pivot_table(
    index=['estado', 'anio'], 
    columns='nivel', 
    values='tasa_abandono'
).reset_index()

df_pivoted.columns.name = None
df_pivoted = df_pivoted.rename(columns={
    'Primaria': 'tasa_abandono_primaria',
    'Secundaria': 'tasa_abandono_secundaria',
    'Media superior': 'tasa_abandono_media_superior',
    'Superior': 'tasa_abandono_superior'
})

#%%
# --- Unión Final (AJUSTE 3: Eliminación de columna y Merge) ---
if 'Unnamed: 0' in datosCompletos.columns:
    datosCompletos = datosCompletos.drop(columns=['Unnamed: 0'])

# Ahora ambos tienen 'anio' como int64
datosCompletos = pd.merge(datosCompletos, df_pivoted, on=['estado', 'anio'], how='outer')

# Guardar
# datosCompletos.to_csv("../datos/porcentajes.csv", index=False)
# print("¡Archivo unificado con éxito!")

#%%

# df = pd.read_csv("../datos/porcentajes.csv")
# %%

# import pandas as pd

# 1. Cargar los archivos
# df_porc = pd.read_csv('../datos/porcentajes.csv')
# El archivo ENTI tiene 5 filas de encabezado antes de los datos reales
#%% 
# --- Datos de hogares con menores de 5 a 17 años 
df_enti_raw = pd.read_csv('../datos/cuadro4_1_pobTotal_conmenores5_17_años.csv', skiprows=5)

# 2. Limpieza de los datos de población (ENTI 2022)
# Seleccionamos solo las columnas de Estado y el Total
df_enti = df_enti_raw[['Unnamed: 0', 'Población Total en hogares con menores de 5 a 17 años']].copy()
df_enti.columns = ['estado', 'pob_total_hogares_menores_5_17']

# Eliminamos filas vacías y basura del pie de página
df_enti = df_enti.dropna(subset=['estado'])

# Limpieza de los números (quitar comas y convertir a numérico)
df_enti['pob_total_hogares_menores_5_17'] = (
    df_enti['pob_total_hogares_menores_5_17']
    .str.replace(',', '')
    .astype(float)
)

# Estandarizar nombres de estados
# Cambiamos 'Nacional' por el nombre que usas en tu otro archivo
# df_enti['estado'] = df_enti['estado'].replace('Nacional', 'Estados Unidos Mexicanos')

# Como este cuadro es de la encuesta 2022, asignamos el año fijo
df_enti['anio'] = 2022

# Filtramos para quedarnos solo con filas que sean estados reales (evitar notas al pie)
estados_validos = datosCompletos['estado'].unique()
df_enti = df_enti[df_enti['estado'].isin(estados_validos)]

# 3. Integración (Merge)
# Unimos la nueva columna al archivo original basándonos en Estado y Año (2022)
df_final = pd.merge(datosCompletos, df_enti[['estado', 'anio', 'pob_total_hogares_menores_5_17']], 
                     on=['estado', 'anio'], 
                     how='left')

#%%
# # 4. Guardar el resultado
df_final.to_csv('porcentajes_2.csv', index=False)

print("¡Integración completada con éxito!")
print(f"Nueva columna añadida: 'pob_total_hogares_menores_5_17'")

# %%
