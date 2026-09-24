"""Infografía ilustrada, exacta y reproducible a partir de resultados/resumen.json."""
from __future__ import annotations

import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parent
W, H = 1080, 1920
NAVY = "#17364C"
TEAL = "#088A81"
INK = "#19374B"
MUTED = "#587180"
BG = "#F7FAF4"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size: int, bold: bool = False):
    return ImageFont.truetype(BOLD if bold else FONT, size)


def centered(draw, xy, text, f, fill):
    x, y = xy
    box = draw.textbbox((0, 0), text, font=f)
    draw.text((x - (box[2] - box[0]) / 2, y), text, font=f, fill=fill)


def icon(draw, kind: str, x: int, y: int, scale: float = 1):
    """Pequeños dibujos originales, trazados con formas geométricas."""
    s = scale
    p = lambda a, b: (int(x + a*s), int(y + b*s))
    if kind in {"house", "two", "block"}:
        if kind == "block":
            draw.rounded_rectangle((*p(4, -17), *p(58, 42)), radius=6, fill="#BED4EB", outline=NAVY, width=3)
            for xx in [14, 32, 50]:
                for yy in [-5, 13]:
                    draw.rectangle((*p(xx, yy), *p(xx+7, yy+9)), fill="#FFFFFF", outline=NAVY, width=2)
            draw.rectangle((*p(29, 29), *p(40, 42)), fill="#F7BB74", outline=NAVY, width=2)
            return
        draw.polygon([p(0, 4), p(29, -20), p(58, 4)], fill="#EB9A71")
        draw.polygon([p(5, 4), p(29, -16), p(53, 4)], fill="#F9C775")
        draw.rectangle((*p(6, 4), *p(52, 40)), fill="#FFF4DB", outline=NAVY, width=3)
        draw.rectangle((*p(23, 19), *p(36, 40)), fill="#8CCABA", outline=NAVY, width=2)
        draw.rectangle((*p(10, 13), *p(19, 22)), fill="#B7DCE9", outline=NAVY, width=2)
        if kind == "two":
            icon(draw, "house", int(x+38*s), int(y+4*s), s*.72)
        return
    if kind == "bolt":
        draw.polygon([p(30,-22),p(9,11),p(25,11),p(17,43),p(50,0),p(32,0),p(42,-22)], fill="#F3B34F", outline=NAVY, width=3)
    elif kind == "drop":
        draw.polygon([p(29,-21),p(11,9),p(8,23),p(16,37),p(29,43),p(44,37),p(50,23),p(45,8)], fill="#83D1E8", outline=NAVY, width=3)
        draw.arc((*p(17,12),*p(38,34)), 50, 150, fill="#FFFFFF", width=4)
    elif kind == "pipe":
        draw.line([p(4,-12),p(44,-12),p(44,15),p(26,15),p(26,38)], fill=NAVY, width=9, joint="curve")
        draw.polygon([p(18,33),p(34,33),p(26,47)], fill="#79C9DE")
    elif kind == "tank":
        draw.rounded_rectangle((*p(3,2),*p(58,38)), radius=7, fill="#A2DCC3", outline=NAVY, width=3)
        draw.line([p(1,2),p(60,2)], fill=NAVY, width=5)
        draw.line([p(21,2),p(21,38)], fill=NAVY, width=3)
        draw.line([p(39,2),p(39,38)], fill=NAVY, width=3)
        draw.line([p(15,-17),p(15,2)], fill=NAVY, width=5)
    elif kind == "wifi":
        for box in [(3,-13,59,43),(13,0,49,39),(23,13,39,35)]:
            draw.arc((*p(box[0],box[1]),*p(box[2],box[3])), 200, 340, fill=NAVY, width=5)
        draw.ellipse((*p(27,36),*p(35,44)), fill=NAVY)
    elif kind == "key":
        draw.ellipse((*p(2,-12),*p(31,17)), outline=NAVY, width=5)
        draw.line([p(30,3),p(59,3),p(59,14),p(51,14),p(51,22),p(43,22),p(43,14)], fill=NAVY, width=5)


def draw_image(r: dict, output: Path) -> None:
    image = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(image)
    d.rectangle((0, 0, W, 305), fill=NAVY)
    d.ellipse((842, 35, 942, 135), fill="#F7C366")
    d.polygon([(0,285),(155,257),(310,287),(525,253),(750,287),(930,248),(1080,267),(1080,305),(0,305)], fill="#1B6268")
    icon(d, "house", 860, 221, 1.3)
    icon(d, "two", 952, 237, .85)
    d.text((60, 40), "UNA MIRADA A NUESTRO MUNICIPIO", font=font(23,True), fill="#B9E6DD")
    d.text((60, 91), "Viviendas en", font=font(60,True), fill="white")
    d.text((60, 157), "San Pedro Mixtepec #22", font=font(48,True), fill="white")
    d.text((60, 238), "Oaxaca  ·  EIC 2025  ·  Clave 20318", font=font(25), fill="#E3F3ED")

    d.rounded_rectangle((50, 327, 1030, 508), radius=31, fill="white", outline="#DCE8E4", width=3)
    icon(d, "house", 91, 408, 1.15)
    d.text((194, 360), f"{r['viviendas_particulares_habitadas']['estimado']:,}".replace(",", " "), font=font(78,True), fill=TEAL)
    d.text((605, 365), "viviendas particulares", font=font(28,True), fill=INK)
    d.text((605, 405), "habitadas estimadas", font=font(28,True), fill=INK)
    d.text((194, 468), "Intervalo aproximado al 90%: 17 226 a 20 316", font=font(22), fill=MUTED)

    d.rounded_rectangle((50, 535, 1030, 967), radius=31, fill="white", outline="#DCE8E4", width=3)
    d.text((90, 572), "¿Qué tipo de viviendas hay?", font=font(35,True), fill=INK)
    d.text((90, 626), "% de 18 771 viviendas particulares habitadas", font=font(21), fill=MUTED)
    types = [
        ("Casa única en su terreno", "Casa única en el terreno", "house"),
        ("Casa que comparte terreno", "Casa que comparte terreno", "two"),
        ("Vecindad o cuartería", "Vivienda en vecindad o cuartería", "block"),
    ]
    for i, (label, key, glyph) in enumerate(types):
        y = 689 + i*95
        icon(d,glyph,93,y+13,.83)
        d.text((191,y-2),label,font=font(26,True),fill=INK)
        pct = r["clases"][key]["porcentaje"]
        d.rounded_rectangle((191,y+48,825,y+69),radius=10,fill="#E5EEEB")
        d.rounded_rectangle((191,y+48,int(191+634*pct/100),y+69),radius=10,fill=TEAL)
        d.text((843,y+32),f"{pct:.2f}%",font=font(27,True),fill=INK)

    d.rounded_rectangle((50, 996, 1030, 1740), radius=31, fill="white", outline="#DCE8E4", width=3)
    d.text((90, 1029), "Servicios y vida cotidiana", font=font(35,True), fill=INK)
    cards=[
        ("Electricidad","Con electricidad","bolt","#FFF1D9"),
        ("Agua dentro de casa","Agua entubada dentro de la vivienda","drop","#E2F5F8"),
        ("Drenaje a red pública","Drenaje conectado a red pública","pipe","#E5F0FA"),
        ("Drenaje a fosa o tanque","Drenaje conectado a fosa o tanque séptico","tank","#E5F5EB"),
        ("Internet","Con internet","wifi","#EEECFB"),
        ("Vivienda rentada","Se paga renta","key","#FCEBDD"),
    ]
    for i,(label,key,glyph,fill) in enumerate(cards):
        col,row=i%2,i//2
        x,y=82+col*469,1093+row*196
        d.rounded_rectangle((x,y,x+447,y+171),radius=23,fill=fill)
        icon(d,glyph,x+23,y+59,.84)
        d.text((x+97,y+25),label,font=font(22,True),fill=INK)
        val=r["indicadores"][key]
        d.text((x+97,y+66),f"{val['porcentaje']:.2f}%",font=font(45,True),fill=NAVY)
        d.text((x+97,y+132),f"{val['estimado']:,} viviendas".replace(","," "),font=font(19),fill=MUTED)
    d.rounded_rectangle((80, 1684, 1000, 1723), radius=14, fill="#E7F3EE")
    centered(d,(540,1691),"% de 18 674 viviendas con características",font(21),INK)
    d.rounded_rectangle((50, 1763, 1030, 1887), radius=24, fill="#E7F3EE")
    d.text((80,1785),"Fuente: INEGI, microdatos EIC 2025.",font=font(21,True),fill=INK)
    d.text((80,1821),"Elaboración independiente. Excluye inmuebles deshabitados.",font=font(19),fill=MUTED)
    output.parent.mkdir(parents=True,exist_ok=True)
    image.save(output, optimize=True)


if __name__ == "__main__":
    r=json.loads((BASE/"resultados/resumen.json").read_text(encoding="utf-8"))
    draw_image(r,BASE/"resultados/infografia.png")
