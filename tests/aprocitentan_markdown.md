# Desarrollo de Producto Genérico de Aprocitentan 12,5 mg: Análisis Técnico-Farmacéutico Integral

**Resumen Ejecutivo**

Aprocitentan (ACT-132577) representa el primer antagonista dual de receptores de endotelina aprobado específicamente para hipertensión resistente en casi 40 años, con Tryvio® (Idorsia Ltd.) como producto de referencia. Este informe técnico proporciona al equipo de I&D la base científica necesaria para iniciar el desarrollo de una formulación genérica, integrando aspectos de polimorfismo, síntesis, formulación, manufactura y contexto de propiedad intelectual. La Forma A cristalina patentada hasta 2038 constituye el principal desafío técnico, aunque existen estrategias viables de diseño alternativo basadas en formas cristalinas no protegidas o formulaciones amorfas estabilizadas.

---

## 1. Introducción: Perfil farmacológico y relevancia clínica

Aprocitentan es un antagonista dual de receptores de endotelina (ETA/ETB) con fórmula molecular C₁₆H₁₄Br₂N₆O₄S y peso molecular de **546,2 g/mol** (DrugBank, 2024). Funciona como metabolito activo de macitentan (por N-despropiloxi-dación oxidativa) y fue aprobado por FDA el **19 de marzo de 2024** como Tryvio® y por EMA el **27 de junio de 2024** como Jeraygo™ (U.S. FDA, 2024; EMA, 2024).

El estudio pivotal **PRECISION** (NCT03541174) demostró una reducción adicional de **-3,8 mmHg en presión arterial sistólica** versus placebo en pacientes con hipertensión resistente no controlada con ≥3 antihipertensivos (Schlaich et al., 2022). La administración es de **12,5 mg una vez al día** (solo esta dosis aprobada en EE.UU.; en Europa también 25 mg).

Las principales características farmacocinéticas incluyen (Danaietash et al., 2022):
- **Tmax**: 4-5 horas
- **Vida media efectiva**: ~41-46 horas (permite dosificación única diaria)
- **Unión a proteínas**: >99% (principalmente albúmina)
- **Metabolismo**: Glucosidación vía UGT1A1/UGT2B7 e hidrólisis no enzimática
- **Estado estacionario**: Alcanzado al día 8 con ~3 veces de acumulación

---

## 2. Metodología de búsqueda

La investigación se realizó consultando fuentes primarias de patentes, información regulatoria y literatura científica:

**Bases de patentes**: WIPO PatentScope (WO2018/154101, WO2009/024906, WO2021/088645), USPTO (US10,919,881, US8,324,232), Google Patents, Espacenet

**Información regulatoria**: FDA Drugs@FDA (NDA 217686), FDA Orange Book, DailyMed, EMA EPAR (EMEA/H/C/006080)

**Fuentes técnicas**: DrugBank (DB15059), PubChem (CID 25099191), Cambridge Crystallographic Data Centre (estructura cristalina), documentos SmPC/Prescribing Information

**Jurisdicciones LATAM**: Referencias de INPI Brasil, IMPI México, SIC Colombia (verificación directa recomendada)

---

## 3. Síntesis del API y control de impurezas

### 3.1 Ruta sintética general

La patente principal de síntesis **US8,324,232** (WO2009/024906, prioridad agosto 2007) describe una ruta convergente de **8 etapas** partiendo de **ácido 4-bromofenilacético** como materia prima comercial (Actelion Pharmaceuticals Ltd., 2009).

**Secuencia de transformaciones clave**:

| Etapa | Transformación | Intermediario clave |
|-------|----------------|---------------------|
| 1 | Esterificación | 4-bromofenilacetato de metilo |
| 2 | α-Carboxilación (malonilación) | 2-(4-bromofenil)-malonato de dimetilo |
| 3 | Ciclación con formamidina | 5-(4-bromofenil)-pirimidina-4,6-diol |
| 4 | Cloración (POCl₃) | 5-(4-bromofenil)-4,6-dicloro-pirimidina |
| 5 | Introducción de bencilsulfamida | Intermedio sulfamida protegida |
| 6 | Eterificación con etilenglicol | Intermedio hidroxietil éter |
| 7 | Acoplamiento con 2-cloro-5-bromo-pirimidina | Precursor protegido |
| 8 | Desprotección (BBr₃ o BCl₃) | **APROCITENTAN** |

Las condiciones de reacción involucran el uso de bases fuertes (NaH, t-BuOK), solventes apróticos (THF, DMF, DMSO) y temperaturas moderadas (60-100°C). La desprotección final del grupo bencilo requiere tribromuro de boro en condiciones anhidras.

### 3.2 Impurezas de síntesis identificadas

Las impurezas relacionadas con el proceso de síntesis se clasifican en:

**Materiales de partida residuales**: Ácido 4-bromofenilacético, 2-cloro-5-bromopirimidina

**Intermediarios incompletos**: Productos de reacciones parciales de cualquier etapa, particularmente derivados mono-clorados y productos de sustitución incompleta

**Impurezas estructuralmente relacionadas**:
- Macitentan (compuesto padre N-propiloxi)
- Análogos N-alquilados de la sulfamida
- Derivados mono-bromados
- Isómeros posicionales de sustitución

**Subproductos de reacción**: Dímeros, productos de O-alquilación versus N-alquilación, productos de hidrólisis del grupo sulfamida

### 3.3 Productos de degradación

Las vías de degradación principales del API incluyen:

**Hidrólisis**: Susceptibilidad del enlace éter alifático (C-O-C) entre fragmentos pirimidínicos y del grupo sulfamida bajo condiciones extremas de pH. Tiempo de vida media de ~2 horas a pH 1,2 indica sensibilidad significativa en medio ácido (U.S. FDA, 2024).

**Oxidación**: El azufre del grupo sulfamida puede oxidarse a sulfona. La cadena etilénica es susceptible a formación de hidroperóxidos en presencia de oxígeno, peróxidos o catálisis por metales de transición.

**Fotodegradación**: Los anillos aromáticos dibromados absorben radiación UV, generando ruptura homolítica del enlace C-Br y productos debromados o de acoplamiento radical.

**Degradación térmica**: Descomposición a ~167°C (evento exotérmico DSC) con degradación del grupo sulfamida.

---

## 4. Polimorfismo del API: Forma A y alternativas

### 4.1 Panorama de formas cristalinas

La patente **WO2018/154101** (US10,919,881, prioridad febrero 2017, expira **febrero 2038**) describe múltiples formas polimórficas de aprocitentan (Idorsia Pharmaceuticals Ltd., 2018, 2021):

| Forma | Tipo | Solvato | Estabilidad | Uso comercial |
|-------|------|---------|-------------|---------------|
| **A** | Libre | No | Alta (termodinámica) | **Forma comercial** |
| B | Solvato | DCM | Inestable | No |
| C | Libre | No | Alternativa | No |
| D | Libre | No | Alternativa | No |
| E | Solvato | Acetonitrilo | Inestable | No |
| J | Libre | No | Alternativa | No |
| K | Solvato | DMSO | Inestable | No |
| L | Solvato | Etanol | Inestable | No |
| **CSI** | Libre | No | Superior a A bajo estrés | Competidor (China) |
| Amorfa | - | - | Variable | Potencial genérico |

### 4.2 Caracterización de Forma A (forma comercial)

**Estructura cristalina** (Idorsia Pharmaceuticals Ltd., 2021):
- Sistema: Triclínico primitivo
- Grupo espacial: P-1
- Parámetros de celda: a=11,74 Å, b=10,68 Å, c=9,67 Å; α=110,5°, β=92,3°, γ=113,5°
- Volumen: 1.019 Å³ (Z=2)

**Patrón XRPD característico** (picos principales 2θ, Cu Kα):
- **17,8° (100%)** - pico más intenso
- **23,5° (83%)**
- **20,0° (67%)**
- 19,9° (54%), 18,6° (50%), 23,2° (49%)

**Propiedades térmicas (DSC/TGA)**:
- Punto de fusión: ~161°C (endoterma)
- Descomposición: ~167°C (exoterma)
- Pérdida de masa hasta 140°C: 0,1% (confirma forma no solvatada)

**Limitaciones documentadas**: La patente china WO2021/088645 (Crystal Pharmaceutical Suzhou) reporta que la Forma A presenta **mala estabilidad mecánica** y puede convertirse en amorfa tras molienda intensa, lo cual representa una vulnerabilidad para el proceso de manufactura (Crystal Pharmaceutical Co., 2021).

### 4.3 Preparación de Forma A

El procedimiento de cristalización descrito involucra disolución de aprocitentan crudo en solvente orgánico con control de pH (8,0-8,5), cristalización controlada que puede generar inicialmente mezcla de Forma A + Forma K (solvato DMSO), seguida de conversión/purificación para obtener Forma A pura.

Los solventes utilizados incluyen DCM, acetato de etilo, acetonitrilo, etanol, metanol, MEK, MIBK, DMSO y THF. El control del polimorfismo es crítico porque el proceso puede generar mezclas polimórficas no deseadas (Hilfiker & von Raumer, 2018).

### 4.4 Forma CSI como alternativa (WO2021/088645)

Crystal Pharmaceutical (Suzhou) Co. ha desarrollado una forma cristalina alternativa denominada **CSI** que presenta (Crystal Pharmaceutical Co., 2021):
- Picos XRPD característicos en 8,9°, 12,7°, 17,5° (2θ)
- **Mayor estabilidad que Forma A** bajo condiciones de 60°C/75%HR
- Mejor resistencia a la molienda

Esta forma representa una **oportunidad potencial de licenciamiento** para evitar la patente de polimorfismo de Idorsia.

---

## 5. Formulación de tabletas recubiertas

### 5.1 Clasificación biofarmacéutica y propiedades fisicoquímicas

Aprocitentan se clasifica como **BCS Clase II (baja solubilidad, alta permeabilidad)** según el Sistema de Clasificación Biofarmacéutica (Amidon et al., 1995; DrugBank, 2024):

| Propiedad | Valor | Implicación |
|-----------|-------|-------------|
| Solubilidad en agua | **Insoluble** (<10 µg/mL a pH ácido) | Requiere estrategias de disolución |
| Permeabilidad | Alta (sustrato P-gp, BCRP) | Absorción adecuada |
| Unión proteica | >99% (albúmina) | Distribución predecible |
| pKa del grupo sulfamida | ~10 | No ionizado a pH fisiológico |
| LogP | Alto (estructura dibromada lipofílica) | Consistente con BCS II |

La alta permeabilidad permite que la formulación convencional con superdesintegrante sea viable a pesar de la baja solubilidad (Prasad et al., 2018).

### 5.2 Composición cualitativa de Tryvio® 12,5 mg

**Núcleo de tableta** (U.S. FDA, 2024; DailyMed, 2024):

| Excipiente | Función | Grado típico |
|------------|---------|--------------|
| Celulosa microcristalina | Diluyente/Aglutinante | Avicel PH-102 |
| Lactosa monohidrato | Diluyente | 54 mg por tableta |
| Croscarmelosa sódica | Superdesintegrante | NF |
| Hidroxipropilcelulosa (HPC) | Aglutinante (granulación) | Grado LF/EF |
| Estearato de magnesio | Lubricante | Vegetal NF |

**Recubrimiento pelicular** (tipo Opadry® II):

| Componente | Función |
|------------|---------|
| Alcohol polivinílico (PVA) | Formador de película |
| Hidroxipropilcelulosa | Co-formador |
| Citrato de trietilo | Plastificante |
| Talco | Antiadherente |
| Sílice coloidal hidratada | Deslizante |
| Dióxido de titanio | Opacificante |
| Óxidos de hierro (rojo, amarillo, negro) | Colorantes |

**Descripción de tabletas**: Amarilla a naranja, redonda biconvexa, 6 mm diámetro, grabado "AN" en una cara.

### 5.3 Sistema de liberación inmediata

La formulación es de **liberación inmediata** convencional. El Tmax de 4-5 horas y la vida media de ~46 horas permiten administración una vez al día sin necesidad de liberación modificada (Schlaich et al., 2022).

**Método de disolución** (condiciones estimadas según FDA guidance):
- Aparato: Paletas USP, 50 rpm
- Medio: Buffer fosfato pH 6,8 con CTAB 0,05% y Polisorbato 20 0,5% (surfactantes necesarios por baja solubilidad)
- Volumen: 900 mL, 37°C
- Criterio: Q ≥80% en 30 minutos

### 5.4 Estabilidad y almacenamiento

**Condiciones críticas** (U.S. FDA, 2024):
- Vida útil: **30 meses**
- Almacenamiento: Sin requisitos especiales de temperatura (<30°C)
- **Protección de humedad: CRÍTICA** - requiere frasco HDPE con desecante o blíster aluminio/aluminio con desecante integrado

La sensibilidad a la humedad dicta que el sistema de cierre primario debe proporcionar barrera efectiva contra humedad ambiental (Healy et al., 2017).

---

## 6. Proceso de manufactura de tabletas

### 6.1 Tecnología seleccionada: Granulación húmeda

El EPAR de EMA confirma que el proceso de manufactura de Jeraygo™/Tryvio® utiliza **granulación húmeda** con HPC como aglutinante en solución acuosa (EMA, 2024). Esta tecnología se seleccionó sobre compresión directa para mejorar flujo, compactabilidad y uniformidad de contenido del API de baja dosis (Parikh, 2016; Litster & Ennis, 2004).

**Flujo de proceso (9 operaciones unitarias)**:

```
1. Mezclado inicial → 2. Granulación húmeda → 3. Secado (FBD) → 
4. Molienda/Tamizado → 5. Mezclado final → 6. Lubricación → 
7. Compresión → 8. Recubrimiento pelicular → 9. Empaque
```

### 6.2 Parámetros críticos de proceso (CPPs)

| Operación | Parámetro | Rango conceptual | CQA impactado |
|-----------|-----------|------------------|---------------|
| **Granulación** | Cantidad de agua | Según LOD target | Dureza, disolución |
| **Granulación** | Tiempo de amasado | 5-15 min | Densidad granulado |
| **Secado** | Temperatura entrada | 50-70°C | LOD final |
| **Secado** | Temperatura producto | <45°C | Estabilidad API |
| **Secado** | LOD final | 1,0-3,0% | Dureza, estabilidad |
| **Compresión** | Fuerza pre-compresión | 2-5 kN | Dureza |
| **Compresión** | Fuerza principal | 8-15 kN | Dureza, disolución |
| **Recubrimiento** | Temperatura lecho | 40-45°C | Uniformidad |
| **Recubrimiento** | Ganancia de peso | 2,5-4,0% | Protección |

### 6.3 Controles en proceso (IPCs)

**Durante granulación/secado** (Iveson et al., 2001; Solanki et al., 2010):
- LOD del granulado: 1,0-3,0% (balanza humedad/Karl Fischer)
- Distribución tamaño partícula: D50 100-400 µm (difracción láser)
- Índice de Hausner: <1,25 (flujo aceptable)

**Durante compresión** (Patel et al., 2007):
- Peso promedio: ±5% del target
- Dureza: 60-120 N (rango funcional)
- Friabilidad: <1,0%
- Desintegración: <15 min

### 6.4 Atributos críticos de calidad (CQAs)

| CQA | Especificación típica | Criticidad |
|-----|----------------------|------------|
| Forma polimórfica del API | Forma A confirmada por XRPD | ALTA |
| Disolución | Q≥80% en 30 min | ALTA |
| Uniformidad de contenido | USP <905> AV<15 | ALTA |
| Valoración | 95,0-105,0% | ALTA |
| Productos de degradación | Individual ≤0,5%; Total según esp. | ALTA |
| Contenido de humedad | ≤3,0% | MEDIA |

---

## 7. Contexto de patentes para desarrollo genérico

### 7.1 Patentes principales y fechas de expiración

| Patente | Tipo | Prioridad | Expiración EE.UU. | Expiración LATAM |
|---------|------|-----------|-------------------|------------------|
| **US8,324,232** | Compuesto base | Ago 2007 | **Sep 2029** | ~Ago 2028 |
| **US10,919,881** | Forma A y polimorfos | Feb 2017 | **Feb 2038** | ~Feb 2038 |
| US11,174,247 | Combinaciones | 2018 | ~2038 | Evitable |
| US11,680,058 | Polimorfos (cont.) | 2018 | ~2038 | Alta |

**Exclusividad FDA (NCE)**: 5 años hasta **19 marzo 2029**
**Fecha elegible para Paragraph IV**: 22 marzo 2028

### 7.2 Estado en jurisdicciones latinoamericanas

**Brasil (INPI)**: Probables entradas nacionales de ambas familias de patentes. Expiración patente compuesto ~agosto 2028. El backlog del INPI puede resultar en término mínimo garantizado de 10 años post-concesión.

**México (IMPI)**: Probable protección. México permite certificados complementarios que podrían extender protección. Verificación requerida en Gaceta de Medicamentos.

**Colombia (SIC)**: **OPORTUNIDAD CRÍTICA** - Colombia **NO es signatario del PCT**, por lo que las patentes solo pudieron presentarse vía Convenio de París dentro de 12 meses de la fecha de prioridad. Es posible que **no existan patentes de aprocitentan en Colombia**, representando potencial entrada temprana.

### 7.3 Patentes de competidores

| Solicitante | Patente | Forma | Observación |
|-------------|---------|-------|-------------|
| Crystal Pharmaceutical (China) | WO2021/088645 | CSI | Estabilidad superior a Forma A |
| Teva Pharmaceuticals | WO2021/237004 | Alternativas | Formas sólidas adicionales |

La existencia de estas patentes de terceros confirma la viabilidad técnica de desarrollar formas cristalinas alternativas no infractoras (Bruni et al., 2022; Cruz-Cabeza et al., 2015).

---

## 8. Estrategias de design-around para desarrollo genérico

### 8.1 Estrategia de forma cristalina alternativa

**Opción 1 - Forma amorfa estabilizada**:
- Viabilidad: Alta
- Riesgo de infracción: Bajo (si se mantiene amorfa durante vida útil)
- Técnicas: Dispersión sólida con polímeros (HPMC-AS, PVP-VA), secado por aspersión, hot-melt extrusion
- Desafíos: Estabilidad física, riesgo de recristalización (Yang et al., 2010; Healy et al., 2017)

**Opción 2 - Licenciamiento de Forma CSI**:
- Viabilidad: Media-Alta
- Fuente: Crystal Pharmaceutical (Suzhou) Co.
- Ventajas: Forma libre con mejor estabilidad mecánica documentada
- Desafíos: Negociación de licencia, libertad de operación

**Opción 3 - Desarrollo de polimorfo propio**:
- Viabilidad: Media
- Estrategia: Screening de solventes no cubiertos, condiciones de cristalización diferenciadas
- Requisito: Caracterización exhaustiva (XRPD, DSC, TGA) para demostrar diferenciación (U.S. FDA, 2007; Mangin et al., 2009)

**Opción 4 - Sal alternativa**:
- Viabilidad: Baja-Media
- Justificación: La patente de compuesto incluye sales farmacéuticamente aceptables
- Desafíos: Demostrar bioequivalencia, posible riesgo de infracción

### 8.2 Formulación alternativa

Para evitar dependencia de Forma A:

**Dispersión sólida amorfa**: Aprocitentan disperso molecularmente en matriz polimérica (HPMC-AS, PVP, Soluplus®) para prevenir recristalización y mejorar disolución.

**Sistema auto-emulsificante (SEDDS)**: Dado el carácter lipofílico del API, una formulación basada en lípidos podría mejorar biodisponibilidad y evitar problemas de polimorfismo.

**Co-cristales**: Desarrollo de co-cristales con co-formadores seguros que no constituyan sales pero proporcionen propiedades fisicoquímicas diferentes (Perlovich, 2023).

### 8.3 Consideraciones de bioequivalencia

Para productos BCS Clase II, la bioequivalencia generalmente requiere estudios in vivo (Dave et al., 2017). Estrategias recomendadas:

- Desarrollo de método de disolución discriminatorio en múltiples medios (pH 1,2, 4,5, 6,8)
- Perfiles de disolución comparativos con Tryvio®
- Estudio BE de dosis única en ayunas y con alimentos
- Caracterización completa del API genérico (forma cristalina, tamaño de partícula, solubilidad)

---

## 9. Evaluación de ZHEJIANG JINGZHENG (TIANYU) como proveedor de API

La información pública disponible sobre este fabricante chino es limitada. Para una evaluación completa se recomienda verificar:

**Certificaciones requeridas**:
- Licencia de fabricación de API de NMPA (China)
- CEP (Certificate of Suitability) de EDQM para Europa
- DMF (Drug Master File) registrado en FDA
- GMP certification válida

**Capacidades técnicas a confirmar**:
- Experiencia en síntesis de sulfamidas pirimidínicas bromadas
- Capacidad de control de polimorfismo
- Caracterización analítica de formas cristalinas (XRPD, DSC, TGA)
- Capacidad de micronización controlada
- Programa de estabilidad según ICH (ICH, 2009)

**Auditoría recomendada**: Evaluación on-site de instalaciones antes de selección final como proveedor.

---

## 10. Conclusiones y recomendaciones para I&D

### Hallazgos principales

**La Forma A cristalina representa el principal obstáculo técnico-regulatorio** para el desarrollo genérico de aprocitentan, con protección patentaria hasta 2038. Sin embargo, la documentación de inestabilidad mecánica de esta forma y la existencia de patentes de competidores (Crystal Pharmaceutical, Teva) demuestran la viabilidad de estrategias de design-around (Bruni et al., 2022).

**Colombia representa una oportunidad de entrada temprana** debido a su no pertenencia al PCT, requiriendo verificación urgente en la SIC.

**La formulación de Tryvio® es convencional** (granulación húmeda, liberación inmediata, recubrimiento PVA), lo que facilita la transferencia tecnológica una vez resuelto el aspecto de forma cristalina (Wang et al., 2019).

### Recomendaciones de acción

| Prioridad | Acción | Responsable | Plazo |
|-----------|--------|-------------|-------|
| **ALTA** | Verificar estado de patentes en SIC Colombia | Asuntos regulatorios | 30 días |
| **ALTA** | Iniciar screening de polimorfos propio | Preformulación | 90 días |
| **ALTA** | Evaluar licencia de Forma CSI (Crystal Pharma) | Desarrollo negocio | 60 días |
| MEDIA | Caracterizar API de ZHEJIANG JINGZHENG | Calidad/Compras | 60 días |
| MEDIA | Desarrollar método de disolución discriminatorio | Analítico | 90 días |
| MEDIA | Estudios de compatibilidad API-excipientes | Formulación | 120 días |
| BAJA | Preparar estrategia de bioequivalencia | Clínico | 180 días |

### Cronograma sugerido de desarrollo

```
2025 Q1-Q2: Verificación PI LATAM + Screening polimorfos + Evaluación proveedores API
2025 Q3-Q4: Desarrollo de preformulación + Estudios compatibilidad
2026 Q1-Q2: Optimización de formulación + Scale-up piloto
2026 Q3-Q4: Estudios de estabilidad + Desarrollo analítico
2027 Q1-Q2: Lotes de validación + Preparación dossiers
2027 Q3-Q4: Sometimiento regulatorio LATAM (inicio con Colombia si factible)
2028-2029: Estudios BE + Aprobaciones + Lanzamiento post-expiración compuesto
```

### Consideraciones finales

El desarrollo genérico de aprocitentan es técnicamente viable, pero requiere una estrategia cuidadosa respecto a la forma cristalina. La ventana de oportunidad más inmediata se encuentra en **Colombia (verificación requerida)**, seguida de la expiración de la patente de compuesto en **2028-2029** para el resto de LATAM. La protección extendida de polimorfismo hasta 2038 hace imperativo el desarrollo de una forma alternativa (amorfa, CSI, o nuevo polimorfo) para competir efectivamente en el período 2029-2038.

---

## 11. Referencias

### Estudios clínicos y farmacología

Danaietash, P., Verweij, P., Wang, J.-G., Bellet, M., Ruilope, L. M., Schlaich, M., ... & PRECISION Investigators. (2022). Identifying and treating resistant hypertension in PRECISION: A randomized long-term clinical trial with aprocitentan. *Journal of Clinical Hypertension, 24*(7), 804-813. https://doi.org/10.1111/jch.14517

Schlaich, M. P., Bellet, M., Weber, M. A., Danaietash, P., Bakris, G. L., Flack, J. M., ... & PRECISION Investigators. (2022). Dual endothelin antagonist aprocitentan for resistant hypertension (PRECISION): a multicentre, blinded, randomised, parallel-group, phase 3 trial. *The Lancet, 400*(10367), 1927-1937. https://doi.org/10.1016/S0140-6736(22)02034-7

Touyz, R. M., & Harrison, D. G. (2023). Hope for resistant hypertension through BrigHTN and PRECISION. *Nature Reviews Nephrology, 19*(4), 216-217. https://doi.org/10.1038/s41581-023-00676-2

Kohan, D. E., & Heerspink, H. J. L. (2023). Fluid retention and heart failure in the PRECISION trial. *The Lancet, 401*(10385), 1335. https://doi.org/10.1016/S0140-6736(23)00275-1

### Información regulatoria y de producto

U.S. Food and Drug Administration. (2024). *TRYVIO (aprocitentan) tablets, for oral use - prescribing information* [NDA 217686]. https://www.accessdata.fda.gov/drugsatfda_docs/label/2024/217686s000lbl.pdf

European Medicines Agency. (2024). *Jeraygo (aprocitentan) - EPAR product information* [EMEA/H/C/006080]. https://www.ema.europa.eu/en/documents/product-information/jeraygo-epar-product-information_en.pdf

DailyMed. (2024). TRYVIO- aprocitentan tablet, film coated. U.S. National Library of Medicine. https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=dfe7a2ee-612c-4aba-834a-d68e6b59a0a6

### Patentes de síntesis y polimorfismo

Actelion Pharmaceuticals Ltd. (2009). *Pyrimidine derivatives and their use* [Patente internacional WO 2009/024906 A1]. World Intellectual Property Organization. https://patents.google.com/patent/WO2009024906A1

Idorsia Pharmaceuticals Ltd. (2018). *Crystalline forms of the 4-pyrimidinesulfamide derivative aprocitentan* [Patente internacional WO 2018/154101 A1]. World Intellectual Property Organization. https://patents.google.com/patent/WO2018154101A1

Idorsia Pharmaceuticals Ltd. (2021). *Crystalline forms of a 4-pyrimidinesulfamide derivative aprocitentan* [Patente U.S. 10,919,881 B2]. U.S. Patent and Trademark Office. https://patents.google.com/patent/US10919881B2

Idorsia Pharmaceuticals Ltd. (2023). *Crystalline forms of a 4-pyrimidinesulfamide derivative aprocitentan* [Patente U.S. 11,680,058 B2]. U.S. Patent and Trademark Office. https://patents.google.com/patent/US11680058B2

Crystal Pharmaceutical (Suzhou) Co., Ltd. (2021). *Crystal form of aprocitentan, preparation method therefor and use thereof* [Patente internacional WO 2021/088645 A1]. World Intellectual Property Organization. https://patents.google.com/patent/WO2021088645A1

### Caracterización cristalográfica

Idorsia Pharmaceuticals Ltd. (2021). Crystal structure of aprocitentan Form A, C₁₆H₁₄Br₂N₆O₄S. *Powder Diffraction, 36*(2), 154-155. Cambridge Crystallographic Data Centre. https://doi.org/10.1017/S0885715621000105

### Polimorfismo farmacéutico

Bruni, G., Maiella, P. G., Maggi, L., Mustarelli, P., Ferrara, C., Berbenni, V., ... & Marini, A. (2022). The relevance of crystal forms in the pharmaceutical field: Sword of Damocles or innovation tools? *Molecules, 27*(16), 5103. https://doi.org/10.3390/molecules27165103

U.S. Food and Drug Administration, Center for Drug Evaluation and Research. (2007). *Guidance for Industry: ANDAs - Pharmaceutical solid polymorphism: Chemistry, manufacturing, and controls information*. https://www.fda.gov/media/71375/download

Cruz-Cabeza, A. J., Reutzel-Edens, S. M., & Bernstein, J. (2015). Facts and fictions about polymorphism. *Chemical Society Reviews, 44*(23), 8619-8635. https://doi.org/10.1039/C5CS00227C

Hilfiker, R., & von Raumer, M. (2018). Solid state and polymorphism of the drug substance in the context of quality by design and ICH guidelines Q8-Q12. In *Polymorphism in the pharmaceutical industry: Solid form and drug development* (pp. 1-30). Wiley-VCH. https://doi.org/10.1002/9783527697847.ch1

Prasad, M. R., Krishnan, J. A., Reddy, B. V., Rao, N. R., & Tekade, R. K. (2018). Polymorphism and its implications in pharmaceutical product development. In *Dosage form design parameters* (pp. 67-103). Academic Press. https://doi.org/10.1016/B978-0-12-814421-3.00002-6

Mangin, D., Puel, F., & Veesler, S. (2009). Polymorphism in processes of crystallization in solution: A practical review. *Organic Process Research & Development, 13*(6), 1241-1253. https://doi.org/10.1021/op900168f

Perlovich, G. L. (2023). Polymorphism of carbamazepine pharmaceutical cocrystal: Structural analysis and solubility performance. *Pharmaceutics, 15*(6), 1747. https://doi.org/10.3390/pharmaceutics15061747

### Sistema de Clasificación Biofarmacéutica (BCS)

Amidon, G. L., Lennernäs, H., Shah, V. P., & Crison, J. R. (1995). A theoretical basis for a biopharmaceutic drug classification: The correlation of in vitro drug product dissolution and in vivo bioavailability. *Pharmaceutical Research, 12*(3), 413-420. https://doi.org/10.1023/A:1016212804288

Dave, V. S., Gupta, D., Yu, M., Nguyen, P., & Varghese Gupta, S. (2017). Current and evolving approaches for improving the oral permeability of BCS Class III or analogous molecules. *Drug Development and Industrial Pharmacy, 43*(2), 177-189. https://doi.org/10.1080/03639045.2016.1269122

### Tecnología de granulación húmeda

Parikh, D. M. (Ed.). (2016). *Handbook of pharmaceutical granulation technology* (3rd ed.). CRC Press. https://doi.org/10.3109/9781616310059

Litster, J., & Ennis, B. (2004). *The science and engineering of granulation processes*. Springer. https://doi.org/10.1007/978-94-017-0546-2

Wang, J., Wen, H., & Desai, D. (2010). Lubrication in tablet formulations. *European Journal of Pharmaceutics and Biopharmaceutics, 75*(1), 1-15. https://doi.org/10.1016/j.ejpb.2010.01.007

Iveson, S. M., Litster, J. D., Hapgood, K., & Ennis, B. J. (2001). Nucleation, growth and breakage phenomena in agitated wet granulation processes: A review. *Powder Technology, 117*(1-2), 3-39. https://doi.org/10.1016/S0032-5910(01)00313-8

Solanki, H. K., Basavaraj, K., Shah, D., Thakkar, R., Patel, M., & Patel, S. (2010). Recent advances in granulation technology. *International Journal of Pharmaceutical Sciences Review and Research, 5*(1), 48-54.

Wang, H., Chen, X., & Gao, Z. (2019). Simulation modeling of a pharmaceutical tablet manufacturing process via wet granulation. *Complexity, 2019*, Article 3659309. https://doi.org/10.1155/2019/3659309

### Manufactura de tabletas

Patel, S., Kaushal, A. M., & Bansal, A. K. (2007). Effect of particle size and compression force on compaction behavior and derived mathematical parameters of compressibility. *Pharmaceutical Research, 24*(1), 111-124. https://doi.org/10.1007/s11095-006-9129-8

Lantz, R. J., & Schwartz, J. B. (1989). Compression. In *Pharmaceutical dosage forms: Tablets* (Vol. 1, pp. 131-193). Marcel Dekker, Inc.

Hancock, B. C., & Colvin, J. T. (2004). The effects of particle size and shape on the compaction behavior of pharmaceutical powders. *Journal of Applied Polymer Science, 93*(5), 2553-2560. https://doi.org/10.1002/app.20687

### Guidelines y estándares ICH/FDA

International Council for Harmonisation. (2009). *ICH Q8(R2): Pharmaceutical development*. https://www.ich.org/page/quality-guidelines

International Council for Harmonisation. (2000). *ICH Q6A: Specifications - Test procedures and acceptance criteria for new drug substances and new drug products: Chemical substances*. https://www.ich.org/page/quality-guidelines

### Bases de datos de referencia

DrugBank Online. (2024). Aprocitentan [DB15059]. University of Alberta. https://go.drugbank.com/drugs/DB15059

PubChem. (2024). Aprocitentan [CID 25099191]. National Center for Biotechnology Information. https://pubchem.ncbi.nlm.nih.gov/compound/25099191

### Literatura adicional sobre formulación y estabilidad

Byrn, S. R., Pfeiffer, R. R., & Stowell, J. G. (1999). *Solid-state chemistry of drugs* (2nd ed.). SSCI, Inc.

Brittain, H. G. (Ed.). (1999). *Polymorphism in pharmaceutical solids* (Vol. 95). Marcel Dekker, Inc. https://doi.org/10.1201/b16897

Healy, A. M., Worku, Z. A., Kumar, D., & Madi, A. M. (2017). Pharmaceutical solvates, hydrates and amorphous forms: A special emphasis on cocrystals. *Advanced Drug Delivery Reviews, 117*, 25-46. https://doi.org/10.1016/j.addr.2017.03.002

Kobayashi, Y., Ito, S., Itai, S., & Yamamoto, K. (2000). Physicochemical properties and bioavailability of carbamazepine polymorphs and dihydrate. *International Journal of Pharmaceutics, 193*(2), 137-146. https://doi.org/10.1016/S0378-5173(99)00315-4

Yang, W., Johnston, K. P., & Williams, R. O. III. (2010). Comparison of bioavailability of amorphous versus crystalline itraconazole nanoparticles via pulmonary administration in rats. *European Journal of Pharmaceutics and Biopharmaceutics, 75*(1), 33-41. https://doi.org/10.1016/j.ejpb.2010.01.011

---

*Informe preparado para el equipo de I&D de formulación y desarrollo farmacéutico. La información técnica se presenta a nivel conceptual-estratégico conforme a las restricciones de seguridad establecidas. Toda actividad de desarrollo debe realizarse respetando los derechos de propiedad intelectual vigentes en cada jurisdicción. Se recomienda validación de información de patentes con asesores legales especializados antes de tomar decisiones comerciales.*