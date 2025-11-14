"""
Archivo: src/simulation.py
Responsable principal: Desarrollador 5 + Desarrollador 1 (Líder)

Orquesta la ejecución de algoritmos sobre los distintos escenarios.
"""

from typing import Dict, List
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

# Mapeo de nombres de algoritmos a sus funciones de simulación
MAPA_ALGORITMOS = {
    "FCFS": simular_fcfs,
    "SJF": simular_sjf,
    "SRTF": simular_srtf,
    "RR_Q3": simular_rr_q3,
    "RR_Q6": simular_rr_q6,
}

# Descripciones legibles de los escenarios
NOMBRES_ESCENARIOS = {
    1: "Escenario 1 - Carga mixta",
    2: "Escenario 2 - Llegadas dispersas",
}


def cargar_escenario(escenario_id: int) -> Dict[str, object]:
    """
    Devuelve la lista de procesos y un nombre legible para el escenario.

    Args:
        escenario_id: ID del escenario (1 o 2).

    Returns:
        Diccionario con:
        - "nombre": nombre legible del escenario.
        - "procesos": lista de objetos Proceso.
    
    Raises:
        ValueError: Si el escenario_id no es válido.
    """
    if escenario_id == 1:
        procesos = scenarios.obtener_escenario_1()
    elif escenario_id == 2:
        procesos = scenarios.obtener_escenario_2()
    else:
        raise ValueError(f"Escenario inválido: {escenario_id}. Debe ser 1 o 2.")
    
    return {
        "nombre": NOMBRES_ESCENARIOS.get(escenario_id, f"Escenario {escenario_id}"),
        "procesos": procesos,
    }


def ejecutar_algoritmo_en_escenario(
    nombre_algoritmo: str,
    escenario_id: int,
) -> ResultadoAlgoritmo:
    """
    Ejecuta un algoritmo específico sobre un escenario.

    Args:
        nombre_algoritmo: Nombre del algoritmo (FCFS, SJF, SRTF, RR_Q3, RR_Q6).
        escenario_id: ID del escenario (1 o 2).

    Returns:
        Objeto ResultadoAlgoritmo con los resultados de la simulación.
    
    Raises:
        ValueError: Si el algoritmo o escenario no existen.
    """
    # Validar y cargar el escenario
    escenario_data = cargar_escenario(escenario_id)
    procesos: List[Proceso] = escenario_data["procesos"]  # type: ignore
    nombre_escenario: str = escenario_data["nombre"]  # type: ignore
    
    # Validar que el algoritmo existe
    if nombre_algoritmo not in MAPA_ALGORITMOS:
        raise ValueError(
            f"Algoritmo '{nombre_algoritmo}' no reconocido. "
            f"Disponibles: {', '.join(ALGORITMOS_DISPONIBLES)}"
        )
    
    # Llamar a la función de simulación del algoritmo
    funcion_simulacion = MAPA_ALGORITMOS[nombre_algoritmo]
    resultado = funcion_simulacion(procesos)
    
    # Establecer los nombres de algoritmo y escenario en el resultado
    resultado.nombre_algoritmo = nombre_algoritmo
    resultado.nombre_escenario = nombre_escenario
    
    return resultado


def ejecutar_todos_los_algoritmos(escenario_id: int) -> Dict[str, ResultadoAlgoritmo]:
    """
    Ejecuta todos los algoritmos disponibles sobre el escenario dado.

    Args:
        escenario_id: ID del escenario (1 o 2).

    Returns:
        Diccionario donde las claves son nombres de algoritmos y los valores
        son objetos ResultadoAlgoritmo con los resultados de cada simulación.
    
    Raises:
        ValueError: Si el escenario no existe.
    """
    resultados = {}
    
    for nombre_algoritmo in ALGORITMOS_DISPONIBLES:
        resultado = ejecutar_algoritmo_en_escenario(nombre_algoritmo, escenario_id)
        resultados[nombre_algoritmo] = resultado
    
    return resultados
