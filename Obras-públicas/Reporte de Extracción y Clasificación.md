# Informe Técnico: Extracción y Clasificación de Datos para la Auditoría Ciudadana de Obras en San Pedro Mixtepec

**Municipio:** San Pedro Mixtepec, Distrito 22, Oaxaca (Clave INEGI: **20318**).  
**Periodo analizado:** 2025 - 2026.  

---

## 1. Resumen de Actividades Realizadas
Para consolidar la plataforma de auditoría ciudadana y el mapa interactivo de obras públicas, se ejecutó un proceso riguroso de extracción, validación y estructuración de fuentes documentales oficiales:

1. **SRFT 2025 (Definitivo):** Descarga y procesamiento del reporte final en Excel de la Secretaría de Finanzas de Oaxaca (SEFIN), extrayendo 78 folios de recursos federales transferidos (74 de ejecución municipal directa en FISM, PROAGUA y otras fuentes).
2. **SRFT 2026 (Cortes 1T y 2T):** Monitoreo trimestral de proyectos plurianuales y de arrastre en los módulos de destino y ejercicio del gasto.
3. **Catálogo SISPLADE 2026:** Extracción íntegra y validación de las **246 acciones priorizadas** por el Consejo de Desarrollo Social Municipal (CDSM) para el ejercicio 2026.
4. **Convenios SEFIN (Aulas Escolares):** Localización y procesamiento de 4 convenios de cofinanciamiento para aulas en escuelas primarias del municipio (Ricardo Flores Magón, José María Morelos, Rufino Tamayo y 21 de Marzo) por un total de $2.56 millones de MXN.
5. **Georreferenciación y Mapeo:** Integración de coordenadas geográficas en un visor Leaflet con filtros dinámicos, desglose presupuestal, buscador por CCT/contratista y panel de detalle tipo drawer.

---

## 2. Inventario de Fuentes y Archivos Procesados

| Fuente Oficial | Tipo de Documento | Registros / Folios | Estado de Integración |
| :--- | :--- | :--- | :--- |
| **SRFT 2025** | Excel / PASH Definitivo | 78 Folios (74 municipales) | Integrado en mapa, buscador y panel de finanzas |
| **SRFT 2026 (1T y 2T)** | Excel / Módulos de Gasto | 8 Registros plurianuales | Vinculado a proyectos activos |
| **SISPLADE 2026** | HTML / Actas CDSM | 246 Acciones priorizadas | Catálogo interactivo de consulta en pestaña dedicada |
| **Convenios SEFIN** | PDF Oficiales | 4 Escuelas primarias | Fichas técnicas con CCT y montos específicos |

---

## 3. Verificación de Visualización en el Entorno
- Se ha reconstruido el archivo único `index_obras_mixtepec_v2.html` optimizado con Leaflet y Tailwind CSS.
- Se incorporó `map.invalidateSize()` en el evento de carga para garantizar que el mapa renderice correctamente las teselas de CARTO sin retrasos visuales.
- Todas las pestañas (Obras y Mapa, SISPLADE 2026, Finanzas) y el Drawer lateral interactivo están completamente operativos.