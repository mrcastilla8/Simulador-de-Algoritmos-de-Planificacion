from typing import List
from ..models import Proceso, ResultadoAlgoritmo, SegmentoGantt, ResultadoProceso
from ..metrics import calcular_metricas


def simular_sjf(procesos: List[Proceso]) -> ResultadoAlgoritmo:
    
    if not procesos:
        return ResultadoAlgoritmo(
            nombre_algoritmo="SJF",
            nombre_escenario="",
            procesos=[],
            segmentos_gantt=[],
            promedios={}
        )
    
    
    procesos_pendientes = procesos.copy()
    
    
    tiempo_actual = 0
    segmentos_gantt: List[SegmentoGantt] = []
    
    
    while procesos_pendientes:
        
        procesos_disponibles = [
            p for p in procesos_pendientes 
            if p.llegada <= tiempo_actual
        ]
        
        
        if not procesos_disponibles:
            
            tiempo_actual = min(p.llegada for p in procesos_pendientes)
            continue
        
        
        
        proceso_seleccionado = min(
            procesos_disponibles,
            key=lambda p: (p.duracion_cpu, p.llegada, p.nombre)
        )
        
        
        tiempo_inicio = tiempo_actual
        tiempo_fin = tiempo_actual + proceso_seleccionado.duracion_cpu
        
        
        segmentos_gantt.append(SegmentoGantt(
            proceso=proceso_seleccionado.nombre,
            inicio=tiempo_inicio,
            fin=tiempo_fin
        ))
        
        
        tiempo_actual = tiempo_fin
        
        
        procesos_pendientes.remove(proceso_seleccionado)
    
    
    resultados_procesos, promedios = calcular_metricas(procesos, segmentos_gantt)
    
    
    return ResultadoAlgoritmo(
        nombre_algoritmo="SJF",
        nombre_escenario="",  
        procesos=resultados_procesos,
        segmentos_gantt=segmentos_gantt,
        promedios=promedios
    )