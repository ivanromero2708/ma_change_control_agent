##############################################################################################################
# TOOL DESCRIPTIONS
##############################################################################################################

EXTRACT_STRUCTURED_DATA_PROMPT_TOOL_DESC = """
  Extrae información clave de documentos de soporte (Controles de Cambio, Comparativos, o Referencias) y prepara un resumen estructurado.

  ## Cuándo usar
  - Cuando se pide "analizar", "procesar", o "extraer" un documento de soporte que NO es el método legado principal.
  - Usar para **Controles de Cambio (CC)**, **comparaciones Side-by-Side**, o **métodos de referencia** (Farmacopea, USP, etc.).
  - Esta herramienta es llamada por subagentes especialistas (como 'change-control-analyst' o 'reference-methods-agent').

  ## Buenas Prácticas
  - **Selección del Modelo:** La decisión más importante es elegir el `document_type` correcto. El agente debe saber su propio rol (ej. 'change_control_analyst') y usar el `document_type` correspondiente ("change_control").
  - **Manejo de Archivos:** La herramienta maneja automáticamente la conversión de DOCX a PDF y la división (chunking). El agente no necesita preocuparse por esto.
  - **Llamada Única:** No llames a esta herramienta varias veces para el mismo archivo.

  ## Parámetros
  - `dir_document (str)`: La ruta completa (path) al archivo DOCX o PDF que se va a procesar.
  - `document_type (Literal)`: El tipo de modelo de extracción a utilizar. Debe ser **exactamente** uno de los siguientes valores:
      - `"change_control"`: Para un documento de Control de Cambios.
      - `"side_by_side"`: Para un documento de comparación "lado a lado".
      - `"reference_methods"`: Para un método de referencia (ej. Farmacopea, USP).

  ## Salida y Efectos en el Estado
  - **Mensaje de Retorno (ToolMessage):** La herramienta devuelve un `ToolMessage` que contiene un **resumen** en lenguaje natural del contenido extraído (ej. "Se extrajeron 5 cambios...").
  - **Actualización del Estado (State):** Esta herramienta tiene un **doble efecto** en el estado `state['files']`:
      1.  **JSON Completo:** Guarda la extracción completa (el objeto Pydantic) en su ruta principal (ej. `/new/change_control.json`). El agente **no** debe leer este archivo gigante.
      2.  **Resumen Estructurado:** Guarda un **nuevo** archivo de resumen pequeño (ej. `/new/change_control_summary.json`). Este archivo SÍ es pequeño y contiene la `lista_cambios` (para CC) u otros datos estructurados listos para usar.

  ## Siguiente Paso Esperado
  - Después de ejecutar esta herramienta, el siguiente paso lógico del agente es:
      1.  Llamar a `read_file()` sobre el archivo de **resumen** (ej. `/new/change_control_summary.json`) para obtener la lista de cambios o los datos estructurados.
      2.  Usar esa lista para informar al supervisor o para el siguiente paso de planificación (ej. 'dictionary-planner').
"""

CHANGE_CONTROL_ANALYSIS_TOOL_DESCRIPTION = """
  Analiza la información estructurada de control de cambios y genera un plan accionable para actualizar el método analítico.

  ## Cuándo usar
  - Después de que existan los archivos procesados por `change_control_agent`, `side_by_side_agent` y/o `reference_methods_agent`.
  - Cuando el supervisor necesita consolidar los cambios propuestos y traducirlos en instrucciones de edición sobre `/new/new_method_final.json`.
  - Úsala una sola vez por ciclo de implementación, una vez que todos los insumos relevantes estén listos.

  ## Buenas Prácticas
  - **Insumos obligatorios:** Siempre debe estar disponible `/new/change_control.json` y contener las descripciones de cambios.
  - **Insumos opcionales:** `/new/side_by_side.json` y `/new/reference_methods.json` pueden no existir; la herramienta manejará su ausencia.
  - **Contexto resumido:** No es necesario leer manualmente los archivos grandes; la herramienta los valida y extrae solo los campos necesarios para el LLM.

  ## Parámetros
  - `change_control_path (str)`: Ruta al JSON estructurado del control de cambios. Debe ser siempre `/new/change_control.json`.
  - `new_method_path (str)`: Ruta al método analítico consolidado sobre el cual se aplicarán los parches. Usualmente `/new/new_method_final.json`.
  - `side_by_side_path (str)`: Ruta al JSON side-by-side (si existe). Normalmente `/new/side_by_side.json`.
  - `reference_methods_path (str)`: Ruta al JSON de métodos de referencia (si existe). Por defecto `/new/reference_methods.json`.

  ## Salida y Efectos en el Estado
  - **Mensaje de Retorno (ToolMessage):** Resume la cantidad de acciones propuestas para implementar los cambios.
  - **Actualización del Estado:** Crea o reemplaza `/new/change_implementation_plan.json`, con un plan estructurado que incluye:
    - listado de cambios,
    - pruebas afectadas o nuevas,
    - acción sugerida (`replace`, `append`, `noop`, `investigar`),
    - JSON Patch propuesto para aplicar sobre el método nuevo.

  ## Siguiente Paso Esperado
  - Revisar el plan generado (leer `/new/change_implementation_plan.json`).
  - Someter cada acción a validación humana si es necesario y, posteriormente, llamar a la herramienta de parcheo (`apply_method_patch`) para aplicar los cambios aprobados.
"""

APPLY_METHOD_PATCH_TOOL_DESCRIPTION = """
  Genera y aplica el contenido completo de una prueba por accion del plan usando la informacion del metodo nuevo,
  del metodo legado, del side-by-side y de los metodos de referencia.
  
  ## Cuando usar
  - Despues de obtener el plan en `/new/change_implementation_plan.json` mediante `analyze_change_impact`.
  - Cuando necesites materializar **una** accion del plan (indice especifico) para actualizar `/new/new_method_final.json`.
  - Cada llamada procesa una accion: editar, adicionar, eliminar o dejar igual. Ejecuta tantas llamadas como acciones existan.
  
  ## Buenas Practicas
  - Proporciona siempre el `action_index` correcto; revisa el plan antes de llamar a la herramienta.
  - Asegurate de que los archivos de referencia (`legacy_method`, `side_by_side` y `reference_method`) esten cargados en el estado para
    que el LLM disponga de contexto completo.
  - La herramienta guarda el resultado en `/new/applied_changes/{action_index}.json` y actualiza `/new/new_method_final.json`.
  
  ## Parametros
  - `plan_path (str)`: Ruta al plan generado por `analyze_change_impact`. Default `/new/change_implementation_plan.json`.
  - `action_index (int)`: Indice (0-based) de la accion a ejecutar.
  - `side_by_side_path (str)`: Ruta al JSON del analisis side-by-side. Default `/new/side_by_side.json`.
  - `reference_method_path (str)`: Ruta al JSON de metodos de referencia. Default `/new/reference_methods.json`.
  - `legacy_method_path (str)`: Ruta al metodo legado estructurado. Default `/actual_method/test_solution_structured_content.json`.
  - `new_method_path (str)`: Ruta al metodo consolidado que sera modificado. Default `/new/new_method_final.json`.
  
  ## Salida y Efectos en el Estado
  - **Mensaje de Retorno (ToolMessage):** Indica si la prueba se genero/aplico y resume notas del LLM.
  - **Actualizacion del Estado:** Sobrescribe `/new/new_method_final.json`, registra la ejecucion en `/logs/change_patch_log.jsonl`
    y deja el parche individual en `/new/applied_changes/{action_index}.json`.
  
  ## Siguiente Paso Esperado
  - Una vez procesadas todas las acciones, ejecutar `consolidate_new_method` para fusionar todos los parches en el metodo final a renderizar.
  """


STRUCTURED_EXTRACTION_CHANGE_CONTROL = """
  Eres un asistente experto en análisis de documentos de control de cambios (CC) farmacéuticos.
  Tu tarea es leer el texto de entrada, que describe los cambios realizados, y extraer la información clave en un formato JSON estructurado.

  Debes generar un JSON que se ajuste perfectamente al siguiente modelo de datos:

  ```json
  {{
    "filename": "CC-001_resumen_cambios.md",
    "summary": "Un resumen conciso en lenguaje natural de los cambios descritos.",
    "lista_cambios": [
      "Descripción textual del primer cambio",
      "Descripción textual del segundo cambio",
      "..."
    ]
  }}
  ````

  # Reglas de Generación de Campos

  Debes seguir estas reglas estrictamente:

  **`filename`**:

    * Genera un nombre de archivo descriptivo basado en el contenido.
    * Debe ser corto, usar guiones bajos (`_`) en lugar de espacios, y terminar en `.md`.
    * Por ejemplo: `CC-00123_actualizacion_limites.md`.

  **`summary`**:

    * Escribe un resumen muy conciso, en una o dos frases, que describa el propósito general de los cambios.
    * Ejemplo: "Actualización de los criterios de aceptación para la prueba de Dureza y ajuste del procedimiento de Disolución."

  **`lista_cambios`**:

    * Esta es la tarea principal. Lee atentamente el texto de entrada.
    * Extrae cada cambio individual o "ítem de cambio" descrito como un **string separado** en la lista.
    * Copia el texto del cambio tan literalmente como sea posible, incluyendo detalles técnicos, valores antiguos y valores nuevos.
    * Si un cambio menciona la "justificación", inclúyela como parte del string de descripción del cambio.
    * Si el texto de entrada describe 5 cambios distintos, la `lista_cambios` debe contener 5 strings.

  # Texto de Entrada (Control de Cambio)

  El texto a continuación contiene la descripción detallada de los cambios.

  <descripcion_detallada_cambio>
  {metadata_content}
  </descripcion_detallada_cambio>

  Genera el JSON estructurado basado *únicamente* en el texto de entrada.
"""

STRUCTURED_EXTRACTION_SIDE_BY_SIDE = """
  Extraer información específica que será insertada en el método analítico modificado a partir de la información extraída de un documento side by side. Debe ser estructurada acorde al formato del método analítico.

  ## JSON de Entrada

  <descripcion_side_by_side>
  {metadata_content}
  </descripcion_side_by_side>
"""

STRUCTURED_EXTRACTION_REFERENCE_METHODS = """
  Extraer información específica que será insertada en el método analítico modificado a partir de la información extraída de diferentes métodos analíticos de referencia. Debe ser estructurada acorde al formato del método analítico.

  ## JSON de Entrada

  <datos_metodo_referencia>
  {metadata_content}
  </datos_metodo_referencia>
"""

CONSOLIDATE_NEW_METHOD_TOOL_DESCRIPTION = """
  Fusiona todos los parches individuales generados por `apply_method_patch` en un solo metodo final listo para renderizar.
  
  ## Cuando usar
  - Despues de aplicar todas las acciones con `apply_method_patch`.
  - Cuando necesites un unico JSON consistente para entregar o renderizar.
  
  ## Parametros
  - `patches_dir (str)`: Directorio virtual donde se guardan los parches individuales. Default `/new/applied_changes`.
  - `base_method_path (str)`: Ruta al metodo base sobre el que se aplicaran los parches. Default `/new/new_method_final.json`.
  - `output_path (str)`: Ruta de salida del metodo consolidado. Default `/new/new_method_final.json`.
  
  ## Salida y Efectos en el Estado
  - **Mensaje de Retorno (ToolMessage):** Resumen de parches leidos y aplicados.
  - **Actualizacion del Estado:** Escribe el metodo consolidado en `output_path` con todos los cambios aplicados.
  
  ## Siguiente Paso Esperado
  - Revisar el metodo consolidado (si es necesario) y proceder con el renderizado o pasos de QA.
  """
