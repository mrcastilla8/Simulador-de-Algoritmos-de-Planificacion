"""
Archivo: src/metrics.py
Responsable principal: Desarrollador 5 (ANGEL)

Implementa la función de apoyo para calcular todas las métricas
de rendimiento (finalización, retorno, espera, respuesta)
basándose en los segmentos de Gantt generados por un algoritmo.
"""

from typing import List, Tuple, Dict, Optional
from .models import Proceso, SegmentoGantt, ResultadoProceso, MetricasPromedio


def calcular_metricas(
    procesos: List[Proceso],
    segmentos_gantt: List[SegmentoGantt]
) -> Tuple[List[ResultadoProceso], MetricasPromedio]:
    """
    Calcula las métricas de rendimiento para cada proceso y los promedios
    generales, basándose en los segmentos de Gantt.

    Además calcula el número de cambios de contexto a partir de los segmentos.
    """

    # Asegurar que los segmentos estén ordenados por tiempo
    segmentos_ordenados = sorted(
        segmentos_gantt,
        key=lambda s: (s.inicio, s.fin)
    )

    # 1. Crear diccionarios para acceso rápido
    # (nombre -> Proceso original)
    mapa_procesos: Dict[str, Proceso] = {p.nombre: p for p in procesos}

    # 2. Inicializar estructuras para calcular métricas
    # (nombre -> primer_inicio)
    mapa_tiempo_respuesta_inicio: Dict[str, int] = {}
    # (nombre -> ultimo_fin)
    mapa_tiempo_finalizacion: Dict[str, int] = {}

    # 3. Analizar los segmentos de Gantt
    # También aprovechamos para contar cambios de contexto
    cambios_contexto: int = 0
    proceso_anterior: Optional[str] = None

    for segmento in segmentos_ordenados:
        nombre_proceso = segmento.proceso

        # Contar cambios de contexto: cada vez que cambia el proceso
        if proceso_anterior is None:
            proceso_anterior = nombre_proceso
        elif nombre_proceso != proceso_anterior:
            cambios_contexto += 1
            proceso_anterior = nombre_proceso

        # Tiempo de respuesta: primera vez que entra a CPU
        if nombre_proceso not in mapa_tiempo_respuesta_inicio:
            mapa_tiempo_respuesta_inicio[nombre_proceso] = segmento.inicio

        # Tiempo de finalización: último fin
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

        finalizacion = mapa_tiempo_finalizacion.get(nombre, 0)
        primer_inicio = mapa_tiempo_respuesta_inicio.get(nombre, 0)

        # Tiempo de Retorno = Finalización - Llegada
        retorno = finalizacion - llegada

        # Tiempo de Espera = Retorno - Duración CPU
        espera = retorno - duracion

        # Tiempo de Respuesta = Primer Inicio - Llegada
        respuesta = primer_inicio - llegada

        total_retorno += retorno
        total_espera += espera
        total_respuesta += respuesta

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

    # Añadir cambios de contexto como métrica adicional
    promedios["cambios_contexto"] = float(cambios_contexto)

    return resultados_individuales, promedios
