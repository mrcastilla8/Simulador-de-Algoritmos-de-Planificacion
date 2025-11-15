from typing import List
from .models import Proceso


def obtener_escenario_1() -> List[Proceso]:
    
    datos_escenario_1 = [
        ("P1", 0, 12),
        ("P2", 2, 4),
        ("P3", 4, 2),
        ("P4", 6, 8),
        ("P5", 8, 3),
    ]

    return [
        Proceso(nombre=n, llegada=l, duracion_cpu=d)
        for (n, l, d) in datos_escenario_1
    ]


def obtener_escenario_2() -> List[Proceso]:
    
    datos_escenario_2 = [
        ("P1", 0, 5),
        ("P2", 1, 9),
        ("P3", 2, 6),
        ("P4", 3, 3),
        ("P5", 10, 4),
        ("P6", 12, 2),
    ]

    return [
        Proceso(nombre=n, llegada=l, duracion_cpu=d)
        for (n, l, d) in datos_escenario_2
    ]