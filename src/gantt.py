"""
Archivo: src/gantt.py
Responsable principal: Desarrollador 5 (ANGEL)

Provee funciones para generar una representación textual del
diagrama de Gantt para mostrar en la consola.
"""

from typing import List
from .models import SegmentoGantt

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