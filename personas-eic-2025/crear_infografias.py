"""Cinco infografías ilustradas, reproducibles desde la auditoría EIC 2025.

Ejecute: python crear_infografias.py
Las figuras son decorativas; cada porcentaje declara su universo estadístico.
"""
from __future__ import annotations

import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parent
OUT = BASE / "infografias"
OUT.mkdir(exist_ok=True)
A = json.loads((BASE / "resultados/auditoria.json").read_text(encoding="utf8"))
S = json.loads((BASE / "resultados/resumen.json").read_text(encoding="utf8"))["indicadores"]
W, H = 1080, 1600
NAVY, INK, TEAL = "#19384D", "#244052", "#087F7C"
MUTED, BG = "#526C78", "#F8FAF7"
MINT, SKY, PEACH, SUN, LILAC = "#DDF4ED", "#E8F4FA", "#FCEADD", "#FFECC5", "#EEEAFB"
WHITE, LINE = "#FFFFFF", "#D7E5E1"
FONTS = [
    ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
    ("C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/arialbd.ttf"),
    ("/System/Library/Fonts/Supplemental/Arial.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
]
REGULAR, BOLD = next(((a,b) for a,b in FONTS if Path(a).exists() and Path(b).exists()), (None,None))
if not REGULAR:
    raise FileNotFoundError("Se requiere DejaVu Sans o Arial")

def font(n, bold=False): return ImageFont.truetype(BOLD if bold else REGULAR, n)
def txt(d, x, y, value, n=28, color=INK, bold=False):
    d.text((x,y), value, font=font(n,bold), fill=color)
def center(d, y, value, n=28, color=INK, bold=False, left=0, right=W):
    width=d.textbbox((0,0),value,font=font(n,bold))[2]
    txt(d, left+(right-left-width)/2,y,value,n,color,bold)
def rr(d, box, fill, r=28, outline=None, width=2):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)
def fmt(v): return f"{v:.2f}".replace(".",",")+" %"
def bar(d, x,y,w,value,maxval=100,color=TEAL):
    rr(d,(x,y,x+w,y+19),"#E3EBEA",10)
    rr(d,(x,y,x+max(10,round(w*value/maxval)),y+19),color,10)

def person(d,x,y,s=1,skin="#C98161",shirt="#F8C36C",pants=NAVY,hair=NAVY,skirt=False):
    """Personaje ilustrado; no representa una categoría ni un conteo."""
    p=lambda xx,yy:(round(x+xx*s),round(y+yy*s))
    thick=max(2,round(3*s))
    d.ellipse((*p(16,3),*p(65,52)),fill=skin,outline=NAVY,width=thick)
    d.pieslice((*p(14,-4),*p(67,39)),180,355,fill=hair)
    d.ellipse((*p(33,32),*p(36,35)),fill=NAVY)
    d.ellipse((*p(51,32),*p(54,35)),fill=NAVY)
    d.arc((*p(35,35),*p(54,47)),10,160,fill=NAVY,width=thick)
    d.rounded_rectangle((*p(1,54),*p(81,126)),radius=round(17*s),fill=shirt,outline=NAVY,width=thick)
    d.line([p(11,67),p(-8,116)],fill=skin,width=max(5,round(13*s)))
    d.line([p(71,67),p(92,115)],fill=skin,width=max(5,round(13*s)))
    if skirt:
        d.polygon([p(13,121),p(68,121),p(82,172),p(0,172)],fill=pants)
        d.line([p(20,172),p(16,196)],fill=NAVY,width=max(5,round(10*s)))
        d.line([p(62,172),p(66,196)],fill=NAVY,width=max(5,round(10*s)))
    else:
        d.rounded_rectangle((*p(5,120),*p(76,169)),radius=round(6*s),fill=pants)
        d.line([p(24,168),p(20,196)],fill=NAVY,width=max(5,round(11*s)))
        d.line([p(58,168),p(62,196)],fill=NAVY,width=max(5,round(11*s)))
    d.line([p(6,197),p(30,197)],fill=NAVY,width=max(4,round(7*s)))
    d.line([p(52,197),p(77,197)],fill=NAVY,width=max(4,round(7*s)))

def bubble(d,x,y,s=1,fill=WHITE):
    p=lambda a,b:(round(x+a*s),round(y+b*s))
    d.rounded_rectangle((*p(0,0),*p(120,76)),radius=round(24*s),fill=fill,outline=NAVY,width=max(2,round(3*s)))
    d.polygon([p(22,71),p(16,101),p(50,74)],fill=fill)
    for xx in (32,60,88): d.ellipse((*p(xx,32),*p(xx+8,40)),fill=TEAL)

def clinic(d,x,y,s=1):
    p=lambda a,b:(round(x+a*s),round(y+b*s))
    d.rounded_rectangle((*p(10,36),*p(172,176)),radius=round(14*s),fill=WHITE,outline=NAVY,width=max(2,round(3*s)))
    d.rectangle((*p(50,10),*p(134,52)),fill="#F9C578",outline=NAVY,width=max(2,round(3*s)))
    d.rectangle((*p(80,14),*p(105,48)),fill=TEAL)
    d.rectangle((*p(68,25),*p(116,37)),fill=TEAL)
    for xx in (32,127):
        d.rounded_rectangle((*p(xx,74),*p(xx+25,109)),radius=round(5*s),fill=SKY,outline=NAVY,width=max(2,round(2*s)))
    d.rounded_rectangle((*p(76,115),*p(112,176)),radius=round(6*s),fill=MINT,outline=NAVY,width=max(2,round(3*s)))

def briefcase(d,x,y,s=1):
    p=lambda a,b:(round(x+a*s),round(y+b*s))
    d.rounded_rectangle((*p(0,33),*p(124,117)),radius=round(12*s),fill="#F5BE72",outline=NAVY,width=max(2,round(4*s)))
    d.arc((*p(39,1),*p(84,63)),180,360,fill=NAVY,width=max(3,round(7*s)))
    d.line([p(0,68),p(124,68)],fill=NAVY,width=max(2,round(3*s)))
    d.rounded_rectangle((*p(52,60),*p(72,78)),radius=round(3*s),fill=WHITE,outline=NAVY,width=max(2,round(2*s)))

def shop(d,x,y,s=1):
    p=lambda a,b:(round(x+a*s),round(y+b*s))
    d.rounded_rectangle((*p(11,63),*p(169,171)),radius=round(7*s),fill=WHITE,outline=NAVY,width=max(2,round(3*s)))
    d.polygon([p(0,63),p(21,22),p(161,22),p(180,63)],fill="#F4BE70",outline=NAVY,width=max(2,round(3*s)))
    for i,fill in enumerate((PEACH,WHITE,PEACH,WHITE,PEACH)):
        d.rectangle((*p(9+i*33,50),*p(42+i*33,76)),fill=fill,outline=NAVY,width=max(2,round(2*s)))
    d.rectangle((*p(27,100),*p(76,140)),fill=SKY,outline=NAVY,width=max(2,round(2*s)))
    d.rectangle((*p(113,99),*p(150,171)),fill=MINT,outline=NAVY,width=max(2,round(2*s)))

def plate(d,x,y,s=1):
    p=lambda a,b:(round(x+a*s),round(y+b*s))
    d.ellipse((*p(19,29),*p(153,163)),fill=WHITE,outline=NAVY,width=max(2,round(4*s)))
    d.ellipse((*p(44,54),*p(128,138)),fill=SUN,outline=TEAL,width=max(2,round(3*s)))
    d.ellipse((*p(70,79),*p(104,113)),fill="#F3A36D")
    d.line([p(0,45),p(0,150)],fill=NAVY,width=max(3,round(5*s)))
    for xx in (-12,0,12): d.line([p(xx,45),p(xx,90)],fill=NAVY,width=max(2,round(3*s)))
    d.line([p(173,45),p(173,152)],fill=NAVY,width=max(3,round(6*s)))

def building(d,x,y,s=1):
    p=lambda a,b:(round(x+a*s),round(y+b*s))
    d.rectangle((*p(20,39),*p(154,173)),fill=SKY,outline=NAVY,width=max(2,round(4*s)))
    d.polygon([p(8,43),p(87,0),p(167,43)],fill="#F7C46D",outline=NAVY,width=max(2,round(3*s)))
    for xx in (42,102):
        for yy in (63,105): d.rectangle((*p(xx,yy),*p(xx+28,yy+27)),fill=WHITE,outline=NAVY,width=max(2,round(2*s)))
    d.rectangle((*p(78,135),*p(103,173)),fill=MINT,outline=NAVY,width=max(2,round(2*s)))

def base(number, title1, title2, mark):
    im=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(im)
    d.rectangle((0,0,W,324),fill=NAVY)
    d.ellipse((895,35,1010,150),fill="#F8C568")
    d.polygon([(0,305),(168,282),(370,305),(565,275),(771,309),(952,275),(1080,302),(1080,328),(0,328)],fill="#20636A")
    txt(d,54,35,"UNA MIRADA A NUESTRA COMUNIDAD",24,MINT,True)
    txt(d,777,35,f"{number} / 5",27,"#F9CE74",True)
    txt(d,54,104,title1,53,WHITE,True)
    txt(d,54,170,title2,53,WHITE,True)
    txt(d,55,264,"San Pedro Mixtepec #22  ·  Oaxaca  ·  EIC 2025",25,WHITE)
    # Escena decorativa pequeña, reconocible en cada portada.
    if mark=="people":
        person(d,841,126,.63,"#C88E71","#F5C569")
        person(d,910,104,.76,"#A97858",MINT)
    elif mark=="speech":
        bubble(d,851,132,1.08,MINT)
    elif mark=="health":
        clinic(d,855,103,.86)
    elif mark=="work":
        briefcase(d,873,153,1.0)
    else:
        shop(d,869,115,.82)
    d.line((52,1452,1027,1452),fill=LINE,width=3)
    txt(d,54,1471,"FUENTE  ·  INEGI, EIC 2025 · personas20.csv · CVEGEO 20318",21,NAVY,True)
    txt(d,54,1507,"Estimaciones ponderadas; universos indicados en cada gráfico.",20,MUTED)
    txt(d,54,1542,"Cálculo y celdas oficiales: FUENTES_INEGI.md · clave 20318",19,MUTED)
    return im,d

def save(im,name):
    path=OUT/name
    im.save(path,optimize=True)
    print(path)

def ages():
    im,d=base(1,"¿Cuántos somos","y qué edades tenemos?","people")
    rr(d,(48,350,1032,635),WHITE,30,LINE)
    txt(d,84,384,"POBLACIÓN ESTIMADA",25,TEAL,True)
    txt(d,83,428,"57 844",83,TEAL,True)
    txt(d,89,541,"personas en el municipio",28,INK,True)
    person(d,727,405,.86,"#CA8869","#F7C876")
    person(d,822,421,.78,"#A86C4F",MINT)
    person(d,913,444,.67,"#E4B08D","#E9B1A2")
    rr(d,(48,658,1032,1418),WHITE,30,LINE)
    txt(d,85,690,"Una comunidad de muchas edades",35,NAVY,True)
    txt(d,85,746,"Porcentaje de los 57 844 habitantes",24,MUTED)
    groups=[
        ("0 a 14 años",S["edad_0-14"]["porcentaje"],SUN),
        ("15 a 29 años",S["edad_15-29"]["porcentaje"],SKY),
        ("30 a 44 años",S["edad_30-44"]["porcentaje"],MINT),
        ("45 a 64 años",S["edad_45-64"]["porcentaje"],PEACH),
        ("65 años y más",S["edad_65+"]["porcentaje"],LILAC),
    ]
    for i,(label,value,color) in enumerate(groups):
        y=806+i*105
        rr(d,(78,y,1000,y+91),color,20)
        d.ellipse((99,y+17,143,y+61),fill="#F9CE9E",outline=NAVY,width=2)
        rr(d,(103,y+58,139,y+79),TEAL if i<4 else "#806DA3",9)
        txt(d,164,y+17,label,28,NAVY,True)
        bar(d,164,y+60,565,value,30,TEAL if i<4 else "#806DA3")
        txt(d,791,y+28,fmt(value),30,NAVY,True)
    rr(d,(80,1344,1000,1399),MINT,16)
    center(d,1356,"Menores de 15: 13 267  ·  65 y más: 4 365",25,NAVY,True)
    save(im,"01_edades.png")

def identity():
    im,d=base(2,"Identidad y lengua","indígena","speech")
    rr(d,(48,350,1032,850),MINT,30)
    rr(d,(73,373,1007,827),WHITE,25)
    txt(d,102,404,"AUTOADSCRIPCIÓN INDÍGENA",24,TEAL,True)
    txt(d,101,462,fmt(A["indigena"][1]),80,TEAL,True)
    txt(d,102,572,"se considera indígena",37,NAVY,True)
    txt(d,103,644,"23 777 de 57 844 personas",27,MUTED)
    person(d,711,424,.76,"#B87352","#F4C16B")
    person(d,817,466,.68,"#8B6048","#92D5C6")
    rr(d,(48,876,1032,1276),SKY,30)
    txt(d,88,911,"LENGUA INDÍGENA",24,TEAL,True)
    txt(d,85,964,fmt(A["habla_lengua_3mas"][1]),75,NAVY,True)
    txt(d,87,1065,"la habla",38,NAVY,True)
    txt(d,88,1132,"2 277 de 55 647 personas de 3 años y más",26,MUTED)
    bubble(d,800,950,1.25,WHITE)
    rr(d,(72,1300,1008,1415),SUN,22)
    txt(d,100,1318,"Dos preguntas y dos universos distintos.",27,NAVY,True)
    txt(d,100,1364,"No se restan ni equivalen al mismo grupo.",24,MUTED)
    save(im,"02_identidad_lengua.png")

def health():
    im,d=base(3,"¿Cómo se relacionan","con la salud?","health")
    rr(d,(48,350,1032,850),PEACH,30)
    txt(d,84,389,"AFILIACIÓN DECLARADA",25,TEAL,True)
    txt(d,84,446,fmt(A["sin_afiliacion"][1]),78,NAVY,True)
    txt(d,88,550,"sin afiliación a servicios de salud",31,NAVY,True)
    txt(d,88,620,"30 402 de 57 844 personas",27,MUTED)
    rr(d,(695,668,965,809),WHITE,20)
    d.rounded_rectangle((750,682,910,789),radius=14,fill=SUN,outline=NAVY,width=4)
    d.ellipse((767,704,815,751),fill="#D18B6F",outline=NAVY,width=3)
    d.line([(833,718),(890,718)],fill=TEAL,width=8)
    d.line([(833,742),(876,742)],fill=TEAL,width=7)
    txt(d,90,736,"La afiliación no determina por sí sola",25,INK,True)
    txt(d,90,777,"dónde se recibe atención.",25,INK,True)
    rr(d,(48,876,1032,1285),SKY,30)
    txt(d,85,911,"LUGAR DE ATENCIÓN",25,TEAL,True)
    txt(d,84,965,fmt(A["atencion_privada_todos"][1]),76,TEAL,True)
    txt(d,88,1066,"se atiende en servicios privados",31,NAVY,True)
    txt(d,88,1136,"21 348 de 57 844 personas",27,MUTED)
    clinic(d,820,939,.78)
    rr(d,(72,1310,1008,1414),SUN,22)
    txt(d,98,1323,"Entre quienes usan algún servicio:",26,NAVY,True)
    txt(d,98,1363,"37,82 %  ·  21 348 de 56 452 (INEGI)",25,NAVY,True)
    save(im,"03_salud.png")

def work():
    im,d=base(4,"Participación en","el trabajo","work")
    rr(d,(48,350,1032,494),WHITE,27,LINE)
    txt(d,84,379,"PARTICIPACIÓN ECONÓMICA",31,NAVY,True)
    txt(d,85,428,"Personas de 12 años y más, según sexo",25,MUTED)
    for x,fill,title,code,numerator,denominator,skin,shirt in [
        (48,PEACH,"Mujeres","participacion_mujeres_12mas","13 450","25 253","#B77555","#F5C16E"),
        (551,SKY,"Hombres","participacion_hombres_12mas","17 357","22 333","#A57052","#84CFC0"),
    ]:
        rr(d,(x,518,x+481,1059),fill,27)
        person(d,x+335,566,.92,skin,shirt,skirt=(title=="Mujeres"))
        txt(d,x+34,555,title,33,NAVY,True)
        txt(d,x+33,787,fmt(A[code][1]),57,TEAL,True)
        bar(d,x+34,881,412,A[code][1],100)
        txt(d,x+34,930,f"{numerator} de {denominator}",23,MUTED)
    rr(d,(48,1083,1032,1279),SUN,28)
    rr(d,(80,1118,180,1219),WHITE,22)
    d.rounded_rectangle((110,1153,151,1191),radius=5,fill=TEAL)
    d.rectangle((125,1140,136,1203),fill=TEAL)
    txt(d,207,1108,fmt(A["servicio_medico_laboral"][1]),53,TEAL,True)
    txt(d,209,1175,"declara servicio médico por su trabajo",26,NAVY,True)
    txt(d,209,1222,"5 450 de 18 999 personas asalariadas",24,MUTED)
    rr(d,(73,1303,1007,1415),MINT,20)
    txt(d,100,1324,"Brecha descriptiva: 24,46 puntos.",26,NAVY,True)
    txt(d,100,1366,"No atribuye causas a la diferencia.",23,MUTED)
    save(im,"04_trabajo.png")

def sectors():
    im,d=base(5,"¿En qué sectores","trabajan?","shop")
    rr(d,(48,350,1032,618),MINT,30)
    txt(d,84,380,"PERSONAS OCUPADAS",24,TEAL,True)
    txt(d,82,425,fmt(A["tres_sectores"][1]),78,TEAL,True)
    txt(d,85,532,"14 312 de 30 544 en estos tres sectores",29,NAVY,True)
    groups=[
        ("Comercio minorista",A["sectores"]["46"][1],"5 657",SUN,shop),
        ("Alojamiento y alimentos",A["sectores"]["72"][1],"5 010",PEACH,plate),
        ("Construcción",A["sectores"]["23"][1],"3 645",SKY,building),
    ]
    for i,(name,value,count,fill,illustrate) in enumerate(groups):
        y=646+i*223
        rr(d,(48,y,1032,y+201),fill,26)
        rr(d,(72,y+21,250,y+179),WHITE,20)
        illustrate(d,80,y+18,.88)
        txt(d,285,y+28,name,30,NAVY,True)
        txt(d,284,y+79,fmt(value),42,TEAL,True)
        bar(d,285,y+141,620,value,20)
        txt(d,924,y+131,count,23,MUTED,True)
    rr(d,(72,1335,1008,1416),SUN,20)
    txt(d,99,1351,"Se clasifica el negocio donde trabaja la persona;",23,NAVY,True)
    txt(d,99,1382,"no su oficio ni la actividad turística directamente.",22,MUTED)
    save(im,"05_sectores.png")

if __name__ == "__main__":
    for fn in (ages,identity,health,work,sectors): fn()
