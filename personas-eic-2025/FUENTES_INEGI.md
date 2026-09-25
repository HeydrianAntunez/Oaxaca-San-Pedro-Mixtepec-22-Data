# Dónde está cada dato en el INEGI

Este inventario permite localizar y comprobar las cifras, sin depender de una referencia genérica a la portada del programa. Se verificó el **24 de septiembre de 2026 (hora de México)**.

## 1. Microdatos de personas de Oaxaca

1. Abra [Encuesta Intercensal 2025, sección Microdatos](https://www.inegi.org.mx/programas/eic/2025/#microdatos).
2. En **Conjunto de datos / Entidades federativas**, elija **Oaxaca**, formato **CSV**. Descargará [`eic2025_micro_20_csv.zip`](https://www.inegi.org.mx/contenidos/programas/eic/2025/microdatos/eic2025_micro_20_csv.zip). El número **20** es la clave estatal de Oaxaca.
3. Abra el ZIP y seleccione `personas20.csv` (los otros archivos son `viviendas20.csv` y `migrantes20.csv`). Filtre `CVEGEO = 20318`, que identifica San Pedro Mixtepec, **Distrito 22**. Use `FACTOR` para expandir cada registro; 17 936 renglones representan 57 844 personas.

Los nombres de las variables y el sentido de sus códigos se consultan en el [diccionario de microdatos `eic2025_micro_fd.xlsx`](https://www.inegi.org.mx/contenidos/programas/eic/2025/microdatos/eic2025_micro_fd.xlsx), pestaña **PERSONAS**. Busque en esa hoja `EDAD`, `PERTE_INDIGENA`, `HLENGUA`, `DHSERSAL1`, `SERSALUD`, `CONACT`, `SITTRA`, `SERVICIO_MEDICO` y `ACTIVIDADES_C`. Las claves 46, 72 y 23 de actividad se contrastan con los [clasificadores del INEGI](https://www.inegi.org.mx/app/biblioteca/ficha.html?upc=889463931966), archivo `ACTIVIDAD_ECONOMICA.csv` del ZIP CSV. La pregunta de lugar de atención `SERSALUD=07` corresponde a consultorio, clínica u hospital privado.

## 2. Tabulado municipal de comprobación

En la sección [Microdatos](https://www.inegi.org.mx/programas/eic/2025/#microdatos), busque la descarga de **Principales resultados por localidad** y su descriptor. El archivo de Excel es [`eic2025_micro_105.xlsx`](https://www.inegi.org.mx/contenidos/programas/eic/2025/microdatos/eic2025_micro_105.xlsx). Abra la hoja **`eic2025_micro_105`**, active un filtro en **CVEGEO** y escriba **`203180000`**. Los cinco registros del municipio ocupan los renglones **7662 a 7666** de la versión analizada:

- Fila **7662**, `ESTIMADOR = Valor`: cifra puntual.
- Fila **7663**, `Error estándar`.
- Filas **7664 y 7665**, límites inferior y superior del intervalo de confianza al 90 %.
- Fila **7666**, coeficiente de variación.

El código del tabulado añade `0000` de localidad a la clave municipal `20318`. La descripción de cada columna está en el [descriptor de principales resultados (`eic2025_micro_fd_105.pdf`)](https://www.inegi.org.mx/contenidos/programas/eic/2025/microdatos/eic2025_micro_fd_105.pdf). Puede buscar el mnemónico en el PDF, por ejemplo `PCN_PSINDER`; no todos los indicadores que calculamos desde microdatos están publicados como columna en este archivo.

| Afirmación del informe | Columna y celda de la cifra oficial | Valor | Qué significa |
|---|---|---:|---|
| Población total | `POBTOT`, **I7662** | 57 844 | Personas residentes estimadas |
| Menores de 15 años | `POB0_14`, **BW7662** | 13 267 | Conteo de 0 a 14 años |
| 65 años y más | `POB65_MAS`, **CA7662** | 4 365 | Conteo de 65 años y más |
| Autoadscripción indígena | `PCN_POB_IND`, **DH7662** | 41,11 % | Porcentaje de toda la población |
| Habla lengua indígena | `PCN_P3YM_HLI`, **DK7662** | 4,09 % | Porcentaje de personas de 3 años y más |
| Sin afiliación médica | `PCN_PSINDER`, **GI7662** | 52,56 % | Porcentaje de toda la población |
| Atención privada | `PCN_PUSU_IPRIV`, **GX7662** | 37,82 % | Porcentaje **entre usuarios de servicios**; 56 452 en `PUSU_SS`, GR7662 |
| PEA | `PCN_PEA`, **FP7662** | 64,74 % | Personas económicamente activas de 12 años y más |
| Ocupados | `POCUPADA`, **FV7662** | 30 544 | Personas ocupadas estimadas |
| Personas con discapacidad | `PCON_DISC`, **EB7662** | 2 966 | Total según definición oficial |
| Escolaridad promedio | `GRAPROES`, **FM7662** | 9,54 años | Indicador oficial citado sin recálculo |
| Tasa global de fecundidad | `TGF`, **CN7662** | 1,33 | Indicador oficial citado sin recálculo |

**Aclaración sobre la atención privada:** el informe calcula **21 348 / 57 844 = 36,91 %** al usar como base *todas* las personas. El tabulado muestra **21 348 / 56 452 = 37,82 %** cuando la base son quienes declararon acudir a algún servicio (`PUSU_SS`). Ambas cifras son correctas con sus respectivos denominadores y no deben rotularse igual.

**Aclaración sobre la actividad de mujeres:** `PCN_PEA_F`, celda **FQ7662 = 43,66 %**, es la proporción de mujeres **dentro de toda la PEA**. Nuestro **53,26 %** es la participación de la PEA **dentro de las mujeres de 12 años y más**. El 77,72 % masculino usa la misma lógica por sexo. Son indicadores distintos.

## 3. Diseño de la muestra y precisión

Desde [EIC 2025, Metodología → Diseño de la muestra](https://www.inegi.org.mx/programas/eic/2025/#documentacion), descargue el [PDF `889463931140.pdf`](https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/889463931140.pdf). Consulte **sección 2.1, Total (pp. 9–10); sección 2.3, Proporción (pp. 12–13); sección 2.5, Jackknife (p. 15)**. Se aplica `FACTOR` y se considera la estructura de estratos y UPM. El texto asigna series de Taylor a los estimadores lineales y Jackknife a la tasa global de fecundidad. El proyecto no recalcula la TGF.

El archivo `resultados/indicadores.csv` ofrece errores derivados de los microdatos para exploración. **La referencia autoritativa de precisión es el Excel oficial**: para población, por ejemplo, consulte I7663:I7665; para discapacidad, EB7663:EB7665. Nuestro recálculo de varianza no reproduce cada ajuste del INEGI, aunque los estimadores puntuales verificados coinciden.

## 4. Cinco conclusiones y su trazabilidad

1. **Edades:** `EDAD` 0–14 y 65+ en `personas20.csv`, con `FACTOR`; controle 13 267 y 4 365 en `POB0_14` y `POB65_MAS`. Los porcentajes 22,94 % y 7,55 % dividen esos conteos entre 57 844.
2. **Identidad y lengua:** `PERTE_INDIGENA=1` da 23 777/57 844 = 41,11 %; `HLENGUA=1` entre 3+ da 2 277/55 647 = 4,09 %. Controle en `PCN_POB_IND` y `PCN_P3YM_HLI`. Son preguntas y universos diferentes.
3. **Salud:** `DHSERSAL1=09` da 30 402/57 844 = 52,56 %; `SERSALUD=07` da 21 348/57 844 = 36,91 %. El porcentaje oficial de atención privada usa 56 452 usuarios como base y es 37,82 %.
4. **Trabajo:** `CONACT` ocupado (10, 13–20) o búsqueda (30), mujeres/hombres `SEXO=3/1`, universo `EDAD≥12`; 13 450/25 253 = 53,26 % y 17 357/22 333 = 77,72 %. Para prestación, `SITTRA` 1–3 y `SERVICIO_MEDICO=5`: 5 450/18 999 = 28,69 %. El tabulado confirma PEA total, ocupados y proporción asalariada; los desgloses propios se verifican en la auditoría reproducible.
5. **Sectores:** `ACTIVIDADES_C` comienza en 46, 72 o 23 para comercio minorista, alojamiento/alimentos o construcción: 5 657 + 5 010 + 3 645 = **14 312**, equivalentes a **46,86 %** de 30 544 ocupados. Los tres porcentajes sectoriales redondeados suman 46,85 %, pero el porcentaje conjunto debe calcularse **antes** de redondear.

Ejecute `validar_conclusiones.py` con los dos archivos oficiales para reproducir las comprobaciones. El listado XML de descarga masiva suministrado por el usuario también registra las URL directas del ZIP, del diccionario y del Excel.
