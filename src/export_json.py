import json
from typing import Dict
from .models import ResultadoAlgoritmo, ResultadoProceso


def resultado_algoritmo_a_dict(resultado: ResultadoAlgoritmo) -> dict:
    
    return {
        "nombre_algoritmo": resultado.nombre_algoritmo,
        "nombre_escenario": resultado.nombre_escenario,
        "procesos": [
            {
                "nombre": p.nombre,
                "llegada": p.llegada,
                "duracion_cpu": p.duracion_cpu,
                "tiempo_finalizacion": p.tiempo_finalizacion,
                "tiempo_retorno": p.tiempo_retorno,
                "tiempo_espera": p.tiempo_espera,
                "tiempo_respuesta": p.tiempo_respuesta,
            }
            for p in resultado.procesos
        ],
        
        "promedios": resultado.promedios,
    }


def exportar_resultado_json(resultado: ResultadoAlgoritmo, ruta: str) -> None:
    
    data = resultado_algoritmo_a_dict(resultado)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def exportar_resultados_multiples_json(
    resultados: Dict[str, ResultadoAlgoritmo],
    ruta: str,
) -> None:
    
    
    data = {
        nombre_algo: resultado_algoritmo_a_dict(res)
        for nombre_algo, res in resultados.items()
    }
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)