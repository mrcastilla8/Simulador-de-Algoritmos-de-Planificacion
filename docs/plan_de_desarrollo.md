

## 1. Objetivo funcional del programa

El programa en Python debe permitir, **por consola**, hacer al menos lo siguiente:

1. Elegir:

   * Escenario 1 o Escenario 2.
   * Un algoritmo concreto o “todos los algoritmos”.
2. Simular la planificación elegida:

   * FCFS
   * SJF no expropiativo
   * SRTF (expropiativo)
   * RR (q = 3 ms)
   * RR (q = 6 ms)
3. Mostrar en consola:

   * Diagrama de Gantt (en texto) por algoritmo y escenario.
   * Tabla con, por proceso:

     * Tiempo de finalización
     * Tiempo de retorno
     * Tiempo de espera
     * Tiempo de respuesta
   * Promedios de cada métrica por algoritmo.
4. (Opcional pero recomendado) Opción “ejecutar todos los algoritmos para ambos escenarios” y mostrar un pequeño resumen comparativo numérico (para que luego puedan escribir el informe).

---

## 2. Arquitectura mínima y flujo general

### Flujo general de ejecución

1. **Menú principal (consola)**

   * Elegir escenario (1 o 2).
   * Elegir algoritmo (FCFS, SJF, SRTF, RR q=3, RR q=6, o “todos”).

2. **Carga de procesos del escenario**

   * El programa no pide datos al usuario: los escenarios están **hardcodeados** en el código (listas de procesos ya definidas).

3. **Simulación**

   * Se llama a una función de simulación por algoritmo:

     * `simular_fcfs(procesos)`
     * `simular_sjf(procesos)`
     * `simular_srtf(procesos)`
     * `simular_rr(procesos, quantum)`

   Cada función:

   * Recibe la lista de procesos (nombre, llegada, duración CPU).
   * Retorna una estructura con:

     * Gantt (lista de segmentos: proceso, t_inicio, t_fin).
     * Métricas por proceso (finalización, retorno, espera, respuesta).
     * Promedios.

4. **Salida por consola**

   * Imprimir diagrama de Gantt en texto.
   * Imprimir tabla de métricas individuales.
   * Imprimir promedios.

---

## 3. Estructura de directorios y archivos

Pensado para **mínimo código**, pero modularizado para repartir el trabajo entre 5 devs.

```text
planificador_cpu/
├─ src/
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
│
├─ tests/
│  ├─ test_fcfs.txt          (casos manuales, no hace falta usar unittest)
│  ├─ test_sjf.txt
│  ├─ test_srtf.txt
│  ├─ test_rr_q3_q6.txt
│
└─ docs/
   ├─ diseño_general.md      (flujo, estructuras de datos, decisiones)
   ├─ guia_uso_consola.md    (cómo ejecutar, ejemplos de salida)
   └─ notas_validacion.md    (resultados esperados y verificación)
```

> Todo el código real vive en `src/`.
> Los tests pueden ser solo instrucciones + resultados esperados escritos a mano. Nada de frameworks si no quieren.

---

## 4. Contenido funcional de cada archivo

### 4.1 `src/models.py`

**Responsabilidad**: definir las estructuras mínimas de datos.

* Definir una representación de **Proceso** con:

  * `nombre` (P1, P2, ...)
  * `llegada`
  * `duracion_cpu`

* Definir una representación de **ResultadoProceso**:

  * `nombre`
  * `llegada`
  * `duracion_cpu`
  * `tiempo_finalizacion`
  * `tiempo_retorno`
  * `tiempo_espera`
  * `tiempo_respuesta`

* Definir una estructura para el **segmento de Gantt**:

  * `proceso` (nombre)
  * `inicio`
  * `fin`

* Definir una estructura de **ResultadoAlgoritmo**:

  * lista de `ResultadoProceso`
  * lista de segmentos de Gantt
  * promedios (espera, retorno, respuesta, etc.)

Todo esto puede ser con diccionarios o clases simples, lo que sea más ligero.

---

### 4.2 `src/scenarios.py`

**Responsabilidad**: definir las listas de procesos estáticas para los dos escenarios.

* Funciones:

  * `obtener_escenario_1()` → lista de procesos ya construidos.
  * `obtener_escenario_2()` → lista de procesos ya construidos.

Internamente, simplemente crean instancias de `Proceso` (o dicts) con los datos de las tablas dadas.

---

### 4.3 `src/algorithms/fcfs.py`

**Responsabilidad**: simulación FCFS no expropiativa.

* Función principal:

  * `simular_fcfs(lista_procesos)` → `ResultadoAlgoritmo`.

* Lógica:

  * Ordenar procesos por tiempo de llegada.
  * Recorrer en orden, avanzando el tiempo actual.
  * Generar segmentos de Gantt (un solo bloque por proceso).
  * Para cada proceso, calcular:

    * tiempo_finalización
    * tiempo_retorno = finalización − llegada
    * tiempo_espera = retorno − duración
    * tiempo_respuesta = momento en que comienza ejec. − llegada (en FCFS coincide con espera)
  * Devolver resultados + promedios.

---

### 4.4 `src/algorithms/sjf.py`

**Responsabilidad**: simulación SJF no expropiativo.

* Función:

  * `simular_sjf(lista_procesos)` → `ResultadoAlgoritmo`.

* Lógica mínima:

  * Simulación basada en tiempo actual:

    * En cada momento en que la CPU queda libre:

      * Seleccionar el proceso disponible (llegada <= tiempo actual) con menor duración.
      * Si no hay proceso disponible, avanzar el tiempo al siguiente tiempo de llegada.
  * Ejecución sin expropiación: cada proceso ejecuta su ráfaga completa en un solo segmento.
  * Calcular métricas como en FCFS.

---

### 4.5 `src/algorithms/srtf.py`

**Responsabilidad**: simulación SRTF expropiativo.

* Función:

  * `simular_srtf(lista_procesos)` → `ResultadoAlgoritmo`.

* Lógica:

  * Mantener, para cada proceso, su **tiempo restante**.
  * Recorres el tiempo en pasos de 1 ms (lo más simple) o saltando a los eventos de llegada/cambio:

    * En cada unidad de tiempo:

      * Añadir nuevos procesos que llegan a una “cola de listos”.
      * Elegir el proceso con menor tiempo restante.
      * Si cambia el proceso en ejecución, se marca cambio de contexto (opcional registrar).
      * Registrar en la lista de segmentos (fusionar segmentos contiguos del mismo proceso para simplificar).
  * Tiempo de respuesta:

    * Se mide cuando el proceso es ejecutado por primera vez.
  * Al terminar, calcular métricas por proceso.

---

### 4.6 `src/algorithms/round_robin.py`

**Responsabilidad**: simulación Round Robin genérico + dos funciones de conveniencia.

* Funciones:

  * `simular_rr(lista_procesos, quantum)`
  * `simular_rr_q3(lista_procesos)` → llama a `simular_rr(..., 3)`
  * `simular_rr_q6(lista_procesos)` → llama a `simular_rr(..., 6)`

* Lógica:

  * Cola circular de listos.
  * En cada iteración:

    * Si no hay procesos disponibles, avanzar tiempo al próximo tiempo de llegada.
    * Tomar el primer proceso de la cola.
    * Ejecutarlo por `min(quantum, tiempo_restante)`.
    * Registrar segmento de Gantt.
    * Actualizar tiempo restante.
    * Si no termina, se vuelve al final de la cola.
  * Calcular métricas como en SRTF (respuesta es el primer instante en que el proceso entra a CPU).

---

### 4.7 `src/simulation.py`

**Responsabilidad**: orquestar escenarios + algoritmos y llamar a `metrics`.

* Funciones sugeridas:

  * `ejecutar_algoritmo_en_escenario(algoritmo, escenario_id)`

    * Carga la lista de procesos (`scenarios.py`).
    * Llama a la función del algoritmo correspondiente.
  * `ejecutar_todos_los_algoritmos(escenario_id)`

    * Ejecuta FCFS, SJF, SRTF, RR q=3, RR q=6 y devuelve todos los `ResultadoAlgoritmo`.

**Importante**: esta capa no recalcula métricas, solo coordina.

---

### 4.8 `src/metrics.py`

**Responsabilidad**: funciones de apoyo para calcular métricas.

Aunque cada algoritmo podría calcular sus métricas internamente, para **reducir código duplicado**:

* Funciones:

  * `calcular_metricas(procesos, segmentos_gantt)`
    Recibe:

    * Lista de procesos (con llegada y duración).
    * Segmentos de Gantt (ordenados por tiempo).
      Devuelve:
    * Lista de `ResultadoProceso`.
    * Diccionario con promedios.

* Dentro:

  * Para cada proceso:

    * tiempo_finalizacion: max `fin` de sus segmentos.
    * tiempo_respuesta: primer `inicio` de sus segmentos − llegada.
    * tiempo_retorno: finalización − llegada.
    * tiempo_espera: retorno − duración CPU.
  * Promedios: promedio simple de cada métrica.

Cada algoritmo:

* Se encarga solo de construir bien los segmentos de Gantt (y, si quiere, de marcar tiempos de fin).
* Llama a `calcular_metricas` para rellenar el resto.

---

### 4.9 `src/gantt.py`

**Responsabilidad**: generar salida textual del diagrama de Gantt.

Funciones:

* `imprimir_gantt(segmentos_gantt)`

  * Imprimir una línea con bloques tipo:

    `0   3   5   9   ...`
    `| P1 | P2 | P3 | ...`

  * Puede ser super simple:

    * Una línea con los nombres de procesos en orden (repetidos según segmentos).
    * Una segunda línea con los tiempos de inicio/fin.

* (Opcional) `formatear_gantt(segmentos_gantt)` que retorna un string para que `cli` lo imprima.

---

### 4.10 `src/cli.py`

**Responsabilidad**: toda la interacción por consola.

Funciones:

* `mostrar_menu_principal()`
* `seleccionar_escenario()`
* `seleccionar_algoritmo()`
* `mostrar_resultados(resultado_algoritmo)`

  * Imprimir:

    * Nombre del algoritmo y escenario.
    * Gantt (usando `gantt.py`).
    * Tabla con métricas por proceso.
    * Promedios.

El CLI SOLO llama a `simulation.py` y muestra resultados. Nada de lógica de planificación aquí.

---

### 4.11 `src/main.py`

**Responsabilidad**: punto de entrada mínimo.

* Contiene:

  * `if __name__ == "__main__":`

    * Llamar a funciones del `cli` para iniciar el programa.

---

## 5. Plan de trabajo por desarrollador

### Reglas

* Somos 5 devs.
* Distribuimos tareas por módulos, equilibrando la carga.

---

### MARCO (Líder) – Arquitectura, integración y revisión

**Tareas principales**

1. **Diseño general y documentación mínima**

   * Crear `docs/diseño_general.md`:

     * Descripción del flujo general.
     * Relación entre módulos (`models`, `algorithms`, `simulation`, `cli`, etc.).
     * Decisiones: simulación por pasos de 1 ms, estructura de datos elegida (objetos o dicts), etc.

2. **Definir modelos comunes**

   * Diseñar y escribir `src/models.py` con estructuras `Proceso`, `ResultadoProceso`, `SegmentoGantt`, `ResultadoAlgoritmo`.
   * Acordar con el equipo cómo se van a usar (ejemplo: atributos obligatorios).

3. **Definir interfaz de escenarios y algoritmos**

   * Especificar, en `diseño_general.md`, las firmas esperadas:

     * `simular_fcfs(lista_procesos)`, etc.
     * Lo que debe devolver cada función.
   * Asegurarse de que todos los devs las respeten.

4. **Integración final**

   * Revisar que:

     * `simulation.py` llame bien a los algoritmos.
     * `cli.py` use bien `simulation.py`.
     * `gantt.py` se integre bien con la estructura de segmentos.
   * Coordinar pruebas rápidas con los escenarios.



---

### POMA – Algoritmos no expropiativos (FCFS y SJF)

**Archivos principales**:

* `src/algorithms/fcfs.py`
* `src/algorithms/sjf.py`
* Ayuda en `tests/test_fcfs.txt` y `tests/test_sjf.txt`

**Tareas concretas**:

1. Implementar `simular_fcfs(lista_procesos)`:

   * Ordenar por llegada.
   * Simular secuencialmente.
   * Construir lista de `SegmentoGantt`.
   * Llamar a `calcular_metricas` de `metrics.py`.

2. Implementar `simular_sjf(lista_procesos)`:

   * Lógica de selección de proceso con menor duración entre los listos.
   * Manejo de huecos de tiempo cuando no hay procesos listos.
   * Construir segmentos de Gantt.

3. Preparar archivos de prueba manual:

   * `tests/test_fcfs.txt`: describir el escenario, ejecución esperada, tiempos de finalización, etc.
   * `tests/test_sjf.txt`: idem.

---

### BRICKZON – Algoritmos expropiativos (SRTF)

**Archivos**:

* `src/algorithms/srtf.py`
* `tests/test_srtf.txt`

**Tareas**:

1. Diseñar e implementar `simular_srtf(lista_procesos)`:

   * Llevar un tiempo actual.
   * En cada paso de tiempo:

     * Añadir procesos que llegan.
     * Elegir el de menor tiempo restante.
   * Registrar segmentos en `SegmentoGantt`:

     * Controlar cuando cambia el proceso activo para cortar segmentos.
   * Al final, entregar segmentos a `metrics.calcular_metricas`.

2. Preparar `tests/test_srtf.txt`:

   * Describir al menos un ejemplo por escenario con los resultados esperados.
   * Marcar claramente tiempos de respuesta/espera para verificar.

---

### AXEL – Round Robin q=3 y q=6, y parte de pruebas

**Archivos**:

* `src/algorithms/round_robin.py`
* `tests/test_rr_q3_q6.txt`

**Tareas**:

1. Implementar la función general `simular_rr(lista_procesos, quantum)`:

   * Lógica de cola circular de listos.
   * Manejo de tiempo actual, llegadas y reingreso de procesos.
   * Construcción de segmentos de Gantt.

2. Implementar funciones de conveniencia:

   * `simular_rr_q3(lista_procesos)`
   * `simular_rr_q6(lista_procesos)`

3. Preparar `tests/test_rr_q3_q6.txt`:

   * Resultados esperados de ambos escenarios con q=3 y q=6.
   * Documentar también el **número de cambios de contexto** observado (dato útil para el informe).

---

### ANGEL – CLI, escenarios, métricas y Gantt

**Archivos**:

* `src/scenarios.py`
* `src/metrics.py`
* `src/gantt.py`
* `src/cli.py`
* `src/simulation.py`
* `docs/guia_uso_consola.md`
* `docs/notas_validacion.md` (junto con los demás)

**Tareas concretas**:

1. `scenarios.py`

   * Implementar `obtener_escenario_1()` y `obtener_escenario_2()`.
   * Usar `Proceso` de `models.py`.

2. `metrics.py`

   * Implementar `calcular_metricas(procesos, segmentos_gantt)`:

     * Calcular finalización, retorno, espera, respuesta para cada proceso.
     * Calcular promedios.

3. `gantt.py`

   * Implementar la función para formatear e imprimir el Gantt:

     * Recibe los segmentos, imprime una representación sencilla en consola.

4. `simulation.py`

   * Implementar las funciones que conectan:

     * Escenario → algoritmos.
     * Opción de ejecutar todos los algoritmos para un escenario.

5. `cli.py`

   * Implementar el menú principal:

     * Preguntar por el escenario.
     * Preguntar por el algoritmo (o “todos”).
     * Llamar a `simulation.py`.
     * Mostrar resultados de cada algoritmo:

       * Gantt.
       * Tabla de métricas (formato texto).
       * Promedios.

6. Documentación de uso:

   * `docs/guia_uso_consola.md`: describir cómo ejecutar `python main.py`, cómo navegar por el menú, ejemplos de salida.
   * `docs/notas_validacion.md`: dejar apuntado algún conjunto de resultados “correctos” para que todos verifiquen que el programa funciona igual.

---

## 6. Orden sugerido de implementación

1. **Líder (MARCO)**:

   * Definir `models.py` y `diseño_general.md`.
2. **ÁNGEL**:

   * Crear `scenarios.py` con los datos fijos.
3. **POMA, BRICKZON Y AXEL**:

   * Implementar algoritmos (FCFS, SJF, SRTF, RR).
4. **ÁNGEL**:

   * Implementar `metrics.py` y `gantt.py`.
5. **ÁNGEL + MARCO**:

   * Implementar `simulation.py` y `cli.py` con el contrato acordado.
6. **Todos**:

   * Probar con los escenarios y completar los `.txt` de tests.
7. **MARCO**:

   * Ajustes finales y validación de coherencia entre módulos.

