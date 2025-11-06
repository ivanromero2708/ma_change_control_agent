from pydantic import BaseModel, Field, model_validator
from typing import Literal, List, Optional
from uuid import uuid4

from pydantic_core.core_schema import str_schema

# =========================
# 2. ALCANCE DEL MÉTODO
# =========================

class ProductosAlcance(BaseModel):
    nombre_producto: str = Field(
        ...,
        description=(
            "Nombre exacto del producto tal como aparece en la tabla de ALCANCE o en el encabezado. "
            "Anclas: '2. ALCANCE', 'Ámbito de aplicación', 'Descripción'. "
            "Incluye la potencia si está pegada al nombre. "
            "Ej.: 'PROGESTERONA 100 mg'. No incluir códigos ni siglas."
        )
    )
    codigo_producto: str = Field(
        ...,
        description=(
            "Código del producto asociado al alcance. "
            "Anclas: en la tabla de ALCANCE o encabezado, columnas 'Código', 'Código Nuevo', 'Código de Producto'. "
            "Ej.: '400002641'. No incluir códigos antiguos ni otros identificadores."
        )
    )

class AlcanceMetodo(BaseModel):
    texto_alcance: str = Field(
        ...,
        description=(
            "Texto literal que describe cuándo aplica el método. "
            "Ancla: encabezado '2. ALCANCE' o equivalente. "
            "Capturar el párrafo completo hasta la tabla/listado. "
            "Ej.: 'Aplica cada vez que se vaya a realizar el control de calidad del producto terminado:'"
        )
    )
    lista_productos_alcance: List[ProductosAlcance] = Field(
        ...,
        description=(
            "Lista de productos del alcance tal como aparecen en la tabla o listado bajo 'ALCANCE'. "
            "Extraer cada fila (nombre y código). Ej.: [{'PROGESTERONA 100 mg','400002641'}]."
        )
    )

# =========================
# 6. EQUIPOS
# =========================

class Equipo(BaseModel):
    nombre: str = Field(
        ...,
        description=(
            "Nombre genérico del equipo (columna NOMBRE o texto en 'EQUIPOS'). "
            "Ej.: 'Balanza analítica', 'Cromatógrafo líquido', 'Desintegrador'. "
            "No incluir marca/modelo aquí."
        )
    )
    marca: str = Field(
        ...,
        description=(
            "Marca y/o modelo tal como aparece (columna MARCA). "
            "Ej.: 'Mettler Toledo XP205', 'Merck Lachrom Elite', 'Agilent 1100'. "
            "Si hay solo marca sin modelo, capturar la marca literal."
        )
    )

# =========================
# 7. DESARROLLO
# =========================

class Solucion(BaseModel):
    nombre_solucion: str = Field(
        ...,
        description=(
            "Encabezado literal tal como en el documento: 'Solución Stock Estándar', "
            "'Solución Estándar', 'Solución Stock Muestra', 'Solución Muestra', etc. "
            "No traducir, no normalizar, no inventar."
        )
    )
    preparacion_solucion: str = Field(
        ...,
        description=(
            "⚠️ COPIAR VERBATIM. Pegar el texto COMPLETO de la preparación exactamente como aparece, "
            "incluyendo saltos de línea, signos, mayúsculas/minúsculas, símbolos (µm, °C), paréntesis y notas. "
            "NO resumir, NO corregir ortografía, NO traducir, NO cambiar unidades. "
            "Límites de captura: desde la línea inmediatamente debajo del encabezado de la solución "
            "hasta ANTES del próximo encabezado de 'Solución ...', 'Procedimiento', 'Criterio de Aceptación' "
            "o siguiente subtítulo (p.ej., '7.x.y'). "
            "Ejemplo (fragmento): 'Transferir aproximadamente 25.0 mg... Pasar a vial por filtro jeringa PVDF 0.45 µm, "
            "descartando los primeros 2 mL del filtrado.'"
        )
    )

class CondicionCromatografica(BaseModel):
    nombre: str = Field(
        ...,
        description=(
            "Nombre de la condición cromatográfica específica. Por ejemplo: Columna, Detector, Volumen de inyección, entre otros."
        )
    )
    descripcion: str = Field(
        ...,
        description=(
            "⚠️ COPIAR VERBATIM de las condiciones cromatográficas especificas, tal como aparecen en el documento."
        )
    )

class Prueba(BaseModel):
    id_prueba: Optional[str] = Field(None)

    prueba: str = Field(
        ...,
        description=(
            "Nombre literal de la prueba sin el número '7.x', conservando etiquetas. "
        )
    )
    procedimientos: str = Field(
        ...,
        description=(
            "⚠️ COPIAR VERBATIM de los Procedimientos de la PRUEBA que se encuentran en la subsección 'Procedimientos'. Es una descripción detallada y exhaustiva del procedimiento de la prueba."
            "EXCLUIR todo bloque que comience por Solución ... (Stock Estándar/Estándar/Stock Muestra/Muestra) y EXCLUIR Condiciones Cromatográficas."
            "Mantén fórmulas de cálculo y la sección Dónde: ... si está pegada al procedimiento."
            "No incluyas numeraciones de subapartados (p. ej. '7.2.1', '7.5.1.2') salvo que estén dentro del propio bloque de Procedimiento."
        )
    )
    equipos: Optional[List[str]] = Field(
        ...,
        description=(
            "Equipos citados explícitamente en ESTA prueba, tal como aparecen. Ej.: "
            "['Espectrofotómetro UV', 'Cromatógrafo líquido', 'Aparato de desintegración']."
        )
    )
    condiciones_cromatograficas: Optional[List[CondicionCromatografica]] = Field(
        ...,
        description=(
            "Solo si aplica (HPLC/UPLC/GC). Incluir el bloque completo (verbatim) de condiciones tal cual aparece."
        )
    )
    reactivos: Optional[List[str]] = Field(
        ...,
        description=(
            "Reactivos mencionados dentro de ESTA prueba (además de los globales), copiados literal. Ej.: "
            "['Metanol HPLC', 'Acetonitrilo HPLC']."
        )
    )
    soluciones: Optional[List[Solucion]] = Field(
        ...,
        description=(
            "Cada 'Solución ...' usada en ESTA prueba, con su preparación copiada VERBATIM (ver 'preparacion_solucion')."
        )
    )
    criterio_aceptacion: Optional[str] = Field(
        ...,
        description=(
            "Texto literal bajo 'Criterio de Aceptación' de ESTA prueba (rangos, unidades, referencias). Copiar completo."
        )
    )

    # 2. El validador 'after'
    @model_validator(mode='after')
    def normalize_short_id(self) -> 'Prueba':
        """Asegura que cada prueba tenga un ID corto hexadecimal de 8 caracteres."""
        raw_id = (self.id_prueba or "").strip()
        candidate: Optional[str] = None

        if raw_id:
            normalized = raw_id.lower()

            if len(normalized) == 8 and all(ch in "0123456789abcdef" for ch in normalized):
                candidate = normalized
            else:
                hex_only = "".join(ch for ch in normalized if ch in "0123456789abcdef")
                if len(hex_only) >= 8:
                    candidate = hex_only[:8]

        if not candidate:
            candidate = uuid4().hex[:8]

        self.id_prueba = candidate
        return self

# =========================
# 8. ANEXOS
# =========================

class Anexo(BaseModel):
    numero: int = Field(
        ...,
        description=(
            "Número del anexo tal como aparece en la tabla/listado de ANEXOS. Ej.: 1, 2, 3."
        )
    )
    descripcion: str = Field(
        ...,
        description=(
            "Descripción literal del anexo. Ej.: 'Espectro UV de Valoración de Progesterona'."
        )
    )

# =========================
# 9. AUTORIZACIONES
# =========================

class Autorizacion(BaseModel):
    tipo_autorizacion: Literal["ELABORADO POR", "APROBADO POR", "REVISADO POR"] = Field(
        ...,
        description=(
            "Etiqueta de firma. Solo uno de: 'ELABORADO POR', 'REVISADO POR', 'APROBADO POR'. "
            "Capturar tal como aparece en la sección de firmas/autorizaciones."
        )
    )
    nombre: str = Field(
        ...,
        description=(
            "Nombre completo que aparece junto al tipo de autorización. Ej.: 'Luisa Beleño'."
        )
    )
    cargo: str = Field(
        ...,
        description=(
            "Cargo asociado al firmante. Ej.: 'Analista', 'Coordinador de Estandarizaciones y métodos', "
            "'Jefe de Laboratorio Fisicoquímico'."
        )
    )

# =========================
# 10. DOCUMENTOS SOPORTE
# =========================

class DocumentoSoporte(BaseModel):
    numero: int = Field(
        ...,
        description=(
            "Número secuencial del documento soporte tal como aparece en la tabla. Ej.: 1, 2, 3."
        )
    )
    fuente: str = Field(
        ...,
        description=(
            "Código/identificador del documento soporte (formato literal). "
            "Ej.: 'F-INST-0310-4', 'Método MG - 0036', 'USP'."
        )
    )
    descripcion: str = Field(
        ...,
        description=(
            "Descripción textual del documento. Ej.: 'Plantilla de Reporte Analítico para Laboratorio'."
        )
    )

# =========================
# 11. HISTÓRICO DE CAMBIOS
# =========================

class HistoricoCambio(BaseModel):
    codigo_cambio: str = Field(
        ...,
        description=(
            "Código del método en el histórico. Ancla: columna 'CÓDIGO'. Ej.: '01-3608'."
        )
    )
    version_cambio: str = Field(
        ...,
        description=(
            "Versión asociada a ese cambio. Ancla: 'VERSIÓN'. Ej.: '01', '00'."
        )
    )
    fecha_modificacion: str = Field(
        ...,
        description=(
            "Fecha exactamente como aparece (no normalizar formato). "
            "Ej.: '16-08-30', '15-01-14'."
        )
    )
    descripcion_cambio: str = Field(
        ...,
        description=(
            "Descripción textual completa del cambio, incluyendo referencias internas. "
            "Ej.: '... En la prueba de valoración se incluye método alterno por Espectrofotometría UV. CC-000000295'."
        )
    )

# =========================
# ESTADO DEL GRAFO / ENCABEZADO
# =========================

class ExtractionModel(BaseModel):
    # Encabezado del documento
    tipo_metodo: Literal[
        "MÉTODO DE ANÁLISIS DE PRODUCTO TERMINADO",
        "MÉTODO DE ANÁLISIS DE MATERIA PRIMA",
        "MÉTODO DE ANÁLISIS DE PROCESO"
    ] = Field(
        ...,
        description=(
            "Frase de tipo de método del encabezado o portada. "
            "Anclas: aparece en mayúsculas cerca del título. "
            "Seleccionar una de las 3 opciones (literal exacto)."
        )
    )
    nombre_producto: str = Field(
        ...,
        description=(
            "Nombre comercial/técnico del producto en el encabezado. "
            "Mantener potencia si viene unida. Ej.: 'PROGESTERONA 100 mg'. "
            "No incluir forma farmacéutica si no aparece en la misma línea."
        )
    )
    numero_metodo: str = Field(
        ...,
        description=(
            "Identificador del método. Anclas: 'Método No', 'CÓDIGO', 'MÉTODO', o tabla de histórico si se repite. "
            "Ej.: '01-3608'. Devolver tal cual (con guiones si existen)."
        )
    )
    version_metodo: str = Field(
        ...,
        description=(
            "Versión indicada en encabezado o portada. Anclas: 'Versión', 'V', 'VER'. "
            "Ej.: '01'. Solo el número/etiqueta literal."
        )
    )
    codigo_producto: str = Field(
        ...,
        description=(
            "Código del producto del encabezado o tabla de alcance (columna 'Código'/'Código Nuevo'). "
            "Ej.: '400002641'. Evitar códigos antiguos ('GR...') salvo que el documento solo muestre ese."
        )
    )
    # 1. Contenido del método analítico
    objetivo: str = Field(
        ...,
        description=(
            "Párrafo completo bajo '1. OBJETIVO' o equivalente. "
            "Ej.: 'Proporcionar la información necesaria para la realización de los análisis...'. "
            "Capturar todo el texto hasta el siguiente encabezado numerado."
        )
    )
    # 2. Alcance
    alcance_metodo: AlcanceMetodo = Field(
        ...,
        description=(
            "Sección 2. ALCANCE con texto y tabla/lista de productos. "
            "Ver campos internos para formato exacto."
        )
    )
    # 3. Definiciones
    definiciones: List[str] = Field(
        ...,
        description=(
            "Lista de siglas/definiciones bajo '3. DEFINICIONES' o '3.1 Siglas'. "
            "Ej.: 'UPLC: Cromatógrafo líquido de ultra resolución'; 'GR: Grado reactivo'. "
            "Una entrada por línea/viñeta."
        )
    )
    # 4. Seguridad
    recomendaciones_seguridad: List[str] = Field(
        ...,
        description=(
            "Viñetas completas bajo 'RECOMENDACIONES CLAVES, PRECAUCIONES Y ADVERTENCIAS' o equivalente. "
            "Incluir referencias SOP y acciones ('Revisar SOP-0547', 'Disponer residuos SOP-0584'). "
            "Una viñeta por entrada, sin resumir."
        )
    )
    # 5. Materiales y reactivos (global)
    materiales: List[str] = Field(
        ...,
        description=(
            "Listado literal de 'MATERIALES Y REACTIVOS' globales (no específicos de una prueba). "
            "Ej.: 'Probetas de 100 mL y 1,000 mL', 'Papel filtro Whatman 541', 'Metanol HPLC', 'Acetonitrilo HPLC'. "
            "Una línea/viñeta por entrada."
        )
    )
    # 6. Equipos (global)
    equipos: List[Equipo] = Field(
        ...,
        description=(
            "Tabla/lista de 'EQUIPOS' con (nombre, marca/modelo). "
            "Ej.: ('Cromatógrafo líquido','Agilent 1100')."
        )
    )
    # 7. Desarrollo (pruebas)
    pruebas: List[Prueba] = Field(
        ...,
        description=(
            "Una entrada por cada prueba '7.x'. Si hay variantes (HPLC vs UV), crear entradas separadas. "
            "Incluir procedimientos, soluciones, condiciones cromatográficas (si aplica) y criterio de aceptación literal."
        )
    )
    # 8. Anexos
    anexos: List[Anexo] = Field(
        ...,
        description=(
            "Tabla/listado de ANEXOS: (número, descripción) tal cual."
        )
    )
    # 9. Autorizaciones
    autorizaciones: List[Autorizacion] = Field(
        ...,
        description=(
            "Bloque de firmas ELABORADO/REVISADO/APROBADO: nombre y cargo por cada uno."
        )
    )
    # 10. Documentos soporte
    documentos_soporte: List[DocumentoSoporte] = Field(
        ...,
        description=(
            "Tabla de documentos: (número, fuente, descripción) tal como aparece."
        )
    )
    # 11. Histórico de cambios
    historico_cambios: List[HistoricoCambio] = Field(
        ...,
        description=(
            "Tabla de cambios: (código, versión, fecha, descripción) con textos literales completos."
        )
    )
