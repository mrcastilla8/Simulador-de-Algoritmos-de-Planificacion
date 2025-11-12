"""
Archivo: src/algorithms/__init__.py
Responsable principal: Desarrollador 1 (Líder)

Agrupa las funciones de simulación de algoritmos de planificación.
"""

from .fcfs import simular_fcfs
from .sjf import simular_sjf
from .srtf import simular_srtf
from .round_robin import simular_rr, simular_rr_q3, simular_rr_q6

__all__ = [
    "simular_fcfs",
    "simular_sjf",
    "simular_srtf",
    "simular_rr",
    "simular_rr_q3",
    "simular_rr_q6",
]
