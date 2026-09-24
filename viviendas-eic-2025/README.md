# Viviendas en San Pedro Mixtepec, Distrito 22 (EIC 2025)

Una lectura pública de las viviendas particulares habitadas del municipio **20318, Oaxaca**. Incluye un [informe](INFORME.md), una [infografía](resultados/infografia.png) y una [nota metodológica](METODOLOGIA.md).

## Tres datos para empezar

- **18 771** viviendas particulares habitadas estimadas en 2025; intervalo aproximado al 90%: **17 226 a 20 316**.
- **63.51%** son casas únicas en el terreno; **23.37%**, casas que comparten terreno; **11.17%**, viviendas en vecindad o cuartería.
- Entre las **18 674 viviendas a las que se captaron características detalladas**, **65.81%** tienen agua entubada dentro, **27.97%** drenaje conectado a red pública y **64.60%** internet.

Se trata de una encuesta: los totales son **estimaciones ponderadas**, no conteos de todos los inmuebles ni una medición del crecimiento municipal.

## Qué hay en el proyecto

| Archivo | Para qué sirve |
| --- | --- |
| `INFORME.md` y `resultados/informe.pdf` | Hallazgos y tablas, con explicaciones para público general. |
| `METODOLOGIA.md` | Universos, códigos, fórmulas, precisión y limitaciones. |
| `resultados/infografia.png` | Imagen vertical para compartir. |
| `analizar_viviendas.py` | Lee los microdatos originales y calcula indicadores e intervalos. |
| `crear_materiales.py` e `infografia_ilustrada.py` | Recrean el informe PDF y la infografía ilustrada a partir del JSON calculado. |
| `resultados/*.csv`, `resultados/resumen.json` | Resultados legibles y auditables. |
| `requirements.txt` | Dependencias para Python. |

## Reproducir en VS Code

Con Python 3.10 o posterior, abre esta carpeta en la terminal:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python analizar_viviendas.py
python crear_materiales.py
```

El primer script descarga automáticamente el ZIP de Oaxaca desde INEGI (aproximadamente 74 MB) a `datos/`. Si ya tienes el archivo, evita la descarga:

```bash
python analizar_viviendas.py --zip ruta/al/eic2025_micro_20_csv.zip
python crear_materiales.py
```

Los datos originales no se incluyen en este repositorio para mantenerlo ligero y conservar la fuente oficial única. `datos/` está excluida de Git; los resultados se pueden recalcular desde el ZIP oficial.

## Fuentes

- [INEGI, EIC 2025: microdatos](https://www.inegi.org.mx/programas/eic/2025/#microdatos).
- [ZIP oficial de Oaxaca, CSV](https://www.inegi.org.mx/contenidos/programas/eic/2025/microdatos/eic2025_micro_20_csv.zip): tabla `viviendas20.csv`.
- [Diccionario de microdatos](https://www.inegi.org.mx/contenidos/programas/eic/2025/microdatos/eic2025_micro_fd.xlsx): hoja `VIVIENDAS`.
- [Diseño de la muestra, INEGI](https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/889463931140.pdf).
- [Principales resultados en datos abiertos](https://www.inegi.org.mx/programas/eic/2025/#datos_abiertos): control del total municipal publicado.

El análisis es una elaboración independiente a partir de los microdatos de INEGI; no es una publicación oficial del instituto.
