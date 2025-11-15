import sys
import os


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
from .export_json import (
    exportar_resultado_json,
    exportar_resultados_multiples_json,
)



def seleccionar_escenario() -> int:
    while True:
        print("\n" + "=" * 60)
        print("SELECCIONAR ESCENARIO")
        print("=" * 60)
        print("1. Escenario 1 - Carga mixta")
        print("2. Escenario 2 - Llegadas dispersas")
        print("-" * 60)
        
        entrada = input("Ingrese el numero del escenario (1 o 2): ").strip()
        
        if entrada in ("1", "2"):
            return int(entrada)
        else:
            print("Entrada invulida. Por favor, ingrese 1 o 2.")


def seleccionar_algoritmo() -> str:
    while True:
        print("\n" + "=" * 60)
        print("SELECCIONAR ALGORITMO")
        print("=" * 60)
        
        for i, algo in enumerate(ALGORITMOS_DISPONIBLES, 1):
            print(f"{i}. {algo}")
        
        print(f"{len(ALGORITMOS_DISPONIBLES) + 1}. Ejecutar TODOS")
        print("-" * 60)
        
        entrada = input("Ingrese el numero del algoritmo: ").strip()
        
        try:
            opcion = int(entrada)
            if 1 <= opcion <= len(ALGORITMOS_DISPONIBLES):
                return ALGORITMOS_DISPONIBLES[opcion - 1]
            elif opcion == len(ALGORITMOS_DISPONIBLES) + 1:
                return "TODOS"
            else:
                print(f"Opciun invulida. Ingrese un numero entre 1 y {len(ALGORITMOS_DISPONIBLES) + 1}.")
        except ValueError:
            print("Entrada invulida. Por favor, ingrese un numero.")


def mostrar_resultados(resultado: ResultadoAlgoritmo, mostrar_grafico: bool = False) -> None:
    print("\n" + separador(80))
    print(formato_titulo(f"RESULTADOS: {resultado.nombre_algoritmo}", 80))
    print(f"  {formato_subtitulo(resultado.nombre_escenario)}")
    print(separador(80))
    
    print(f"\n{formato_subtitulo('DIAGRAMA DE GANTT:')}")
    print(separador(80, "-"))
    imprimir_gantt(resultado.segmentos_gantt)
    
    print(f"\n{formato_subtitulo('TABLA DE MuTRICAS POR PROCESO:')}")
    print(separador(80, "-"))
    print(tabla_metricas_procesos(resultado.procesos))
    
    print(f"\n{formato_subtitulo('PROMEDIOS:')}")
    print(separador(80, "-"))
    print(tabla_promedios(resultado.promedios))

    if "cambios_contexto" in resultado.promedios:
        cambios = int(resultado.promedios["cambios_contexto"])
        print(f"\nCambios de contexto: {cambios}")
    
    print("\n" + separador(80))
    
    if mostrar_grafico:
        graficar_gantt(
            resultado.segmentos_gantt,
            resultado.nombre_algoritmo,
            resultado.nombre_escenario
        )


def mostrar_grafico_solo(resultado: ResultadoAlgoritmo) -> None:
    graficar_gantt(
        resultado.segmentos_gantt,
        resultado.nombre_algoritmo,
        resultado.nombre_escenario
    )


def seleccionar_visualizacion() -> bool:
    while True:
        opcion = input("\nsDesea ver el diagrama de Gantt grufico? (s/n): ").strip().lower()
        if opcion in ("s", "si", "suu"):
            return True
        elif opcion in ("n", "no"):
            return False
        else:
            print("Entrada invulida. Ingrese 's' o 'n'.")


def mostrar_resultados_multiples(resultados: dict, mostrar_graficos: bool = False) -> None:
    print("\n" + separador(100))
    print(formato_titulo("RESUMEN COMPARATIVO - TODOS LOS ALGORITMOS", 100))
    print(separador(100))
    
    print("\n" + tabla_comparativa_algoritmos(resultados))
    
    print("\n" + formato_subtitulo("Cambios de contexto por algoritmo:"))
    for nombre_algo, resultado in resultados.items():
        cambios = resultado.promedios.get("cambios_contexto")
        if cambios is not None:
            print(f"  - {nombre_algo}: {int(cambios)}")
    
    print("\n" + separador(100))
    
    if mostrar_graficos:
        datos_para_graficar = {
        datos_para_graficar = {
            nombre: resultado.segmentos_gantt 
            for nombre, resultado in resultados.items()
        }
        primer_resultado = next(iter(resultados.values()))
        nombre_escenario = primer_resultado.nombre_escenario
        
        graficar_gantt_subplots(datos_para_graficar, nombre_escenario)


def mostrar_graficos_comparativos(resultados: dict) -> None:
    datos_para_graficar = {
        nombre: resultado.segmentos_gantt 
        for nombre, resultado in resultados.items()
    }
    
    primer_resultado = next(iter(resultados.values()))
    nombre_escenario = primer_resultado.nombre_escenario
    
    graficar_gantt_subplots(datos_para_graficar, nombre_escenario)

def _sanitizar_nombre_archivo(texto: str) -> str:
    return (
        texto.replace(" ", "_")
             .replace("(", "")
             .replace(")", "")
             .replace("-", "_")
             .replace(":", "")
    )


def preguntar_guardar_gantt_png(resultado: ResultadoAlgoritmo) -> None:
    while True:
        opcion = input("\nsDesea guardar el diagrama de Gantt como imagen PNG? (s/n): ").strip().lower()
        if opcion in ("n", "no"):
            return
        elif opcion in ("s", "si", "suu"):
            base_alg = _sanitizar_nombre_archivo(resultado.nombre_algoritmo)
            base_esc = _sanitizar_nombre_archivo(resultado.nombre_escenario)
            nombre_defecto = f"gantt_{{base_alg}}_{{base_esc}}.png"

            nombre = input(f"Nombre de archivo PNG [{nombre_defecto}]: ").strip()
            if not nombre:
                nombre = nombre_defecto

            try:
                graficar_gantt(
                    resultado.segmentos_gantt,
                    resultado.nombre_algoritmo,
                    resultado.nombre_escenario,
                    guardar_como=nombre,
                    mostrar=False,  
                )
                print(f"Diagrama de Gantt guardado en: {nombre}")
            except Exception as e:
                print(f"Error al guardar el diagrama de Gantt: {e}")
            return
        else:
            print("Entrada invulida. Ingrese 's' o 'n'.")


def preguntar_guardar_graficos_comparativos_png(resultados: dict) -> None:
    if not resultados:
        return

    while True:
        opcion = input("\nsDesea guardar los diagramas comparativos como PNG? (s/n): ").strip().lower()
        if opcion in ("n", "no"):
            return
        elif opcion in ("s", "si", "suu"):
            primer_resultado = next(iter(resultados.values()))
            nombre_escenario = primer_resultado.nombre_escenario
            base_esc = _sanitizar_nombre_archivo(nombre_escenario)
            nombre_defecto = f"gantt_comparativo_{{base_esc}}.png"

            nombre = input(f"Nombre de archivo PNG [{nombre_defecto}]: ").strip()
            if not nombre:
                nombre = nombre_defecto
            datos_para_graficar = {
                nombre_algo: resultado.segmentos_gantt
                for nombre_algo, resultado in resultados.items()
            }

            try:
                graficar_gantt_subplots(
                    datos_para_graficar,
                    nombre_escenario,
                    guardar_como=nombre,
                    mostrar=False,  
                )
                print(f"Diagramas comparativos guardados en: {nombre}")
            except Exception as e:
                print(f"Error al guardar los diagramas comparativos: {e}")
            return
        else:
            print("Entrada invulida. Ingrese 's' o 'n'.")


def preguntar_exportar_resultado_json(resultado: ResultadoAlgoritmo) -> None:
    while True:
        opcion = input("\nsDesea exportar estos resultados a JSON? (s/n): ").strip().lower()
        if opcion in ("n", "no"):
            return
        elif opcion in ("s", "si", "suu"):
            nombre_alg = resultado.nombre_algoritmo.replace(" ", "_").replace("(", "").replace(")", "")
            nombre_esc = resultado.nombre_escenario.replace(" ", "_").replace("-", "")
            nombre_defecto = f"resultado_{{nombre_alg}}_{{nombre_esc}}.json"

            nombre = input(f"Nombre de archivo JSON [{nombre_defecto}]: ").strip()
            if not nombre:
                nombre = nombre_defecto

            try:
                exportar_resultado_json(resultado, nombre)
                print(f"Resultados exportados en: {nombre}")
            except Exception as e:
                print(f"Error al exportar a JSON: {e}")
            return
        else:
            print("Entrada invulida. Ingrese 's' o 'n'.")


def preguntar_exportar_resultados_multiples_json(resultados: dict, escenario_id: int) -> None:
    while True:
        opcion = input("\nsDesea exportar el resumen comparativo a JSON? (s/n): ").strip().lower()
        if opcion in ("n", "no"):
            return
        elif opcion in ("s", "si", "suu"):
            nombre_defecto = f"resultados_escenario_{{escenario_id}}.json"
            nombre = input(f"Nombre de archivo JSON [{nombre_defecto}]: ").strip()
            if not nombre:
                nombre = nombre_defecto

            try:
                exportar_resultados_multiples_json(resultados, nombre)
                print(f"Resumen exportado en: {nombre}")
            except Exception as e:
                print(f"Error al exportar a JSON: {e}")
            return
        else:
            print("Entrada invulida. Ingrese 's' o 'n'.")


def ejecutar_aplicacion() -> None:
    print("\n" + "= " * 20)
    print("BIENVENIDO AL SIMULADOR DE ALGORITMOS DE PLANIFICACIuN CPU")
    print("= " * 20)
    
    while True:
        try:
            escenario_id = seleccionar_escenario()
            
            algoritmo_seleccionado = seleccionar_algoritmo()
            
            if algoritmo_seleccionado == "TODOS":
                print("\nEjecutando todos los algoritmos...")
                resultados = ejecutar_todos_los_algoritmos(escenario_id)
                
                for nombre_algo, resultado in resultados.items():
                    mostrar_resultados(resultado, mostrar_grafico=False)
                
                mostrar_resultados_multiples(resultados, mostrar_graficos=False)
                
                mostrar_graficos = seleccionar_visualizacion()
                if mostrar_graficos:
                    mostrar_graficos_comparativos(resultados)
                    
                preguntar_guardar_graficos_comparativos_png(resultados)

                preguntar_exportar_resultados_multiples_json(resultados, escenario_id)                    
            else:
                print(f"\nEjecutando {algoritmo_seleccionado}...")
                resultado = ejecutar_algoritmo_en_escenario(algoritmo_seleccionado, escenario_id)
                
                mostrar_resultados(resultado, mostrar_grafico=False)
                
                mostrar_grafico = seleccionar_visualizacion()
                if mostrar_grafico:
                    mostrar_grafico_solo(resultado)
                    
                preguntar_guardar_gantt_png(resultado)

                
                preguntar_exportar_resultado_json(resultado)
                    
            
            print("\n" + "=" * 80)
            while True:
                opcion = input("\u0073Desea ejecutar otra simulaciun? (s/n): ").strip().lower()
                if opcion in ("s", "si", "suu"):
                    break
                elif opcion in ("n", "no"):
                    return
                else:
                    print("Entrada invulida. Ingrese 's' o 'n'.")
        
        except ValueError as e:
            print(f"\nError: {e}")
        except Exception as e:
            print(f"\nError inesperado: {e}")
            print("Por favor, intente de nuevo.")
