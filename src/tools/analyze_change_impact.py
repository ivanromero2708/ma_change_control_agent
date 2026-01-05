"""
Tool mejorado para análisis de control de cambios con validaciones robustas,
retry logic y logging detallado.
"""

from __future__ import annotations

import warnings

# Silenciar warnings de Pydantic sobre NotRequired y FileData de deepagents
warnings.filterwarnings(
    "ignore",
    message=".*NotRequired.*",
    category=UserWarning,
    module="pydantic.*"
)

import json
import logging
from datetime import datetime, timezone
from typing import Annotated, Any, Optional, Literal, List

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage
from langchain_core.tools import InjectedToolCallId, tool
from langgraph.prebuilt import InjectedState
from langgraph.types import Command
from pydantic import BaseModel, Field, ValidationError, field_validator
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from src.graph.state import DeepAgentState
from src.prompts.tool_description_prompts import CHANGE_CONTROL_ANALYSIS_TOOL_DESCRIPTION
from src.prompts.tool_llm_calls_prompts import UNIFIED_CHANGE_HUMAN_ANALYSIS_PROMPT, UNIFIED_CHANGE_SYSTEM_ANALYSIS_PROMPT

# --- Configuración ---
logger = logging.getLogger(__name__)

## LLMs
change_control_analysis_model = init_chat_model(model="openai:gpt-5-mini")


# --- Modelos Pydantic ---
class CambioListaCambios(BaseModel):
    """Referencia a un cambio en la lista de cambios del control de cambios."""
    indice: int = Field(description="Índice del cambio en la lista de cambios (0-indexed)")
    texto: str = Field(description="Texto completo del cambio de /new/change_control_summary.json")


class ElementoMetodoPropuesto(BaseModel):
    """Referencia a una prueba en el método propuesto."""
    prueba: str = Field(description="Nombre de la prueba en el método propuesto")
    indice: int = Field(description="Índice de la prueba en /proposed_method/test_solution_structured_content.json")
    source_id: Optional[int] = Field(default=None, description="source_id de la prueba en el método propuesto")


class UnifiedInterventionAction(BaseModel):
    """Una acción individual en el plan de intervención."""
    orden: int = Field(description="Número de orden en el plan de intervención")
    cambio: str = Field(description="Descripción concisa del cambio a implementar")
    prueba_ma_legado: Optional[str] = Field(
        default=None,
        description="Nombre de la prueba del método legado o null si es nueva",
    )
    source_id_ma_legado: Optional[str] = Field(
        default=None,
        description="section_id de la prueba en /actual_method/test_solution_structured_content.json o null",
    )
    accion: Literal["editar", "adicionar", "eliminar", "dejar igual"] = Field(
        description="Acción requerida: editar, adicionar, eliminar o dejar igual"
    )
    cambio_lista_cambios: Optional[CambioListaCambios] = Field(
        default=None,
        description="Elemento de lista_cambios con índice y texto. null si no hay cambio (dejar igual)",
    )
    elemento_metodo_propuesto: Optional[ElementoMetodoPropuesto] = Field(
        default=None,
        description="Prueba e índice en /proposed_method/test_solution_structured_content.json. null si no aplica (ej: eliminar)",
    )

    @field_validator("accion", mode="before")
    @classmethod
    def _normalize_accion(cls, value: Any) -> str:
        """Normaliza las variaciones de nombres de acciones al formato estándar."""
        if isinstance(value, str):
            normalized = value.strip().lower()
            # Reemplazar ñ por n
            normalized = normalized.replace("\u00f1", "n")
            
            mapping = {
                "editar": "editar",
                "edita": "editar",
                "modificar": "editar",
                "actualizar": "editar",
                "adicionar": "adicionar",
                "agregar": "adicionar",
                "anadir": "adicionar",
                "aniadir": "adicionar",
                "nuevo": "adicionar",
                "nueva": "adicionar",
                "eliminar": "eliminar",
                "remover": "eliminar",
                "borrar": "eliminar",
                "quitar": "eliminar",
                "dejar igual": "dejar igual",
                "sin cambio": "dejar igual",
                "sin cambios": "dejar igual",
                "mantener": "dejar igual",
                "no cambiar": "dejar igual",
            }
            
            if normalized in mapping:
                return mapping[normalized]
        return value


class UnifiedInterventionPlan(BaseModel):
    """Plan completo de intervención con resumen y acciones."""
    resumen: str = Field(description="Resumen ejecutivo del plan de intervención")
    plan_intervencion: List[UnifiedInterventionAction] = Field(
        description="Listado ordenado de acciones por prueba"
    )


# --- Funciones auxiliares de carga y normalización ---

def _load_json_payload(files: dict[str, Any], path: str) -> Optional[dict[str, Any]]:
    """
    Extrae un payload JSON normalizado desde el filesystem virtual.
    
    Args:
        files: Diccionario de archivos del estado
        path: Ruta del archivo a cargar
        
    Returns:
        Diccionario con los datos JSON o None si no se encuentra/parsea
    """
    entry = files.get(path)
    if entry is None:
        logger.warning(f"No se encontró archivo en la ruta: {path}")
        return None

    # Caso 1: Entry es un diccionario con estructura anidada
    if isinstance(entry, dict):
        if "data" in entry and isinstance(entry["data"], dict):
            return entry["data"]
        if "content" in entry and isinstance(entry["content"], str):
            try:
                return json.loads(entry["content"])
            except json.JSONDecodeError as e:
                logger.error(f"Error al parsear JSON desde 'content' en {path}: {e}")
                return None
        # Si no tiene 'data' ni 'content', asumimos que es el payload directo
        return entry

    # Caso 2: Entry es una cadena JSON
    if isinstance(entry, str):
        try:
            return json.loads(entry)
        except json.JSONDecodeError as e:
            logger.error(f"Error al parsear JSON string en {path}: {e}")
            return None

    logger.warning(f"Formato no reconocido para archivo en {path}: {type(entry)}")
    return None


def _normalize_name(name: Optional[str]) -> Optional[str]:
    """
    Normaliza un nombre de prueba para comparación consistente.
    
    Aplicaciones:
    - Convierte a minúsculas
    - Elimina acentos
    - Normaliza espacios en blanco
    
    Args:
        name: Nombre a normalizar
        
    Returns:
        Nombre normalizado o None si el input es None/vacío
    """
    if not name:
        return None
    
    normalized = name.strip().lower()
    
    # Reemplazos de acentos
    replacements = {
        "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u",
        "à": "a", "è": "e", "ì": "i", "ò": "o", "ù": "u",
        "ä": "a", "ë": "e", "ï": "i", "ö": "o", "ü": "u",
        "â": "a", "ê": "e", "î": "i", "ô": "o", "û": "u",
        "ñ": "n",
    }
    
    for src, dst in replacements.items():
        normalized = normalized.replace(src, dst)
    
    # Normalizar espacios (múltiples espacios → un espacio)
    return " ".join(normalized.split())


def _collect_prueba_records_with_index(
    pruebas: Optional[list], 
    source_id_key: str = "id_prueba"
) -> list[dict[str, Any]]:
    """
    Convierte una lista de pruebas a formato unificado con índices.
    
    Args:
        pruebas: Lista de objetos de prueba (pueden ser Pydantic models o dicts)
        source_id_key: Nombre del campo que contiene el ID (puede variar)
        
    Returns:
        Lista de diccionarios con formato: {"prueba": str, "source_id": str, "indice": int}
    """
    if not pruebas:
        return []
    
    records: list[dict[str, Any]] = []
    
    for idx, prueba in enumerate(pruebas):
        nombre: Optional[str] = None
        source_id: Optional[str] = None

        # Caso 1: Objeto Pydantic con atributos
        if hasattr(prueba, "prueba"):
            nombre = getattr(prueba, "prueba", None)
            # Intentar obtener source_id de varios campos posibles
            source_id = (
                getattr(prueba, source_id_key, None) or 
                getattr(prueba, "section_id", None) or
                getattr(prueba, "id", None)
            )
        
        # Caso 2: Diccionario
        elif isinstance(prueba, dict):
            nombre = prueba.get("prueba") or prueba.get("test_name") or prueba.get("nombre")
            source_id = (
                prueba.get(source_id_key) or 
                prueba.get("section_id") or 
                prueba.get("id") or
                prueba.get("id_prueba")
            )

        # Solo agregar si al menos tenemos un nombre
        if isinstance(nombre, str) and nombre.strip():
            record: dict[str, Any] = {
                "prueba": nombre.strip(),
                "source_id": source_id,
                "indice": idx,
            }
            records.append(record)
        else:
            logger.warning(f"Prueba en índice {idx} no tiene nombre válido: {prueba}")

    logger.debug(f"Recolectadas {len(records)} pruebas con índices")
    return records


def _collect_cambios_with_index(cambios: Optional[list]) -> list[dict[str, Any]]:
    """
    Convierte una lista de cambios a formato unificado con índices.
    
    Args:
        cambios: Lista de objetos de cambio (pueden ser Pydantic models o dicts)
        
    Returns:
        Lista de diccionarios con formato: {"indice": int, "prueba": str, "texto": str}
    """
    if not cambios:
        return []
    
    records: list[dict[str, Any]] = []
    
    for idx, cambio in enumerate(cambios):
        prueba: Optional[str] = None
        texto: Optional[str] = None

        # Caso 1: Objeto Pydantic
        if hasattr(cambio, "prueba"):
            prueba = getattr(cambio, "prueba", None)
            texto = getattr(cambio, "texto", None) or getattr(cambio, "descripcion", None)
        
        # Caso 2: Diccionario
        elif isinstance(cambio, dict):
            prueba = cambio.get("prueba")
            texto = cambio.get("texto") or cambio.get("descripcion") or cambio.get("cambio")

        record = {
            "indice": idx,
            "prueba": prueba.strip() if isinstance(prueba, str) else None,
            "texto": texto.strip() if isinstance(texto, str) else None,
        }
        records.append(record)

    logger.debug(f"Recolectados {len(records)} cambios con índices")
    return records


def _collect_cambios_from_strings(cambios_strings: list[str]) -> list[dict[str, Any]]:
    """
    Convierte una lista de strings de cambios a formato unificado con índices.
    
    El archivo change_control_summary.json contiene lista_cambios como List[str],
    donde cada string describe un cambio completo.
    
    Args:
        cambios_strings: Lista de strings describiendo cada cambio
        
    Returns:
        Lista de diccionarios con formato: {"indice": int, "prueba": str|None, "texto": str}
    """
    if not cambios_strings:
        return []
    
    records: list[dict[str, Any]] = []
    
    for idx, cambio_text in enumerate(cambios_strings):
        if not isinstance(cambio_text, str):
            cambio_text = str(cambio_text) if cambio_text else ""
        
        # Intentar extraer nombre de prueba del texto
        # Patrones comunes: "Prueba X: descripción" o "X - descripción"
        prueba: Optional[str] = None
        texto = cambio_text.strip()
        
        # Buscar patrones como "Prueba:" o nombre seguido de ":"
        if ":" in texto:
            parts = texto.split(":", 1)
            potential_prueba = parts[0].strip()
            # Si la primera parte es corta, probablemente es el nombre de la prueba
            if len(potential_prueba) < 100:
                prueba = potential_prueba
        
        record = {
            "indice": idx,
            "prueba": prueba,
            "texto": texto,
        }
        records.append(record)
    
    logger.debug(f"Recolectados {len(records)} cambios desde strings")
    return records

# --- Funciones de extracción de pruebas ---

def _extract_tests_from_legacy(legacy_payload) -> list:
    """
    Extrae lista de pruebas del método legado.
    
    La estructura real del legado puede ser:
    1. Lista de wrappers: [{"tests": [...], "source_id": N}, ...]
    2. Dict con "tests" o "pruebas": {"tests": [...]} o {"pruebas": [...]}
    3. Lista directa de pruebas
    
    Args:
        legacy_payload: Payload del archivo test_solution_structured_content.json
        
    Returns:
        Lista de pruebas aplanada (pueden ser dicts o objetos)
    """
    if not legacy_payload:
        return []
    
    # Si es lista, puede ser lista de wrappers o lista directa de pruebas
    if isinstance(legacy_payload, list):
        flattened = []
        for item in legacy_payload:
            if isinstance(item, dict):
                # Verificar si es un wrapper con "tests" anidado
                if "tests" in item and isinstance(item["tests"], list):
                    flattened.extend(item["tests"])
                else:
                    # Es una prueba directa
                    flattened.append(item)
        
        if flattened:
            logger.debug(f"Extraídas {len(flattened)} pruebas del método legado (aplanadas)")
            return flattened
        
        logger.debug(f"Payload legado es lista directa con {len(legacy_payload)} elementos")
        return legacy_payload
    
    # Si es dict, buscar "tests" o "pruebas"
    if isinstance(legacy_payload, dict):
        tests = legacy_payload.get("tests") or legacy_payload.get("pruebas") or []
        # Recursivamente aplanar si es necesario
        if isinstance(tests, list):
            return _extract_tests_from_legacy(tests)
        logger.debug(f"Extraídas {len(tests)} pruebas del método legado")
        return tests
    
    logger.warning(f"Formato inesperado de legacy_payload: {type(legacy_payload)}")
    return []


def _extract_tests_from_proposed(proposed_payload) -> list:
    """
    Extrae lista de pruebas del método propuesto.
    
    La estructura es igual que el método legado:
    Lista de wrappers: [{"tests": [...], "source_id": N}, ...]
    
    Args:
        proposed_payload: Payload del archivo /proposed_method/test_solution_structured_content.json
        
    Returns:
        Lista de pruebas aplanada con source_id preservado
    """
    if not proposed_payload:
        return []
    
    # Si es lista, puede ser lista de wrappers o lista directa de pruebas
    if isinstance(proposed_payload, list):
        flattened = []
        for item in proposed_payload:
            if isinstance(item, dict):
                source_id = item.get("source_id")
                # Verificar si es un wrapper con "tests" anidado
                if "tests" in item and isinstance(item["tests"], list):
                    for test in item["tests"]:
                        if isinstance(test, dict):
                            # Preservar source_id del wrapper en cada test
                            test_copy = dict(test)
                            if source_id is not None:
                                test_copy["_source_id"] = source_id
                            flattened.append(test_copy)
                else:
                    # Es una prueba directa
                    flattened.append(item)
        
        if flattened:
            logger.debug(f"Extraídas {len(flattened)} pruebas del método propuesto (aplanadas)")
            return flattened
        
        logger.debug(f"Payload propuesto es lista directa con {len(proposed_payload)} elementos")
        return proposed_payload
    
    # Si es dict, buscar "tests" o "pruebas"
    if isinstance(proposed_payload, dict):
        tests = proposed_payload.get("tests") or proposed_payload.get("pruebas") or []
        if isinstance(tests, list):
            return _extract_tests_from_proposed(tests)
        logger.debug(f"Extraídas {len(tests)} pruebas del método propuesto")
        return tests
    
    logger.warning(f"Formato inesperado de proposed_payload: {type(proposed_payload)}")
    return []


# --- Funciones de validación ---

def _validate_context(llm_context: dict) -> tuple[bool, str]:
    """
    Valida que el contexto tenga la estructura mínima requerida.
    
    Args:
        llm_context: Contexto que se enviará al LLM
        
    Returns:
        Tupla (es_válido, mensaje_error)
    """
    required_keys = ["pruebas_metodo_legado", "lista_cambios", "pruebas_metodo_propuesto"]
    
    for key in required_keys:
        if key not in llm_context:
            return False, f"Falta clave requerida en contexto: '{key}'"
    
    # Validar tipos
    if not isinstance(llm_context["pruebas_metodo_legado"], list):
        return False, "'pruebas_metodo_legado' debe ser una lista"
    
    if not isinstance(llm_context["lista_cambios"], list):
        return False, "'lista_cambios' debe ser una lista"
    
    if not isinstance(llm_context["pruebas_metodo_propuesto"], list):
        return False, "'pruebas_metodo_propuesto' debe ser una lista"
    
    logger.info("Contexto validado exitosamente")
    return True, ""


def _validate_plan_completeness(
    plan: UnifiedInterventionPlan, 
    expected_legacy_count: int,
    expected_new_count: int
) -> tuple[bool, str]:
    """
    Verifica que el plan cubra todas las pruebas esperadas.
    
    Args:
        plan: Plan de intervención generado por el LLM
        expected_legacy_count: Número esperado de pruebas legadas
        expected_new_count: Número esperado de pruebas nuevas
        
    Returns:
        Tupla (es_completo, mensaje)
    """
    # Contar acciones por tipo
    legacy_actions = [
        a for a in plan.plan_intervencion 
        if a.prueba_ma_legado is not None
    ]
    new_actions = [
        a for a in plan.plan_intervencion 
        if a.accion == "adicionar"
    ]
    
    issues = []
    
    # Validar cobertura de pruebas legadas
    if len(legacy_actions) != expected_legacy_count:
        msg = (
            f"Cobertura incompleta de pruebas legadas: "
            f"esperadas {expected_legacy_count}, encontradas {len(legacy_actions)}"
        )
        issues.append(msg)
        logger.warning(msg)
    
    # Validar pruebas nuevas
    if len(new_actions) < expected_new_count:
        msg = (
            f"Faltan pruebas nuevas: "
            f"esperadas al menos {expected_new_count}, encontradas {len(new_actions)}"
        )
        issues.append(msg)
        logger.warning(msg)
    
    # Validar orden
    for i, action in enumerate(plan.plan_intervencion, 1):
        if action.orden != i:
            msg = f"Orden incorrecto: acción en posición {i} tiene orden={action.orden}"
            issues.append(msg)
            logger.warning(msg)
    
    if issues:
        return False, "; ".join(issues)
    
    logger.info(f"Plan completo: {len(legacy_actions)} acciones legadas, {len(new_actions)} nuevas")
    return True, "Plan validado correctamente"


# --- Función con retry para invocar LLM ---

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((json.JSONDecodeError, ValidationError)),
    reraise=True
)
def _invoke_llm_with_retry(llm_structured, human_prompt: str, system_prompt: str) -> UnifiedInterventionPlan:
    """
    Invoca el LLM con retry automático en caso de errores de parseo.
    
    Args:
        llm_structured: Modelo LLM configurado con structured output
        prompt: Prompt completo a enviar
        
    Returns:
        Plan de intervención validado
        
    Raises:
        ValidationError: Si el LLM no devuelve datos válidos después de 3 intentos
        json.JSONDecodeError: Si hay error de parseo JSON persistente
    """
    logger.debug("Invocando LLM para generar plan de intervención...")
    response = llm_structured.invoke([SystemMessage(content=system_prompt), HumanMessage(content=human_prompt)])
    logger.debug("LLM respondió exitosamente")
    return response


# --- Tool principal ---

# --- Constantes de rutas ---
LEGACY_METHOD_DEFAULT_PATH = "/actual_method/test_solution_structured_content.json"
CHANGE_CONTROL_DEFAULT_PATH = "/new/change_control_summary.json"
PROPOSED_METHOD_DEFAULT_PATH = "/proposed_method/test_solution_structured_content.json"

CHANGE_IMPLEMENTATION_PLAN_PATH = "/new/change_implementation_plan.json"



@tool(description=CHANGE_CONTROL_ANALYSIS_TOOL_DESCRIPTION)
def analyze_change_impact(
    state: Annotated[DeepAgentState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId],

    # Rutas por defecto
    proposed_method_path: str = PROPOSED_METHOD_DEFAULT_PATH,
    legacy_method_path: str = LEGACY_METHOD_DEFAULT_PATH,
    change_control_path: str = CHANGE_CONTROL_DEFAULT_PATH,
) -> Command:
    """
    Analiza el impacto de cambios y genera un plan de intervención detallado.
    
    Este tool:
    1. Carga y valida todos los archivos necesarios (rutas por defecto)
    2. Extrae y normaliza las pruebas de cada fuente
    3. Invoca un LLM para generar el plan de intervención
    4. Valida la completitud del plan
    5. Guarda el resultado en el filesystem virtual
    
    Args:
        state: Estado del grafo con el filesystem virtual
        tool_call_id: ID de la llamada al tool
        
    Returns:
        Command con el estado actualizado y mensaje de resultado
    """
    logger.info("=" * 80)
    logger.info("Iniciando 'analyze_change_impact'")
    logger.info("=" * 80)
    
    files = state.get("files", {}) or {}
    logger.info(f"Archivos disponibles: {len(files)}")
    
    # --- Paso 1: Cargar payloads ---
    logger.info("Cargando archivos necesarios...")
    
    cc_payload = _load_json_payload(files, change_control_path)
    proposed_payload = _load_json_payload(files, proposed_method_path)
    legacy_payload = _load_json_payload(files, legacy_method_path)
    
    # Validar archivos críticos
    if cc_payload is None:
        msg = f"ERROR: No se encontró el archivo de control de cambios en {change_control_path}."
        logger.error(msg)
        return Command(update={"messages": [ToolMessage(content=msg, tool_call_id=tool_call_id)]})
    
    if proposed_payload is None:
        msg = f"ERROR: No se encontró el método propuesto en {proposed_method_path}."
        logger.error(msg)
        return Command(update={"messages": [ToolMessage(content=msg, tool_call_id=tool_call_id)]})
    
    logger.info("✓ Control de cambios cargado")
    logger.info("✓ Método propuesto cargado")
    if legacy_payload: logger.info("✓ Método legado cargado")
    
    # --- Paso 2: Extraer lista de cambios del resumen ---
    logger.info("Extrayendo lista de cambios del resumen...")
    
    # El archivo change_control_summary.json tiene estructura:
    # {"filename": str, "summary": str, "lista_cambios": List[str]}
    raw_lista_cambios = cc_payload.get("lista_cambios", [])
    
    if not raw_lista_cambios:
        msg = "ERROR: No se encontró 'lista_cambios' en el archivo de control de cambios o está vacía."
        logger.error(msg)
        return Command(update={"messages": [ToolMessage(content=msg, tool_call_id=tool_call_id)]})
    
    logger.info(f"✓ Control de cambios cargado con {len(raw_lista_cambios)} cambios")
    
    # --- Paso 3: Extraer y normalizar datos ---
    logger.info("Extrayendo y normalizando datos...")
    
    # Método legado
    legacy_tests_raw = _extract_tests_from_legacy(legacy_payload)
    pruebas_metodo_legado = _collect_prueba_records_with_index(
        legacy_tests_raw, 
        source_id_key="section_id"
    )
    logger.info(f"  → Pruebas método legado: {len(pruebas_metodo_legado)}")
    
    # Lista de cambios - convertir strings a formato estructurado
    lista_cambios = _collect_cambios_from_strings(raw_lista_cambios)
    logger.info(f"  → Cambios identificados: {len(lista_cambios)}")
    
    # Método propuesto (de /proposed_method/test_solution_structured_content.json)
    proposed_tests_raw = _extract_tests_from_proposed(proposed_payload)
    pruebas_metodo_propuesto = _collect_prueba_records_with_index(
        proposed_tests_raw,
        source_id_key="_source_id"
    )
    logger.info(f"  → Pruebas método propuesto: {len(pruebas_metodo_propuesto)}")
    
    # --- Paso 4: Construir contexto unificado ---
    llm_context = {
        "pruebas_metodo_legado": pruebas_metodo_legado,
        "lista_cambios": lista_cambios,
        "pruebas_metodo_propuesto": pruebas_metodo_propuesto,
    }
    
    # Validar contexto
    is_valid, error_msg = _validate_context(llm_context)
    if not is_valid:
        msg = f"ERROR: Contexto inválido para LLM: {error_msg}"
        logger.error(msg)
        return Command(update={"messages": [ToolMessage(content=msg, tool_call_id=tool_call_id)]})
    
    context_json = json.dumps(llm_context, ensure_ascii=False, indent=2)
    logger.debug(f"Contexto unificado (primeros 500 chars): {context_json[:500]}...")
    
    # --- Paso 5: Invocar LLM ---
    logger.info("Invocando LLM para generar plan de intervención...")
    
    try:
        llm_structured = change_control_analysis_model.with_structured_output(UnifiedInterventionPlan)
        response = _invoke_llm_with_retry(
            llm_structured = llm_structured,
            human_prompt = UNIFIED_CHANGE_HUMAN_ANALYSIS_PROMPT.format(context=context_json),
            system_prompt = UNIFIED_CHANGE_SYSTEM_ANALYSIS_PROMPT
        )
        logger.info("✓ Plan de intervención generado exitosamente")
    except Exception as exc:
        msg = f"ERROR: Fallo al invocar LLM después de reintentos: {exc}"
        logger.exception(msg)
        return Command(update={"messages": [ToolMessage(content=msg, tool_call_id=tool_call_id)]})
    
    # --- Paso 6: Validar completitud del plan ---
    logger.info("Validando completitud del plan...")
    
    # Contar pruebas nuevas esperadas (las que no están en legado)
    legacy_test_names = {_normalize_name(p["prueba"]) for p in pruebas_metodo_legado}
    expected_new = sum(
        1 for c in lista_cambios 
        if c["prueba"] and _normalize_name(c["prueba"]) not in legacy_test_names
    )
    
    is_complete, validation_msg = _validate_plan_completeness(
        response,
        expected_legacy_count=len(pruebas_metodo_legado),
        expected_new_count=expected_new
    )
    
    if not is_complete:
        logger.warning(f"ADVERTENCIA: {validation_msg}")
        # Continuamos pero registramos la advertencia
    else:
        logger.info(f"✓ {validation_msg}")
    
    # --- Paso 7: Guardar resultado ---
    plan_payload = response.model_dump()
    
    files_update = dict(files)
    files_update[CHANGE_IMPLEMENTATION_PLAN_PATH] = {
        "content": json.dumps(plan_payload, ensure_ascii=False, indent=2),
        "data": plan_payload,
        "modified_at": datetime.now(timezone.utc).isoformat(),
    }
    
    logger.info(f"✓ Plan guardado en {CHANGE_IMPLEMENTATION_PLAN_PATH}")
    
    # --- Paso 8: Generar mensaje de resumen ---
    summary = response.resumen
    total_actions = len(response.plan_intervencion)
    
    acciones_count = {"editar": 0, "adicionar": 0, "eliminar": 0, "dejar igual": 0}
    for action in response.plan_intervencion:
        if action.accion in acciones_count:
            acciones_count[action.accion] += 1
    
    details = (
        f"Plan generado con {total_actions} acciones: "
        f"{acciones_count['editar']} a editar, "
        f"{acciones_count['adicionar']} a adicionar, "
        f"{acciones_count['eliminar']} a eliminar, "
        f"{acciones_count['dejar igual']} sin cambios."
    )
    
    tool_message = f"{summary}\n\n{details}".strip()
    
    if not is_complete:
        tool_message += f"\n\n⚠️ ADVERTENCIA: {validation_msg}"
    
    logger.info("=" * 80)
    logger.info("'analyze_change_impact' completado exitosamente")
    logger.info("=" * 80)
    
    return Command(
        update={
            "files": files_update,
            "messages": [ToolMessage(content=tool_message, tool_call_id=tool_call_id)],
        }
    )
