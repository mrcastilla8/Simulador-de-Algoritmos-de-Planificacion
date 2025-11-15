from typing import List
from ..models import Proceso, ResultadoAlgoritmo, SegmentoGantt, ResultadoProceso
from ..metrics import calcular_metricas


def simular_fcfs(procesos: List[Proceso]) -> ResultadoAlgoritmo:
    
    if not procesos:
        return ResultadoAlgoritmo(
            nombre_algoritmo="FCFS",
            nombre_escenario="",
            procesos=[],
            segmentos_gantt=[],
            promedios={}
        )
    
    
    
    procesos_ordenados = sorted(procesos, key=lambda p: (p.llegada, p.nombre))
    
    
    tiempo_actual = 0
    segmentos_gantt: List[SegmentoGantt] = []
    
    for proceso in procesos_ordenados:
        
        if proceso.llegada > tiempo_actual:
            tiempo_actual = proceso.llegada
        
        
        tiempo_inicio = tiempo_actual
        tiempo_fin = tiempo_actual + proceso.duracion_cpu
        
        
        segmentos_gantt.append(SegmentoGantt(
            proceso=proceso.nombre,
            inicio=tiempo_inicio,
            fin=tiempo_fin
        ))
        
        
        tiempo_actual = tiempo_fin
    
    
    resultados_procesos, promedios = calcular_metricas(procesos, segmentos_gantt)
    
    
    return ResultadoAlgoritmo(
        nombre_algoritmo="FCFS",
        nombre_escenario="",  
        procesos=resultados_procesos,
        segmentos_gantt=segmentos_gantt,
        promedios=promedios
    )