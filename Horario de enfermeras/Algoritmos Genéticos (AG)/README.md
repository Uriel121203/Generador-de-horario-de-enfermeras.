# Generador de Horarios de Enfermeras con Algoritmos Genéticos

Este proyecto implementa una solución de optimización basada en inteligencia artificial para resolver el problema de **Programación de Horarios de Enfermeras**.

El objetivo principal es encontrar la distribución semanal óptima para **8 enfermeras**, asegurando el cumplimiento estricto de las normativas del hospital y, en la medida de lo posible, respetando las preferencias individuales del personal.

## Características Principales

* **Optimización:** El algoritmo utiliza un sistema de penalización donde las restricciones operativas del hospital (Duras) tienen un peso significativamente mayor que las preferencias personales (Blandas).
* **Algoritmo Genético con Elitismo:** Implementa un mecanismo para preservar los mejores individuos ("Salón de la Fama") para garantizar la convergencia hacia soluciones de alta calidad.
* **Reportes Automáticos:** Generación de horarios en Excel con formato visual y gráficas de evolución del fitness.

## Lógica de Restricciones y Penalización

El núcleo del algoritmo se basa en minimizar una función de costo. Un costo de 0 representaría un horario perfecto.

### Restricciones Duras (Reglas del Hospital)
*Son de cumplimiento obligatorio. Tienen una penalización alta porque su violación hace que el horario sea inviable operativamente.*

1.  **Turnos Consecutivos:** Una enfermera **no** puede trabajar dos turnos seguidos (ej. Mañana y luego Tarde el mismo día).
2.  **Carga Máxima Semanal:** Una enfermera **no** puede exceder los **5 turnos por semana**.
3.  **Cobertura de Personal por Turno:** Se deben respetar estrictamente los siguientes límites de personal en el departamento:
    * **Turno Mañana:** Mínimo 2, Máximo 3 enfermeras.
    * **Turno Tarde:** Mínimo 2, Máximo 4 enfermeras.
    * **Turno Noche:** Mínimo 1, Máximo 2 enfermeras.

### Restricciones Blandas (Preferencias)
*Son deseables pero no críticas. Tienen una penalización menor.*

1.  **Preferencias Individuales:** Se intenta asignar a cada enfermera los turnos que prefiere y evitar los que no, pero esto se sacrifica si es necesario para cumplir las reglas del hospital.

## Estructura del Proyecto

* **`ProblemaProgramacionEnfermeras`:** Define la plantilla de 8 enfermeras y calcula el fitness basado en las penalizaciones descritas arriba.
* **`eaSimpleConElitismo`:** Motor evolutivo modificado.
* **`AG_Horario_de_enfermeras.py`:** Script de ejecución y visualización.

## Tecnologías y Librerías
El proyecto está desarrollado en Python y utiliza las siguientes librerías clave:

* **DEAP (Distributed Evolutionary Algorithms in Python):** El *framework* principal para implementar el Algoritmo Genético, incluyendo la selección, cruce y mutación.
* **NumPy / Pandas:** Utilizado para la manipulación eficiente de datos y la estructuración del horario.
* **Matplotlib / Seaborn:** Para la visualización de la convergencia del algoritmo (gráfica de Fitness).
* **OpenPyXL:** Para generar el archivo de horario final en formato Excel (`.xlsx`) con un formato visual claro.

## Instrucciones de Ejecución

1.  Instalar dependencias:
    ```bash
    pip install -r requirements.txt
    ```
2.  Ejecutar el optimizador:
    ```bash
    python AG_Horario_de_enfermeras.py
    ```
    
Al finalizar, el sistema genera:
* **Consola:** Reporte de violaciones restantes (si las hay).
* **Excel:** Archivo `horario_enfermeras.xlsx` con la tabla de turnos.
* **Gráfica:** Curva de convergencia del algoritmo.

## Excel Output Horario
![Excel Output](imágenes/horario_enfermeras_AG.png)
