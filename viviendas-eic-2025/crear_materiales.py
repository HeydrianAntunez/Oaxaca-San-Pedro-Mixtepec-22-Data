"""Crea PDF e infografía con los resultados reproducidos por analizar_viviendas.py."""
from __future__ import annotations

import json
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether

ROOT = Path(__file__).resolve().parent
RESULTADOS = ROOT / "resultados"
JSON = RESULTADOS / "resumen.json"
AZUL = "#10273D"
TURQUESA = "#008C86"
CORAL = "#F0A766"
GRIS = "#4B6070"


def cargar() -> dict:
    if not JSON.exists():
        raise SystemExit("Primero ejecuta python analizar_viviendas.py")
    return json.loads(JSON.read_text(encoding="utf-8"))


def ficha(ax, x, y, w, h, valor, rotulo, color=TURQUESA):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.01,rounding_size=0.02",
                                facecolor="white", edgecolor="#D6E1E4", linewidth=1))
    ax.text(x + 0.03, y + h - 0.016, valor, va="top", fontsize=29, fontweight="bold", color=color)
    ax.text(x + 0.03, y + 0.012, rotulo, va="bottom", fontsize=12, color=AZUL)


def barra(ax, y, etiqueta, porcentaje, color=TURQUESA):
    ax.text(0.07, y + 0.022, etiqueta, fontsize=12, color=AZUL, va="bottom")
    ax.add_patch(FancyBboxPatch((0.07, y - 0.017), 0.75, 0.028,
                                boxstyle="round,pad=0,rounding_size=0.012", facecolor="#DCE7E7", linewidth=0))
    ax.add_patch(FancyBboxPatch((0.07, y - 0.017), 0.75 * porcentaje / 100, 0.028,
                                boxstyle="round,pad=0,rounding_size=0.012", facecolor=color, linewidth=0))
    valor = Decimal(str(porcentaje)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
    ax.text(0.91, y - 0.001, f"{valor}%", fontsize=14, fontweight="bold", ha="right", color=AZUL)


def infografia(r: dict) -> None:
    from infografia_ilustrada import draw_image
    draw_image(r, RESULTADOS / "infografia.png")
    return
    plt.rcParams.update({"font.family": "DejaVu Sans", "figure.facecolor": "#F6F9F8"})
    fig = plt.figure(figsize=(8, 12), dpi=200)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.add_patch(FancyBboxPatch((0, 0.835), 1, 0.165, boxstyle="square,pad=0",
                                linewidth=0, facecolor=AZUL))
    ax.text(0.065, 0.970, "SAN PEDRO MIXTEPEC · DISTRITO 22", color="#B9DDD9", fontsize=12, fontweight="bold")
    ax.text(0.065, 0.920, "Así son sus viviendas", color="white", fontsize=29, fontweight="bold")
    ax.text(0.065, 0.878, "Oaxaca  ·  EIC 2025  ·  clave 20318", color="#DCE8E9", fontsize=13)
    ficha(ax, 0.06, 0.736, 0.88, 0.080, "18 771", "viviendas particulares habitadas estimadas")
    ax.text(0.07, 0.716, "Intervalo aproximado 90%: 17 226–20 316", fontsize=10.5, color=GRIS)

    ax.text(0.065, 0.673, "TIPO DE VIVIENDA", fontsize=14, fontweight="bold", color=AZUL)
    for y, name, short in [(0.620, "Casa única en el terreno", "Casa única en terreno"),
                            (0.562, "Casa que comparte terreno", "Casa que comparte terreno"),
                            (0.504, "Vivienda en vecindad o cuartería", "Vecindad o cuartería")]:
        barra(ax, y, short, r["clases"][name]["porcentaje"])
    ax.text(0.065, 0.463, "% de 18 771 viviendas habitadas", fontsize=10, color=GRIS)
    ax.plot([0.065, 0.935], [0.445, 0.445], color="#C8D8DB", linewidth=1)

    ax.text(0.065, 0.409, "SERVICIOS Y VIDA COTIDIANA", fontsize=14, fontweight="bold", color=AZUL)
    names = ["Con electricidad", "Agua entubada dentro de la vivienda",
             "Drenaje conectado a red pública", "Drenaje conectado a fosa o tanque séptico",
             "Con internet", "Se paga renta"]
    labels = ["Electricidad", "Agua dentro de la vivienda", "Drenaje a red pública",
              "Drenaje a fosa o tanque séptico", "Internet", "Vivienda rentada"]
    for i, (name, label) in enumerate(zip(names, labels)):
        barra(ax, 0.368 - i * 0.057, label, r["indicadores"][name]["porcentaje"],
              CORAL if i in (2, 5) else TURQUESA)
    ax.text(0.065, 0.047, "% de 18 674 viviendas con características", fontsize=10, color=GRIS)
    ax.text(0.065, 0.024,
            "Fuente: INEGI, microdatos EIC 2025. Elaboración independiente.\n"
            "Estimaciones ponderadas; excluye viviendas deshabitadas y otros inmuebles.",
            fontsize=8.6, color=GRIS, va="top", linespacing=1.3)
    fig.savefig(RESULTADOS / "infografia.png", dpi=200, facecolor=fig.get_facecolor())
    plt.close(fig)


def pdf(r: dict) -> None:
    target = RESULTADOS / "informe.pdf"
    doc = SimpleDocTemplate(str(target), pagesize=(21 * cm, 29.7 * cm),
                            leftMargin=2.1 * cm, rightMargin=2.1 * cm,
                            topMargin=2.1 * cm, bottomMargin=1.9 * cm)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="TituloPropio", parent=styles["Title"], fontName="Helvetica-Bold",
                              fontSize=19, leading=24, textColor=colors.HexColor(AZUL), spaceAfter=12))
    styles.add(ParagraphStyle(name="SeccionPropia", parent=styles["Heading2"], fontSize=12.7, leading=16,
                              textColor=colors.HexColor(TURQUESA), spaceBefore=13, spaceAfter=6))
    styles.add(ParagraphStyle(name="TextoPropio", parent=styles["BodyText"], fontSize=9.5, leading=14,
                              textColor=colors.HexColor(AZUL), spaceAfter=8))
    styles.add(ParagraphStyle(name="NotaPropia", parent=styles["BodyText"], fontSize=8, leading=11,
                              textColor=colors.HexColor(GRIS), spaceAfter=7))
    styles.add(ParagraphStyle(name="CeldaPropia", parent=styles["BodyText"], fontSize=8.2, leading=11,
                              textColor=colors.HexColor(AZUL)))
    P = lambda s: Paragraph(s, styles["TextoPropio"])
    H = lambda s: Paragraph(s, styles["SeccionPropia"])
    N = lambda s: Paragraph(s, styles["NotaPropia"])
    C = lambda s: Paragraph(s, styles["CeldaPropia"])

    def tabla(filas, anchos):
        t = Table([[C(str(c)) for c in row] for row in filas], colWidths=anchos, repeatRows=1, hAlign="LEFT")
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DCEFEB")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F5F8F8")]),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7), ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LINEBELOW", (0, 0), (-1, 0), .5, colors.HexColor(TURQUESA)),
        ]))
        return t

    story = [Paragraph("Cómo son las viviendas de San Pedro Mixtepec", styles["TituloPropio"]),
             N("Distrito 22, Oaxaca · Clave 20318 · Encuesta Intercensal 2025"),
             P("La EIC estima <b>18 771 viviendas particulares habitadas</b> en el municipio "
               "(intervalo aproximado al 90%: <b>17 226 a 20 316</b>). La casa única en su terreno "
               "es la clase más frecuente. Entre las viviendas con características, la electricidad "
               "es casi universal, mientras que el drenaje conectado a la red pública es minoritario."),
             H("Tipos de vivienda")]
    seleccion = ["Casa única en el terreno", "Casa que comparte terreno", "Vivienda en vecindad o cuartería",
                 "Departamento en edificio", "Casa dúplex", "Local no construido para habitación",
                 "Vivienda móvil", "Refugio", "No especificado"]
    filas = [["Clase", "Estimadas", "% de 18 771"]]
    for nombre in seleccion:
        v = r["clases"][nombre]
        filas.append([nombre, f"{v['estimado']:,}".replace(",", " "), f"{v['porcentaje']:.2f}%"])
    story += [tabla(filas, [9.3 * cm, 3.3 * cm, 3.6 * cm]),
              N("La suma de porcentajes puede diferir ligeramente de 100% por el redondeo. "
                "Las clases con muy pocos casos tienen mayor incertidumbre."),
              H("Materiales y espacio"),
              P("De las <b>18 674 viviendas con características</b>, 93.28% tienen paredes predominantemente "
                "de tabique, ladrillo, block, piedra, cantera, cemento o concreto; 64.89% techo de losa "
                "y 26.04% techo de lámina metálica. El piso es de cemento o firme en 69.15%, de madera, "
                "mosaico u otro recubrimiento en 27.60% y de tierra en 3.25%. "
                "El 23.24% tiene un cuarto total y el 44.71% un dormitorio."),
              PageBreak(),
              Paragraph("Servicios, equipamiento y tenencia", styles["TituloPropio"]),
              N("Porcentajes sobre 18 674 viviendas con características; intervalos aproximados al 90%")]
    services = ["Agua entubada dentro de la vivienda", "Agua entubada solo en patio o terreno",
                "Drenaje conectado a red pública", "Drenaje conectado a fosa o tanque séptico",
                "Con electricidad", "Con internet", "Con refrigerador", "Con lavadora", "Se paga renta"]
    filas = [["Característica", "Estimadas", "%", "Intervalo 90%"]]
    for nombre in services:
        v = r["indicadores"][nombre]
        filas.append([nombre, f"{v['estimado']:,}".replace(",", " "),
                      f"{v['porcentaje']:.2f}%", f"{v['ic90_porcentaje'][0]:.2f}–{v['ic90_porcentaje'][1]:.2f}%"])
    story += [tabla(filas, [7.3 * cm, 2.8 * cm, 2.3 * cm, 3.8 * cm]),
              Spacer(1, 0.3 * cm),
              P("La fosa o tanque séptico se registra como <b>una forma de drenaje</b>; no equivale "
                "a ausencia de drenaje. Agua entubada en el patio tampoco significa carencia de agua entubada. "
                "El 1.94% carece de esta última y el 1.05% no tiene drenaje."),
              P("En 59.69% de las viviendas con características vive la persona propietaria, en 28.33% "
                "se paga renta y en 10.91% se ocupa una vivienda prestada o de un familiar."),
              H("Cómo leer estas cifras"),
              P("Se multiplicó cada registro por su factor de expansión. Los porcentajes de clases "
                "usan las 18 771 viviendas particulares habitadas; las preguntas detalladas, las "
                "18 674 con características. Se estimó la precisión con estratos y pares estrato-UPM por "
                "linearización de Taylor y un nivel de confianza de 90%. Los intervalos son una "
                "aproximación independiente, no los intervalos oficiales de INEGI."),
              P("Los resultados describen 2025: <b>no miden crecimiento</b> ni cuentan viviendas "
                "deshabitadas, de uso temporal o todos los inmuebles. Para replicar cálculos, consultar "
                "<i>METODOLOGIA.md</i> y <i>analizar_viviendas.py</i> en el proyecto."),
              N("Fuente: INEGI, EIC 2025, microdatos de Oaxaca (`viviendas20.csv`) y descriptor de "
                "microdatos; diseño de la muestra, producto 889463931140. Elaboración independiente. "
                "Consulta: 24 de septiembre de 2026. https://www.inegi.org.mx/programas/eic/2025/")]

    def pie(canvas, d):
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#B8CFD1"))
        canvas.line(2 * cm, 1.5 * cm, 19 * cm, 1.5 * cm)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor(GRIS))
        canvas.drawString(2.1 * cm, 1.13 * cm, "Viviendas · San Pedro Mixtepec · EIC 2025")
        canvas.drawRightString(18.9 * cm, 1.13 * cm, f"{d.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=pie, onLaterPages=pie)


def main() -> None:
    r = cargar()
    RESULTADOS.mkdir(parents=True, exist_ok=True)
    infografia(r)
    pdf(r)
    print("Listos: resultados/infografia.png y resultados/informe.pdf")


if __name__ == "__main__":
    main()
