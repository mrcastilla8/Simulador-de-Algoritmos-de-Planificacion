"""
Archivo: src/models.py
Responsable principal: Desarrollador 1 (Líder)

Define las estructuras de datos utilizadas en el simulador.
"""

from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Proceso:
    """
    Representa un proceso de entrada al planificador.
    """
    nombre: str
    llegada: int
    duracion_cpu: int


@dataclass
class SegmentoGantt:
    """
    Representa un bloque de ejecución en el diagrama de Gantt.
    """
    proceso: str
    inicio: int
    fin: int


@dataclass
class ResultadoProceso:
    """
    Métricas calculadas para un proceso después de la simulación.
    """
    nombre: str
    llegada: int
    duracion_cpu: int
    tiempo_finalizacion: int = 0
    tiempo_retorno: int = 0
    tiempo_espera: int = 0
    tiempo_respuesta: int = 0


@dataclass
class ResultadoAlgoritmo:
    """
    Resultado completo de un algoritmo de planificación sobre un escenario.
    """
    nombre_algoritmo: str
    nombre_escenario: str
    procesos: List[ResultadoProceso] = field(default_factory=list)
    segmentos_gantt: List[SegmentoGantt] = field(default_factory=list)
    promedios: Dict[str, float] = field(default_factory=dict)
