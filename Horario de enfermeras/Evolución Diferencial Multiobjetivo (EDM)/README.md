# Generador de horarios de enfermeras con Evolución Diferencial Multiobjetivo 

## Características Principales

* **Optimización Jerárquica:** Implementa un sistema de decisión estricto donde la viabilidad legal (Restricciones Duras) siempre tiene prioridad absoluta sobre las preferencias personales (Restricciones Suaves).

* **Representación Continua a Discreta:** Utiliza vectores de números reales que se mapean a decisiones binarias mediante un umbral de activación optimizado (`0.78`) para gestionar la escasez inicial de turnos.

* **Lógica Temporal Cíclica:** Verifica la continuidad laboral no solo dentro de la semana, sino entre el final de una semana (Domingo noche) y el inicio de la siguiente (Lunes mañana).

* **Mecanismos Anti-Estancamiento:** Sistema inteligente que detecta mínimos locales e inyecta diversidad genética ("sangre nueva") reemplazando parcialmente la población si no hay mejoras.

* **Visualización Profesional:** Genera automáticamente una interfaz gráfica (GUI) con un diagrama de calendario codificado por colores.

## Estructura del Proyecto

El proyecto está contenido en un script monolítico para facilitar su ejecución y portabilidad:

* **`EDM_Horario_de_enfermeras.py`**: Archivo principal que contiene:

  * **Configuración:** Definición de enfermeras, turnos y reglas.

  * **Motor DE:** Implementación de la clase `Individuo` y el bucle evolutivo.

  * **Modelo de Evaluación:** Funciones de penalización (`hard` y `soft`).

  * **Interfaz Gráfica:** Código de `matplotlib` y `tkinter` para el reporte final.

## Requisitos Previos

* **Lenguaje:** Python 3.8 o superior.

* **Librerías Externas:**

  * `numpy`: Para operaciones vectoriales de alta velocidad.

  * `matplotlib`: Para la generación de gráficos.

  * `tkinter`: Para la ventana emergente (generalmente incluido en Python).

### Instalación

	pip install numpy matplotlib

### Instrucciones de Ejecución

Para iniciar el algoritmo de optimización, ejecuta el siguiente comando en la terminal:


	 python EDM_Horario_de_enfermeras.py

## Tecnologías Utilizadas

* **Algoritmo:** Evolución Diferencial (variante `DE/rand/1/bin`).

* **Estrategia de Selección:** Torneo binario basado en dominancia de Pareto restringida.

* **Visualización:** `matplotlib` (`patches`, `pyplot`).

* **Backend Matemático:** `numpy` (arrays, vectorización y generación aleatoria).

## Parámetros del Algoritmo

Los siguientes valores han sido ajustados empíricamente para garantizar la convergencia:

| Parámetro | Valor | Descripción |
|---------|------|-------------|
| Población | 300 – 500 | Número de vectores (horarios) compitiendo simultáneamente |
| Generaciones | 1500 – 2000 | Número de iteraciones del ciclo evolutivo |
| Factor F | 0.4 – 0.9 | *Dithering* para balancear exploración y explotación |
| Cruce (CR) | 0.9 | Alta probabilidad de heredar genes del vector mutante |
| Umbral | 0.78 | Valor de corte para decodificar el vector real a binario |
| Dimensión | 168 | 8 enfermeras × 21 slots (7 días × 3 turnos) |

## Lógica de Restricciones

El “juez” del algoritmo evalúa cada horario sumando puntos de penalización.  
El objetivo es alcanzar **0 puntos en restricciones duras** y minimizar las restricciones suaves.

### Restricciones Duras (Hard Constraints)

Violaciones a la normativa laboral u hospitalaria.  
Penalización: **2000 puntos** por violación.

1. **Cobertura de Personal:**
   * Mañana: mínimo 2, máximo 3
   * Tarde: mínimo 2, máximo 4
   * Noche: mínimo 1, máximo 2

2. **Sobrecarga Laboral:**  
   Máximo 5 turnos por semana por enfermera.

3. **Descanso Ininterrumpido (Ventana Deslizante):**  
   Prohibido trabajar turnos consecutivos:
   * Mañana → Tarde
   * Tarde → Noche  

  Se permite Mañana → Noche.

4. **Continuidad Cíclica:**  
   Prohibido trabajar Domingo Noche → Lunes Mañana.

### Restricciones Suaves (Soft Constraints)

Preferencias personales.  
Penalización: **1 punto**.

1. **Preferencia de Turno:**  
   Se evalúa si el turno asignado coincide con las preferencias definidas por cada enfermera.

## Resultados

El programa genera una ventana emergente en donde se podra visualizar el mejor horario encontrado.

### Consola (Progreso Evolutivo)

Durante la ejecución del algoritmo se muestra en consola la evolución de las penalizaciones *hard* y *soft* a lo largo de las generaciones:

	Gen 0:   Hard=68000, Soft=19
	...
	Gen 500: Hard=6000,  Soft=12
	...
	>>> ¡PERFECCIÓN ALCANZADA! <<<
	 Cálculo finalizado. Generando reporte visual...
