from typing import List, Dict, Any
from tabulate import tabulate
from .models import ResultadoProceso, ResultadoAlgoritmo



class Colores:
    
    RESET = '\033[0m'
    NEGRITA = '\033[1m'
    TENUE = '\033[2m'
    
    
    ROJO = '\033[91m'
    VERDE = '\033[92m'
    AMARILLO = '\033[93m'
    AZUL = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    BLANCO = '\033[97m'
    
    
    FONDO_GRIS = '\033[100m'
    FONDO_ROJO_CLARO = '\033[101m'
    FONDO_VERDE_CLARO = '\033[102m'


def colorear_encabezado(texto: str) -> str:
    
    return f"{Colores.NEGRITA}{Colores.AZUL}{texto}{Colores.RESET}"


def colorear_exito(texto: str) -> str:
    
    return f"{Colores.VERDE}{texto}{Colores.RESET}"


def colorear_advertencia(texto: str) -> str:
    
    return f"{Colores.AMARILLO}{texto}{Colores.RESET}"


def colorear_error(texto: str) -> str:
    
    return f"{Colores.ROJO}{texto}{Colores.RESET}"


def formato_titulo(titulo: str, ancho: int = 80) -> str:
    
    titulo_coloreado = colorear_encabezado(titulo)
    return titulo_coloreado.center(ancho + len(titulo_coloreado) - len(titulo))


def formato_subtitulo(subtitulo: str) -> str:
    
    return colorear_encabezado(subtitulo)


def tabla_metricas_procesos(procesos: List[ResultadoProceso]) -> str:
    
    datos = []
    for proc in procesos:
        datos.append([
            colorear_exito(proc.nombre),
            proc.llegada,
            proc.duracion_cpu,
            proc.tiempo_finalizacion,
            proc.tiempo_retorno,
            proc.tiempo_espera,
            proc.tiempo_respuesta
        ])
    
    encabezados = [
        colorear_encabezado("Proceso"),
        colorear_encabezado("Llegada"),
        colorear_encabezado("Duración"),
        colorear_encabezado("Finalización"),
        colorear_encabezado("Retorno"),
        colorear_encabezado("Espera"),
        colorear_encabezado("Respuesta")
    ]
    
    return tabulate(
        datos,
        headers=encabezados,
        tablefmt="grid",
        stralign="center",
        numalign="right",
        floatfmt=".2f"
    )


def tabla_promedios(promedios: Dict[str, float]) -> str:
    
    datos = [
        [
            colorear_encabezado("Tiempo de Retorno"),
            f"{promedios.get('tiempo_retorno_promedio', 0):.2f}"
        ],
        [
            colorear_encabezado("Tiempo de Espera"),
            f"{promedios.get('tiempo_espera_promedio', 0):.2f}"
        ],
        [
            colorear_encabezado("Tiempo de Respuesta"),
            f"{promedios.get('tiempo_respuesta_promedio', 0):.2f}"
        ]
    ]
    
    return tabulate(
        datos,
        headers=[colorear_encabezado("Métrica"), colorear_encabezado("Promedio (ms)")],
        tablefmt="grid",
        stralign="left",
        numalign="right"
    )


def tabla_comparativa_algoritmos(resultados: Dict[str, ResultadoAlgoritmo]) -> str:
    
    datos = []
    
    for nombre_algo, resultado in resultados.items():
        retorno_prom = resultado.promedios.get('tiempo_retorno_promedio', 0)
        espera_prom = resultado.promedios.get('tiempo_espera_promedio', 0)
        respuesta_prom = resultado.promedios.get('tiempo_respuesta_promedio', 0)
        
        datos.append([
            colorear_exito(nombre_algo),
            f"{retorno_prom:.2f}",
            f"{espera_prom:.2f}",
            f"{respuesta_prom:.2f}"
        ])
    
    encabezados = [
        colorear_encabezado("Algoritmo"),
        colorear_encabezado("Retorno Prom."),
        colorear_encabezado("Espera Prom."),
        colorear_encabezado("Respuesta Prom.")
    ]
    
    return tabulate(
        datos,
        headers=encabezados,
        tablefmt="grid",
        stralign="center",
        numalign="right"
    )


def separador(ancho: int = 80, simbolo: str = "=") -> str:
    
    return simbolo * ancho


def linea_info(clave: str, valor: Any) -> str:
    
    return f"{colorear_encabezado(clave):<40} {valor}"