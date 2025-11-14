"""
Archivo: src/cli.py
Responsable principal: Desarrollador 5 (ANGEL)

Interfaz de línea de comandos (CLI) para controlar el programa.
"""

from typing import Union
from .models import ResultadoAlgoritmo
from .simulation import (
    ALGORITMOS_DISPONIBLES,
    ejecutar_algoritmo_en_escenario,
    ejecutar_todos_los_algoritmos,
)
from .gantt import imprimir_gantt


def seleccionar_escenario() -> int:
    """
    Muestra un menú para seleccionar el escenario.

    Returns:
        ID del escenario elegido (1 o 2).
    
    Raises:
        ValueError: Si la entrada no es válida.
    """
    while True:
        print("\n" + "=" * 60)
        print("SELECCIONAR ESCENARIO")
        print("=" * 60)
        print("1. Escenario 1 - Carga mixta")
        print("2. Escenario 2 - Llegadas dispersas")
        print("-" * 60)
        
        entrada = input("Ingrese el número del escenario (1 o 2): ").strip()
        
        if entrada in ("1", "2"):
            return int(entrada)
        else:
            print("Entrada inválida. Por favor, ingrese 1 o 2.")


def seleccionar_algoritmo() -> str:
    """
    Muestra un menú para seleccionar el algoritmo o 'todos'.

    Returns:
        Nombre del algoritmo (FCFS, SJF, SRTF, RR_Q3, RR_Q6) o 'TODOS'.
    """
    while True:
        print("\n" + "=" * 60)
        print("SELECCIONAR ALGORITMO")
        print("=" * 60)
        
        for i, algo in enumerate(ALGORITMOS_DISPONIBLES, 1):
            print(f"{i}. {algo}")
        
        print(f"{len(ALGORITMOS_DISPONIBLES) + 1}. Ejecutar TODOS")
        print("-" * 60)
        
        entrada = input("Ingrese el número del algoritmo: ").strip()
        
        try:
            opcion = int(entrada)
            if 1 <= opcion <= len(ALGORITMOS_DISPONIBLES):
                return ALGORITMOS_DISPONIBLES[opcion - 1]
            elif opcion == len(ALGORITMOS_DISPONIBLES) + 1:
                return "TODOS"
            else:
                print(f"Opción inválida. Ingrese un número entre 1 y {len(ALGORITMOS_DISPONIBLES) + 1}.")
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número.")


def mostrar_resultados(resultado: ResultadoAlgoritmo) -> None:
    """
    Muestra en consola los resultados de un algoritmo.

    Args:
        resultado: Objeto ResultadoAlgoritmo con los datos de la simulación.
    """
    print("\n" + "=" * 80)
    print(f"RESULTADOS: {resultado.nombre_algoritmo} - {resultado.nombre_escenario}")
    print("=" * 80)
    
    # 1. Mostrar diagrama de Gantt
    print("\nDIAGRAMA DE GANTT:")
    print("-" * 80)
    imprimir_gantt(resultado.segmentos_gantt)
    
    # 2. Mostrar tabla de métricas por proceso
    print("\nTABLA DE MÉTRICAS POR PROCESO:")
    print("-" * 80)
    
    # Encabezados
    print(f"{'Proceso':<10} {'Llegada':<10} {'Duración':<10} {'Finalización':<15} {'Retorno':<10} {'Espera':<10} {'Respuesta':<10}")
    print("-" * 80)
    
    # Filas de datos
    for resultado_proceso in resultado.procesos:
        print(
            f"{resultado_proceso.nombre:<10} "
            f"{resultado_proceso.llegada:<10} "
            f"{resultado_proceso.duracion_cpu:<10} "
            f"{resultado_proceso.tiempo_finalizacion:<15} "
            f"{resultado_proceso.tiempo_retorno:<10} "
            f"{resultado_proceso.tiempo_espera:<10} "
            f"{resultado_proceso.tiempo_respuesta:<10}"
        )
    
    # 3. Mostrar promedios
    print("\n" + "-" * 80)
    print("PROMEDIOS:")
    print("-" * 80)
    print(f"Tiempo de Retorno Promedio:   {resultado.promedios.get('tiempo_retorno_promedio', 0):.2f}")
    print(f"Tiempo de Espera Promedio:    {resultado.promedios.get('tiempo_espera_promedio', 0):.2f}")
    print(f"Tiempo de Respuesta Promedio: {resultado.promedios.get('tiempo_respuesta_promedio', 0):.2f}")
    print("=" * 80)


def mostrar_resultados_multiples(resultados: dict) -> None:
    """
    Muestra los resultados de múltiples algoritmos de forma resumida.

    Args:
        resultados: Diccionario con los resultados de cada algoritmo.
    """
    print("\n" + "=" * 100)
    print("RESUMEN COMPARATIVO - TODOS LOS ALGORITMOS")
    print("=" * 100)
    
    # Tabla comparativa de promedios
    print(f"{'Algoritmo':<15} {'Retorno Prom.':<18} {'Espera Prom.':<18} {'Respuesta Prom.':<18}")
    print("-" * 100)
    
    for nombre_algo, resultado in resultados.items():
        retorno_prom = resultado.promedios.get('tiempo_retorno_promedio', 0)
        espera_prom = resultado.promedios.get('tiempo_espera_promedio', 0)
        respuesta_prom = resultado.promedios.get('tiempo_respuesta_promedio', 0)
        
        print(
            f"{nombre_algo:<15} "
            f"{retorno_prom:<18.2f} "
            f"{espera_prom:<18.2f} "
            f"{respuesta_prom:<18.2f}"
        )
    
    print("=" * 100)


def ejecutar_aplicacion() -> None:
    """
    Orquesta el flujo de interacción completo de la aplicación.
    
    Pasos:
    1. Seleccionar escenario.
    2. Seleccionar algoritmo o 'TODOS'.
    3. Ejecutar la simulación.
    4. Mostrar resultados.
    5. Opción de repetir o salir.
    """
    print("\n" + "= " * 20)
    print("BIENVENIDO AL SIMULADOR DE ALGORITMOS DE PLANIFICACIÓN CPU")
    print("= " * 20)
    
    while True:
        try:
            # 1. Seleccionar escenario
            escenario_id = seleccionar_escenario()
            
            # 2. Seleccionar algoritmo
            algoritmo_seleccionado = seleccionar_algoritmo()
            
            # 3. Ejecutar simulación
            if algoritmo_seleccionado == "TODOS":
                print("\nEjecutando todos los algoritmos...")
                resultados = ejecutar_todos_los_algoritmos(escenario_id)
                
                # Mostrar cada resultado
                for nombre_algo, resultado in resultados.items():
                    mostrar_resultados(resultado)
                
                # Mostrar resumen comparativo
                mostrar_resultados_multiples(resultados)
            else:
                print(f"\nEjecutando {algoritmo_seleccionado}...")
                resultado = ejecutar_algoritmo_en_escenario(algoritmo_seleccionado, escenario_id)
                
                # 4. Mostrar resultados
                mostrar_resultados(resultado)
            
            # 5. Preguntar si continuar
            print("\n" + "=" * 80)
            while True:
                opcion = input("¿Desea ejecutar otra simulación? (s/n): ").strip().lower()
                if opcion in ("s", "si", "sí"):
                    break
                elif opcion in ("n", "no"):
                    print("\nGracias por usar el simulador. ¡Hasta luego!")
                    return
                else:
                    print("Entrada inválida. Ingrese 's' o 'n'.")
        
        except ValueError as e:
            print(f"\nError: {e}")
        except Exception as e:
            print(f"\nError inesperado: {e}")
            print("Por favor, intente de nuevo.")
