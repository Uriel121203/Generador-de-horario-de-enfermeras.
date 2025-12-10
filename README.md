# Generador de Horario de Enfermeras mediante Heurísticas Evolutivas 

Este repositorio presenta **dos enfoques distintos basados en heurísticas evolutivas** para resolver el mismo problema **de generación de horarios** para un equipo de **8 enfermeras**, considerando **restricciones duras** (obligatorias) y **restricciones suaves** (preferencias). Ambos proyectos persiguen el mismo objetivo general, pero difieren en la técnica de optimización empleada y en la forma de representar y explorar el espacio de soluciones.

---

## Objetivo General

Encontrar un horario semanal que:

- Cumpla todas las **restricciones operativas del hospital**.
- Limite la **carga laboral semanal** del personal.
- Garantice **descansos adecuados y continuidad temporal**.
- Minimice las **violaciones a las preferencias individuales** de turno.

---

## Enfoques Implementados

### Evolución Diferencial Multiobjetivo

Este enfoque utiliza **Evolución Diferencial**, una técnica de optimización continua que trabaja sobre poblaciones de vectores de números reales, los cuales posteriormente se transforman a decisiones discretas mediante un umbral de activación.

Características principales:

- Optimización jerárquica.
- Representación continua → discreta.
- Control de continuidad temporal cíclica.
- Mecanismos anti-estancamiento.
- Visualización gráfica del horario resultante.

Archivo principal:

- `EDM_Horario_de_enfermeras.py`

---

### Algoritmos Genéticos con Elitismo

Este enfoque implementa un **Algoritmo Genético clásico**, basado en selección, cruza y mutación, incorporando **elitismo** mediante un Salón de la Fama para preservar las mejores soluciones encontradas.

Características principales:

- Representación binaria directa.
- Función de fitness basada en penalizaciones.
- Elitismo explícito.
- Exportación de resultados a Excel.
- Gráficas de convergencia del fitness.

Archivo principal:

- `AG_Horario_de_enfermeras.py`

---

## Representación de los Individuos

Una diferencia fundamental entre ambos métodos es la representación de una solución candidata.

### Algoritmos Genéticos

Cada enfermera se representa como un **vector binario** de 21 posiciones (7 días × 3 turnos):

	(0,1,0,1,1,0,1,0,0,0,0,1,0,1,0,1,0,1,0,1,1)

Cada bit indica la asignación o no de un turno.

###  Evolución Diferencial Multiobjetivo

Cada enfermera se representa como un vector de valores reales, el cual se transforma posteriormente a binario mediante un umbral:

	[0.23, 0.45, 0.46, 0.90, 0.67, 0.65, 0.34, 0.54, 0.46, 0.23, 0.50, 0.21, ...]

##  Eficiencia Computacional

Durante la fase experimental se observó una diferencia clara en la eficiencia de ambos enfoques, medida en términos del número de generaciones necesarias para alcanzar una solución viable y estable:

- **Algoritmos Genéticos:** 300 generaciones.
- **Evolución Diferencial Multiobjetivo:** 1500 generaciones.

Esto indica que, para este problema específico, los Algoritmos Genéticos convergen de manera más rápida hacia soluciones de alta calidad, mientras que la Evolución Diferencial requiere un mayor número de iteraciones para estabilizarse.

## Resultados Obtenidos

Ambos enfoques lograron generar **horarios completamente viables**, cumpliendo todas las restricciones duras establecidas por el hospital.

### Algoritmos Genéticos

- Violaciones por turnos consecutivos: 0  
- Violaciones por exceso de turnos semanales: 0  
- Violaciones por cobertura de personal: 0  
- Violaciones a preferencias personales: **2**

### Evolución Diferencial Multiobjetivo

- Violaciones por turnos consecutivos: 0  
- Violaciones por exceso de turnos semanales: 0  
- Violaciones por cobertura de personal: 0  
- Violaciones a preferencias personales: **7**

## Tabla Comparativa: AG vs DEM

| Criterio | Algoritmos Genéticos (AG) | Evolución Diferencial Multiobjetivo (DEM) |
|--------|---------------------------|------------------------------------------|
| Representación del individuo | Binaria (0/1) | Continua (valores reales) |
| Dimensión por enfermera | 21 bits | 21 valores reales |
| Conversión real → binario | No | Sí (umbral) |
| Generaciones necesarias | **300** | **1500** |
| Violaciones duras | 0 | 0 |
| Violaciones a preferencias | **2** | **7** |
| Tipo de optimización | Penalización | Multiobjetivo jerárquico |
| Complejidad computacional | Baja | Mayor |
| Calidad del resultado | **Alta** | Media |
| Eficiencia global | **Alta** | Moderada |

## Conclusión

Los resultados obtenidos muestran que **ambos enfoques evolutivos son capaces de generar un horario aceptable**, ya que en ambos casos se cumple estrictamente con todas las restricciones duras impuestas por la normativa del hospital. Esto confirma la robustez de las metaheurísticas evolutivas para abordar problemas de optimización combinatoria con múltiples restricciones.

No obstante, se observan diferencias claras en términos de eficiencia computacional y calidad de la solución final.  

Los **Algoritmos Genéticos** presentan una convergencia más rápida, alcanzando soluciones estables en un menor número de generaciones. Esto se debe principalmente a su representación binaria directa y al uso de elitismo, lo cual permite preservar y refinar las mejores soluciones a lo largo de la evolución.

Por otro lado, la **Evolución Diferencial Multiobjetivo**, al trabajar en un espacio continuo, requiere un proceso adicional de transformación real–discreto mediante un umbral. Aunque este enfoque proporciona mayor flexibilidad y generalidad, introduce una mayor complejidad computacional y una convergencia más lenta para este problema específico.

En términos de calidad, ambos métodos evitan completamente violaciones a las restricciones duras; sin embargo, la Evolución Diferencial Multiobjetivo presenta un mayor número de violaciones a las preferencias personales del personal de enfermería, lo que impacta directamente en la satisfacción del personal.
