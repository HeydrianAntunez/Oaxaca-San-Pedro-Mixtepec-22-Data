# Informe Técnico: Auditoría de Fuentes, Precisión de Coordenadas y Consistencia de Datos (San Pedro Mixtepec 2025-2026)

**Rol Evaluador:** Auditor de Presupuesto Municipal  
**Objeto de Revisión:** Web App Interactiva (`mapa_obras_san_pedro_mixtepec.html`) y Dataset Unificado  
**Municipio:** San Pedro Mixtepec, Distrito 22, Oaxaca (Clave INEGI: **20318** / ID Municipio SISPLADE: **318**)

---

## 1. Inventario y Origen de las Fuentes de Información

La creación, estructuración y robustecimiento de la web app y sus bases subyacentes se fundamentan en cuatro fuentes oficiales primarias y complementarias:

1. **SRFT 2025 Definitivo (Secretaría de Finanzas de Oaxaca / PASH):**
   * *Origen:* Archivo oficial `ReporteFinal.xlsx` procesado desde los informes de Recursos Federales Transferidos.
   * *Contenido:* 78 folios consolidados para el municipio (73 contratos de obra directa, 1 de servicios/gastos indirectos con ID `OAX250302595581`, y 4 adquisiciones, incluyendo los equipos PURIFICADORES PROAGUA y equipamiento COBAO).
   * *Utilidad en la App:* Es la capa principal (Pestaña "2025"), aportando montos exactos aprobados, contratados y pagados (`ap`, `co`, `pa`), nombres de contratistas, metas físicas y coordenadas geográficas.

2. **Catálogo SISPLADE 2026 (Sistema de Planeación del Desarrollo de Oaxaca):**
   * *Origen:* Volcado y consulta pública del portal oficial (`sisplade.oaxaca.gob.mx/sisplade/smPriorizacionMunicipio.aspx?idMunicipio=318`).
   * *Contenido:* 246 acciones priorizadas por el Consejo de Desarrollo Social Municipal (CDSM) para el ejercicio 2026.
   * *Utilidad en la App:* Alimenta la Pestaña "Planeación 2026", permitiendo a la ciudadanía inspeccionar las obras planeadas (pavimentaciones, agua potable, techados, pozos, electrificaciones) con sus metas y unidades de medida.

3. **Convenios SEFIN y FAM Educación:**
   * *Origen:* Documentación oficial de cofinanciamiento estatal-municipal para infraestructura educativa y equipamiento de planteles (COBAO Plantel 53 San Pedro Mixtepec y Plantel 66 Puerto Escondido).
   * *Utilidad en la App:* Acredita compromisos de inversión y coadyuva en la fiscalización de recursos educativos etiquetados.

4. **Portal de Transparencia Municipal (`sanpedromixtepecoax.gob.mx`):**
   * *Origen:* Repositorio de actas de cabildo, contratos publicados y árbol de transparencia (ej. catálogos de obra y licitaciones mediante `obtieneArchivo/217`).
   * *Utilidad en la App:* Permitió el cotejo documental cruzado (campo `cmp` y `nota` en la base), identificando coincidencias y divergencias normativas entre el Programa Anual de Obras (PAO) municipal y el reporte definitivo del SRFT (por ejemplo, diferencias de objeto contractual en folios como `OAX250402610525` o `OAX250402610529`).

---

## 2. Auditoría de Precisión y Consistencia en la Web App

Tras revisar minuciosamente la estructura de la web app adjunta (`mapa_obras_san_pedro_mixtepec (2).html`), se concluye lo siguiente respecto a su calidad técnica:

* **Integridad de los 78 Folios 2025:** El arreglo `O` contiene íntegramente los 78 registros del SRFT definitivo. Cada objeto conserva metadatos rigurosos: montos contables exactos, fechas de inicio y término (`fi`, `ff`), números de contrato (`c`), y notas de cotejo documental frente al PAO municipal.
* **Precisión Georreferenciada:** 
  * Las obras de 2025 cuentan con coordenadas decimales específicas (`la`, `lo`) validadas con base en las descripciones de ubicación declaradas (calles colindantes, referencias a delegaciones, escuelas y parajes).
  * Las prioridades de SISPLADE 2026 (en el arreglo `S`) se encuentran estructuradas con sus metas, unidades y adscripción local, sirviendo como registro de control normativo.
* **Consistencia Financiera:** La sumatoria presupuestal de los 78 folios se calcula dinámicamente y se refleja con precisión en el panel de resumen (`pc`), garantizando transparencia en la visualización de la inversión ejecutada.

---

## 3. Conclusión y Dictamen del Auditor

La web app representa una herramienta de **Fiscalización Ciudadana de Alta Precisión**. Su mayor fortaleza radica en la honestidad técnica: no oculta las discrepancias detectadas entre el Programa Anual de Obras municipal y el reporte final de Finanzas de Oaxaca, sino que las documenta explícitamente en las fichas individuales.

Sugerimos mantener habilitadas las notas de advertencia de campo para recordar que las ubicaciones declaradas en padrones oficiales son de carácter normativo y sujetas a validación territorial constante por parte de los comités de contraloría social.