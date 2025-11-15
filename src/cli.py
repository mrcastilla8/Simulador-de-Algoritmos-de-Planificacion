"""
Archivo: src/cli.py
Responsable principal: Desarrollador 5 (ANGEL)

Interfaz de línea de comandos (CLI) para controlar el programa.
"""

import sys
import os

# Configurar encoding UTF-8 para Windows
if sys.platform == 'win32':
    try:
        import ctypes
        ctypes.windll.kernel32.SetConsoleCP(65001)
        ctypes.windll.kernel32.SetConsoleOutputCP(65001)
        os.environ['PYTHONIOENCODING'] = 'utf-8'
    except:
        pass

from typing import Union
from .models import ResultadoAlgoritmo
from .simulation import (
    ALGORITMOS_DISPONIBLES,
    ejecutar_algoritmo_en_escenario,
    ejecutar_todos_los_algoritmos,
)
from .gantt import imprimir_gantt, graficar_gantt, graficar_gantt_subplots
from .formatters import (
    Colores,
    formato_titulo,
    formato_subtitulo,
    tabla_metricas_procesos,
    tabla_promedios,
    tabla_comparativa_algoritmos,
    separador,
)


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


def mostrar_resultados(resultado: ResultadoAlgoritmo, mostrar_grafico: bool = False) -> None:
    """
    Muestra en consola los resultados de un algoritmo con formato mejorado.

    Args:
        resultado: Objeto ResultadoAlgoritmo con los datos de la simulación.
        mostrar_grafico: Si es True, también genera un gráfico con matplotlib.
    """
    # Encabezado
    print("\n" + separador(80))
    print(formato_titulo(f"RESULTADOS: {resultado.nombre_algoritmo}", 80))
    print(f"  {formato_subtitulo(resultado.nombre_escenario)}")
    print(separador(80))
    
    # 1. Mostrar diagrama de Gantt
    print(f"\n{formato_subtitulo('DIAGRAMA DE GANTT:')}")
    print(separador(80, "-"))
    imprimir_gantt(resultado.segmentos_gantt)
    
    # 2. Mostrar tabla de métricas por proceso
    print(f"\n{formato_subtitulo('TABLA DE MÉTRICAS POR PROCESO:')}")
    print(separador(80, "-"))
    print(tabla_metricas_procesos(resultado.procesos))
    
    # 3. Mostrar promedios
    print(f"\n{formato_subtitulo('PROMEDIOS:')}")
    print(separador(80, "-"))
    print(tabla_promedios(resultado.promedios))

    # 3.1 Mostrar cambios de contexto (si está disponible)
    if "cambios_contexto" in resultado.promedios:
        cambios = int(resultado.promedios["cambios_contexto"])
        print(f"\nCambios de contexto: {cambios}")
    
    print("\n" + separador(80))
    
    # 4. Mostrar gráfico si se solicita
    if mostrar_grafico:
        graficar_gantt(
            resultado.segmentos_gantt,
            resultado.nombre_algoritmo,
            resultado.nombre_escenario
        )



def mostrar_grafico_solo(resultado: ResultadoAlgoritmo) -> None:
    """
    Muestra solo el gráfico de Gantt sin las tablas (para evitar duplicación).

    Args:
        resultado: Objeto ResultadoAlgoritmo con los datos de la simulación.
    """
    graficar_gantt(
        resultado.segmentos_gantt,
        resultado.nombre_algoritmo,
        resultado.nombre_escenario
    )


def seleccionar_visualizacion() -> bool:
    """
    Pregunta al usuario si desea ver el diagrama de Gantt gráfico.

    Returns:
        True si desea ver el gráfico, False en caso contrario.
    """
    while True:
        opcion = input("\n¿Desea ver el diagrama de Gantt gráfico? (s/n): ").strip().lower()
        if opcion in ("s", "si", "sí"):
            return True
        elif opcion in ("n", "no"):
            return False
        else:
            print("Entrada inválida. Ingrese 's' o 'n'.")


def mostrar_resultados_multiples(resultados: dict, mostrar_graficos: bool = False) -> None:
    """
    Muestra los resultados de múltiples algoritmos de forma resumida con formato mejorado.

    Args:
        resultados: Diccionario con los resultados de cada algoritmo.
        mostrar_graficos: Si es True, genera gráficos comparativos.
    """
    print("\n" + separador(100))
    print(formato_titulo("RESUMEN COMPARATIVO - TODOS LOS ALGORITMOS", 100))
    print(separador(100))
    
    print("\n" + tabla_comparativa_algoritmos(resultados))
    
    # Resumen de cambios de contexto por algoritmo
    print("\n" + formato_subtitulo("Cambios de contexto por algoritmo:"))
    for nombre_algo, resultado in resultados.items():
        cambios = resultado.promedios.get("cambios_contexto")
        if cambios is not None:
            print(f"  - {nombre_algo}: {int(cambios)}")
    
    print("\n" + separador(100))
    
    # Si se solicita, mostrar gráficos comparativos
    if mostrar_graficos:
        # Preparar datos para subplots
        datos_para_graficar = {
            nombre: resultado.segmentos_gantt 
            for nombre, resultado in resultados.items()
        }
        
        # Obtener el nombre del escenario del primer resultado
        primer_resultado = next(iter(resultados.values()))
        nombre_escenario = primer_resultado.nombre_escenario
        
        # Generar gráfico con subplots
        graficar_gantt_subplots(datos_para_graficar, nombre_escenario)



def mostrar_graficos_comparativos(resultados: dict) -> None:
    """
    Muestra solo los gráficos comparativos sin las tablas (para evitar duplicación).

    Args:
        resultados: Diccionario con los resultados de cada algoritmo.
    """
    # Preparar datos para subplots
    datos_para_graficar = {
        nombre: resultado.segmentos_gantt 
        for nombre, resultado in resultados.items()
    }
    
    # Obtener el nombre del escenario del primer resultado
    primer_resultado = next(iter(resultados.values()))
    nombre_escenario = primer_resultado.nombre_escenario
    
    # Generar gráfico con subplots
    graficar_gantt_subplots(datos_para_graficar, nombre_escenario)


def ejecutar_aplicacion() -> None:
    """
    Orquesta el flujo de interacción completo de la aplicación.
    
    Pasos:
    1. Seleccionar escenario.
    2. Seleccionar algoritmo o 'TODOS'.
    3. Ejecutar la simulación.
    4. Mostrar resultados.
    5. Opción de ver gráficos.
    6. Opción de repetir o salir.
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
                    mostrar_resultados(resultado, mostrar_grafico=False)
                
                # Mostrar resumen comparativo
                mostrar_resultados_multiples(resultados, mostrar_graficos=False)
                
                # Preguntar si desea ver gráficos comparativos
                mostrar_graficos = seleccionar_visualizacion()
                if mostrar_graficos:
                    mostrar_graficos_comparativos(resultados)
            else:
                print(f"\nEjecutando {algoritmo_seleccionado}...")
                resultado = ejecutar_algoritmo_en_escenario(algoritmo_seleccionado, escenario_id)
                
                # 4. Mostrar resultados
                mostrar_resultados(resultado, mostrar_grafico=False)
                
                # Preguntar si desea ver gráfico
                mostrar_grafico = seleccionar_visualizacion()
                if mostrar_grafico:
                    mostrar_grafico_solo(resultado)
            
            # 5. Preguntar si continuar
            print("\n" + "=" * 80)
            while True:
                opcion = input("¿Desea ejecutar otra simulación? (s/n): ").strip().lower()
                if opcion in ("s", "si", "sí"):
                    break
                elif opcion in ("n", "no"):
                    return
                else:
                    print("Entrada inválida. Ingrese 's' o 'n'.")
        
        except ValueError as e:
            print(f"\nError: {e}")
        except Exception as e:
            print(f"\nError inesperado: {e}")
            print("Por favor, intente de nuevo.")
