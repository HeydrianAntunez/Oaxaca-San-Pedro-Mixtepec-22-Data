"""Crea cinco infografías PNG de las conclusiones verificadas de la EIC 2025.

Uso: python crear_infografias.py
Fuente numérica: resultados/auditoria.json, generado por validar_conclusiones.py.
"""
from __future__ import annotations

import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
DEST = ROOT / "infografias"
DEST.mkdir(exist_ok=True)
AUDIT = json.loads((ROOT / "resultados/auditoria.json").read_text(encoding="utf-8"))
SUMMARY = json.loads((ROOT / "resultados/resumen.json").read_text(encoding="utf-8"))["indicadores"]
W, H = 1080, 1350
NAVY = "#1D394D"
TEAL = "#067F80"
TURQ = "#D7F1EC"
YELLOW = "#F6C96B"
PAPER = "#FCFCF8"
INK = "#253B4C"
MUTED = "#526B79"
PINK = "#FCE8DF"
BLUE = "#E4F2FC"
FONT_PAIRS = [
    ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
     "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
    ("C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/arialbd.ttf"),
    ("/System/Library/Fonts/Supplemental/Arial.ttf",
     "/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
]
FONT, BOLD = next(((a,b) for a,b in FONT_PAIRS if Path(a).exists() and Path(b).exists()), (None,None))
if FONT is None:
    raise FileNotFoundError("Instala DejaVu Sans o Arial para generar las infografías")

def f(size, bold=False): return ImageFont.truetype(BOLD if bold else FONT, size)
def centered(d, text, y, font, fill, box=(0,W)):
    width = d.textbbox((0,0),text,font=font)[2]
    d.text((box[0]+(box[1]-box[0]-width)/2,y),text,font=font,fill=fill)
def line(d, text, x,y, size=31, color=INK, bold=False): d.text((x,y),text,font=f(size,bold),fill=color)
def rect(d, box, fill, radius=30, outline=None, width=2): d.rounded_rectangle(box,radius=radius,fill=fill,outline=outline,width=width)
def pct(v): return f"{v:.2f}".replace(".",",") + " %"

def icon(d, name, x, y, scale=1):
    """Dibujos sencillos de apoyo, sin codificar cantidades."""
    def oval(b,c): d.ellipse(tuple(int(x+z*scale) if i%2==0 else int(y+z*scale) for i,z in enumerate(b)),fill=c)
    def box(b,c,r=8):
        x0,y0,x1,y1=b;rect(d,(x+x0*scale,y+y0*scale,x+x1*scale,y+y1*scale),c,r*scale)
    if name=="people":
        for a,b,c in [(8,40,YELLOW),(64,10,TURQ),(118,42,PINK)]:
            oval((a,b,a+39,b+39),c); box((a-5,b+43,a+44,b+112),c,18)
    elif name=="speech":
        box((4,12,148,92),TURQ,23); d.polygon([(x+35*scale,y+88*scale),(x+25*scale,y+119*scale),(x+70*scale,y+89*scale)],fill=TURQ)
        for a in (42,75,108): oval((a,46,a+11,57),NAVY)
    elif name=="health":
        oval((10,10,139,139),TURQ); box((58,35,90,112),TEAL,5);box((36,57,112,89),TEAL,5)
    elif name=="work":
        box((7,47,152,133),TURQ,13);box((57,23,104,56),YELLOW,9);box((76,49,86,128),NAVY,3)
    elif name=="shop":
        box((10,50,147,137),TURQ,8);d.polygon([(x+5*scale,y+50*scale),(x+151*scale,y+50*scale),(x+133*scale,y+22*scale),(x+23*scale,y+22*scale)],fill=YELLOW)
        box((61,80,96,137),PAPER,4)

def base(number, title1, title2, icon_name, source):
    im=Image.new("RGB",(W,H),PAPER); d=ImageDraw.Draw(im)
    d.rectangle((0,0,W,342),fill=NAVY)
    d.polygon([(0,319),(220,285),(530,337),(780,300),(W,334),(W,365),(0,365)],fill="#236068")
    line(d,"UNA MIRADA A NUESTRA COMUNIDAD",55,46,26,TURQ,True)
    line(d,f"{number} / 5",932,45,29,YELLOW,True)
    line(d,title1,55,125,53,PAPER,True)
    line(d,title2,55,193,53,PAPER,True)
    line(d,"San Pedro Mixtepec #22 · Oaxaca · EIC 2025",55,288,27,PAPER)
    icon(d,icon_name,873,130,.9)
    d.line((53,1195,1027,1195),fill="#C9DAD8",width=3)
    line(d,"Fuente: INEGI · personas20.csv · CVEGEO 20318",55,1222,22,MUTED,True)
    line(d,source,55,1260,20,MUTED)
    line(d,"Estimaciones ponderadas · lectura y fuentes: FUENTES_INEGI.md",55,1298,19,MUTED)
    return im,d

def bar(d,x,y,length,val,maxval=100,color=TEAL,width=650):
    rect(d,(x,y,x+width,y+24),"#E8F0EF",12)
    rect(d,(x,y,x+max(8,width*val/maxval),y+24),color,12)

def save(im,name):
    path=DEST/name
    im.quantize(colors=128,method=Image.Quantize.FASTOCTREE).save(path,optimize=True)
    print(path)

def graphic1():
    im,d=base("1","Edades de la","población","people","Control INEGI: POBTOT, POB0_14 y POB65_MAS; hoja y celdas en FUENTES_INEGI.md")
    rect(d,(48,371,1032,1157),"#FFFFFF",outline="#D2E3E2")
    line(d,"57 844",88,398,81,TEAL,True)
    line(d,"habitantes estimados",465,445,31,INK,True)
    line(d,"Distribución por grupos de edad",88,543,35,NAVY,True)
    groups=[("0 a 14",SUMMARY["edad_0-14"]["porcentaje"]),
            ("15 a 29",SUMMARY["edad_15-29"]["porcentaje"]),
            ("30 a 44",SUMMARY["edad_30-44"]["porcentaje"]),
            ("45 a 64",SUMMARY["edad_45-64"]["porcentaje"]),
            ("65 y más",SUMMARY["edad_65+"]["porcentaje"])]
    for i,(label,v) in enumerate(groups):
        y=627+i*82
        line(d,label,88,y,28,INK,True)
        bar(d,285,y+10,0,v,27,YELLOW if i==4 else TEAL,527)
        line(d,pct(v),839,y,27,NAVY,True)
    rect(d,(82,1058,998,1135),TURQ,18)
    centered(d,"Menores de 15: 13 267 · 65 y más: 4 365",1081,f(26,True),NAVY)
    save(im,"01_edades.png")

def graphic2():
    im,d=base("2","Identidad y","lengua indígena","speech","Control INEGI: PCN_POB_IND y PCN_P3YM_HLI; bases de distinta edad")
    rect(d,(48,377,1032,1165),"#FFFFFF",outline="#D2E3E2")
    rect(d,(79,409,1001,705),TURQ,26)
    line(d,pct(AUDIT["indigena"][1]),113,448,79,TEAL,True)
    line(d,"se considera indígena",113,557,39,NAVY,True)
    line(d,"23 777 de 57 844 personas",113,624,27,MUTED)
    rect(d,(79,737,1001,1002),BLUE,26)
    line(d,pct(AUDIT["habla_lengua_3mas"][1]),113,779,79,NAVY,True)
    line(d,"habla una lengua indígena",113,888,38,NAVY,True)
    line(d,"2 277 de 55 647 personas de 3 años y más",113,950,25,MUTED)
    rect(d,(79,1032,1001,1134),"#FFF5DD",18)
    line(d,"Son preguntas y grupos de edad distintos.",108,1053,29,NAVY,True)
    line(d,"No se restan ni se interpretan como el mismo grupo.",108,1094,22,MUTED)
    save(im,"02_identidad_lengua.png")

def graphic3():
    im,d=base("3","Servicios de","salud","health","Control INEGI: PCN_PSINDER y PCN_PUSU_IPRIV; denominadores visibles")
    rect(d,(48,377,1032,1165),"#FFFFFF",outline="#D2E3E2")
    rect(d,(80,409,1000,720),PINK,26)
    line(d,pct(AUDIT["sin_afiliacion"][1]),112,447,79,NAVY,True)
    line(d,"sin afiliación declarada",112,556,35,NAVY,True)
    line(d,"30 402 de 57 844 personas",112,619,27,MUTED)
    bar(d,112,676,0,52.56,100,TEAL,816)
    rect(d,(80,745,1000,1045),BLUE,26)
    line(d,pct(AUDIT["atencion_privada_todos"][1]),112,783,79,TEAL,True)
    line(d,"se atiende en servicios privados",112,894,31,NAVY,True)
    line(d,"21 348 de 57 844 personas",112,952,26,MUTED)
    line(d,"Entre usuarios de algún servicio: 37,82 % (INEGI).",112,1000,22,MUTED)
    rect(d,(80,1070,1000,1138),"#FFF5DD",18)
    centered(d,"Afiliación y lugar de atención son preguntas diferentes.",1088,f(24,True),NAVY)
    save(im,"03_salud.png")

def graphic4():
    im,d=base("4","Participación y","trabajo","work","PEA por sexo de 12+; prestación entre asalariados · cálculo propio")
    rect(d,(48,377,1032,1165),"#FFFFFF",outline="#D2E3E2")
    line(d,"Participación económica, 12 años y más",83,421,33,NAVY,True)
    line(d,"Mujeres",84,505,30,INK,True)
    line(d,pct(AUDIT["participacion_mujeres_12mas"][1]),771,500,31,TEAL,True)
    bar(d,84,555,0,53.26,100,TEAL,902)
    line(d,"13 450 de 25 253",84,589,23,MUTED)
    line(d,"Hombres",84,660,30,INK,True)
    line(d,pct(AUDIT["participacion_hombres_12mas"][1]),771,655,31,NAVY,True)
    bar(d,84,710,0,77.72,100,NAVY,902)
    line(d,"17 357 de 22 333",84,744,23,MUTED)
    rect(d,(83,814,997,905),TURQ,22)
    gap=AUDIT["participacion_hombres_12mas"][1]-AUDIT["participacion_mujeres_12mas"][1]
    centered(d,f"Diferencia descriptiva: {gap:.2f} puntos".replace(".",","),838,f(31,True),NAVY)
    rect(d,(83,936,997,1136),"#FFF4D9",22)
    line(d,pct(AUDIT["servicio_medico_laboral"][1]),108,963,58,TEAL,True)
    line(d,"declara servicio médico",433,978,29,NAVY,True)
    line(d,"por su trabajo",433,1018,29,NAVY,True)
    line(d,"5 450 de 18 999 personas asalariadas",108,1088,25,MUTED)
    save(im,"04_trabajo.png")

def graphic5():
    im,d=base("5","Sectores de","actividad","shop","Claves 46, 72, 23 de ACTIVIDADES_C; 30 544 personas ocupadas")
    rect(d,(48,377,1032,1165),"#FFFFFF",outline="#D2E3E2")
    rect(d,(80,408,1000,632),TURQ,26)
    line(d,pct(AUDIT["tres_sectores"][1]),109,448,84,TEAL,True)
    line(d,"en tres sectores del negocio",110,553,31,NAVY,True)
    line(d,"14 312 de 30 544 personas ocupadas",84,658,26,MUTED)
    groups=[("Comercio minorista",AUDIT["sectores"]["46"][1],"5 657"),
            ("Alojamiento y alimentos",AUDIT["sectores"]["72"][1],"5 010"),
            ("Construcción",AUDIT["sectores"]["23"][1],"3 645")]
    for i,(label,v,n) in enumerate(groups):
        y=724+i*121
        line(d,label,84,y,31,INK,True)
        line(d,pct(v),817,y,29,NAVY,True)
        bar(d,84,y+48,0,v,20,TEAL if i<2 else YELLOW,738)
        line(d,n,844,y+49,24,MUTED)
    rect(d,(82,1093,998,1150),"#FFF5DD",16)
    centered(d,"Se clasifica el negocio; no el oficio ni el turismo.",1108,f(23,True),NAVY)
    save(im,"05_sectores.png")

if __name__=="__main__":
    for make in (graphic1,graphic2,graphic3,graphic4,graphic5): make()
