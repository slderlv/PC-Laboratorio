![Logo UCN](images/60x60-ucn-negro.png)

# Laboratorio 02: Análisis de Flujo Peatonal y Cálculo de Velocidad

## 1. Introducción

En este laboratorio, se aborda el análisis del flujo peatonal en un espacio público, específicamente en un pasillo de un metro. Se utilizan varios archivos de texto que contienen datos relevantes sobre las personas detectadas, incluyendo su ID, el frame del video en el que aparecen y sus coordenadas (x, y, z) en un espacio tridimensional. El objetivo es procesar estos datos para calcular la velocidad peatonal en diferentes áreas y analizar su comportamiento.

### 1.1 Justificación

El análisis del flujo peatonal es esencial para la gestión eficiente de espacios públicos y el diseño de infraestructuras adecuadas. Comprender cómo se mueven las personas en áreas determinadas permite tomar decisiones informadas para mejorar la experiencia de los usuarios y optimizar la planificación urbana.

### 1.3 Objetivos

**Objetivo General**

- Analizar y calcular, la frecuencia y velocidad peatonal en un espacio público utilizando datos de coordenadas proporcionados en un archivo de texto.

**Objetivos específicos**

1. Extraer y almacenar las coordenadas (x, y, z) de las personas del archivo de texto en una estructura de datos.
2. Obtener la velocidad que tiene cada individuo por Frame.
3. Mostrar un gráfico por pantalla el cual muestra la velocidad promedio de la multitud, para un determinado frame.

## 2. Marco teórico

En este laboratorio, utilizaremos las siguientes herramientas y librerías:

- Python: Lenguaje de programación para el procesamiento de datos y cálculos matemáticos.
- NumPy: Librería para la manipulación y operación de arreglos numéricos.
- Matplotlib: Librería para la visualización de datos en gráficos y figuras.
- Pandas: Librería para el análisis y manipulación de datos tabulares.
- Math: Librería para cálculos y operaciónes.

## 3. Materiales y métodos

### Dataset

Se utilizará un archivo de texto que contiene información sobre el flujo peatonal en un pasillo del tren subterráneo. Cada línea del archivo incluye el ID de la persona, el frame del video y las coordenadas (x, y, z).

### Procedimiento

1. Leer y procesar el archivo de texto para obtener las coordenadas (x, y, z) de cada persona.
2. Calcular la velocidad de las personas a lo largo del frame para obtener posteriormente velocidad promedio de la multiutd.
3. Visualizar por pantalla la velocidad promedio que hay por frame.

## 4. Resultados obtenidos

En este laboratorio, atravéz de la lectura de archivos y un posterior cálculo de velocidades por persona, se lograron obtener las siguientes velocidades de la mulitud:

![Velocity Scatter](images/scatter.jpeg)

La visualización final muestra la velocidad peatonal, lo que proporciona una visión clara y detallada del flujo de personas en el espacio público.

## 5. Conclusiones

`velocity_module` es una potente herrarmienta para poder visualizar el comportamiento de las velocidades de los peatones en multitudes, permitiendo así a los usuarios apoyarse de este recurso gráfico para así poder gestionar de manera más eficiente los espacios públicos, o bien ser útil para las proyecciones de futuras construcciones relacionadas con el flujo peatonal.
