import logging

from pydantic import BaseModel, Field
from typing import Annotated, Dict, List, Literal, Optional, Type, Union, Any

from langgraph.types import Command
from langchain_core.tools import InjectedToolCallId, tool
from langchain_core.messages import ToolMessage, HumanMessage
from langgraph.prebuilt import InjectedState
from langchain.chat_models import init_chat_model

from uuid import UUID
import os
import tempfile
import shutil
from pathlib import Path
from docx2pdf import convert as docx_to_pdf_convert
from PyPDF2 import PdfReader, PdfWriter
from mistralai import Mistral
from mistralai.extra import response_format_from_pydantic_model
import time
import base64
import json
from contextlib import contextmanager

from src.prompts.tool_prompts import *
from src.models import *
from src.graph.state import DeepAgentState

logger = logging.getLogger(__name__)

# LLMs

summarization_model = init_chat_model(model="openai:gpt-4.1-mini")

# Diccionarios de trabajo

extraction_models = {
    "legacy_method": ExtractionModel,
    "change_control": ChangeControlModel,
    "annex_documents": ExtractionModel
}

filenames = {
    "legacy_method": "/legacy/legacy_method.json",
    "change_control": "/legacy/change_control.json",
    "annex_documents": "/legacy/annex_documents.json"
}

# Modelos de datos requeridos

class Summary(BaseModel):
    """Schema for webpage content summarization."""
    filename: str = Field(description="Nombre del archivo a almacenar.")
    summary: str = Field(description="Resumen en lenguaje natural del documento.")
    lista_pruebas: List[str] = Field(description="Lista de identificadores cortos (8 caracteres hex) de todas las 'pruebas' encontradas.")

# Funciones de utilidad

## PDF preparation
@contextmanager
def _prepare_pdf_document(document_path: str):
    """Ensure the provided document is available as a PDF, converting DOCX files on the fly."""
    if not document_path:
        raise ValueError("No se proporcionó la ruta del documento a procesar.")

    resolved_path = Path(document_path)
    if not resolved_path.exists():
        raise FileNotFoundError(f"El documento {document_path} no existe.")

    suffix = resolved_path.suffix.lower()
    if suffix == ".pdf":
        yield str(resolved_path)
        return

    if suffix == ".docx":
        temp_dir = tempfile.mkdtemp(prefix="doc_annotation_")
        pdf_output_path = os.path.join(temp_dir, resolved_path.with_suffix(".pdf").name)
        try:
            try:
                from docx2pdf import convert as docx_to_pdf_convert
            except ImportError as exc:
                raise ImportError("La librería docx2pdf es requerida para convertir archivos DOCX a PDF.") from exc

            logger.info(f"Convirtiendo DOCX a PDF: {document_path}")
            docx_to_pdf_convert(str(resolved_path), pdf_output_path)

            if not os.path.exists(pdf_output_path):
                raise RuntimeError(f"No se generó el archivo PDF convertido para {document_path}.")

            yield pdf_output_path
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
        return

    raise ValueError(f"Formato de archivo no soportado para {document_path}. Solo se permiten PDF o DOCX.")

## Document Annotation
def get_pdf_page_count(pdf_path: str) -> int:
    """Get the number of pages in a PDF."""
    try:
        with open(pdf_path, "rb") as pdf_file:
            reader = PdfReader(pdf_file)
            return len(reader.pages)
    except Exception as e:
        logger.error(f"Error counting pages in {pdf_path}: {e}")
        return 0

def split_pdf_into_chunks(pdf_path: str, max_pages_per_chunk: int = 8, chunk_overlap_pages: int = 2) -> list[str]:
    """Split PDF into chunks of pages with overlap and temporary files."""
    chunk_files: list[str] = []
    try:
        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)
        if total_pages == 0:
            return []

        overlap = max(chunk_overlap_pages, 0)
        chunk_size = max(max_pages_per_chunk, 1)
        step = max(chunk_size - overlap, 1)

        for start in range(0, total_pages, step):
            end = min(start + chunk_size, total_pages)
            chunk_writer = PdfWriter()
            for page_idx in range(start, end):
                chunk_writer.add_page(reader.pages[page_idx])

            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as chunk_pdf:
                chunk_writer.write(chunk_pdf)
                chunk_files.append(chunk_pdf.name)

        return chunk_files
    except Exception as e:  # pragma: no cover - defensive
        logger.error(f"Error splitting PDF into chunks: {e}")
        for chunk_file in chunk_files:
            try:
                os.unlink(chunk_file)
            except OSError:
                pass
        return []

def encode_pdf(pdf_path: str) -> str:
    """Encode the pdf to base64."""
    try:
        with open(pdf_path, "rb") as pdf_file:
            return base64.b64encode(pdf_file.read()).decode('utf-8')
    except Exception as e:
        logger.error(f"Error encoding PDF {pdf_path}: {e}")
        return None

def process_chunk(pdf_path: str, extraction_model: Type[BaseModel], chunk_retry_backoff_seconds: int = 5, chunk_retry_attempts: int = 3):
    """Process a single PDF chunk with Mistral OCR."""
    base64_pdf = encode_pdf(pdf_path)
    if not base64_pdf:
        return None
    
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise EnvironmentError("Defina MISTRAL_API_KEY en el entorno o en el archivo .env")
    ocr_client = Mistral(api_key=api_key, timeout_ms=300000)

    request_params = {
        "model": "mistral-ocr-latest",
        "document": {
            "type": "document_url",
            "document_url": f"data:application/pdf;base64,{base64_pdf}"
        },
        "include_image_base64": False,
    }

    if extraction_model:
        try:
            request_params["document_annotation_format"] = response_format_from_pydantic_model(extraction_model)
        except Exception as exc:
            logger.warning(f"No se pudo generar schema pydantic para {pdf_path}: {exc}")

    last_exception: Optional[Exception] = None
    total_attempts = max(chunk_retry_attempts, 1)

    for attempt in range(1, total_attempts + 1):
        try:
            return ocr_client.ocr.process(**request_params)
        except Exception as exc:
            last_exception = exc
            if attempt >= total_attempts:
                break
            wait_seconds = chunk_retry_backoff_seconds * attempt
            logger.warning(
                f"Retrying chunk {pdf_path} after error: {exc}. Intento {attempt}/{chunk_retry_attempts} en {wait_seconds}s"
            )
            time.sleep(wait_seconds)

    logger.error(f"Error processing chunk {pdf_path}: {last_exception}")
    return None

def process_document(
    pdf_path: str,
    extraction_model: Type[BaseModel],
    max_pages_per_chunk: int = 8,
    chunk_overlap_pages: int = 2,
) -> list:
    """Process PDF with automatic chunking if needed."""
    total_pages = get_pdf_page_count(pdf_path)
    logger.info(f"Processing PDF {pdf_path} with {total_pages} pages")
    if total_pages == 0:
        logger.error(f"Skipping {pdf_path}: could not read any pages")
        return []
    
    if total_pages <= max_pages_per_chunk:
        # Process directly if within limit
        result = process_chunk(pdf_path, extraction_model, chunk_retry_backoff_seconds=5, chunk_retry_attempts=3)
        return [result] if result else []
    
    # Split into chunks and process each
    chunk_files = split_pdf_into_chunks(
        pdf_path,
        max_pages_per_chunk=max_pages_per_chunk,
        chunk_overlap_pages=chunk_overlap_pages,
    )
    results = []
    
    try:
        for i, chunk_file in enumerate(chunk_files):
            logger.info(f"Processing chunk {i+1}/{len(chunk_files)}")
            result = process_chunk(chunk_file, extraction_model, chunk_retry_backoff_seconds=5, chunk_retry_attempts=3)
            if result:
                results.append(result)
    finally:
        # Clean up temporary files
        for chunk_file in chunk_files:
            try:
                os.unlink(chunk_file)
            except Exception as e:
                logger.warning(f"Could not delete temporary file {chunk_file}: {e}")
    
    return results

def _merge_list_items(target_list: list, source_list: list):
    """Mergea listas cuidando duplicados y combinando elementos dict similares."""
    for item in source_list:
        if item in (None, [], {}, ""):
            continue

        if isinstance(item, dict):
            existing = next((t for t in target_list if isinstance(t, dict) and t == item), None)
            if existing is not None:
                _merge_chunk_data(existing, item)
                continue

        if item not in target_list:
            target_list.append(item)

def _merge_chunk_data(target: dict, source: dict):
    """Mergea datos de un chunk con el diccionario consolidado."""
    for key, value in source.items():
        if value in (None, [], {}, ""):
            continue

        if key not in target or target[key] in (None, [], {}):
            target[key] = value
            continue

        target_value = target[key]

        if isinstance(target_value, list) and isinstance(value, list):
            _merge_list_items(target_value, value)
        elif isinstance(target_value, dict) and isinstance(value, dict):
            _merge_chunk_data(target_value, value)
        elif isinstance(target_value, str) and isinstance(value, str):
            # Prefer the longer text to keep additional context
            if len(value.strip()) > len(target_value.strip()):
                target[key] = value
        else:
            target[key] = value

def consolidate_chunks_data(chunk_responses: list, document_name: str, extraction_model: type[BaseModel]):
    """Consolida los document_annotation de todos los chunks y crea una instancia del modelo Pydantic."""
    try:
        if not chunk_responses:
            logger.warning(f"No chunks to process for {document_name}")
            return None
        
        # Consolidar todos los datos de los chunks
        all_chunk_data = {}
        
        for i, response in enumerate(chunk_responses):
            if not response:
                continue
                
            # Extraer document_annotation del chunk
            annotation_data = None
            if hasattr(response, 'document_annotation'):
                annotation_data = response.document_annotation
            elif isinstance(response, dict) and 'document_annotation' in response:
                annotation_data = response['document_annotation']
            
            if annotation_data:
                try:
                    # Convertir a dict si es necesario
                    if isinstance(annotation_data, str):
                        chunk_data = json.loads(annotation_data)
                    elif isinstance(annotation_data, dict):
                        chunk_data = annotation_data
                    else:
                        chunk_data = json.loads(str(annotation_data))
                    
                    # Mergear datos del chunk con el consolidado
                    _merge_chunk_data(all_chunk_data, chunk_data)
                    logger.debug(f"Merged chunk {i+1} data")
                    
                except (json.JSONDecodeError, TypeError) as e:
                    logger.warning(f"Error parsing chunk {i+1} annotation: {e}")
        
        # Crear instancia del modelo Pydantic con los datos consolidados
        if all_chunk_data and extraction_model:
            try:
                model_instance = extraction_model(**all_chunk_data)
                logger.info(f"Created {extraction_model.__name__} instance for {document_name}")
                return model_instance
            except Exception as e:
                logger.error(f"Error creating model instance for {document_name}: {e}")
                # Fallback: retornar los datos raw
                return all_chunk_data
        
        logger.warning(f"No valid data to create model instance for {document_name}")
        return None
        
    except Exception as e:
        logger.error(f"Error consolidating chunks for {document_name}: {e}")
        return None

def _get_summary_object(model_instance: Union[BaseModel, Dict[str, Any], None]) -> Summary:
    """Get the summary text from the model instance or raw dict."""
    
    # ... (Lógica para obtener 'extracted_content' sin cambios) ...
    if isinstance(model_instance, BaseModel):
        extracted_content: Dict[str, Any] = model_instance.model_dump()
    elif isinstance(model_instance, dict):
        extracted_content = model_instance
    elif model_instance is None:
        extracted_content = {}
    else:
        extracted_content = json.loads(str(model_instance)) if isinstance(model_instance, str) else {"data": model_instance}

    # --- INICIO: SECCIÓN MODIFICADA (Lógica de extracción determinística) ---
    # Ahora es mucho más simple. Confiamos en el validador del modelo.
    correct_uuid_list = []
    if extracted_content and 'pruebas' in extracted_content and isinstance(extracted_content.get('pruebas'), list):
        for prueba in extracted_content['pruebas']:
            # El validador GARANTIZA que 'id_prueba' existe y es un string UUID
            if isinstance(prueba, dict) and 'id_prueba' in prueba and isinstance(prueba.get('id_prueba'), str):
                correct_uuid_list.append(prueba['id_prueba']) 
            else:
                # Este log ya no debería aparecer, pero es buena defensa
                logger.warning(f"Se encontró una 'prueba' sin 'id_prueba' (string) válido después de la validación.")
    # --- FIN: SECCIÓN MODIFICADA ---

    try:
        if not extracted_content:
            raise ValueError("No se extrajeron datos del documento.")

        metadata_for_summary = {
            "tipo_metodo": extracted_content.get("tipo_metodo"),
            "nombre_producto": extracted_content.get("nombre_producto"),
            "total_pruebas": len(correct_uuid_list),
        }

        structured_model = summarization_model.with_structured_output(Summary)

        summary_and_filename = structured_model.invoke([
            HumanMessage(
                content=SUMMARIZE_EXTRACTED_LEGACY_METHOD.format(
                    metadata_content=json.dumps(metadata_for_summary, ensure_ascii=False, indent=2)
                )
            )
        ])

        # Sobrescribe con la lista de STRINGS (esto ya no dará error de JSON)
        summary_and_filename.lista_pruebas = correct_uuid_list

        return summary_and_filename

    except Exception as exc: 
        logger.warning("Fallo al generar resumen estructurado: %s", exc)
        serialized = json.dumps(extracted_content, ensure_ascii=False, default=str)
        return Summary(
            filename="No se extrajeron datos del documento.json",
            summary=serialized[:1000] + "..." if len(serialized) > 1000 else serialized,
            lista_pruebas=correct_uuid_list  # Usa la lista de STRINGS
        )

def _model_instance_to_dict(model_instance: Union[BaseModel, Dict[str, Any], None]) -> Dict[str, Any]:
    """Serialize the consolidated model output so it can be stored as JSON."""
    if model_instance is None:
        return {}

    if isinstance(model_instance, BaseModel):
        return model_instance.model_dump()

    if isinstance(model_instance, dict):
        return model_instance

    if isinstance(model_instance, str):
        try:
            return json.loads(model_instance)
        except json.JSONDecodeError:  # pragma: no cover - defensive
            return {"data": model_instance}

    return {"data": json.loads(str(model_instance)) if isinstance(model_instance, str) else str(model_instance)}


@tool(description=EXTRACT_LEGACY_SECTIONS_PROMPT_TOOL_DESC)
def extract_legacy_sections(
    dir_legacy_method: str,
    extract_model: Literal["legacy_method", "change_control", "annex_documents"],
    state: Annotated[DeepAgentState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> Command:
    # Filename
    document_name = filenames[extract_model]

    # Extraction Model
    extraction_model = extraction_models[extract_model]

    # Document Processing
    try:
        with _prepare_pdf_document(dir_legacy_method) as pdf_document_path:
            chunk_responses = process_document(pdf_path=pdf_document_path, extraction_model=extraction_model, max_pages_per_chunk=8)
    except Exception as exc:
        logger.error(f"Error procesando el documento {document_name}: {exc}")
        raise

    # Consolidate Chunks
    model_instance = consolidate_chunks_data(chunk_responses, document_name, extraction_model)

    logger.info(f"Completed processing {document_name}")
    
    # 1. Llama a la nueva función que devuelve el objeto Summary
    summary_object = _get_summary_object(model_instance)

    # 2. Prepara el estado 'files'
    files = state.get("files", {})
    
    # 3. Guarda el JSON gigante en formato estructurado y string para herramientas de lectura
    if model_instance:
        serialized_data = _model_instance_to_dict(model_instance)
        full_json_string = json.dumps(serialized_data, indent=2, ensure_ascii=False)
        files[document_name] = {
            "content": full_json_string,
            "data": serialized_data,
        }
    else:
        files[document_name] = {
            "content": "{}",
            "data": {},
        }  # Guarda un JSON vacío si falla

    # 4. Guarda el archivo de resumen y pruebas (en el formato que 'read_file' espera)
    # Serializa el objeto Summary a un string JSON
    summary_serialized = summary_object.model_dump()
    summary_json_string = json.dumps(summary_serialized, indent=2, ensure_ascii=False)
    # Guarda el string DENTRO de la clave 'content' y la versión estructurada
    files["/legacy/summary_and_tests.json"] = {
        "content": summary_json_string,
        "data": summary_serialized,
    }

    # --- (FIN DE LA SECCIÓN MODIFICADA) ---

    return Command(
        update={
            "files": files, # Esto ahora guarda AMBOS archivos en el estado
            "messages": [
                # Devuelve solo el resumen legible por humanos al LLM
                ToolMessage(summary_object.summary, tool_call_id=tool_call_id)
            ],
        }
    )
