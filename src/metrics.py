"""
Archivo: src/metrics.py
Responsable principal: Desarrollador 5 (ANGEL)

Implementa la función de apoyo para calcular todas las métricas
de rendimiento (finalización, retorno, espera, respuesta)
basándose en los segmentos de Gantt generados por un algoritmo.
"""

from typing import List, Tuple, Dict
# Importamos las clases y tipos necesarios de models.py
from .models import Proceso, SegmentoGantt, ResultadoProceso, MetricasPromedio


def calcular_metricas(
    procesos: List[Proceso], 
    segmentos_gantt: List[SegmentoGantt]
) -> Tuple[List[ResultadoProceso], MetricasPromedio]:
    """
    Calcula las métricas de rendimiento para cada proceso y los promedios
    generales, basándose en los segmentos de Gantt.
    """
    
    # 1. Crear diccionarios para acceso rápido
    # (nombre -> Proceso original)
    mapa_procesos: Dict[str, Proceso] = {p.nombre: p for p in procesos}
    
    # 2. Inicializar estructuras para calcular métricas
    # (nombre -> primer_inicio)
    mapa_tiempo_respuesta_inicio: Dict[str, int] = {}
    # (nombre -> ultimo_fin)
    mapa_tiempo_finalizacion: Dict[str, int] = {}

    # 3. Analizar los segmentos de Gantt
    # Los segmentos deben estar ordenados por tiempo para que esto funcione
    for segmento in segmentos_gantt:
        nombre_proceso = segmento.proceso
        
        # Calcular Tiempo de Respuesta (primera vez que se ejecuta)
        if nombre_proceso not in mapa_tiempo_respuesta_inicio:
            mapa_tiempo_respuesta_inicio[nombre_proceso] = segmento.inicio
            
        # Actualizar Tiempo de Finalización (última vez que terminó)
        mapa_tiempo_finalizacion[nombre_proceso] = max(
            mapa_tiempo_finalizacion.get(nombre_proceso, 0),
            segmento.fin
        )

    # 4. Calcular métricas individuales
    resultados_individuales: List[ResultadoProceso] = []
    
    total_retorno = 0
    total_espera = 0
    total_respuesta = 0
    
    # Iteramos sobre los procesos originales para mantener el orden
    for proceso in procesos:
        nombre = proceso.nombre
        llegada = proceso.llegada
        duracion = proceso.duracion_cpu
        
        # Obtener métricas calculadas
        finalizacion = mapa_tiempo_finalizacion.get(nombre, 0)
        primer_inicio = mapa_tiempo_respuesta_inicio.get(nombre, 0)

        # Calcular métricas derivadas (según el plan)
        # Tiempo de Retorno = Finalización - Llegada
        retorno = finalizacion - llegada
        
        # Tiempo de Espera = Retorno - Duración CPU
        espera = retorno - duracion
        
        # Tiempo de Respuesta = Primer Inicio - Llegada
        respuesta = primer_inicio - llegada

        # Acumular para promedios
        total_retorno += retorno
        total_espera += espera
        total_respuesta += respuesta
        
        # Guardar resultado
        resultados_individuales.append(ResultadoProceso(
            nombre=nombre,
            llegada=llegada,
            duracion_cpu=duracion,
            tiempo_finalizacion=finalizacion,
            tiempo_retorno=retorno,
            tiempo_espera=espera,
            tiempo_respuesta=respuesta
        ))

    # 5. Calcular promedios
    num_procesos = len(procesos)
    promedios: MetricasPromedio = {
        "tiempo_retorno_promedio": total_retorno / num_procesos if num_procesos > 0 else 0,
        "tiempo_espera_promedio": total_espera / num_procesos if num_procesos > 0 else 0,
        "tiempo_respuesta_promedio": total_respuesta / num_procesos if num_procesos > 0 else 0,
    }

    return resultados_individuales, promedios