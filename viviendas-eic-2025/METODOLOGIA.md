# Cómo se hizo el análisis

## Universo y fuente

La unidad de observación es la **vivienda particular habitada** de la Encuesta Intercensal 2025, no el inmueble o lote del listado de campo. Se leyó `viviendas20.csv` del ZIP de Oaxaca y se filtró `CVEGEO == "20318"`, San Pedro Mixtepec, Distrito 22. Se conservan los ceros iniciales al leer todos los identificadores y códigos como texto. Se comprueba que `ID_VIV` no se repita y que `FACTOR` sea positivo.

Hay **5 797 registros** en el archivo municipal, con `COBERTURA=2` (municipio muestreado). El total de los factores es **18 771**. Todos los registros municipales tienen `TIPO_REG=0` (encuestado). El diseño comprende **3 estratos y 485 pares distintos de estrato-UPM**; el número de UPM solo, sin estrato, no sirve como identificador único.

## Dos denominadores

La distribución por `CLAVIVP` usa las **18 771 viviendas particulares habitadas estimadas**. Para paredes, techos, pisos, cuartos, servicios, equipamiento y tenencia se emplean las **18 674 viviendas particulares habitadas con características** (`VIVPARHAB_C`, denominación de INEGI): se excluyen `CLAVIVP=07` (local no construido para habitación), `08` (vivienda móvil) y `09` (refugio), pues esas preguntas figuran en blanco por pase. La diferencia estimada es 97 viviendas. En las variables seleccionadas no aparecieron otros códigos de no especificado dentro de ese dominio municipal; si se amplía el análisis, hay que comprobarlo de nuevo.

Los porcentajes de la infografía siempre indican su universo. No se suman porcentajes de preguntas diferentes. La categoría «casa que comparte terreno» alude a clase de vivienda, no al número de inmuebles, hogares o terrenos.

## Estimación y precisión

Para cualquier condición `A`, la estimación del número de viviendas es la suma de factores de expansión: `T_A = Σ_i FACTOR_i × 1(A_i)`. La proporción es `p_A = T_A / T_D`, donde `D` es el universo indicado. Multiplicamos por 100 para obtener el porcentaje. En las viviendas del dominio todas cuentan con su propio factor; no se usan porcentajes de filas sin ponderar.

Las medidas de precisión son una implementación reproducible del método de **linearización de Taylor** para estratos y unidades primarias de muestreo (UPM). Para un total, se suma el aporte ponderado por par estrato-UPM y, dentro de cada estrato con `n_h` conglomerados, se calcula `n_h/(n_h−1) × Σ_j (t_hj−media_h)^2`. Luego se suman las varianzas estratales. Para una proporción, cada registro aporta `FACTOR_i × [1(A_i)×1(D_i)−p_A×1(D_i)] / T_D`; se aplica la misma fórmula a los aportes agregados por conglomerado. El error estándar es la raíz de la varianza. Para proporciones entre 0 y 1 se calculan intervalos logit aproximados al **90%** usando `z=1.64485`; para totales se usa `estimación ± z × error estándar`.

**Importante:** se trata de una aproximación propia a la precisión de INEGI; no incorpora correcciones de población finita ni reproduce todos los ajustes oficiales. El total general y su error estándar (18 771 y 939.22) coinciden con los principales resultados de INEGI, pero los límites e intervalos de otros indicadores no se deben presentar como intervalos oficiales. Las clases raras (`CLAVIVP=03`, `04`, `08`, `09`, `99`) tienen una precisión relativa débil; se muestran por transparencia, sin interpretaciones contundentes.

## Controles y límites

- Total ponderado de 18 771 comparado con `VIVPARHAB=18771` del conjunto de principales resultados de INEGI; las 18 674 con características corresponden a `VIVPARHAB_C=18674`.
- Los porcentajes de las clases suman 100% antes de redondear. El campo `FACTOR` no se redondea antes de agregar.
- Es una fotografía de 2025: no permite estimar crecimiento sin una serie comparable anterior ni atribuir causas a las diferencias entre viviendas.
- No incluye viviendas deshabitadas, de uso temporal, viviendas colectivas ni todos los inmuebles captados en el listado de campo.
- Una estimación municipal muestreada está sujeta a incertidumbre; las cifras pequeñas pueden tener error relativo elevado.

**Fuentes:** [microdatos EIC 2025](https://www.inegi.org.mx/programas/eic/2025/#microdatos), [descriptor de variables](https://www.inegi.org.mx/contenidos/programas/eic/2025/microdatos/eic2025_micro_fd.xlsx) y [diseño muestral](https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/889463931140.pdf). Fecha de consulta: 24 de septiembre de 2026.
