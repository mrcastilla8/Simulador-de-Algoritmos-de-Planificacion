"""
Archivo: src/algorithms/fcfs.py
Responsable principal: Desarrollador 2 (POMA)

Implementa el algoritmo FCFS (First Come First Served).
"""

from typing import List
from ..models import Proceso, ResultadoAlgoritmo, SegmentoGantt, ResultadoProceso
from ..metrics import calcular_metricas


def simular_fcfs(procesos: List[Proceso]) -> ResultadoAlgoritmo:
    """
    Simula el algoritmo FCFS sobre la lista de procesos dada.

    Estrategia FCFS (First Come First Served):
    - Los procesos se atienden en el orden en que llegan.
    - No hay expropiación: cada proceso ejecuta su ráfaga completa.
    - Si la CPU está libre y no hay procesos disponibles, avanza al siguiente tiempo de llegada.

    Args:
        procesos: Lista de procesos a planificar.

    Returns:
        ResultadoAlgoritmo con el nombre del algoritmo, segmentos de Gantt,
        métricas por proceso y promedios.
    """
    if not procesos:
        return ResultadoAlgoritmo(
            nombre_algoritmo="FCFS",
            nombre_escenario="",
            procesos=[],
            segmentos_gantt=[],
            promedios={}
        )
    
    # 1. Ordenar los procesos por tiempo de llegada
    # (si hay empate, mantener orden original)
    procesos_ordenados = sorted(procesos, key=lambda p: (p.llegada, p.nombre))
    
    # 2. Simular la ejecución
    tiempo_actual = 0
    segmentos_gantt: List[SegmentoGantt] = []
    
    for proceso in procesos_ordenados:
        # Si el proceso aún no ha llegado, la CPU queda ociosa
        if proceso.llegada > tiempo_actual:
            tiempo_actual = proceso.llegada
        
        # El proceso comienza a ejecutarse
        tiempo_inicio = tiempo_actual
        tiempo_fin = tiempo_actual + proceso.duracion_cpu
        
        # Crear segmento de Gantt para este proceso
        segmentos_gantt.append(SegmentoGantt(
            proceso=proceso.nombre,
            inicio=tiempo_inicio,
            fin=tiempo_fin
        ))
        
        # Avanzar el tiempo actual
        tiempo_actual = tiempo_fin
    
    # 3. Calcular métricas usando la función del módulo metrics
    resultados_procesos, promedios = calcular_metricas(procesos, segmentos_gantt)
    
    # 4. Construir y devolver el resultado del algoritmo
    return ResultadoAlgoritmo(
        nombre_algoritmo="FCFS",
        nombre_escenario="",  # Se establecerá en simulation.py
        procesos=resultados_procesos,
        segmentos_gantt=segmentos_gantt,
        promedios=promedios
    )
