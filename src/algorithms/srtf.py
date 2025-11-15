
from typing import List, Dict, Optional
from ..models import Proceso, ResultadoAlgoritmo, SegmentoGantt
from ..metrics import calcular_metricas


def simular_srtf(procesos: List[Proceso]) -> ResultadoAlgoritmo:
    
    
    
    tiempo_actual: int = 0
    procesos_completados: int = 0
    total_procesos: int = len(procesos)
    
    
    tiempo_restante: Dict[str, int] = {p.nombre: p.duracion_cpu for p in procesos}
    
    segmentos_gantt: List[SegmentoGantt] = []
    
    
    proceso_ejecucion_actual: Optional[str] = None
    inicio_segmento: int = 0

    
    while procesos_completados < total_procesos:
        
        
        candidatos = [
            p for p in procesos 
            if p.llegada <= tiempo_actual and tiempo_restante[p.nombre] > 0
        ]

        if not candidatos:
            
            
            if proceso_ejecucion_actual is not None:
                segmentos_gantt.append(SegmentoGantt(
                    proceso=proceso_ejecucion_actual,
                    inicio=inicio_segmento,
                    fin=tiempo_actual
                ))
                proceso_ejecucion_actual = None
            
            
            tiempo_actual += 1
            continue

        
        
        proceso_seleccionado = min(candidatos, key=lambda p: tiempo_restante[p.nombre])

        
        
        if proceso_ejecucion_actual != proceso_seleccionado.nombre:
            
            if proceso_ejecucion_actual is not None:
                segmentos_gantt.append(SegmentoGantt(
                    proceso=proceso_ejecucion_actual,
                    inicio=inicio_segmento,
                    fin=tiempo_actual
                ))
            
            
            proceso_ejecucion_actual = proceso_seleccionado.nombre
            inicio_segmento = tiempo_actual

        
        tiempo_restante[proceso_seleccionado.nombre] -= 1
        tiempo_actual += 1

        
        if tiempo_restante[proceso_seleccionado.nombre] == 0:
            procesos_completados += 1
            

    
    
    if proceso_ejecucion_actual is not None:
        segmentos_gantt.append(SegmentoGantt(
            proceso=proceso_ejecucion_actual,
            inicio=inicio_segmento,
            fin=tiempo_actual
        ))

    
    
    resultados_procesos, promedios = calcular_metricas(procesos, segmentos_gantt)

    
    return ResultadoAlgoritmo(
        nombre_algoritmo="SRTF",
        nombre_escenario="N/A",  
        procesos=resultados_procesos,
        segmentos_gantt=segmentos_gantt,
        promedios=promedios
    )
