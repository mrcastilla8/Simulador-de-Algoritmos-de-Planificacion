from dataclasses import dataclass, field
from typing import List, Dict


MetricasPromedio = Dict[str, float]


@dataclass
class Proceso:
    
    nombre: str
    llegada: int
    duracion_cpu: int


@dataclass
class SegmentoGantt:
    
    proceso: str
    inicio: int
    fin: int


@dataclass
class ResultadoProceso:
    
    nombre: str
    llegada: int
    duracion_cpu: int
    tiempo_finalizacion: int = 0
    tiempo_retorno: int = 0
    tiempo_espera: int = 0
    tiempo_respuesta: int = 0


@dataclass
class ResultadoAlgoritmo:
    
    nombre_algoritmo: str
    nombre_escenario: str
    procesos: List[ResultadoProceso] = field(default_factory=list)
    segmentos_gantt: List[SegmentoGantt] = field(default_factory=list)
    promedios: MetricasPromedio = field(default_factory=dict)