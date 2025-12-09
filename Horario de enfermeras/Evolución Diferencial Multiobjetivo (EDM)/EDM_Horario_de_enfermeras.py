import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import ListedColormap

# ==========================================
# 1. CONFIGURACIÓN (NUEVA ESTRUCTURA)
# ==========================================
NUM_ENFERMERAS = 8
DIAS = 7
TURNOS_DIA = 3  # Mañana, Tarde, Noche
TOTAL_SLOTS = DIAS * TURNOS_DIA # 21 slots en total por enfermera

# Mapeo de índices de slots a tipo de turno
# Slot 0=M, 1=T, 2=N, 3=M, 4=T, 5=N ...
IDX_MANANA = 0
IDX_TARDE = 1
IDX_NOCHE = 2

# Restricciones de Personal por Tipo de Turno (Min, Max)
RESTRICCION_STAFF = {
    IDX_MANANA: (2, 3), # Mañana
    IDX_TARDE:  (2, 4), # Tarde
    IDX_NOCHE:  (1, 2)  # Noche
}

MAX_TURNOS_SEMANA = 5

# Preferencias 
# Convertimos las preferencias originales (1,2,3) a nuestros nuevos índices (0,1,2)
# 0: Mañana, 1: Tarde, 2: Noche
PREFERENCIAS = {
    0: [0],       # Enf 1: Mañana
    1: [0, 1],    # Enf 2: Mañana o Tarde
    2: [1, 2],    # Enf 3: Tarde o Noche
    3: [1],       # Enf 4: Tarde
    4: [2],       # Enf 5: Noche
    5: [0, 1, 2], # Enf 6: Cualquiera
    6: [1, 2],    # Enf 7: Tarde o Noche
    7: [0, 1, 2]  # Enf 8: Cualquiera
}

# ==========================================
# 2. MODELO Y EVALUACIÓN
# ==========================================

def decodificar_vector(vector):
    """
    Convierte vector continuo en matriz binaria (Enfermeras x 21 Slots).
    1 = Trabaja ese turno específico, 0 = No trabaja.
    """
    matriz = vector.reshape((NUM_ENFERMERAS, TOTAL_SLOTS))
    horario = np.zeros((NUM_ENFERMERAS, TOTAL_SLOTS), dtype=int)
    
    # Umbral de activación: Probamos con 0.4 para fomentar que trabajen
    # Si el gen es > 0.4, se asigna el turno.
    horario[matriz > 0.5] = 1 
    return horario

def evaluar_horario(horario):
    hard_constraints = 0
    soft_constraints = 0
    
    # ... (Parte A: Cobertura de Personal se queda igual) ...
    for slot in range(TOTAL_SLOTS):
        tipo_turno = slot % 3 
        total_enfermeras = np.sum(horario[:, slot])
        t_min, t_max = RESTRICCION_STAFF[tipo_turno]
        
        if total_enfermeras < t_min:
            hard_constraints += (t_min - total_enfermeras) * 2000
        elif total_enfermeras > t_max:
            hard_constraints += (total_enfermeras - t_max) * 2000 

    # B. Restricciones por Enfermera
    for n in range(NUM_ENFERMERAS):
        fila = horario[n, :]
        
        # 1. Máximo 5 turnos
        turnos_trabajados = np.sum(fila)
        if turnos_trabajados > MAX_TURNOS_SEMANA:
            hard_constraints += (turnos_trabajados - MAX_TURNOS_SEMANA) * 2000
            
        # 2. TURNOS CONSECUTIVOS (Lineal: Lunes a Domingo)
        for k in range(TOTAL_SLOTS - 1):
            if fila[k] == 1 and fila[k+1] == 1:
                hard_constraints += 2000 

        # 3. TURNO CÍCLICO (Domingo Noche -> Lunes Mañana)
        # Esto se pone FUERA del bucle 'for k', a la misma altura (indentación)
        # Verificamos el último slot (20) y el primero (0)
        ultimo_slot = TOTAL_SLOTS - 1 # Slot 20
        primer_slot = 0               # Slot 0
        
        if fila[ultimo_slot] == 1 and fila[primer_slot] == 1:
            hard_constraints += 2000 # Penalización por rotación cíclica prohibida

    # --- 2. PREFERENCIAS ---
    if hard_constraints == 0: # Solo optimizamos preferencias si es legal
        for n in range(NUM_ENFERMERAS):
            prefs = PREFERENCIAS[n]
            for slot in range(TOTAL_SLOTS):
                if horario[n, slot] == 1:
                    tipo_turno = slot % 3
                    if tipo_turno not in prefs:
                        soft_constraints += 1

    return hard_constraints, soft_constraints

# ==========================================
# 3. MOTOR DE EVOLUCIÓN DIFERENCIAL
# ==========================================

POBLACION_TAM = 300
GENERACIONES = 1500 
CR = 0.9 
DIMENSION = NUM_ENFERMERAS * TOTAL_SLOTS

class Individuo:
    def __init__(self, vector=None):
        if vector is None:
            self.vector = np.random.rand(DIMENSION)
        else:
            self.vector = vector
        self.horario = decodificar_vector(self.vector)
        self.hard, self.soft = evaluar_horario(self.horario)
        
    def domina(self, otro):
        if self.hard == 0 and otro.hard == 0:
            return self.soft < otro.soft
        if self.hard == 0 and otro.hard > 0:
            return True
        if self.hard > 0 and otro.hard == 0:
            return False
        return self.hard < otro.hard

def main():
    print("Generando horarios con turnos múltiples permitidos...")
    poblacion = [Individuo() for _ in range(POBLACION_TAM)]
    mejor = min(poblacion, key=lambda x: (x.hard, x.soft))
    
    sin_cambios = 0

    for gen in range(GENERACIONES):
        # Dithering para evitar estancamiento
        F = np.random.uniform(0.4, 0.6)
        
        nueva_poblacion = []
        for i in range(POBLACION_TAM):
            x = poblacion[i]
            
            idxs = [idx for idx in range(POBLACION_TAM) if idx != i]
            a, b, c = np.random.choice(idxs, 3, replace=False)
            
            # Mutación DE/rand/1/bin
            v_mut = poblacion[a].vector + F * (poblacion[b].vector - poblacion[c].vector)
            v_mut = np.clip(v_mut, 0, 1)
            
            v_prueba = np.copy(x.vector)
            j_rand = np.random.randint(DIMENSION)
            mask = np.random.rand(DIMENSION) < CR
            mask[j_rand] = True
            v_prueba[mask] = v_mut[mask]
            
            cand = Individuo(v_prueba)
            
            if cand.domina(x):
                nueva_poblacion.append(cand)
                if cand.domina(mejor):
                    mejor = cand
                    sin_cambios = 0
            else:
                nueva_poblacion.append(x)
        
        poblacion = nueva_poblacion
        sin_cambios += 1
        
        if gen % 50 == 0:
            print(f"Gen {gen}: Hard={mejor.hard}, Soft={mejor.soft}")
            if mejor.hard == 0 and mejor.soft == 0:
                print(">>> ¡PERFECCIÓN ALCANZADA! <<<")
                break
            
            # Reinicio parcial si se estanca mucho tiempo
            if sin_cambios > 150 and mejor.hard > 0:
                print("! Estancamiento detectado. Inyectando sangre nueva...")
                num_nuevos = POBLACION_TAM // 3
                for k in range(num_nuevos):
                    poblacion[k] = Individuo() # Aleatorios nuevos
                sin_cambios = 0
            if sin_cambios > 150 and mejor.hard == 0 and mejor.soft > 0:
                print("! Estancamiento detectado. Inyectando sangre nueva...")
                num_nuevos = POBLACION_TAM // 3
                for k in range(num_nuevos):
                    poblacion[k] = Individuo() # Aleatorios nuevos
                sin_cambios = 0
    print("\nCalculo finalizado. Generando reporte visual...")
    visualizar_horario_grafico(mejor)

    # --- REPORTE FINAL ---
def visualizar_horario_grafico(mejor_individuo):
    """
    Genera un gráfico tipo grid/calendario con colores usando Matplotlib.
    """
    horario = mejor_individuo.horario
    
    # Configuración de la figura
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.set_title("Planificación Semanal de Enfermería (Optimizado)", fontsize=16, pad=20)
    
    # Colores
    COLOR_M = '#FFD700' # Oro (Mañana)
    COLOR_T = '#FF8C00' # Naranja Oscuro (Tarde)
    COLOR_N = '#191970' # Azul Medianoche (Noche)
    COLOR_OFF = '#F0F0F0' # Gris Claro (Descanso)
    TEXT_COLOR_N = 'white' # Texto blanco para fondo oscuro
    
    # Dibujar celdas
    dias_labels = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    
    # Configurar ejes
    ax.set_xlim(0, TOTAL_SLOTS)
    ax.set_ylim(0, NUM_ENFERMERAS)
    
    # Etiquetas Eje Y (Enfermeras) - Invertimos orden para que Enf 1 esté arriba
    ax.set_yticks(np.arange(NUM_ENFERMERAS) + 0.5)
    ax.set_yticklabels([f"Enfermera {i+1}" for i in range(NUM_ENFERMERAS)][::-1], fontsize=11)
    
    # Etiquetas Eje X (Días) - Ponemos etiquetas centradas en cada bloque de 3 slots
    ax.set_xticks(np.arange(1.5, TOTAL_SLOTS, 3))
    ax.set_xticklabels(dias_labels, fontsize=11, fontweight='bold')
    ax.tick_params(axis='x', which='both', bottom=False, top=True, labelbottom=False, labeltop=True)
    
    # Dibujando la cuadrícula
    for i in range(NUM_ENFERMERAS):
        # Invertimos índice para dibujar de arriba a abajo
        y_pos = NUM_ENFERMERAS - 1 - i
        
        for j in range(TOTAL_SLOTS):
            x_pos = j
            es_activo = horario[i, j] == 1
            tipo_turno = j % 3 # 0=M, 1=T, 2=N
            
            # Determinar color y texto
            color = COLOR_OFF
            texto = ""
            text_color = 'black'
            
            if es_activo:
                if tipo_turno == 0:
                    color = COLOR_M
                    texto = "M"
                elif tipo_turno == 1:
                    color = COLOR_T
                    texto = "T"
                elif tipo_turno == 2:
                    color = COLOR_N
                    texto = "N"
                    text_color = TEXT_COLOR_N
            
            # Dibujar rectángulo
            rect = patches.Rectangle((x_pos, y_pos), 1, 1, linewidth=1, edgecolor='white', facecolor=color)
            ax.add_patch(rect)
            
            # Añadir texto si trabaja (o un punto si descansa, opcional)
            if texto:
                ax.text(x_pos + 0.5, y_pos + 0.5, texto, 
                        ha='center', va='center', color=text_color, fontsize=10, fontweight='bold')

    # Líneas verticales divisorias de días (más gruesas)
    for d in range(1, DIAS):
        ax.axvline(x=d*3, color='black', linewidth=2)
        
    # Texto de estadísticas al pie
    info_text = (f"Violaciones Reglas (Hard): {mejor_individuo.hard}   |   "
                 f"Preferencias Ignoradas (Soft): {mejor_individuo.soft}\n"
                 f"M = Mañana ({RESTRICCION_STAFF[0][0]}-{RESTRICCION_STAFF[0][1]})  |  "
                 f"T = Tarde ({RESTRICCION_STAFF[1][0]}-{RESTRICCION_STAFF[1][1]})  |  "
                 f"N = Noche ({RESTRICCION_STAFF[2][0]}-{RESTRICCION_STAFF[2][1]})")
    
    plt.figtext(0.5, 0.02, info_text, ha="center", fontsize=10, 
                bbox={"facecolor":"white", "alpha":0.8, "pad":5, "edgecolor":"gray"})

    # Ajustar márgenes
    plt.tight_layout()
    plt.subplots_adjust(top=0.9, bottom=0.15) # Espacio para títulos y pie
    
    # Mostrar
    print("Abriendo gráfico...")
    plt.show()

if __name__ == "__main__":
    main()