"""
Archivo: src/algorithms/round_robin.py
Responsable principal: Desarrollador 4

Implementa el algoritmo Round Robin con quantum paramétrico y
versiones específicas para q=3 y q=6.
"""

from typing import List
from ..models import Proceso, ResultadoAlgoritmo, SegmentoGantt, ResultadoProceso
from ..metrics import calcular_metricas


def simular_rr(procesos: List[Proceso], quantum: int) -> ResultadoAlgoritmo:
    """
    Simula el algoritmo Round Robin con el quantum dado.

    Debe:
    - Manejar una cola de listos circular.
    - Avanzar el tiempo actual.
    - Ejecutar cada proceso por min(quantum, tiempo_restante).
    - Generar segmentos de Gantt.
    - Usar calcular_metricas(...) para métricas finales.
    - Devolver un ResultadoAlgoritmo.

    TODO: Implementar la lógica de simulación Round Robin genérico.
    """
    raise NotImplementedError("simular_rr aún no está implementado.")


def simular_rr_q3(procesos: List[Proceso]) -> ResultadoAlgoritmo:
    """
    Versión de conveniencia de Round Robin con quantum = 3 ms.

    TODO: Llamar internamente a simular_rr(..., 3).
    """
    raise NotImplementedError("simular_rr_q3 aún no está implementado.")


def simular_rr_q6(procesos: List[Proceso]) -> ResultadoAlgoritmo:
    """
    Versión de conveniencia de Round Robin con quantum = 6 ms.

    TODO: Llamar internamente a simular_rr(..., 6).
    """
    raise NotImplementedError("simular_rr_q6 aún no está implementado.")
