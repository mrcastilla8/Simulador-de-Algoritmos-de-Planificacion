"""
Archivo: src/algorithms/srtf.py
Responsable principal: Desarrollador 3

Implementa el algoritmo SRTF (Shortest Remaining Time First, expropiativo).
"""

from typing import List
from ..models import Proceso, ResultadoAlgoritmo, SegmentoGantt, ResultadoProceso
from ..metrics import calcular_metricas


def simular_srtf(procesos: List[Proceso]) -> ResultadoAlgoritmo:
    """
    Simula el algoritmo SRTF (preemptive).

    Debe:
    - Mantener tiempos restantes por proceso.
    - Avanzar el tiempo actual (por ejemplo, en pasos de 1 ms).
    - En cada paso, seleccionar el proceso con menor tiempo restante.
    - Crear segmentos de Gantt dividiendo cuando cambia el proceso en ejecución.
    - Usar calcular_metricas(...) al final.
    - Devolver un ResultadoAlgoritmo.

    TODO: Implementar la lógica de simulación SRTF.
    """
    raise NotImplementedError("simular_srtf aún no está implementado.")
