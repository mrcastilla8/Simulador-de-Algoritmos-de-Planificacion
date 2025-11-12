"""
Archivo: src/cli.py
Responsable principal: Desarrollador 5

Interfaz de línea de comandos (CLI) para controlar el programa.
"""

from typing import Optional
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

    Debe:
    - Pedir al usuario un número (por ejemplo, 1 o 2).
    - Validar la entrada.
    - Devolver el entero correspondiente.

    TODO: Implementar interacción real por consola.
    """
    raise NotImplementedError("seleccionar_escenario aún no está implementado.")


def seleccionar_algoritmo() -> str:
    """
    Muestra un menú para seleccionar el algoritmo o 'todos'.

    Debe:
    - Mostrar opciones basadas en ALGORITMOS_DISPONIBLES.
    - Incluir una opción 'TODOS'.
    - Devolver uno de:
      - Un nombre de algoritmo, por ejemplo 'FCFS', 'SJF', ...
      - La cadena 'TODOS'.

    TODO: Implementar interacción real por consola.
    """
    raise NotImplementedError("seleccionar_algoritmo aún no está implementado.")


def mostrar_resultados(resultado: ResultadoAlgoritmo) -> None:
    """
    Muestra en consola los resultados de un algoritmo:

    Debe:
    - Imprimir nombre del algoritmo y escenario.
    - Mostrar el diagrama de Gantt (usando imprimir_gantt).
    - Imprimir una tabla de métricas por proceso.
    - Imprimir los promedios.

    TODO: Implementar impresión amigable de resultados en consola.
    """
    raise NotImplementedError("mostrar_resultados aún no está implementado.")


def ejecutar_aplicacion() -> None:
    """
    Orquesta el flujo de interacción completo:

    Pasos sugeridos:
    1. Preguntar escenario.
    2. Preguntar algoritmo o 'TODOS'.
    3. Ejecutar la simulación correspondiente.
    4. Mostrar resultados.
    5. Ofrecer repetir o salir (opcional).

    TODO: Implementar menú principal y bucle de la aplicación.
    """
    raise NotImplementedError("ejecutar_aplicacion aún no está implementado.")
