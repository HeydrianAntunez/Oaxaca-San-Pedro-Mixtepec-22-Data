# Cómo se hizo el análisis

## Fuente, unidad y alcance

La fuente es la Encuesta Intercensal (EIC) 2025 del INEGI, archivo de microdatos de Oaxaca `eic2025_micro_20_csv.zip`, tabla `personas20.csv`. Cada renglón representa a una persona registrada en una vivienda particular incluida en la muestra. Se filtra `CVEGEO == "20318"`: San Pedro Mixtepec, Distrito 22, Oaxaca. No debe confundirse con otro municipio de nombre parecido. La identificación municipal en el tabulado oficial es `203180000` porque añade la clave de localidad `0000`.

La extracción arroja 17 936 observaciones de personas, pertenecientes a 5 797 viviendas muestreadas. Hay tres estratos y 485 combinaciones de estrato y unidad primaria de muestreo (UPM). Se comprobaron unicidad de `ID_PERSONA`, factores positivos y coincidencia de indicadores clave con el tabulado municipal del INEGI. Hay 142 registros marcados como imputados (`TIPO_REG=1`), que representan 452 personas estimadas; se conservan como parte de la base oficial. No se distribuyen microdatos de personas en este proyecto.

## Estimadores

Cada registro tiene un factor de expansión `FACTOR` proporcionado por INEGI. Un total estimado para la característica A se calcula como:

`T(A) = suma_i [FACTOR_i × I(persona_i cumple A)]`.

Para un porcentaje en el grupo D:

`P(A | D) = 100 × T(A y D) / T(D)`.

Ejemplo: la proporción de población de 65 años y más es `100 × 4 365 / 57 844 = 7,55 %`. En cambio, la participación económica femenina usa como denominador a **mujeres de 12 años y más**, no a toda la población municipal ni a toda la PEA. Los dominios de edad se definen con `EDAD`; los valores fuera de edad plausible, los códigos de no respuesta y los pases no son categorías afirmativas. Los porcentajes no se recalculan sobre los casos con respuesta válida salvo cuando se indica expresamente, como en la mediana de ingresos.

La mediana y los cuartiles se obtienen ordenando los valores válidos y acumulando `FACTOR` hasta alcanzar 25, 50 o 75 % del peso en el dominio. Son cuantiles ponderados **sin interpolación**. `INGTRMEN` es ingreso por trabajo mensualizado: 0 a 999 997 pesos se trata como monto conocido; 999 998 es superior al límite publicado y 999 999 es no especificado. La mediana incluye ceros. `HORTRA` acepta 0 a 140 horas y descarta el código 999. Ninguna de estas cifras equivale a ingresos de hogar o salario por hora.

## Definiciones seleccionadas

| Tema | Variables y regla | Denominador |
|---|---|---|
| Población, sexo y edad | `FACTOR`, `SEXO`, `EDAD` | Toda la población, salvo edad indicada |
| Localidad | `TAMLOC` | Toda la población |
| Nacimiento y residencia anterior | `ENT_PAIS_NAC`, `ENT_PAIS_RES_5A`, `MUN_RES_5A`; residencia en octubre de 2020 | Toda la población para nacimiento; 5 años y más para residencia anterior |
| Identidad | `PERTE_INDIGENA=1`, `AFRODES=1` | Toda la población |
| Lengua | `HLENGUA=1`; `HESPANOL=1` dentro de hablantes | 3 años y más; luego hablantes |
| Discapacidad | Alguna de `DIS_VER`, `DIS_OIR`, `DIS_CAMINAR`, `DIS_RECORDAR`, `DIS_BANARSE`, `DIS_HABLAR` con código 3 o 4 | Toda la población, o 60 años y más |
| Condición mental | `DIS_MENTAL=5`, separada de la definición anterior | Toda la población |
| Asistencia y alfabetismo | `ASISTEN=1` (asiste), `ASISTEN=3` (no asiste); `ALFABET=3` (no sabe leer y escribir) | Edades 6–14, 15–17, 18–24; alfabetismo de 15 y más |
| Escolaridad | `NIVACAD`: 00–01 sin escolaridad; 02,03,06 básica; 04,05,07,09 media superior; 08,10,11 superior; 12–14 posgrado | 15 años y más |
| Salud | `DHSERSAL1` códigos 01–08 para afiliación, 09 para ninguna; `SERSALUD` para lugar habitual | Toda la población |
| Actividad laboral | `CONACT` códigos 10,13–20 ocupación; 30 búsqueda de trabajo; PEA = ambos | 12 años y más |
| Posición, prestaciones, ingreso | `SITTRA`, `AGUINALDO`, `VACACIONES`, `SERVICIO_MEDICO`, `INGTRMEN` | Ocupados; prestaciones entre asalariados (`SITTRA` 1–3) |
| Sector del negocio | Primeros dos dígitos de `ACTIVIDADES_C`, según clasificador oficial | Ocupados |
| Traslado | `TIE_TRASLADO_TRAB`; cualquiera de `MED_TRASLADO_TRAB1..3`; `MUN_TRAB` y `ENT_PAIS_TRAB` | Ocupados |
| Unión e hijos | `SITUA_CONYUGAL` para 12+; `HIJOS_NAC_VIVOS` válido para mujeres 15–49 | Grupo indicado |

La pregunta de discapacidad se basa en dificultad severa o imposibilidad en al menos una de seis actividades. El problema o condición mental tiene variable propia y no se suma al total de `PCON_DISC`. La autoadscripción indígena y el habla de lengua indígena son medidas distintas. En salud, la afiliación puede tener varios derechos registrados, pero aquí se usa la primera variable para la presencia de al menos una afiliación; el valor reproduce el tabulado oficial. Para medios de traslado se revisan tres respuestas posibles, por lo que varias modalidades pueden contarse para una misma persona.

## Diseño muestral e incertidumbre

La EIC es una encuesta de diseño complejo. El [Diseño de la muestra del INEGI](https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/889463931140.pdf), secciones 2.1–2.3, establece **linearización de Taylor** para totales y proporciones; su sección 2.5 usa **Jackknife para la tasa global de fecundidad**, que este script no calcula. El script incorpora `ESTRATO` y `UPM` para una aproximación de la varianza: agrega los valores ponderados por UPM dentro de cada estrato y suma `n_h/(n_h−1) × suma_j (z_hj − promedio_h)^2`. Para porcentajes usa la variable linearizada `z_i = FACTOR_i × [I(A y D) − p × I(D)] / T(D)`. No aplica corrección por población finita ni reproduce necesariamente todos los ajustes internos de INEGI. Hay 485 UPM y 3 estratos. Los intervalos exploratorios usan **1,645** por error estándar para totales, según la fórmula escrita en la sección 2.1, y `t(0,95; 482) = 1,64802` con transformación logit para proporciones, según la sección 2.3. Las medianas no incluyen intervalo calculado.

**Prioridad de publicación:** cuando existe una cifra oficial en [`eic2025_micro_105.xlsx`](https://www.inegi.org.mx/contenidos/programas/eic/2025/microdatos/eic2025_micro_105.xlsx), se prefiere su error e intervalo al del script. El total poblacional coincide en valor y error estándar (57 844 y 2 957,35), pero el intervalo oficial es 52 970,22–62 717,78, ligeramente distinto del obtenido con el factor 1,645 escrito en el documento de diseño. No se atribuye esa diferencia a un procedimiento no documentado. El total de personas con discapacidad coincide en 2 966, pero el error estándar derivado por el script (**202,57**) difiere del oficial (**174,49**), y por tanto su intervalo oficial (2 678,10–3 253,90) debe prevalecer. El archivo `resultados/indicadores.csv` contiene intervalos **aproximados** y no sustituye la precisión publicada por INEGI.

La comparación de subgrupos requiere sus errores y covarianzas antes de afirmar que una diferencia es estadísticamente significativa. Aquí se habla de **diferencias descriptivas**. Los indicadores de subgrupos pequeños pueden tener mayor coeficiente de variación; las lecturas más sensibles a esta limitación, como prestaciones o ingresos específicos, merecen un examen posterior.

## Verificación y reproducibilidad

El script lee el ZIP original directamente y sólo retiene los registros de la clave 20318. Los puntos de control comparados con el tabulado oficial fueron: población 57 844, mujeres 30 346, hombres 27 498, discapacidad 2 966, no asistencia escolar 6–14 de 4,91 %, alfabetismo 15+ de 6,13 % sin leer y escribir, educación básica 47,59 %, media superior 25,12 %, superior 19,32 %, afiliación de 47,36 %, PEA de 64,74 % y 30 544 personas ocupadas. Las estimaciones puntuales coinciden. Un segundo script, `validar_conclusiones.py`, recalcula de manera independiente desde el ZIP las cinco conclusiones numeradas y las confronta con el Excel cuando existe una columna equivalente. Detectó y corrigió el porcentaje conjunto de tres sectores: **46,86 %** a partir de 14 312/30 544, en vez de sumar porcentajes sectoriales redondeados (46,85 %). El grado promedio de escolaridad (9,54 años) y la tasa global de fecundidad (1,33) fueron tomados del tabulado oficial y no son salidas del script.

Para reproducir: descargar el ZIP oficial de Oaxaca desde [microdatos EIC 2025](https://www.inegi.org.mx/programas/eic/2025/#microdatos), instalar los paquetes de `requirements.txt` y ejecutar `python analizar_personas.py --zip /ruta/eic2025_micro_20_csv.zip --salida resultados`. Si se omite `--zip`, el script intenta descargarlo a `datos/`. Se generan `resumen.json` e `indicadores.csv`. La descarga puede ser grande; el script procesa el CSV por bloques. No necesita ni publica datos personales identificables.

## Lo que no se puede concluir aquí

- Es una fotografía de 2025: no cuantifica crecimiento, trayectorias laborales ni cambios desde 2020.
- La residencia anterior sólo pregunta a los residentes actuales de 5 años y más y no observa las salidas del municipio.
- La categoría del negocio no identifica por sí sola actividad turística, informalidad ni calidad del empleo.
- La diferencia entre medianas de ingreso de mujeres y hombres no es un efecto causal ni una brecha salarial ajustada.
- La tasa de búsqueda de trabajo de la EIC no se equipara automáticamente a la tasa de desocupación de la ENOE.

**Localización exacta de archivos, fila y columnas:** [`FUENTES_INEGI.md`](FUENTES_INEGI.md). **Documentación oficial:** [programa EIC 2025](https://www.inegi.org.mx/programas/eic/2025/), [síntesis metodológica](https://www.inegi.org.mx/app/biblioteca/ficha.html?upc=889463931133) y [diseño muestral](https://www.inegi.org.mx/app/biblioteca/ficha.html?upc=889463931140).
