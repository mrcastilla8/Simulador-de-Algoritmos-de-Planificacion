from typing import List, Tuple, Dict, Optional
from .models import Proceso, SegmentoGantt, ResultadoProceso, MetricasPromedio


def calcular_metricas(
    procesos: List[Proceso],
    segmentos_gantt: List[SegmentoGantt]
) -> Tuple[List[ResultadoProceso], MetricasPromedio]:
    

    
    segmentos_ordenados = sorted(
        segmentos_gantt,
        key=lambda s: (s.inicio, s.fin)
    )

    
    
    mapa_procesos: Dict[str, Proceso] = {p.nombre: p for p in procesos}

    
    
    
    mapa_tiempo_respuesta_inicio: Dict[str, int] = {}
    
    mapa_tiempo_finalizacion: Dict[str, int] = {}

    
    
    cambios_contexto: int = 0
    proceso_anterior: Optional[str] = None

    for segmento in segmentos_ordenados:
        nombre_proceso = segmento.proceso

        
        if proceso_anterior is None:
            proceso_anterior = nombre_proceso
        elif nombre_proceso != proceso_anterior:
            cambios_contexto += 1
            proceso_anterior = nombre_proceso

        
        if nombre_proceso not in mapa_tiempo_respuesta_inicio:
            mapa_tiempo_respuesta_inicio[nombre_proceso] = segmento.inicio

        
        mapa_tiempo_finalizacion[nombre_proceso] = max(
            mapa_tiempo_finalizacion.get(nombre_proceso, 0),
            segmento.fin
        )

    
    resultados_individuales: List[ResultadoProceso] = []

    total_retorno = 0
    total_espera = 0
    total_respuesta = 0

    
    for proceso in procesos:
        nombre = proceso.nombre
        llegada = proceso.llegada
        duracion = proceso.duracion_cpu

        finalizacion = mapa_tiempo_finalizacion.get(nombre, 0)
        primer_inicio = mapa_tiempo_respuesta_inicio.get(nombre, 0)

        
        retorno = finalizacion - llegada

        
        espera = retorno - duracion

        
        respuesta = primer_inicio - llegada

        total_retorno += retorno
        total_espera += espera
        total_respuesta += respuesta

        resultados_individuales.append(ResultadoProceso(
            nombre=nombre,
            llegada=llegada,
            duracion_cpu=duracion,
            tiempo_finalizacion=finalizacion,
            tiempo_retorno=retorno,
            tiempo_espera=espera,
            tiempo_respuesta=respuesta
        ))

    
    num_procesos = len(procesos)
    promedios: MetricasPromedio = {
        "tiempo_retorno_promedio": total_retorno / num_procesos if num_procesos > 0 else 0,
        "tiempo_espera_promedio": total_espera / num_procesos if num_procesos > 0 else 0,
        "tiempo_respuesta_promedio": total_respuesta / num_procesos if num_procesos > 0 else 0,
    }

    
    promedios["cambios_contexto"] = float(cambios_contexto)

    return resultados_individuales, promedios