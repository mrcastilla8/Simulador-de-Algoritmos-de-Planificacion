"""
Archivo: src/gantt.py
Responsable principal: Desarrollador 5 (ANGEL)

Provee funciones para generar una representación textual del
diagrama de Gantt para mostrar en la consola.
"""

from typing import List, Optional
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from .models import SegmentoGantt


# Diccionario de colores para procesos (permite hasta 10 procesos con colores distintos)
COLORES_PROCESOS = {
    'P1': '#FF6B6B',
    'P2': '#4ECDC4',
    'P3': '#45B7D1',
    'P4': '#FFA07A',
    'P5': '#98D8C8',
    'P6': '#F7DC6F',
    'P7': '#BB8FCE',
    'P8': '#85C1E2',
    'P9': '#F8B88B',
    'P10': '#ABEBC6',
}


def formatear_gantt_string(segmentos_gantt: List[SegmentoGantt]) -> str:
    """
    Toma una lista de segmentos de Gantt (ordenados por tiempo) y 
    retorna un string de dos líneas (timeline y chart) 
    listo para imprimir.
    """
    
    # Listas para ir construyendo las partes de cada línea
    timeline_parts = []
    chart_parts = []
    
    if not segmentos_gantt:
        return "No hay segmentos de Gantt para mostrar."

    # 1. Manejar el inicio del Gantt
    # El primer tiempo es el inicio del primer segmento
    primer_segmento = segmentos_gantt[0]
    tiempo_inicio_str = str(primer_segmento.inicio)
    
    timeline_parts.append(tiempo_inicio_str)
    # Agregamos un espacio en el gráfico para alinear el primer '|'
    chart_parts.append(" " * len(tiempo_inicio_str)) 

    # 2. Iterar sobre cada segmento
    for segmento in segmentos_gantt:
        proceso_str = segmento.proceso
        tiempo_fin_str = str(segmento.fin)
        
        # Estandarizar el ancho del bloque de proceso (ej: "| P1  |")
        # Ajusta el 'padding' (ej: 4) si los nombres son más largos (P10, P100)
        padding_proceso = 4
        bloque_proceso_str = f" {proceso_str.ljust(padding_proceso)} "
        
        # Crear el bloque del gráfico (ej: "| P1    |")
        bloque_chart = f"|{bloque_proceso_str}|"
        
        # Calcular cuántos espacios de relleno necesita la línea de tiempo
        # para alinear el 'tiempo_fin_str' con el final del bloque
        ancho_bloque = len(bloque_chart)
        relleno_timeline = " " * (ancho_bloque - len(tiempo_fin_str))
        
        # Armar las partes
        timeline_parts.append(relleno_timeline + tiempo_fin_str)
        chart_parts.append(bloque_chart)

    # 3. Unir todas las partes
    timeline_str = "".join(timeline_parts)
    chart_str = "".join(chart_parts)
    
    return f"{timeline_str}\n{chart_str}"


def imprimir_gantt(segmentos_gantt: List[SegmentoGantt]):
    """
    Función de conveniencia que formatea y luego imprime
    directamente en consola el diagrama de Gantt.
    """
    gantt_string = formatear_gantt_string(segmentos_gantt)
    print(gantt_string)


def graficar_gantt(
    segmentos_gantt: List[SegmentoGantt],
    nombre_algoritmo: str,
    nombre_escenario: str,
    guardar_como: Optional[str] = None,
    mostrar: bool = True,
) -> None:
    """
    Crea un diagrama de Gantt gráfico usando matplotlib.
    
    Args:
        segmentos_gantt: Lista de segmentos de Gantt ordenados por tiempo
        nombre_algoritmo: Nombre del algoritmo (ej: "FCFS", "SJF", etc.)
        nombre_escenario: Nombre del escenario (ej: "Escenario 1")
        guardar_como: Ruta de archivo para guardar la imagen (opcional)
    """
    
    if not segmentos_gantt:
        print("No hay segmentos de Gantt para graficar.")
        return
    
    # Crear figura y ejes
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # Obtener procesos únicos y asignarles posiciones en Y
    procesos_unicos = []
    for seg in segmentos_gantt:
        if seg.proceso not in procesos_unicos:
            procesos_unicos.append(seg.proceso)
    
    # Crear mapeo de proceso a posición Y
    proceso_a_y = {proc: i for i, proc in enumerate(reversed(procesos_unicos))}
    
    # Obtener rango de tiempo
    tiempo_minimo = min(seg.inicio for seg in segmentos_gantt)
    tiempo_maximo = max(seg.fin for seg in segmentos_gantt)
    
    # Dibujar los segmentos de Gantt
    for segmento in segmentos_gantt:
        y_pos = proceso_a_y[segmento.proceso]
        duracion = segmento.fin - segmento.inicio
        
        # Obtener color del proceso
        color = COLORES_PROCESOS.get(segmento.proceso, '#95A5A6')
        
        # Crear rectángulo
        rect = mpatches.Rectangle(
            (segmento.inicio, y_pos - 0.4),
            duracion,
            0.8,
            linewidth=2,
            edgecolor='black',
            facecolor=color,
            alpha=0.8
        )
        ax.add_patch(rect)
        
        # Añadir etiqueta del proceso dentro del rectángulo
        x_center = segmento.inicio + duracion / 2
        ax.text(
            x_center,
            y_pos,
            segmento.proceso,
            ha='center',
            va='center',
            fontweight='bold',
            fontsize=10,
            color='black'
        )
    
    # Configurar los ejes
    ax.set_xlim(tiempo_minimo - 1, tiempo_maximo + 1)
    ax.set_ylim(-0.5, len(procesos_unicos) - 0.5)
    
    # Etiquetas y títulos
    ax.set_xlabel('Tiempo (ms)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Procesos', fontsize=12, fontweight='bold')
    ax.set_title(
        f'Diagrama de Gantt - {nombre_algoritmo} ({nombre_escenario})',
        fontsize=14,
        fontweight='bold',
        pad=20
    )
    
    # Configurar eje Y con nombres de procesos
    ax.set_yticks(range(len(procesos_unicos)))
    ax.set_yticklabels(reversed(procesos_unicos), fontsize=10)
    
    # Configurar eje X con marcas de tiempo
    ax.set_xticks(range(tiempo_minimo, tiempo_maximo + 1, max(1, (tiempo_maximo - tiempo_minimo) // 10)))
    ax.grid(True, axis='x', alpha=0.3, linestyle='--')
    
    # Ajustar espaciado
    plt.tight_layout()
    
    # Guardar o mostrar
    if guardar_como:
        plt.savefig(guardar_como, dpi=100, bbox_inches='tight')
        print(f"Diagrama guardado en: {guardar_como}")
    
    plt.show()


def graficar_gantt_subplots(
    resultados: dict,
    nombre_escenario: str,
    guardar_como: Optional[str] = None,
    mostrar: bool = True,
) -> None:
    """
    Crea una figura con múltiples subplots, uno para cada algoritmo.
    Útil para comparar visualmente diferentes algoritmos en el mismo escenario.
    
    Args:
        resultados: Diccionario {nombre_algoritmo: segmentos_gantt}
        nombre_escenario: Nombre del escenario
        guardar_como: Ruta de archivo para guardar la imagen (opcional)
    """
    
    if not resultados:
        print("No hay resultados para graficar.")
        return
    
    num_algoritmos = len(resultados)
    fig, axes = plt.subplots(num_algoritmos, 1, figsize=(14, 3 * num_algoritmos))
    
    # Si hay un solo algoritmo, axes no es un array
    if num_algoritmos == 1:
        axes = [axes]
    
    # Procesar cada algoritmo
    for idx, (nombre_algoritmo, segmentos_gantt) in enumerate(resultados.items()):
        ax = axes[idx]
        
        if not segmentos_gantt:
            ax.text(0.5, 0.5, 'Sin datos', ha='center', va='center',
                   transform=ax.transAxes, fontsize=12)
            continue
        
        # Obtener procesos únicos
        procesos_unicos = []
        for seg in segmentos_gantt:
            if seg.proceso not in procesos_unicos:
                procesos_unicos.append(seg.proceso)
        
        proceso_a_y = {proc: i for i, proc in enumerate(reversed(procesos_unicos))}
        
        # Obtener rango de tiempo
        tiempo_minimo = min(seg.inicio for seg in segmentos_gantt)
        tiempo_maximo = max(seg.fin for seg in segmentos_gantt)
        
        # Dibujar segmentos
        for segmento in segmentos_gantt:
            y_pos = proceso_a_y[segmento.proceso]
            duracion = segmento.fin - segmento.inicio
            color = COLORES_PROCESOS.get(segmento.proceso, '#95A5A6')
            
            rect = mpatches.Rectangle(
                (segmento.inicio, y_pos - 0.4),
                duracion,
                0.8,
                linewidth=2,
                edgecolor='black',
                facecolor=color,
                alpha=0.8
            )
            ax.add_patch(rect)
            
            x_center = segmento.inicio + duracion / 2
            ax.text(
                x_center,
                y_pos,
                segmento.proceso,
                ha='center',
                va='center',
                fontweight='bold',
                fontsize=9,
                color='black'
            )
        
        # Configurar ejes
        ax.set_xlim(tiempo_minimo - 1, tiempo_maximo + 1)
        ax.set_ylim(-0.5, len(procesos_unicos) - 0.5)
        ax.set_xlabel('Tiempo (ms)', fontsize=10)
        ax.set_ylabel('Procesos', fontsize=10)
        ax.set_title(f'{nombre_algoritmo}', fontsize=12, fontweight='bold')
        ax.set_yticks(range(len(procesos_unicos)))
        ax.set_yticklabels(reversed(procesos_unicos), fontsize=9)
        ax.set_xticks(range(tiempo_minimo, tiempo_maximo + 1, 
                           max(1, (tiempo_maximo - tiempo_minimo) // 10)))
        ax.grid(True, axis='x', alpha=0.3, linestyle='--')
    
    fig.suptitle(f'Diagramas de Gantt - {nombre_escenario}', 
                 fontsize=14, fontweight='bold', y=1.00)
    plt.tight_layout()
    
    if guardar_como:
        plt.savefig(guardar_como, dpi=100, bbox_inches='tight')
        print(f"Diagrama guardado en: {guardar_como}")
    
    plt.show()