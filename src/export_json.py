"""
Archivo: src/export_json.py
Responsable principal: (pueden ponerse como equipo)

Funciones para exportar los resultados de los algoritmos a JSON,
para facilitar la elaboración del informe.
"""

import json
from typing import Dict
from .models import ResultadoAlgoritmo, ResultadoProceso


def resultado_algoritmo_a_dict(resultado: ResultadoAlgoritmo) -> dict:
    """
    Convierte un ResultadoAlgoritmo a un diccionario listo para serializar a JSON.
    No incluye el diagrama de Gantt gráfico, solo datos (procesos, métricas, promedios).
    """
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
        # Aquí ya vienen los promedios + cambios de contexto desde metrics.py
        "promedios": resultado.promedios,
    }


def exportar_resultado_json(resultado: ResultadoAlgoritmo, ruta: str) -> None:
    """
    Exporta un solo ResultadoAlgoritmo a un archivo JSON.
    """
    data = resultado_algoritmo_a_dict(resultado)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def exportar_resultados_multiples_json(
    resultados: Dict[str, ResultadoAlgoritmo],
    ruta: str,
) -> None:
    """
    Exporta varios resultados (por algoritmo) a un solo archivo JSON.

    Estructura:
    {
      "FCFS": { ... },
      "SJF": { ... },
      ...
    }
    """
    data = {
        nombre_algo: resultado_algoritmo_a_dict(res)
        for nombre_algo, res in resultados.items()
    }
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
