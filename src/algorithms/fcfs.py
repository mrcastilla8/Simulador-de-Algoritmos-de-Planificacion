"""
Archivo: src/algorithms/fcfs.py
Responsable principal: Desarrollador 2

Implementa el algoritmo FCFS (First Come First Served).
"""

from typing import List
from ..models import Proceso, ResultadoAlgoritmo, SegmentoGantt, ResultadoProceso
from ..metrics import calcular_metricas


def simular_fcfs(procesos: List[Proceso]) -> ResultadoAlgoritmo:
    """
    Simula el algoritmo FCFS sobre la lista de procesos dada.

    Debe:
    - Ordenar los procesos por tiempo de llegada.
    - Generar una lista de SegmentoGantt.
    - Usar calcular_metricas(...) para obtener ResultadoProceso y promedios.
    - Construir y devolver un ResultadoAlgoritmo.

    TODO: Implementar la lógica de simulación FCFS.
    """
    raise NotImplementedError("simular_fcfs aún no está implementado.")
