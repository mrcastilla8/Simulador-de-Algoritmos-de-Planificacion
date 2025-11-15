from typing import List, Optional
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from .models import SegmentoGantt



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
    
    
    
timeline_parts = []
    chart_parts = []
    
    if not segmentos_gantt:
        return "No hay segmentos de Gantt para mostrar."

    
    
    primer_segmento = segmentos_gantt[0]
    tiempo_inicio_str = str(primer_segmento.inicio)
    
    timeline_parts.append(tiempo_inicio_str)
    
    chart_parts.append(" " * len(tiempo_inicio_str)) 

    
    for segmento in segmentos_gantt:
        proceso_str = segmento.proceso
        tiempo_fin_str = str(segmento.fin)
        
        
        
        padding_proceso = 4
        bloque_proceso_str = f" {proceso_str.ljust(padding_proceso)} "
        
        
        bloque_chart = f"|{bloque_proceso_str}|"
        
        
        
        ancho_bloque = len(bloque_chart)
        relleno_timeline = " " * (ancho_bloque - len(tiempo_fin_str))
        
        
        timeline_parts.append(relleno_timeline + tiempo_fin_str)
        chart_parts.append(bloque_chart)

    
timeline_str = "".join(timeline_parts)
    chart_str = "".join(chart_parts)
    
    return f"{timeline_str}\n{chart_str}"


def imprimir_gantt(segmentos_gantt: List[SegmentoGantt]):
    
    gantt_string = formatear_gantt_string(segmentos_gantt)
    print(gantt_string)

def graficar_gantt(
    segmentos_gantt: List[SegmentoGantt],
    nombre_algoritmo: str,
    nombre_escenario: str,
    guardar_como: Optional[str] = None,
    mostrar: bool = True,
) -> None:
    
    
    if not segmentos_gantt:
        print("No hay segmentos de Gantt para graficar.")
        return
    
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    
    procesos_unicos = []
    for seg in segmentos_gantt:
        if seg.proceso not in procesos_unicos:
            procesos_unicos.append(seg.proceso)
    
    
    proceso_a_y = {proc: i for i, proc in enumerate(reversed(procesos_unicos))}
    
    
    tiempo_minimo = min(seg.inicio for seg in segmentos_gantt)
    tiempo_maximo = max(seg.fin for seg in segmentos_gantt)
    
    
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
            fontsize=10,
            color='black'
        )
    
    
    ax.set_xlim(tiempo_minimo - 1, tiempo_maximo + 1)
    ax.set_ylim(-0.5, len(procesos_unicos) - 0.5)
    
    
    ax.set_xlabel('Tiempo (ms)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Procesos', fontsize=12, fontweight='bold')
    ax.set_title(
        f'Diagrama de Gantt - {nombre_algoritmo} ({nombre_escenario})',
        fontsize=14,
        fontweight='bold',
        pad=20
    )
    
    
    ax.set_yticks(range(len(procesos_unicos)))
    ax.set_yticklabels(reversed(procesos_unicos), fontsize=10)
    
    
    ax.set_xticks(range(tiempo_minimo, tiempo_maximo + 1, max(1, (tiempo_maximo - tiempo_minimo) // 10)))
    ax.grid(True, axis='x', alpha=0.3, linestyle='--')
    
    
    plt.tight_layout()
    
    
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
    
    
    if not resultados:
        print("No hay resultados para graficar.")
        return
    
    num_algoritmos = len(resultados)
    fig, axes = plt.subplots(num_algoritmos, 1, figsize=(14, 3 * num_algoritmos))
    
    
    if num_algoritmos == 1:
        axes = [axes]
    
    
    for idx, (nombre_algoritmo, segmentos_gantt) in enumerate(resultados.items()):
        ax = axes[idx]
        
        if not segmentos_gantt:
            ax.text(0.5, 0.5, 'Sin datos', ha='center', va='center',
                   transform=ax.transAxes, fontsize=12)
            continue
        
        
        procesos_unicos = []
        for seg in segmentos_gantt:
            if seg.proceso not in procesos_unicos:
                procesos_unicos.append(seg.proceso)
        
        proceso_a_y = {proc: i for i, proc in enumerate(reversed(procesos_unicos))}
        
        
        tiempo_minimo = min(seg.inicio for seg in segmentos_gantt)
        tiempo_maximo = max(seg.fin for seg in segmentos_gantt)
        
        
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