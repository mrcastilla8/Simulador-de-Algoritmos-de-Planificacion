
from typing import List, Dict
from collections import deque
from ..models import Proceso, ResultadoAlgoritmo, SegmentoGantt, ResultadoProceso
from ..metrics import calcular_metricas


def simular_rr(procesos: List[Proceso], quantum: int) -> ResultadoAlgoritmo:
    
    
    
    tiempo_actual: int = 0
    procesos_completados: int = 0
    total_procesos: int = len(procesos)
    
    procesos_pendientes = sorted(procesos, key=lambda p: p.llegada)
    
    cola_listos: deque[Proceso] = deque() 
    
    tiempo_restante: Dict[str, int] = {p.nombre: p.duracion_cpu for p in procesos}
    
    segmentos_gantt: List[SegmentoGantt] = []
    
    idx_proximo_proceso = 0

    
    
    while procesos_completados < total_procesos:
        

        while (idx_proximo_proceso < total_procesos and 
               procesos_pendientes[idx_proximo_proceso].llegada <= tiempo_actual):
            
            cola_listos.append(procesos_pendientes[idx_proximo_proceso])
            idx_proximo_proceso += 1

        if not cola_listos:
            if idx_proximo_proceso < total_procesos:
                tiempo_actual = procesos_pendientes[idx_proximo_proceso].llegada
            else:
                break
            continue

        proceso_actual = cola_listos.popleft()
        nombre_proceso = proceso_actual.nombre
        
        tiempo_a_ejecutar = min(quantum, tiempo_restante[nombre_proceso])
        
        inicio_segmento = tiempo_actual
        fin_segmento = tiempo_actual + tiempo_a_ejecutar
        
        segmentos_gantt.append(SegmentoGantt(
            proceso=nombre_proceso,
            inicio=inicio_segmento,
            fin=fin_segmento
        ))
        
        tiempo_restante[nombre_proceso] -= tiempo_a_ejecutar
        tiempo_actual = fin_segmento

        while (idx_proximo_proceso < total_procesos and 
               procesos_pendientes[idx_proximo_proceso].llegada <= tiempo_actual):
            
            cola_listos.append(procesos_pendientes[idx_proximo_proceso])
            idx_proximo_proceso += 1
            
        if tiempo_restante[nombre_proceso] > 0:
            cola_listos.append(proceso_actual)
        else:
            
            procesos_completados += 1

    
    
    resultados_procesos, promedios = calcular_metricas(procesos, segmentos_gantt)

    
    
    return ResultadoAlgoritmo(
        nombre_algoritmo=f"Round Robin (q={quantum})",
        nombre_escenario="N/A",
        procesos=resultados_procesos,
        segmentos_gantt=segmentos_gantt,
        promedios=promedios
    )


def simular_rr_q3(procesos: List[Proceso]) -> ResultadoAlgoritmo:
    
    resultado = simular_rr(procesos, 3)
    resultado.nombre_algoritmo = "Round Robin (q=3)"
    return resultado


def simular_rr_q6(procesos: List[Proceso]) -> ResultadoAlgoritmo:
    
    resultado = simular_rr(procesos, 6)
    resultado.nombre_algoritmo = "Round Robin (q=6)"
    return resultado
