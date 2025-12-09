# Programación de Horarios de Enfermeras mediante Heurísticas Evolutivas

La **programación de horarios de enfermeras** es un problema clásico de optimización combinatoria que consiste en asignar turnos de trabajo cumpliendo estrictas normativas operativas, laborales y de cobertura, al mismo tiempo que se busca respetar, en la medida de lo posible, las preferencias individuales del personal.

Este repositorio presenta **dos enfoques distintos basados en heurísticas evolutivas** para resolver el mismo problema de asignación de turnos semanales para un equipo de **8 enfermeras**, considerando **restricciones duras** (obligatorias) y **restricciones suaves** (preferencias). Ambos proyectos persiguen el mismo objetivo general, pero difieren en la técnica de optimización empleada y en la forma de representar y explorar el espacio de soluciones.

## Objetivo General

Encontrar un horario semanal **factible y de alta calidad** que:

- Cumpla todas las **restricciones operativas del hospital**.
- Limite la **carga laboral** de cada enfermera.
- Respete los **descansos y la continuidad temporal**.
- Minimice el incumplimiento de **preferencias individuales de turno**.

## Enfoques Implementados

### Algoritmos Genéticos con Elitismo

El primer proyecto implementa una solución basada en **Algoritmos Genéticos**, utilizando operadores clásicos de selección, cruza y mutación, junto con un **mecanismo de elitismo** que preserva las mejores soluciones encontradas durante la evolución.

Este enfoque se distingue por:
- Función de fitness basada en penalizaciones.
- Uso de un Salón de la Fama (elitismo).
- Generación automática de reportes en Excel.
- Visualización de la convergencia del fitness.

Archivo principal:
- `AG_Horario_de_enfermeras.py`

### Evolución Diferencial Multiobjetivo

El segundo proyecto aborda el problema utilizando **Evolución Diferencial**, una técnica de optimización continua que trabaja con poblaciones de vectores reales, los cuales son posteriormente transformados a decisiones discretas para representar la asignación de turnos.

Este enfoque se caracteriza por:
- Optimización jerárquica (lexicográfica).
- Mecanismos anti-estancamiento.
- Manejo explícito de continuidad temporal cíclica.
- Visualización gráfica directa del horario resultante.

Archivo principal:
- `EDM_Horario_de_enfermeras.py`

## Comparación General

Ambos proyectos:

- Resuelven el mismo problema de programación de horarios.
- Comparten la misma lógica de restricciones operativas.
- Utilizan **metaheurísticas evolutivas**.
- Buscan soluciones factibles antes que óptimas irreales.
