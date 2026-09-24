"""Análisis reproducible de viviendas EIC 2025, municipio 20318.

Uso: python analizar_viviendas.py [--zip ruta/eic2025_micro_20_csv.zip]
"""
from __future__ import annotations

import argparse
import json
import math
import urllib.request
import zipfile
from pathlib import Path

import pandas as pd

MUNICIPIO = "20318"
FUENTE = "https://www.inegi.org.mx/contenidos/programas/eic/2025/microdatos/eic2025_micro_20_csv.zip"
Z90 = 1.6448536269514722
CLASES = {
    "01": "Casa única en el terreno",
    "02": "Casa que comparte terreno",
    "03": "Casa dúplex",
    "04": "Departamento en edificio",
    "05": "Vivienda en vecindad o cuartería",
    "06": "Cuarto de azotea",
    "07": "Local no construido para habitación",
    "08": "Vivienda móvil",
    "09": "Refugio",
    "99": "No especificado",
}
# Cada par variable/código procede del descriptor eic2025_micro_fd.xlsx.
INDICADORES = [
    ("PAREDES", "8", "Paredes de tabique, ladrillo, block, piedra, cantera, cemento o concreto", "materiales"),
    ("TECHOS", "10", "Techo de losa de concreto o viguetas con bovedilla", "materiales"),
    ("TECHOS", "03", "Techo de lámina metálica", "materiales"),
    ("PISOS", "2", "Piso de cemento o firme", "materiales"),
    ("PISOS", "3", "Piso de madera, mosaico u otro recubrimiento", "materiales"),
    ("PISOS", "1", "Piso de tierra", "materiales"),
    ("TOTCUART", "1", "Vivienda de un cuarto", "espacios"),
    ("CUADORM", "1", "Vivienda de un dormitorio", "espacios"),
    ("AGUA_ENTUBADA", "1", "Agua entubada dentro de la vivienda", "servicios"),
    ("AGUA_ENTUBADA", "2", "Agua entubada solo en patio o terreno", "servicios"),
    ("AGUA_ENTUBADA", "3", "Sin agua entubada", "servicios"),
    ("DRENAJE", "1", "Drenaje conectado a red pública", "servicios"),
    ("DRENAJE", "2", "Drenaje conectado a fosa o tanque séptico", "servicios"),
    ("DRENAJE", "5", "Sin drenaje", "servicios"),
    ("ELECTRICIDAD", "1", "Con electricidad", "servicios"),
    ("INTERNET", "7", "Con internet", "equipamiento"),
    ("REFRIGERADOR", "1", "Con refrigerador", "equipamiento"),
    ("LAVADORA", "3", "Con lavadora", "equipamiento"),
    ("AIRE_ACON", "5", "Con aire acondicionado", "equipamiento"),
    ("TENENCIA", "1", "Habita la persona propietaria", "tenencia"),
    ("TENENCIA", "2", "Propiedad aún en pago", "tenencia"),
    ("TENENCIA", "3", "Se paga renta", "tenencia"),
    ("TENENCIA", "4", "Prestada o de familiar", "tenencia"),
]


def descargar(destino: Path) -> Path:
    destino.parent.mkdir(parents=True, exist_ok=True)
    if not destino.exists():
        print(f"Descargando microdatos de Oaxaca desde INEGI: {FUENTE}")
        urllib.request.urlretrieve(FUENTE, destino)
    return destino


def leer(zip_path: Path) -> pd.DataFrame:
    with zipfile.ZipFile(zip_path) as archivo:
        with archivo.open("viviendas20.csv") as datos:
            df = pd.read_csv(datos, dtype=str, keep_default_na=False, low_memory=False)
    df = df.loc[df["CVEGEO"] == MUNICIPIO].copy()
    if df.empty:
        raise ValueError("No se encontró el municipio 20318 en viviendas20.csv")
    if df["ID_VIV"].duplicated().any():
        raise ValueError("Hay identificadores de vivienda duplicados en el municipio")
    df["FACTOR"] = pd.to_numeric(df["FACTOR"], errors="raise")
    if (df["FACTOR"] <= 0).any():
        raise ValueError("Se detectaron factores de expansión no positivos")
    return df


def varianza_taylor(df: pd.DataFrame, contribucion: pd.Series) -> float:
    """Taylor de conglomerados estratificados; sin corrección de población finita.

    La clave de UPM se usa junto con el estrato: UPM sola NO es única.
    """
    tmp = df[["ESTRATO", "UPM"]].copy()
    tmp["z"] = contribucion.to_numpy()
    grupos = tmp.groupby(["ESTRATO", "UPM"], sort=False, observed=True)["z"].sum()
    v = 0.0
    for _, valores in grupos.groupby(level=0, sort=False):
        n = len(valores)
        if n < 2:
            raise ValueError("Un estrato tiene una sola UPM; revisar el diseño")
        v += n / (n - 1) * ((valores - valores.mean()) ** 2).sum()
    return float(v)


def total(df: pd.DataFrame, mask: pd.Series) -> dict:
    contrib = df["FACTOR"] * mask.astype(float)
    est = float(contrib.sum())
    se = math.sqrt(varianza_taylor(df, contrib))
    return {
        "estimado": round(est), "error_estandar": round(se, 2),
        "ic90_inferior": round(max(0, est - Z90 * se), 2),
        "ic90_superior": round(est + Z90 * se, 2),
        "cv_porcentaje": round(100 * se / est, 2) if est else None,
    }


def proporcion(df: pd.DataFrame, evento: pd.Series, dominio: pd.Series) -> dict:
    w = df["FACTOR"]
    denom = float((w * dominio).sum())
    numer = float((w * evento * dominio).sum())
    p = numer / denom
    # Linealización de una razón: y - p*x dividido entre el total expandido x.
    linear = w * (evento.astype(float) * dominio - p * dominio) / denom
    se = math.sqrt(varianza_taylor(df, linear))
    if 0 < p < 1 and se > 0:
        # INEGI informa intervalos logit para proporciones; se aplica al 90%.
        logit = math.log(p / (1 - p))
        margen = Z90 * se / (p * (1 - p))
        inversa = lambda x: 1 / (1 + math.exp(-x))
        limites = (inversa(logit - margen), inversa(logit + margen))
    else:
        limites = (max(0, p - Z90 * se), min(1, p + Z90 * se))
    return {
        "estimado": round(numer), "denominador": round(denom),
        "porcentaje": round(100 * p, 2),
        "error_estandar_pp": round(100 * se, 2),
        "ic90_porcentaje": [round(100 * limites[0], 2), round(100 * limites[1], 2)],
        "cv_porcentaje": round(100 * se / p, 2) if p else None,
    }


def analizar(df: pd.DataFrame) -> dict:
    todas = pd.Series(True, index=df.index)
    con_caracteristicas = ~df["CLAVIVP"].isin(["07", "08", "09"])
    clase = {nombre: proporcion(df, df["CLAVIVP"] == codigo, todas)
             for codigo, nombre in CLASES.items()}
    indicadores = {}
    for variable, codigo, nombre, grupo in INDICADORES:
        indicadores[nombre] = {
            "grupo": grupo, "variable": variable, "codigo": codigo,
            **proporcion(df, df[variable] == codigo, con_caracteristicas),
        }
    return {
        "municipio": "San Pedro Mixtepec, Distrito 22, Oaxaca",
        "clave_geoestadistica": MUNICIPIO, "encuesta": "EIC 2025",
        "fuente_zip": FUENTE, "archivo": "viviendas20.csv",
        "registros_muestra": len(df),
        "registros_imputados": int((df["TIPO_REG"] == "1").sum()),
        "cobertura_codigos": df["COBERTURA"].value_counts().to_dict(),
        "numero_estratos": df["ESTRATO"].nunique(),
        "numero_upm_estrato": df.groupby(["ESTRATO", "UPM"]).ngroups,
        "viviendas_particulares_habitadas": total(df, todas),
        "viviendas_con_caracteristicas": total(df, con_caracteristicas),
        "clases": clase, "indicadores": indicadores,
        "nota": "Porcentajes de clases sobre todas las viviendas particulares habitadas; otras características sobre las viviendas a las que se captan características detalladas (VIVPARHAB_C). Intervalos al 90%, Taylor estrato-UPM; aproximación reproducible, no publicación oficial de precisión por indicador.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--zip", type=Path, default=None, help="ZIP de microdatos de Oaxaca ya descargado")
    parser.add_argument("--salida", type=Path, default=Path("resultados"))
    args = parser.parse_args()
    ruta = args.zip or descargar(Path("datos/eic2025_micro_20_csv.zip"))
    df = leer(ruta)
    resultado = analizar(df)
    args.salida.mkdir(parents=True, exist_ok=True)
    (args.salida / "resumen.json").write_text(json.dumps(resultado, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    filas = [{"caracteristica": k, **v} for k, v in resultado["clases"].items()]
    pd.DataFrame(filas).to_csv(args.salida / "tipos_vivienda.csv", index=False, encoding="utf-8-sig")
    filas = [{"caracteristica": k, **v} for k, v in resultado["indicadores"].items()]
    pd.DataFrame(filas).to_csv(args.salida / "indicadores.csv", index=False, encoding="utf-8-sig")
    print(f"{resultado['municipio']}: {resultado['viviendas_particulares_habitadas']['estimado']:,} viviendas estimadas")
    print(f"Resultados guardados en {args.salida.resolve()}")


if __name__ == "__main__":
    main()
