# AI Log - DatofilODS

## Herramientas
- Gemini
- DeepSeek
- Claude

## Filosofía de uso
La postura de DatofilODS es usar la IA como una herramienta para ayudar a reflejar nuestro propósito, es nuestra labor encontrar la fuente de datos de calidad y asegurar que estén correctamente procesados para poder generar gráficos de valor, es por ello que la usamos para que nos apoye estructurando mejor los gráficos y la visualición para poder plasmar de mejor forma nuestro mensaje, la IA no habla por nosotros, nosotros somos los creadores y motor de la idea, la IA solo nos ayuda a maquetarlo para que sea visible nuestra voz.

## Registro de uso

### 2026-abril-13 | Gemini | Limpieza de datos
- **Tarea**: Buscar una forma de acomodar datos adecuadamente
- **Prompt**: Para esos datos, que scripts requiero hacer de prepocesamiento usando python
- **Resultado**:
Dio un script general para limpiar los datos y acomodarlos de forma larga

- **Decisión**:
Se decide generar los datos de la forma larga que propone y se genera un codigo inspirado en el generado por IA para que se pueda limpiar todos los archivos que hemos escogido iterando en las modificaciones conforme la presentación de los datos obtenidos.

### 2026-abril-13  | Gemini | Gráficas básicas
- **Tarea**: Encontrar gráficas adecuadas para visualizar
- **Prompt**: quiero hacer un dashboard en quarto, ya tengo mi csv de datos y va enfocado a 
¿Es verdad que todos podemos acceder a la educación?, para mostrar los sesgos que se tienen respecto a la educación en el pais y evidenciar que la típica frase de “pues que se pongan a estudiar en vez de …” no es más que solo un sesgo junto con el eslogan o la parte fuerte del proyectro "La educación puede esperar, el hambre no" que tipo de graficas pudiera hacer con estos datos para mi qmd,
- **Resultado**: nos arrojo graficas de barras para dos variables
de inseguridad de hambre
- **Decisión**: Se decide usar el layout propuesto y se ajusta a variables de rezago educativo también

### 2026-abril-14  | DeepSeek & Claude | Debugging
- **Tarea**: Solucionar el correcto renderizado de gráficas
- **Prompt**: Ayudame a que se muestren correctamente las gráficas ya que se encuentran desplegadas por capas usando mi código
- **Resultado**: Generó un código mejor estructurado pero sin solucionar correctamente el problema
- **Decisión**: Se decidió usar el código para una mejor composición del gráfico pero se investigó en otros foros la solución a nuestro problema presentado


### NO usamos IA para hacer lo siguiente:
- La búsqueda y selección de las bases de datos para nuestro proyecto
- La pregunta de interés a desarrollar en nuestro dashboard
- Selección de indicadores para nuestro mapa de México
