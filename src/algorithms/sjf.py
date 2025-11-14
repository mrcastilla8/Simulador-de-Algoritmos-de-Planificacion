"""
Archivo: src/algorithms/sjf.py
Responsable principal: Desarrollador 2 (POMA)

Implementa el algoritmo SJF (Shortest Job First, no expropiativo).
"""

from typing import List
from ..models import Proceso, ResultadoAlgoritmo, SegmentoGantt, ResultadoProceso
from ..metrics import calcular_metricas


def simular_sjf(procesos: List[Proceso]) -> ResultadoAlgoritmo:
    """
    Simula el algoritmo SJF no expropiativo.

    Estrategia SJF (Shortest Job First):
    - En cada momento en que la CPU queda libre, selecciona el proceso disponible
      con menor duración de CPU.
    - Un proceso está "disponible" si su tiempo de llegada <= tiempo actual.
    - No hay expropiación: una vez que un proceso comienza, ejecuta completamente.
    - Si no hay procesos disponibles, la CPU avanza al siguiente tiempo de llegada.

    Args:
        procesos: Lista de procesos a planificar.

    Returns:
        ResultadoAlgoritmo con el nombre del algoritmo, segmentos de Gantt,
        métricas por proceso y promedios.
    """
    if not procesos:
        return ResultadoAlgoritmo(
            nombre_algoritmo="SJF",
            nombre_escenario="",
            procesos=[],
            segmentos_gantt=[],
            promedios={}
        )
    
    # 1. Crear una copia de la lista de procesos para trabajar
    procesos_pendientes = procesos.copy()
    
    # 2. Inicializar variables de simulación
    tiempo_actual = 0
    segmentos_gantt: List[SegmentoGantt] = []
    
    # 3. Simular mientras haya procesos pendientes
    while procesos_pendientes:
        # Filtrar los procesos que ya han llegado
        procesos_disponibles = [
            p for p in procesos_pendientes 
            if p.llegada <= tiempo_actual
        ]
        
        # Si no hay procesos disponibles, avanzar al siguiente tiempo de llegada
        if not procesos_disponibles:
            # Encontrar el proceso que llega más pronto
            tiempo_actual = min(p.llegada for p in procesos_pendientes)
            continue
        
        # Seleccionar el proceso con menor duración de CPU (Shortest Job First)
        # En caso de empate, seleccionar el que llegó primero
        proceso_seleccionado = min(
            procesos_disponibles,
            key=lambda p: (p.duracion_cpu, p.llegada, p.nombre)
        )
        
        # El proceso seleccionado comienza a ejecutarse
        tiempo_inicio = tiempo_actual
        tiempo_fin = tiempo_actual + proceso_seleccionado.duracion_cpu
        
        # Crear segmento de Gantt para este proceso
        segmentos_gantt.append(SegmentoGantt(
            proceso=proceso_seleccionado.nombre,
            inicio=tiempo_inicio,
            fin=tiempo_fin
        ))
        
        # Avanzar el tiempo actual
        tiempo_actual = tiempo_fin
        
        # Eliminar el proceso de la lista de pendientes
        procesos_pendientes.remove(proceso_seleccionado)
    
    # 4. Calcular métricas usando la función del módulo metrics
    resultados_procesos, promedios = calcular_metricas(procesos, segmentos_gantt)
    
    # 5. Construir y devolver el resultado del algoritmo
    return ResultadoAlgoritmo(
        nombre_algoritmo="SJF",
        nombre_escenario="",  # Se establecerá en simulation.py
        procesos=resultados_procesos,
        segmentos_gantt=segmentos_gantt,
        promedios=promedios
    )
