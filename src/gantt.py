"""
Archivo: src/gantt.py
Responsable principal: Desarrollador 5

Generación y visualización simple del diagrama de Gantt en consola.
"""

from typing import List
from .models import SegmentoGantt


def formatear_gantt(segmentos: List[SegmentoGantt]) -> str:
    """
    Devuelve una representación en texto del diagrama de Gantt.

    Ejemplo muy simple (puede modificarse mientras sea legible):
    0    3    5    9
    | P1 | P2 | P3 |

    TODO: Implementar la construcción del string con el diagrama.
    """
    raise NotImplementedError("formatear_gantt aún no está implementado.")


def imprimir_gantt(segmentos: List[SegmentoGantt]) -> None:
    """
    Imprime en consola el diagrama de Gantt usando formatear_gantt.

    TODO: Llamar a formatear_gantt(...) y hacer print del resultado.
    """
    raise NotImplementedError("imprimir_gantt aún no está implementado.")
