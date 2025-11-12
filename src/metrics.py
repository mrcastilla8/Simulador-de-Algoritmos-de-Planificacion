"""
Archivo: src/metrics.py
Responsable principal: Desarrollador 5

Funciones para calcular métricas de los procesos a partir
de los segmentos de Gantt.
"""

from typing import List, Dict, Tuple
from .models import Proceso, SegmentoGantt, ResultadoProceso


def calcular_metricas(
    procesos: List[Proceso],
    segmentos_gantt: List[SegmentoGantt],
) -> Tuple[List[ResultadoProceso], Dict[str, float]]:
    """
    Calcula las métricas individuales y los promedios para cada proceso.

    Debe:
    - Para cada proceso:
      - Determinar tiempo_finalizacion (último fin en sus segmentos).
      - tiempo_retorno = tiempo_finalizacion - llegada.
      - tiempo_espera = tiempo_retorno - duracion_cpu.
      - tiempo_respuesta = primer_inicio_en_CPU - llegada.
    - Calcular promedios para cada métrica.

    Retorna:
    - Lista de ResultadoProceso.
    - Diccionario de promedios, por ejemplo:
      {
          "promedio_retorno": ...,
          "promedio_espera": ...,
          "promedio_respuesta": ...,
      }

    TODO: Implementar el cálculo de métricas y promedios.
    """
    raise NotImplementedError("calcular_metricas aún no está implementado.")
