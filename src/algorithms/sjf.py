"""
Archivo: src/algorithms/sjf.py
Responsable principal: Desarrollador 2

Implementa el algoritmo SJF (Shortest Job First, no expropiativo).
"""

from typing import List
from ..models import Proceso, ResultadoAlgoritmo, SegmentoGantt, ResultadoProceso
from ..metrics import calcular_metricas


def simular_sjf(procesos: List[Proceso]) -> ResultadoAlgoritmo:
    """
    Simula el algoritmo SJF no expropiativo.

    Debe:
    - Ir avanzando el tiempo actual.
    - Escoger el proceso disponible (llegada <= tiempo) con menor duración restante.
    - Generar segmentos de Gantt (un único segmento por proceso).
    - Usar calcular_metricas(...) para obtener métricas.
    - Devolver un ResultadoAlgoritmo.

    TODO: Implementar la lógica de simulación SJF.
    """
    raise NotImplementedError("simular_sjf aún no está implementado.")
