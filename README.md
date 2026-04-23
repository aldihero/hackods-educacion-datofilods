# Equipo DatofilODS
## Integrantes

### Alma Diana Herrera Ortiz
Estudiante de maestría con gran interés en los problemas sociales de México que estén relacionados con el desarrollo del país. Con formación en ingeniería en sistemas y actualmente trabajando en el sector fintech con herramientas en la nube para automatización de infraestructura. 

### Santiago Botero Sierra
Estudiante de maestría en Ciencia de Datos, con formación en ingeniería, derecho y economía. Disfruto mucho analizar datos para contribuir a la toma de decisiones en el sector público, en organizaciones de la sociedad civil y en la defensa de los derechos humanos de las y los migrantes. Más información en [mi página de internet](sboteros.com).

### Daniel Mondragon Tapia
Desarrollador de Software con enfoque en sistemas de alto rendimiento. Estudiante en Economía. Me interesa la intersección entre la tecnología y las ciencias sociales.

[Declaración de uso de IA](ai-log.md)
---


## Descripción del proyecto
"La educación puede esperar, el hambre no" es un proyecto que busca cuestionar y desmontar el sesgo social detrás de la frase "pues que se pongan a estudiar en vez de…", evidenciando que el acceso a la educación no es únicamente una cuestión de voluntad individual, sino que está profundamente ligado a la pobreza multidimensional en México. A partir de los datos del CONEVAL, queremos  analizar si realmente todas las personas pueden acceder a la educación en condiciones de rezago educativo, carencia por acceso a la alimentación y otras privaciones. Este trabajo se alinea con el *ODS 4* (Educación de calidad) y *ODS 2* (Hambre cero).

## Datos

- **Fuentes** 
    - Consejo Nacional de Evaluación de la Política de Desarrollo Social (CONEVAL). (2022). "Anexo estadísti​co de pobreza en México". [Base de datos en línea]. Recuperado el 7 de abril de 2026 de https://www.coneval.org.mx/Medicion/MP/Documents/MMP_2022/AE_estatal_2022.zip Para condiciones de uso https://www.coneval.org.mx/Paginas/Pie/terminos-uso-libre.aspx 
    - INEGI  Tasa de abandono escolar por entidad federativa según nivel educativo, ciclos escolares seleccionados de 2000/2001 a 2023/2024  Recuperado el 7 de abril de 2026 de https://www.inegi.org.mx/app/tabulados/interactivos/?px=Educacion_11&bd=Educacion 
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
- **Justificación de selección de datos** Los datos del CONEVAL son relevantes porque vinculan directamente  dimensiones de la pobreza multidimensional como lo es el rezago educativo e inseguridad alimentaria para demostrar con evidencia empírica que el hambre es un obstáculo para el acceso a la educación y avanzar en ella. Los datos incluyen cuatro años de medición (2016-2022) lo que nos permitirá comparar cómo ha sido el impacto de esas variables para la educación, los datos posibilitan cuestionar el sesgo que responsabiliza individualmente a las personas de su situación educativa, cuando en realidad la carencia alimentaria y carencias en general inciden en la inasistencia escolar. Además la tasa de abandono escolar proporcionado por el INEGI ayudará a encontrar relaciones más cercanas al impacto que tienen las carencias de pobreza con el estudio.

    ## Datos

- **Fuentes** 
    - Consejo Nacional de Evaluación de la Política de Desarrollo Social (CONEVAL). (2022). "Anexo estadísti​co de pobreza en México". [Base de datos en línea]. Recuperado el 7 de abril de 2026 de https://www.coneval.org.mx/Medicion/MP/Documents/MMP_2022/AE_estatal_2022.zip Para condiciones de uso https://www.coneval.org.mx/Paginas/Pie/terminos-uso-libre.aspx 
    - INEGI  Tasa de abandono escolar por entidad federativa según nivel educativo, ciclos escolares seleccionados de 2000/2001 a 2023/2024  Recuperado el 7 de abril de 2026 de https://www.inegi.org.mx/app/tabulados/interactivos/?px=Educacion_11&bd=Educacion 
- **Fecha de descarga** 07-abril-2026
- **Licencia Uso Libre con Atribución** Permite copia, distribución, adaptación y uso comercial, siempre que se dé crédito al CONEVAL, no se alteren metadatos, no se tergiverse el sentido original y no se implique aval oficial.
- **Descripción de variables** Se tomaron en cuenta variables relacionadas a rezago educativo, carencia alimentaria y carencias en general. Los valores de todas las variables exceptuando `'estado'` y `'anio'` indican porcentajes.

Link de descarga de datos compilados:
TODO --- Documentar origen y estructura
https://drive.google.com/file/d/1CBTqcbOAZbm1xlSVOKFV9mA-cErVV4uK/view?usp=drive_link


# Storytelling

Buscamos hacer visible el sesgo que tenemos como población con respecto al acceso a la educación. No basta con que la educación sea gratuita, tiene que ser accesible, justa y de calidad. Queremos contestar la pregunta: ¿Es verdad que todos podemos acceder a la educación?, con el objetivo de concientizar sobre los problemas educativos que existen en gran parte de la población y así evitar que se sigan propagando sesgos dañinos comunes, por ejemplo: "pues que se pongan a estudiar en vez de …", es un pensamiento limitante para todos y evade buscar soluciones al problema.

Para poder evidenciar los problemas de educación resaltamos los datos que muestran las poblaciones que dejan de asistir a la escuela especialmente en el nivel educativo básico y cómo se relaciona con los niveles de pobreza en diferentes ámbitos como lo es la alimentación, carencias sociales y carencias en general, así como también resaltar las tasas de abandono escolar en ese nivel para reflejar un poco mejor cómo está México.

Nuestro objetivo principal es exponer y visualizar la estructura educativa completa del país para indicar a dónde que tenemos que voltear y consecuentemente proponer soluciones, concientizar, divulgar y exponer problemas ayuda a que en sociedad podamos solventar esas carencias y dejemos de señalar sin argumentos. 

# Prototipo
El tablero al momento cuenta con 3 gráficas principales, reflejando datos del 2022 en el que se visualiza la inasistencia escolar en diferentes grupos en infancias de 6 a 11 y adolescentes 12 a 17 años, por otro lado está un gráfico que refleja la inseguridad alimentaria severa en todo el país dandonos un primer indicio de los estados que presentan este problema con mayor intensidad. Finalmente está nuestro mapa que refleja qué estados cuentan con inseguridad alimentaria. 
Para la siguiente etapa se quiere reflejar los años 2016, 2018, 2020 y 2022 para ver qué tanto ha cambiado los índices de inasistencia y tasa de abandono, así como agregar indicadores para éste último con los datos del INEGI referentes a la tasa de abandono escolar a nivel básico.

Para el procesamiento de datos se siguió el [script](scripts/limpieza.py) que permitió procesar datos provenientes del CONEVAL y acomodar un dataset para facilitar la generación del dashboard.

El [script](scripts/graficas.py) sirvió para hacer el maquetado de gráficas, dejando las que actualmente están en el tablero, sirvió para entender la librería de plotly y hacer un primera visualización de nuestros datos.

El siguiente enlace es al avance al tablero https://aldihero.github.io/hackods-educacion-datofilods/HackODS.html
