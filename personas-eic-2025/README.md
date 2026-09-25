# Personas de San Pedro Mixtepec, Distrito 22

Este proyecto describe a las **personas residentes** de San Pedro Mixtepec, Distrito 22, Oaxaca, con los microdatos de la Encuesta Intercensal 2025 del INEGI. Su clave municipal es **20318**. Es la continuación temática de un análisis de viviendas; aquí el foco está en edad, identidad, educación, salud, trabajo y otros rasgos de las personas.

**Resultado principal:** se estiman **57 844 habitantes**: **52,46 % mujeres**, **22,94 % menores de 15 años** y **7,55 % con 65 años o más**. Una encuesta produce estimaciones con margen de error, no un censo persona por persona.

## Qué leer primero

- [`INFORME.md`](INFORME.md): explicación de los resultados en lenguaje accesible.
- `Informe_personas_San_Pedro_Mixtepec_2025.pdf`: versión visual para lectura y distribución.
- [`METODOLOGIA.md`](METODOLOGIA.md): fuentes, definiciones, cálculos y límites.
- [`FUENTES_INEGI.md`](FUENTES_INEGI.md): ruta exacta de descarga, hoja, fila y columnas del tabulado oficial; comprobación de cada una de las cinco conclusiones.
- [`analizar_personas.py`](analizar_personas.py): script reproducible; `resultados/` contiene los indicadores generados.
- [`validar_conclusiones.py`](validar_conclusiones.py): auditoría independiente de las cinco conclusiones contra el CSV original y el Excel oficial.
- [`infografias/`](infografias/): cinco imágenes para compartir, una por cada conclusión numerada. Se generan con [`crear_infografias.py`](crear_infografias.py).

## Para reproducir los datos

Se necesita Python 3.10 o posterior y el [ZIP oficial de microdatos de Oaxaca](https://www.inegi.org.mx/programas/eic/2025/#microdatos) (tabla `personas20.csv`). Las bases originales no se redistribuyen aquí.

```bash
python -m pip install -r requirements.txt
python analizar_personas.py --zip /ruta/eic2025_micro_20_csv.zip --salida resultados
python validar_conclusiones.py --zip /ruta/eic2025_micro_20_csv.zip --tabulado /ruta/eic2025_micro_105.xlsx
python crear_infografias.py
python generar_pdf.py
```

El primer script puede intentar la descarga oficial si se omite `--zip`; ésta puede ser grande. Las salidas incluyen un JSON detallado y un CSV de indicadores. El informe coteja cifras con el [tabulado oficial `eic2025_micro_105.xlsx`](https://www.inegi.org.mx/contenidos/programas/eic/2025/microdatos/eic2025_micro_105.xlsx), hoja homónima, municipio `203180000`, filas **7662 a 7666**. Su grado promedio de escolaridad y tasa global de fecundidad se citan del tabulado, no son calculados por el script. Algunos intervalos generados desde microdatos son aproximados; ante una diferencia se usa la precisión publicada por el INEGI. La auditoría corrigió el porcentaje conjunto de tres sectores a **46,86 %** al calcularlo antes del redondeo.

Las cinco infografías están aquí: [edades](infografias/01_edades.png), [identidad y lengua](infografias/02_identidad_lengua.png), [salud](infografias/03_salud.png), [trabajo](infografias/04_trabajo.png) y [sectores](infografias/05_sectores.png). Cada una muestra el universo de sus porcentajes. El proyecto ocupa esta carpeta, hermana de `viviendas-eic-2025/` en el mismo repositorio.

**Fuente:** [INEGI, Encuesta Intercensal 2025](https://www.inegi.org.mx/programas/eic/2025/). Revisión: 24 de septiembre de 2026, hora de México.
