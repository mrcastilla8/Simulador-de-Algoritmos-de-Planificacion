"""
Archivo: src/algorithms/srtf.py
Responsable principal: Desarrollador 3 (BRICKZON)

Implementa el algoritmo SRTF (Shortest Remaining Time First, expropiativo).
"""

from typing import List, Dict, Optional
from ..models import Proceso, ResultadoAlgoritmo, SegmentoGantt
from ..metrics import calcular_metricas


def simular_srtf(procesos: List[Proceso]) -> ResultadoAlgoritmo:
    """
    Simula el algoritmo SRTF (preemptive).

    Lógica:
    - Se crea un mapa local para controlar el tiempo restante de cada proceso.
    - Se avanza un reloj global (tiempo_actual).
    - En cada instante, se seleccionan los procesos que ya llegaron ("ready").
    - De los ready, se elige el de menor tiempo restante.
    - Se detectan cambios de contexto para cerrar y abrir Segmentos de Gantt.
    """
    
    # 1. Inicialización de estructuras de control
    tiempo_actual: int = 0
    procesos_completados: int = 0
    total_procesos: int = len(procesos)
    
    # Mapa para no modificar los objetos originales: { nombre_proceso: tiempo_restante }
    tiempo_restante: Dict[str, int] = {p.nombre: p.duracion_cpu for p in procesos}
    
    segmentos_gantt: List[SegmentoGantt] = []
    
    # Variables para controlar el bloque actual del Gantt
    proceso_ejecucion_actual: Optional[str] = None
    inicio_segmento: int = 0

    # 2. Bucle principal de simulación (paso a paso)
    while procesos_completados < total_procesos:
        
        # Buscar candidatos: procesos que ya llegaron (llegada <= actual) y no han terminado
        candidatos = [
            p for p in procesos 
            if p.llegada <= tiempo_actual and tiempo_restante[p.nombre] > 0
        ]

        if not candidatos:
            # CPU Ociosa (Idle)
            # Si veníamos ejecutando algo, cerramos ese segmento
            if proceso_ejecucion_actual is not None:
                segmentos_gantt.append(SegmentoGantt(
                    proceso=proceso_ejecucion_actual,
                    inicio=inicio_segmento,
                    fin=tiempo_actual
                ))
                proceso_ejecucion_actual = None
            
            # Avanzamos tiempo sin ejecutar nada
            tiempo_actual += 1
            continue

        # Selección SRTF: El proceso con menor tiempo restante
        # En caso de empate, Python 'min' conserva el orden estable (el que aparece primero o ya estaba)
        proceso_seleccionado = min(candidatos, key=lambda p: tiempo_restante[p.nombre])

        # 3. Gestión del cambio de contexto (Gantt)
        # Si el proceso seleccionado es diferente al que estaba corriendo
        if proceso_ejecucion_actual != proceso_seleccionado.nombre:
            # Si había uno corriendo antes, cerramos su segmento
            if proceso_ejecucion_actual is not None:
                segmentos_gantt.append(SegmentoGantt(
                    proceso=proceso_ejecucion_actual,
                    inicio=inicio_segmento,
                    fin=tiempo_actual
                ))
            
            # Iniciamos el nuevo segmento
            proceso_ejecucion_actual = proceso_seleccionado.nombre
            inicio_segmento = tiempo_actual

        # 4. Ejecución (1 ms)
        tiempo_restante[proceso_seleccionado.nombre] -= 1
        tiempo_actual += 1

        # Verificamos si terminó justo ahora
        if tiempo_restante[proceso_seleccionado.nombre] == 0:
            procesos_completados += 1
            # Nota: No cerramos el segmento aquí inmediatamente; 
            # se cerrará en la siguiente iteración al detectar cambio de proceso o idle.

    # 5. Cierre final
    # Al salir del bucle, queda un segmento abierto (el último proceso que terminó)
    if proceso_ejecucion_actual is not None:
        segmentos_gantt.append(SegmentoGantt(
            proceso=proceso_ejecucion_actual,
            inicio=inicio_segmento,
            fin=tiempo_actual
        ))

    # 6. Cálculo de métricas
    # Delegamos el cálculo matemático al módulo metrics.py
    resultados_procesos, promedios = calcular_metricas(procesos, segmentos_gantt)

    # 7. Retorno del resultado encapsulado
    return ResultadoAlgoritmo(
        nombre_algoritmo="SRTF",
        nombre_escenario="N/A",  # El orquestador (simulation.py) puede actualizar esto
        procesos=resultados_procesos,
        segmentos_gantt=segmentos_gantt,
        promedios=promedios
    )