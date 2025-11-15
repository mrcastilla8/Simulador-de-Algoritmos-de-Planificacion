# Simulador de Planificacion de CPU

Aplicacion de consola para estudiar algoritmos clasicos de planificacion bajo escenarios controlados. El sistema permite elegir un escenario, ejecutar uno o todos los algoritmos disponibles, inspeccionar metricas por proceso y documentar los resultados mediante graficos o archivos JSON.

---

## Funcionalidades principales

- **Interfaz CLI guiada** (archivo `src/cli.py`): menues paso a paso para elegir escenario, algoritmo y acciones posteriores.
- **Escenarios fijos** (`src/scenarios.py`): dos conjuntos de procesos (carga mixta y llegadas dispersas) pensados para comparar comportamientos.
- **Algoritmos incluidos** (`src/algorithms/`):
  - FCFS
  - SJF (no expropiativo)
  - SRTF (expropiativo)
  - Round Robin con quantum 3 ms
  - Round Robin con quantum 6 ms
- **Metricas detalladas** (`src/metrics.py`): tiempos de finalizacion, retorno, espera y respuesta por proceso, mas promedios y conteo de cambios de contexto.
- **Visualizaciones de Gantt** (`src/gantt.py`):
  - Diagrama ASCII impreso directamente en consola.
  - Graficos Matplotlib opcionales (individuales o comparativos tipo subplots) con posibilidad de guardarlos como PNG.
- **Formatos de salida complementarios**:
  - Tablas enriquecidas con colores ANSI y `tabulate` (`src/formatters.py`).
  - Exportacion a JSON de un algoritmo (`exportar_resultado_json`) o de todos los algoritmos de un escenario (`exportar_resultados_multiples_json`).

---

## Requisitos e instalacion rapida

1. Python 3.10 o superior.
2. Dependencias externas:
   - `matplotlib`
   - `tabulate`

Instalacion sugerida desde la carpeta raiz (`planificador_cpu/`):

```bash
python -m venv .venv
.venv\Scripts\activate    # en Linux/macOS: source .venv/bin/activate
pip install --upgrade pip
pip install matplotlib tabulate
```

---

## Ejecucion

Desde la carpeta principal del proyecto:

```bash
python -m src.main
```

Flujo general de la aplicacion:

1. Elegir escenario (1 o 2).
2. Elegir un algoritmo especifico o la opcion "TODOS".
3. Revisar tabla de metricas, promedios y conteo de cambios de contexto.
4. Opcional: abrir los graficos Matplotlib, guardar PNG del Gantt (individual o comparativo) y exportar los datos a JSON.
5. Decidir si se repite la simulacion con otros parametros.

---

## Salidas disponibles

- **Consola**:
  - Titulos y secciones coloreadas para cada algoritmo.
  - Diagrama de Gantt en texto alineado.
  - Tabla con metricas por proceso y tabla con promedios.
  - Resumen comparativo cuando se ejecutan todos los algoritmos.
- **PNG**:
  - Gantt individual (`graficar_gantt`) y comparativo (`graficar_gantt_subplots`).
- **JSON**:
  - Resultados completos de un algoritmo (`resultado_algoritmo_a_dict`).
  - Coleccion de algoritmos para un mismo escenario.

---

## Estructura relevante


- `src/simulation.py`: orquesta la carga del escenario y la ejecucion del algoritmo seleccionado.
- `src/models.py`: define los dataclasses usados en toda la aplicacion.
- `src/export_json.py`: helpers para serializar resultados.
- `src/main.py`: punto de entrada que llama a `ejecutar_aplicacion`.
