# Equipo DatofilODS
## Integrantes

### Alma Diana Herrera Ortiz
Estudiante de maestría con gran interés en los problemas sociales de México que estén relacionados con el desarrollo del país. Con formación en ingeniería en sistemas y actualmente trabajando en el sector fintech con herramientas en la nube para automatización de infraestructura. 

### Santiago

### Daniel

[Declaración de uso de IA](ai-log.md)

## Descripción del proyecto
"La educación puede esperar, el hambre no" es un proyecto que busca cuestionar y desmontar el sesgo social detrás de la frase "pues que se pongan a estudiar en vez de…", evidenciando que el acceso a la educación no es únicamente una cuestión de voluntad individual, sino que está profundamente condicionado por la pobreza multidimensional en México. A partir de los datos del CONEVAL, queremos  analizar si realmente todas las personas pueden acceder a la educación en condiciones de rezago educativo, carencia por acceso a la alimentación y otras privaciones. Este trabajo se alinea con el *ODS 4* (Educación de calidad) y *ODS 2* (Hambre cero).

## Datos

- **Fuente** Consejo Nacional de Evaluación de la Política de Desarrollo Social (CONEVAL). (2022). "Anexo estadísti​co de pobreza en México". [Base de datos en línea]. Recuperado el 7 de abril de 2026 de https://www.coneval.org.mx/Medicion/MP/Documents/MMP_2022/AE_estatal_2022.zip Para condiciones de uso https://www.coneval.org.mx/Paginas/Pie/terminos-uso-libre.aspx 

- **Fecha de descarga** 07-abril-2026
- **Licencia Uso Libre con Atribución** Permite copia, distribución, adaptación y uso comercial, siempre que se dé crédito al CONEVAL, no se alteren metadatos, no se tergiverse el sentido original y no se implique aval oficial.
- **Descripción de variables** Se tomaron en cuenta variables relacionadas a rezago educativo, carencia alimentaria y carencias en general. Los valores de todas las variables exceptuando `'estado'` y `'anio'` indican porcentajes.

    - `'estado'`: Entidad federativa
    - `'anio'`: Diferentes años de 2016,2018,2020,2022
    - `'porc_pob_3_21_no_asist_sin_oblig'`: Población de 3 a 21 años que no asiste a la escuela y no cuenta con educación obligatoria1 		
    - `'porc_pob_16mas_sin_secu'`: Población de 16 años o más nacida entre 1982 y 1997 sin secundaria completa	
    - `'porc_pob_16mas_sin_prim'`: Población de 16 años o más nacida antes de 1982 sin primaria completa					
    - `'porc_tasa_inasistencia_3_15'`: Tasa de inasistencia para la población de 3 a 15 años (Población sin educación obligatoria)
    - `'porc_tasa_inasistencia_16_21'`: Tasa de inasistencia para la población de 16 a 21 años (Población sin educación obligatoria)
    - `'porc_seg_aliment'`: Personas con seguridad alimentaria
    - `'porc_inseg_aliment_leve'`: Personas con inseguridad alimentaria leve
    - `'porc_inseg_aliment_mode'`: Personas con inseguridad alimentaria moderada
    - `'porc_inseg_aliment_seve'`: Personas con inseguridad alimentaria severa
    - `'porc_limit_consumo'`: Personas con limitación en el consumo de alimentos
    - `'porc_carencia_menor18'`: Personas con carencia menores a 18 años
    - `'porc_carencia_6_11'`: Personas con carencia entre 6 y 11 años
    - `'porc_carencia_12_17'`: Personas con carencia entre 12 y 17 años
- **Justificación de selección de datos** Los datos del CONEVAL son relevantes porque vinculan directamente  dimensiones de la pobreza multidimensional como lo es el rezago educativo e inseguridad alimentaria para demostrar con evidencia empírica que el hambre es un obstáculo para el acceso a la educación y avanzar en ella. Los datos incluyen cuatro años de medición (2016-2022) lo que nos permitirá comparar cómo ha sido el impacto de esas variables para la educación, los datos posibilitan cuestionar el sesgo que responsabiliza individualmente a las personas de su situación educativa, cuando en realidad la carencia alimentaria y carencias en general inciden en la inasistencia escolar.



# Storytelling
- Pregunta o problema central — Pregunta clara que guía el tablero
- Coherencia narrativa — Coherencia entre ODS, datos e historia
- Potencial de impacto — Visibiliza un problema real en México

# Prototipo