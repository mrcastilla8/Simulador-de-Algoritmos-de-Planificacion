"""
Archivo: src/simulation.py
Responsable principal: Desarrollador 5 + Desarrollador 1 (Líder)

Orquesta la ejecución de algoritmos sobre los distintos escenarios.
"""

from typing import Dict
from .models import Proceso, ResultadoAlgoritmo
from . import scenarios
from .algorithms import (
    simular_fcfs,
    simular_sjf,
    simular_srtf,
    simular_rr_q3,
    simular_rr_q6,
)

ALGORITMOS_DISPONIBLES = ("FCFS", "SJF", "SRTF", "RR_Q3", "RR_Q6")


def cargar_escenario(escenario_id: int) -> Dict[str, object]:
    """
    Devuelve la lista de procesos y un nombre legible para el escenario.

    Debe:
    - Según escenario_id, llamar a obtener_escenario_1 o 2.
    - Retornar algo como:
      {
         "nombre": "Escenario 1 - Carga mixta",
         "procesos": [...]
      }

    TODO: Implementar la carga del escenario.
    """
    raise NotImplementedError("cargar_escenario aún no está implementado.")


def ejecutar_algoritmo_en_escenario(
    nombre_algoritmo: str,
    escenario_id: int,
) -> ResultadoAlgoritmo:
    """
    Ejecuta un algoritmo específico sobre un escenario.

    Debe:
    - Cargar el escenario mediante cargar_escenario.
    - Según nombre_algoritmo, llamar a la función de simulación correspondiente.
    - Ajustar el campo nombre_escenario en el ResultadoAlgoritmo.
    - Devolver el ResultadoAlgoritmo.

    TODO: Implementar la lógica de orquestación para un algoritmo.
    """
    raise NotImplementedError("ejecutar_algoritmo_en_escenario aún no está implementado.")


def ejecutar_todos_los_algoritmos(escenario_id: int) -> Dict[str, ResultadoAlgoritmo]:
    """
    Ejecuta todos los algoritmos disponibles sobre el escenario dado.

    Debe:
    - Iterar sobre ALGORITMOS_DISPONIBLES.
    - Llamar a ejecutar_algoritmo_en_escenario para cada uno.
    - Devolver un diccionario:
      {
          "FCFS": ResultadoAlgoritmo,
          "SJF": ResultadoAlgoritmo,
          ...
      }

    TODO: Implementar la ejecución para todos los algoritmos.
    """
    raise NotImplementedError("ejecutar_todos_los_algoritmos aún no está implementado.")
