![Logo UCN](images/60x60-ucn-negro.png)

# Laboratorio 04: Cálculo del Sk

## 1. Introducción

En este laboratorio, se aborda el análisis del flujo peatonal en un espacio público, específicamente en un pasillo de un metro. Se utilizan varios archivos de texto que contienen datos relevantes sobre las personas detectadas, incluyendo su ID, el frame del video en el que aparecen y sus coordenadas (x, y, z) en un espacio tridimensional. El objetivo es procesar estos datos para calcular la velocidad peatonal en diferentes áreas y analizar su comportamiento, además de incorporar el cálculo del valor Sk para evaluar la dispersión de las distancias entre individuos cercanos.

### 1.1 Justificación

El análisis del flujo peatonal es esencial para la gestión eficiente de espacios públicos y el diseño de infraestructuras adecuadas. Comprender cómo se mueven las personas en áreas determinadas permite tomar decisiones informadas para mejorar la experiencia de los usuarios y optimizar la planificación urbana.

### 1.3 Objetivos

**Objetivo General**

- Analizar y calcular, la frecuencia y velocidad peatonal en un espacio público utilizando datos de coordenadas proporcionados en un archivo de texto, además de incorporar el cálculo del valor Sk para evaluar la dispersión de las distancias entre individuos cercanos.

**Objetivos específicos**

1. Extraer y almacenar las coordenadas (x, y, z) de las personas del archivo de texto en una estructura de datos.
2. Obtener la velocidad que tiene cada individuo por Frame.
3. Calcular el valor Sk para medir la dispersión de las distancias entre individuos cercanos.
4. Mostrar un gráfico por pantalla el cual muestra la velocidad promedio de la multitud, para un determinado frame.
5. Implementar el módulo `velocity_module`, que proporciona funciones para calcular la velocidad de los peatones, generar visualizaciones y obtener información de recursos durante la ejecución, incluyendo el cálculo del valor Sk.


## 2. Marco teórico

En este laboratorio, utilizaremos las siguientes herramientas y librerías:

- Python: Lenguaje de programación para el procesamiento de datos y cálculos matemáticos.
- NumPy: Librería para la manipulación y operación de arreglos numéricos.
- Matplotlib: Librería para la visualización de datos en gráficos y figuras.
- Pandas: Librería para el análisis y manipulación de datos tabulares.
- Math: Librería para cálculos y operaciones.
- psutil: Librería para obtener información sobre el uso de recursos del sistema.

## 3. Materiales y métodos

### Dataset

Se utilizarán dos archivos de texto que contienen información sobre el flujo peatonal en un pasillo del tren subterráneo. Cada línea del archivo incluye el ID de la persona, el frame del video y las coordenadas (x, y, z).

### Procedimiento

1. Leer y procesar el archivo de texto para obtener las coordenadas (x, y, z) de cada persona.
2. Calcular la velocidad de las personas a lo largo del frame para obtener posteriormente la velocidad promedio de la multitud.
3. Calcular el valor Sk para evaluar la dispersión de las distancias entre individuos cercanos.
4. Visualizar por pantalla la velocidad promedio que hay por frame y el valor Sk calculado.
5. Utilizar el módulo `velocity_module` para automatizar el cálculo de velocidad, generar gráficos y obtener información de recursos, incluyendo el valor Sk.


## 4. Resultados obtenidos

En este laboratorio, a través de la lectura de archivos y el cálculo de velocidades por persona, así como el cálculo del valor Sk, se lograron obtener las siguientes velocidades de la multitud:

![Velocity Histogram Comparisson](images/histogram_velocity_comparisson.png)
![Randomly Selected PersID Box Plot](images/velocity_boxplot.png)


La visualización final muestra la velocidad peatonal y los valores Sk, lo que proporciona una visión completa y detallada del flujo de personas en el espacio público, así como la dispersión de las distancias entre individuos cercanos. La implementación del módulo `velocity_module` facilitó la automatización de cálculos y la generación de visualizaciones, incluyendo el cálculo del valor Sk.

## 5. Conclusiones

`velocity_module` es una potente herramienta desarrollada en este laboratorio para visualizar el comportamiento de las velocidades de los peatones en multitudes, junto con la evaluación de la dispersión de las distancias entre individuos cercanos utilizando el valor Sk. Esta incorporación agiliza el análisis y ofrece una solución completa para el cálculo, la representación visual de las velocidades peatonales y la evaluación de la dispersión en función de los datos proporcionados en los archivos de texto.

Al analizar los resultados obtenidos, se observa que el primer archivo de texto, UNI_CORR_500_01, presenta una velocidad constante alrededor de los 1.5 metros por segundo a lo largo de aproximadamente 2000 frames. Esto podría indicar que las personas en este archivo mantuvieron una velocidad constante mientras se movían por el pasillo del tren subterráneo.

Por otro lado, en el caso del quinto archivo de texto, UNI_CORR_500_05, se evidencia un patrón diferente. Aquí, la velocidad parece comenzar con 1.5 metros por segundo y luego disminuye hasta el frame 1000. A partir de ese punto, se estabiliza alrededor de 0.7 metros por segundo hasta el final del registro (frame 4000 aproximadamente). Esta variación en las velocidades podría sugerir cambios en la densidad de personas o en las condiciones del entorno a lo largo del tiempo.

En cuanto al valor Sk, este es un indicador que intenta predecir la velocidad real de cada persona en cada frame en base a la cantidad de vecinos cercanos. A mayor cantidad de vecinos cercanos, menor es la velocidad predicha, y a menor cantidad de vecinos cerca, mayor es la velocidad predicha. Este cálculo del valor Sk proporciona información adicional sobre cómo se distribuyen las velocidades y las distancias entre los peatones en el espacio público, lo que contribuye a una comprensión más completa de los patrones de flujo peatonal y su variabilidad.

En resumen, este laboratorio y el módulo `velocity_module` brindan herramientas esenciales para el análisis del flujo peatonal y la comprensión de los patrones de velocidad y dispersión en espacios públicos. La posibilidad de calcular y visualizar velocidades, junto con la evaluación de la dispersión de las distancias utilizando el valor Sk, proporciona información valiosa para la planificación y el diseño de espacios urbanos eficientes y seguros.


