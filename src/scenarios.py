"""
Archivo: src/scenarios.py
Responsable principal: Desarrollador 5 (ANGEL)

Define las listas de procesos estáticas para los dos escenarios.
"""

from typing import List
from .models import Proceso

def obtener_escenario_1() -> List[Proceso]:
    """
    Escenario 1: Carga Mixta y Ráfagas Cortas
    """
    
    # Datos: (nombre, llegada, duracion_cpu)
    datos_escenario_1 = [
        ("P1", 0, 8),
        ("P2", 1, 4),
        ("P3", 2, 9),
        ("P4", 3, 5),
    ]

    lista_procesos = [
        Proceso(nombre=d[0], llegada=d[1], duracion_cpu=d[2]) 
        for d in datos_escenario_1
    ]
    
    return lista_procesos

def obtener_escenario_2() -> List[Proceso]:
    """
    Escenario 2: Llegadas Dispersas y Ráfagas Irregulares
    """
    
    # Datos: (nombre, llegada, duracion_cpu)
    datos_escenario_2 = [
        ("P1", 0, 7),
        ("P2", 5, 3),
        ("P3", 6, 12),
        ("P4", 7, 2),
        ("P5", 15, 5),
    ]

    lista_procesos = [
        Proceso(nombre=d[0], llegada=d[1], duracion_cpu=d[2]) 
        for d in datos_escenario_2
    ]
    
    return lista_procesos