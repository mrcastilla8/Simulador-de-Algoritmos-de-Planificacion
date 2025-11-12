# Diseño General del Simulador de Planificación de CPU

## 1. Objetivo del sistema

El objetivo de este proyecto es **simular algoritmos de planificación de CPU** sobre dos escenarios fijos de procesos y calcular las métricas clásicas de planificación:

- Tiempo de finalización
- Tiempo de retorno (turnaround)
- Tiempo de espera
- Tiempo de respuesta

Para los algoritmos:

- FCFS (First Come First Served)
- SJF (Shortest Job First, no expropiativo)
- SRTF (Shortest Remaining Time First, expropiativo)
- Round Robin con quantum = 3 ms
- Round Robin con quantum = 6 ms

El sistema se controla **únicamente por consola** y produce salidas textuales (tablas + diagramas de Gantt simplificados) que luego se usarán para elaborar el informe.

---

## 2. Alcance funcional mínimo

El programa debe permitir:

1. **Elegir escenario**  
   - Escenario 1 – Carga mixta  
   - Escenario 2 – Llegadas dispersas y ráfagas irregulares

2. **Elegir algoritmo** (o todos):
   - FCFS
   - SJF
   - SRTF
   - RR (q = 3)
   - RR (q = 6)
   - Opción “Todos los algoritmos”

3. **Simular el algoritmo seleccionado** sobre el escenario escogido.

4. **Mostrar por consola**:
   - Diagrama de Gantt textual por algoritmo y escenario.
   - Tabla con métricas por proceso:
     - Tiempo de finalización
     - Tiempo de retorno
     - Tiempo de espera
     - Tiempo de respuesta
   - Promedios de cada métrica por algoritmo.

5. (Opcional pero recomendado) Ejecutar todos los algoritmos sobre un escenario y mostrar un pequeño resumen comparativo numérico para facilitar las conclusiones del informe.

No se requiere interfaz gráfica ni lectura de archivos externos: los escenarios están codificados en el propio programa.

---

## 3. Arquitectura general

El sistema se organiza en capas simples:

- **Capa de Presentación (CLI)**  
  - Archivo: `src/cli.py`  
  - Interacción con el usuario por consola (menús, opciones, impresión de resultados).

- **Capa de Orquestación**  
  - Archivo: `src/simulation.py`  
  - Decide qué escenario cargar y qué algoritmo ejecutar, y coordina con la capa de algoritmos.

- **Capa de Lógica de Negocio (Algoritmos y Métricas)**  
  - Carpeta: `src/algorithms/`  
  - Archivo: `src/metrics.py`  
  - Implementan los algoritmos de planificación y el cálculo de métricas.

- **Capa de Modelo de Datos**  
  - Archivo: `src/models.py`  
  - Define las estructuras `Proceso`, `SegmentoGantt`, `ResultadoProceso`, `ResultadoAlgoritmo`.

- **Capa de Escenarios y Formato de Gantt**  
  - Archivo: `src/scenarios.py` (escenarios fijos)  
  - Archivo: `src/gantt.py` (formato textual del diagrama de Gantt)

- **Punto de entrada**  
  - Archivo: `src/main.py`  
  - Llama a la función principal de CLI (`ejecutar_aplicacion`).

---

## 4. Estructura de directorios

Estructura propuesta del proyecto:

```text
planificador_cpu/
├─ src/
│  ├─ __init__.py
│  ├─ main.py
│  ├─ models.py
│  ├─ scenarios.py
│  ├─ algorithms/
│  │  ├─ __init__.py
│  │  ├─ fcfs.py
│  │  ├─ sjf.py
│  │  ├─ srtf.py
│  │  ├─ round_robin.py
│  ├─ simulation.py
│  ├─ metrics.py
│  ├─ gantt.py
│  ├─ cli.py
└─ docs/
   ├─ diseño_general.md      (este archivo)
   ├─ guia_uso_consola.md
   └─ notas_validacion.md
