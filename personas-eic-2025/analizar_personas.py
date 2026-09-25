"""Indicadores de personas, EIC 2025, San Pedro Mixtepec D22 (20318).

Uso: python analizar_personas.py --zip /ruta/eic2025_micro_20_csv.zip
El ZIP original no se redistribuye. Requiere pandas y numpy.
"""
from __future__ import annotations

import argparse
import json
import math
import urllib.request
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import t

ZIP_URL = "https://www.inegi.org.mx/contenidos/programas/eic/2025/microdatos/eic2025_micro_20_csv.zip"
CRITICAL90_TOTAL = 1.645  # Diseño de la muestra, sección 2.1: intervalo normal de totales.
CRITICAL90_PROP = t.ppf(.95, 485 - 3)  # Sección 2.3: logit con 482 gl.


def load_people(path: Path) -> pd.DataFrame:
    rows = []
    with zipfile.ZipFile(path) as z, z.open("personas20.csv") as f:
        for chunk in pd.read_csv(f, dtype=str, keep_default_na=False, chunksize=100_000):
            part = chunk.loc[chunk.CVEGEO.eq("20318")]
            if len(part):
                rows.append(part.copy())
    if not rows:
        raise ValueError("No hay registros para CVEGEO 20318")
    df = pd.concat(rows, ignore_index=True)
    if df.ID_PERSONA.duplicated().any():
        raise ValueError("ID_PERSONA duplicado")
    df["FACTOR"] = pd.to_numeric(df.FACTOR, errors="raise")
    if (df.FACTOR <= 0).any():
        raise ValueError("FACTOR no positivo")
    return df


def var_taylor(df: pd.DataFrame, z: pd.Series) -> float:
    """Conglomerados UPM dentro de ESTRATO, sin corrección de población finita."""
    tmp = df[["ESTRATO", "UPM"]].copy()
    tmp["z"] = z.to_numpy()
    g = tmp.groupby(["ESTRATO", "UPM"], sort=False)["z"].sum()
    v = 0.0
    for _, a in g.groupby(level=0, sort=False):
        n = len(a)
        if n < 2:
            raise ValueError("Estrato con una sola UPM")
        v += n / (n - 1) * float(((a - a.mean()) ** 2).sum())
    return v


def number(df: pd.DataFrame, mask: pd.Series) -> dict:
    w = df.FACTOR * mask.astype(float)
    est = float(w.sum())
    se = math.sqrt(var_taylor(df, w))
    return dict(estimado=round(est), muestra=int(mask.sum()), precision="aproximada_no_oficial", error_estandar=round(se, 2),
                ic90=[round(max(0, est - CRITICAL90_TOTAL * se), 2), round(est + CRITICAL90_TOTAL * se, 2)],
                cv=round(se / est * 100, 2) if est else None)


def pct(df: pd.DataFrame, event: pd.Series, domain: pd.Series) -> dict:
    w = df.FACTOR
    denom = float(w[domain].sum())
    numer = float(w[event & domain].sum())
    if denom == 0:
        raise ValueError("Denominador cero")
    p = numer / denom
    z = w * (event.astype(float) * domain - p * domain) / denom
    se = math.sqrt(var_taylor(df, z))
    if 0 < p < 1 and se > 0:
        logit = math.log(p / (1 - p))
        m = CRITICAL90_PROP * se / (p * (1 - p))
        ci = [100 / (1 + math.exp(-(logit - m))), 100 / (1 + math.exp(-(logit + m)))]
    else:
        ci = [max(0., (p - CRITICAL90_PROP * se) * 100), min(100., (p + CRITICAL90_PROP * se) * 100)]
    return dict(estimado=round(numer), denominador=round(denom), precision="aproximada_no_oficial", muestra=int((event & domain).sum()),
                muestra_dominio=int(domain.sum()), porcentaje=round(100 * p, 2),
                error_estandar_pp=round(100 * se, 2), ic90=[round(v, 2) for v in ci],
                cv=round(100 * se / p, 2) if p else None)


def weighted_quantile(a: pd.Series, w: pd.Series, q: float) -> float:
    values = pd.DataFrame({"x": a.astype(float), "w": w.astype(float)}).sort_values("x")
    return float(values.loc[values.w.cumsum().ge(q * values.w.sum()), "x"].iloc[0])


def analyze(df: pd.DataFrame) -> dict:
    d = {}
    a = pd.Series(True, index=df.index)
    age = pd.to_numeric(df.EDAD, errors="coerce")
    age_valid = age.le(130)
    a3, a5, a6, a12, a15, a18, a25 = [age.between(n, 130) for n in (3, 5, 6, 12, 15, 18, 25)]
    female, male = df.SEXO.eq("3"), df.SEXO.eq("1")

    d["poblacion"] = number(df, a)
    d["mujeres"] = number(df, female)
    d["hombres"] = number(df, male)
    d["proporcion_mujeres"] = pct(df, female, a)
    d["imputados"] = number(df, df.TIPO_REG.eq("1"))
    for label, lo, hi in [("0-14", 0, 14), ("15-29", 15, 29), ("30-44", 30, 44),
                          ("45-64", 45, 64), ("65+", 65, 130), ("0-4", 0, 4),
                          ("5-9", 5, 9), ("10-14", 10, 14), ("15-19", 15, 19),
                          ("20-24", 20, 24), ("25-29", 25, 29), ("30-34", 30, 34),
                          ("35-39", 35, 39), ("40-44", 40, 44), ("45-49", 45, 49),
                          ("50-54", 50, 54), ("55-59", 55, 59), ("60-64", 60, 64),
                          ("65-69", 65, 69), ("70-74", 70, 74), ("75+", 75, 130)]:
        d[f"edad_{label}"] = pct(df, age.between(lo, hi), a)
    d["edad_mediana_ponderada_sin_interpolacion"] = weighted_quantile(age[age_valid], df.FACTOR[age_valid], .5)
    for code, label in [("1", "menos_2500"), ("2", "2500_14999"), ("3", "15000_49999"),
                        ("4", "50000_99999"), ("5", "100000_mas")]:
        d[f"localidad_{label}"] = pct(df, df.TAMLOC.eq(code), a)

    d["nacido_oaxaca"] = pct(df, df.ENT_PAIS_NAC.eq("020"), a)
    d["nacido_otra_entidad"] = pct(df, df.ENT_PAIS_NAC.str.match(r"0(0[1-9]|[12][0-9]|3[0-2])") & df.ENT_PAIS_NAC.ne("020"), a)
    d["nacido_otro_pais"] = pct(df, df.ENT_PAIS_NAC.str.match(r"[1-5][0-9][0-9]") & ~df.ENT_PAIS_NAC.isin(["997","998","999"]), a)
    d["mismo_municipio_2020"] = pct(df, df.ENT_PAIS_RES_5A.eq("020") & df.MUN_RES_5A.eq("318"), a5)
    d["otra_entidad_2020"] = pct(df, df.ENT_PAIS_RES_5A.str.match(r"0(0[1-9]|[12][0-9]|3[0-2])") & df.ENT_PAIS_RES_5A.ne("020"), a5)
    d["otro_pais_2020"] = pct(df, df.ENT_PAIS_RES_5A.str.match(r"[1-5][0-9][0-9]") & ~df.ENT_PAIS_RES_5A.isin(["997","998","999"]), a5)

    d["indigena_autoadscripcion"] = pct(df, df.PERTE_INDIGENA.eq("1"), a)
    d["afro_autoadscripcion"] = pct(df, df.AFRODES.eq("1"), a)
    d["habla_lengua_indigena_3mas"] = pct(df, df.HLENGUA.eq("1"), a3)
    d["habla_espanol_entre_hli"] = pct(df, df.HESPANOL.eq("1"), df.HLENGUA.eq("1"))

    difficulties = ["DIS_VER", "DIS_OIR", "DIS_CAMINAR", "DIS_RECORDAR", "DIS_BANARSE", "DIS_HABLAR"]
    # La definición de PCON_DISC del descriptor oficial usa solo seis actividades.
    # La condición mental se publica por separado y no se agrega a este total.
    severe = df[difficulties].isin(["3", "4"]).any(axis=1)
    d["discapacidad"] = number(df, severe)
    d["discapacidad_pct"] = pct(df, severe, a)
    d["condicion_mental"] = pct(df, df.DIS_MENTAL.eq("5"), a)
    d["discapacidad_60mas"] = pct(df, severe, age.ge(60) & age_valid)

    d["asiste_6_14"] = pct(df, df.ASISTEN.eq("1"), age.between(6, 14))
    d["no_asiste_6_14"] = pct(df, df.ASISTEN.eq("3"), age.between(6, 14))
    d["asiste_15_17"] = pct(df, df.ASISTEN.eq("1"), age.between(15, 17))
    d["asiste_18_24"] = pct(df, df.ASISTEN.eq("1"), age.between(18, 24))
    d["analfabetismo_15mas"] = pct(df, df.ALFABET.eq("3"), a15)
    d["analfabetismo_mujeres_15mas"] = pct(df, df.ALFABET.eq("3"), a15 & female)
    d["analfabetismo_hombres_15mas"] = pct(df, df.ALFABET.eq("3"), a15 & male)
    for key, codes in [("sin_escolaridad", ["00", "01"]), ("basica", ["02", "03", "06"]),
                       ("media_superior", ["04", "05", "07", "09"]), ("superior", ["08", "10", "11"]),
                       ("posgrado", ["12", "13", "14"])]:
        d[f"escolaridad_{key}_15mas"] = pct(df, df.NIVACAD.isin(codes), a15)

    affiliated = df.DHSERSAL1.isin(["01", "02", "03", "04", "05", "06", "07", "08"])
    d["afiliacion_salud"] = pct(df, affiliated, a)
    d["sin_afiliacion_salud"] = pct(df, df.DHSERSAL1.eq("09"), a)
    d["atiende_privado"] = pct(df, df.SERSALUD.eq("07"), a)
    d["atiende_consultorio_farmacia"] = pct(df, df.SERSALUD.eq("08"), a)
    d["atiende_centro_publico"] = pct(df, df.SERSALUD.eq("06"), a)
    d["no_se_atiende"] = pct(df, df.SERSALUD.eq("10"), a)

    work_codes = ["10", "13", "14", "15", "16", "17", "18", "19", "20"]
    employed = df.CONACT.isin(work_codes)
    labor = employed | df.CONACT.eq("30")
    d["pea_12mas"] = pct(df, labor, a12)
    d["pea_mujeres_12mas"] = pct(df, labor, a12 & female)
    d["pea_hombres_12mas"] = pct(df, labor, a12 & male)
    d["ocupados"] = number(df, employed)
    d["ocupados_entre_pea"] = pct(df, employed, labor)
    d["desocupados_entre_pea"] = pct(df, df.CONACT.eq("30"), labor)
    # Sector de actividad del negocio; las claves de dos dígitos se obtienen
    # del clasificador oficial incluido con los microdatos.
    for code, label in [("46", "comercio_minorista"), ("72", "alojamiento_alimentos"),
                        ("23", "construccion"), ("81", "otros_servicios"),
                        ("11", "agropecuario_pesca"), ("61", "educacion")]:
        d[f"sector_{label}"] = pct(df, df.ACTIVIDADES_C.str.startswith(code), employed)
    for key, codes in [("asalariados", ["1", "2", "3"]), ("empleadores", ["4"]),
                       ("cuenta_propia", ["5"]), ("sin_pago", ["6"])]:
        d[f"posicion_{key}"] = pct(df, df.SITTRA.isin(codes), employed)
    d["aguinaldo_entre_asalariados"] = pct(df, df.AGUINALDO.eq("1"), employed & df.SITTRA.isin(["1","2","3"]))
    d["servicio_medico_laboral_entre_asalariados"] = pct(df, df.SERVICIO_MEDICO.eq("5"), employed & df.SITTRA.isin(["1","2","3"]))
    d["vacaciones_entre_asalariados"] = pct(df, df.VACACIONES.eq("3"), employed & df.SITTRA.isin(["1","2","3"]))
    inc = pd.to_numeric(df.INGTRMEN, errors="coerce")
    known_income = employed & inc.between(0, 999997)
    d["ingreso_reportado_ocupados"] = pct(df, known_income, employed)
    d["ingreso_cero_ocupados_con_dato"] = pct(df, inc.eq(0), known_income)
    for label, dom in [("total", known_income), ("mujeres", known_income & female), ("hombres", known_income & male)]:
        d[f"ingreso_mensual_{label}"] = {
            "universo_estimado": round(df.FACTOR[dom].sum()), "muestra": int(dom.sum()),
            "mediana": round(weighted_quantile(inc[dom], df.FACTOR[dom], .5)),
            "q1": round(weighted_quantile(inc[dom], df.FACTOR[dom], .25)),
            "q3": round(weighted_quantile(inc[dom], df.FACTOR[dom], .75)),
        }
    hours = pd.to_numeric(df.HORTRA, errors="coerce")
    known_hours = employed & hours.between(0, 140)
    d["horas_semanales_mediana"] = {"mediana": weighted_quantile(hours[known_hours], df.FACTOR[known_hours], .5),
                                   "universo_estimado": round(df.FACTOR[known_hours].sum())}
    d["trabaja_mismo_municipio"] = pct(df, df.ENT_PAIS_TRAB.eq("020") & df.MUN_TRAB.eq("318"), employed)
    d["traslado_trabajo_30min_o_menos"] = pct(df, df.TIE_TRASLADO_TRAB.isin(["1","2"]), employed)
    d["traslado_trabajo_no_se_traslada"] = pct(df, df.TIE_TRASLADO_TRAB.eq("7"), employed)
    d["traslado_trabajo_caminar"] = pct(df, df[["MED_TRASLADO_TRAB1","MED_TRASLADO_TRAB2","MED_TRASLADO_TRAB3"]].eq("01").any(axis=1), employed)
    d["traslado_trabajo_motocicleta"] = pct(df, df[["MED_TRASLADO_TRAB1","MED_TRASLADO_TRAB2","MED_TRASLADO_TRAB3"]].eq("10").any(axis=1), employed)

    for label,codes in [("soltera",["09"]),("union_o_casada",["01","06","07","08"]),
                        ("separada_divorciada_viuda",["02","03","04","05"])]:
        d[f"conyugal_{label}_12mas"] = pct(df, df.SITUA_CONYUGAL.isin(codes), a12)
    hnv = pd.to_numeric(df.HIJOS_NAC_VIVOS, errors="coerce")
    women_15_49 = female & age.between(15,49) & hnv.between(0,25)
    d["hijos_nacidos_vivos_15_49"] = {
        "mujeres_estimadas_con_dato": round(df.FACTOR[women_15_49].sum()),
        "muestra": int(women_15_49.sum()),
        "promedio": round(float((hnv[women_15_49] * df.FACTOR[women_15_49]).sum() / df.FACTOR[women_15_49].sum()), 2),
    }
    d["sin_hijos_nacidos_vivos_15_49"] = pct(df, hnv.eq(0), women_15_49)
    return d


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--zip", type=Path, default=Path("datos/eic2025_micro_20_csv.zip"))
    p.add_argument("--salida", type=Path, default=Path("resultados"))
    args = p.parse_args()
    if not args.zip.exists():
        args.zip.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(ZIP_URL, args.zip)
    df = load_people(args.zip)
    result = {"municipio": "San Pedro Mixtepec, Distrito 22, Oaxaca", "clave": "20318",
              "registros_personas": len(df), "viviendas_muestra": int(df.ID_VIV.nunique()),
              "estratos": int(df.ESTRATO.nunique()),
              "upm_en_estrato": int(df.groupby(["ESTRATO","UPM"]).ngroups),
              "indicadores": analyze(df)}
    args.salida.mkdir(parents=True, exist_ok=True)
    (args.salida / "resumen.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    pd.DataFrame([{"indicador": k, **(v if isinstance(v, dict) else {"valor": v})}
                  for k,v in result["indicadores"].items()]).to_csv(args.salida / "indicadores.csv", index=False)
    print(result["indicadores"]["poblacion"])


if __name__ == "__main__":
    main()
