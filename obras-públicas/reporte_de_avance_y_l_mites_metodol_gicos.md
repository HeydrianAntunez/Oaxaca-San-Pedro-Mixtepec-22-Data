# Reporte de Estado y Justificación Metodológica: Auditoría de Obras Públicas 2025-2026

**Sujeto Obligado:** H. Ayuntamiento de San Pedro Mixtepec, Distrito 22 (Clave INEGI 20318)
**Elaborado por:** Auditoría de Presupuesto Municipal
**Fecha de corte metodológico:** Noviembre de 2026 (Basado en los trabajos documentados al 20 de octubre de 2026).

El presente dictamen resume los hallazgos y limitaciones documentados extensamente en el archivo de referencia "informe_extraccion_clasificacion_mixtepec.md". Su objetivo es establecer con rigor técnico qué se ha validado, qué información sigue pendiente y cuáles son los obstáculos sistémicos para acceder al expediente completo de las obras.

## 1. ¿Qué se revisó realmente de las obras públicas?

Hasta el momento, la revisión se ha enfocado en la **trazabilidad documental y el reporte de gasto público**, más no en la fiscalización física. Hemos logrado estructurar y verificar las siguientes representaciones de datos oficiales:

1. **Planeación Municipal (SISPLADE 2026):**

   * Se extrajo el catálogo completo de **246 acciones priorizadas** por el Consejo de Desarrollo Social Municipal (CDSM).

   * Se identificaron las prioridades, localidades, metas físicas proyectadas (M2, ML, etc.) y las fuentes de financiamiento planeadas (FISM y Otras).

   * Se revisaron visualmente fracciones de las actas de integración y priorización (marzo 2026) en PDF, cotejando coordenadas y metas de 4 convenios educativos.

2. **Reporte de Gasto Ejecutado (SRFT Finanzas Oaxaca):**

   * Se procesó íntegramente el **Reporte Final definitivo de 2025**, recuperando **78 folios** (74 de responsabilidad municipal, incluyendo 73 contratos declarados de obra).

   * Se vincularon los montos reportados como *Aprobados, Contratados y Pagados* con sus respectivos contratistas y coordenadas geográficas de referencia.

   * Se analizaron los cortes del 1T y 2T de 2026, identificando que los folios municipales presentes corresponden a recursos arrastrados de 2025, no a obras nuevas de 2026.

3. **Convenios de Cofinanciamiento (SEFIN):**

   * Se localizaron y extrajeron 4 convenios específicos para la construcción de aulas (Escuelas Ricardo Flores Magón, José María Morelos, Rufino Tamayo y 21 de Marzo), verificando montos de aportación estatal y municipal (\$640,000 MXN por aula).

4. **Transparencia Municipal (PNT y Portal Web):**

   * Se recuperó el árbol del catálogo público del municipio (respuestas JSON).

   * Se analizaron exportaciones públicas de la PNT (presupuestos, actas de cabildo, inventarios).

## 2. ¿Qué faltó revisar? (Vacíos de Auditoría)

A pesar de tener un mapa presupuestal y de planeación robusto, **aún no contamos con los elementos necesarios para auditar exhaustivamente los materiales, cantidades y pagos reales por obra**. Los vacíos documentales pendientes son:

* **Expediente Técnico Constructivo:** Faltan los planos, croquis precisos y catálogos de conceptos con precios unitarios.

* **Contratos Firmados y Anexos:** Solo tenemos la *referencia* del contrato en el SRFT, pero no el documento legal firmado que establece las garantías y obligaciones del contratista.

* **Comprobación Financiera:** No tenemos facturas, estimaciones de avance de obra firmadas, ni números generadores. El SRFT solo muestra una celda con un número "Pagado", pero no hay soporte documental que avale dicho flujo de efectivo.

* **Cierre y Entrega-Recepción:** Faltan actas de entrega a las comunidades o comités.

* **Inspección Física:** Ninguna de las cantidades declaradas ha sido ubicada o verificada topográficamente en campo.

## 3. Justificación Metodológica: ¿Por qué no pudimos acceder a ello?

La imposibilidad de acceder a los expedientes completos no se debe a una falla en el proceso de extracción, sino a la naturaleza de las publicaciones de los sujetos obligados y las limitaciones de acceso a bases de datos públicas:

* **Inexistencia de API's y Restricciones de Sistema:** Como se detalla en el documento "informe_extraccion_clasificacion_mixtepec.md", no tenemos credenciales de administrador ni acceso a servidores SQL (por ejemplo, del Sistema de Contabilidad Municipal). Interactuamos estrictamente con lo que las entidades hacen público (endpoints públicos, HTML, y descargas habilitadas).

* **Ausencia de Documentos en la Plataforma Nacional de Transparencia (PNT):** Al buscar mediante el endpoint de la API de la PNT para contratos, los sistemas devolvieron estructuras JSON vacías. El buscador temático tampoco arrojó los contratos municipales de obras, mostrando únicamente resultados de arrendamientos o contratos de CFE irrelevantes.

* **Formatos No Estructurados (PDF Escaneados):** Las actas del SISPLADE y los convenios de la SEFIN son imágenes escaneadas dentro de un PDF. Esto impide una extracción directa y tabular. Obliga a utilizar OCR (Reconocimiento Óptico de Caracteres), el cual es propenso a errores en sellos y firmas, requiriendo revisión manual página por página.

* **Fragmentación de la Información:** El portal municipal publica un Programa Anual de Obras (PAO), el SISPLADE tiene priorizaciones y el SRFT tiene gasto reportado. No existe un ID único interoperable. Un mismo proyecto debe ser "unido" manualmente comparando CCTs, montos o nombres de calles, lo cual deja margen para que obras no reportadas queden en la opacidad.

En conclusión, los datos construidos en nuestra plataforma son veraces respecto a lo *declarado* por las dependencias en sus repositorios abiertos. Sin embargo, auditar la obra pública requiere transitar del análisis de la "verdad declarada" (metadatos) a la "verdad material" (facturas, contratos físicos y visitas de campo), información que los portales actuales del municipio aún no proveen de forma abierta y estructurada.