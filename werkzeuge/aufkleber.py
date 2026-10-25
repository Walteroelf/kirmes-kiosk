#!/usr/bin/env python3
"""
Zeichnet die Aufkleber für das Sammelalbum (je Laden 12) und schreibt aufkleber.js
(window.AUFKLEBER = { kirmes: [[Name, SVG], …], … }). Flach im Stil München 1972.

Aufruf:  python3 werkzeuge/aufkleber.py
"""
import json, math, os
T = '#1d3a5c'; BL = '#3d9ad6'; HB = '#9fd3f0'; GR = '#2f9e55'; HG = '#8cc63f'; GE = '#ffd200'; OR = '#f39325'; SI = '#c5ccd3'; RO = '#f2a7b8'


def kreis_bg(farbe):
    return f'<circle cx="60" cy="60" r="52" fill="{farbe}"/>'


def riesenrad():
    s = kreis_bg(HB)
    s += f'<path d="M60 60 L40 108 M60 60 L80 108 M34 108 H86" stroke="{T}" stroke-width="5" stroke-linecap="round"/>'
    s += f'<circle cx="60" cy="56" r="34" fill="none" stroke="#fff" stroke-width="5"/>'
    for a in range(0, 360, 45):
        x, y = 60 + 34 * math.cos(math.radians(a)), 56 + 34 * math.sin(math.radians(a))
        s += f'<line x1="60" y1="56" x2="{x:.1f}" y2="{y:.1f}" stroke="#fff" stroke-width="2.5"/>'
    for j, a in enumerate(range(0, 360, 45)):
        x, y = 60 + 34 * math.cos(math.radians(a)), 56 + 34 * math.sin(math.radians(a))
        s += f'<rect x="{x - 7:.1f}" y="{y - 2:.1f}" width="14" height="11" rx="3" fill="{[OR, GE, GR, BL][j % 4]}"/>'
    return s + f'<circle cx="60" cy="56" r="6" fill="{T}"/>'


def karussell():
    s = kreis_bg(GE)
    s += f'<path d="M60 18 L100 50 H20 Z" fill="#fff"/><path d="M60 18 L73 50 H47 Z" fill="{OR}"/><path d="M60 18 L100 50 H86 Z M60 18 L34 50 H20 Z" fill="{OR}"/>'
    s += f'<path d="M60 10 v10" stroke="{T}" stroke-width="3"/><path d="M60 10 l12 4 -12 4z" fill="{BL}"/>'
    s += ''.join(f'<line x1="{x}" y1="50" x2="{x}" y2="92" stroke="{T}" stroke-width="3"/>' for x in (32, 60, 88))
    s += f'<ellipse cx="60" cy="96" rx="44" ry="8" fill="{BL}"/>'
    for x, f in ((32, '#fff'), (60, OR), (88, '#fff')):   # Pferdchen, vereinfacht
        s += f'<ellipse cx="{x}" cy="74" rx="11" ry="6" fill="{f}" stroke="{T}" stroke-width="2"/><path d="M{x + 8} 72 l6 -8 4 2 -4 8z" fill="{f}" stroke="{T}" stroke-width="2"/>'
    return s


def autoscooter():
    s = kreis_bg(HG)
    s += f'<path d="M24 26 H96" stroke="{T}" stroke-width="3"/><path d="M70 26 L64 58" stroke="{T}" stroke-width="3"/><circle cx="70" cy="27" r="3" fill="{GE}"/>'
    s += f'<rect x="20" y="70" width="80" height="24" rx="12" fill="{T}"/><path d="M28 70 Q34 54 52 54 H72 Q86 54 92 70Z" fill="{BL}"/>'
    s += f'<circle cx="48" cy="58" r="7" fill="#f6cfae"/><path d="M41 55 q7 -8 14 0" fill="#7a5233"/><rect x="62" y="58" width="12" height="4" rx="2" fill="{T}"/>'
    return s + f'<rect x="20" y="86" width="80" height="6" rx="3" fill="{GE}"/>'


def kettenkarussell():
    s = kreis_bg(HB)
    s += f'<rect x="56" y="34" width="8" height="70" fill="{T}"/><path d="M30 34 L60 16 L90 34 Z" fill="{OR}"/><rect x="28" y="32" width="64" height="6" rx="3" fill="{GE}"/>'
    for x0, x1, y1, f in ((34, 16, 78, GR), (48, 40, 84, OR), (72, 80, 84, BL), (86, 104, 78, GE)):
        s += f'<line x1="{x0}" y1="38" x2="{x1}" y2="{y1}" stroke="{T}" stroke-width="2"/><rect x="{x1 - 7}" y="{y1}" width="14" height="7" rx="2" fill="{f}"/>'
    return s + f'<rect x="38" y="102" width="44" height="6" rx="3" fill="{T}"/>'


def achterbahn():
    s = kreis_bg(GE)
    s += f'<path d="M12 92 C30 92 30 30 50 30 C70 30 66 74 84 74 C96 74 100 52 108 52" fill="none" stroke="{OR}" stroke-width="7" stroke-linecap="round"/>'
    s += ''.join(f'<line x1="{x}" y1="{y}" x2="{x}" y2="108" stroke="{T}" stroke-width="3"/>' for x, y in ((28, 76), (44, 34), (60, 40), (76, 70), (96, 66)))
    return s + f'<rect x="36" y="18" width="26" height="12" rx="4" fill="{BL}" transform="rotate(-4 49 24)"/><circle cx="42" cy="31" r="3" fill="{T}"/><circle cx="56" cy="30" r="3" fill="{T}"/>'


def schiffschaukel():
    s = kreis_bg(HG)
    s += f'<path d="M30 104 L60 22 L90 104" fill="none" stroke="{T}" stroke-width="5" stroke-linejoin="round"/><circle cx="60" cy="24" r="5" fill="{GE}"/>'
    s += f'<g transform="rotate(18 60 24)"><line x1="52" y1="24" x2="48" y2="78" stroke="{T}" stroke-width="3"/><line x1="68" y1="24" x2="72" y2="78" stroke="{T}" stroke-width="3"/>'
    s += f'<path d="M34 76 H86 Q80 96 60 96 Q40 96 34 76Z" fill="{OR}"/><rect x="34" y="74" width="52" height="5" rx="2" fill="#fff"/></g>'
    return s


def losbude():
    s = kreis_bg(HB)
    s += f'<rect x="24" y="44" width="72" height="56" fill="#fff"/><path d="M18 46 L30 24 H90 L102 46 Z" fill="{OR}"/>'
    s += ''.join(f'<path d="M{x} 46 l6 -22 h6 l-6 22z" fill="#fff"/>' for x in (34, 54, 74))
    s += f'<rect x="20" y="78" width="80" height="22" fill="{GE}"/><path d="M38 78 Q60 58 82 78" fill="{BL}"/>'
    s += ''.join(f'<rect x="{x}" y="{y}" width="10" height="7" rx="1.5" fill="{c}" transform="rotate({r} {x + 5} {y + 3})"/>' for x, y, c, r in ((44, 62, OR, -20), (56, 58, GR, 10), (66, 64, '#fff', 30)))
    return s


def luftballons():
    s = kreis_bg(GE)
    for cx, cy, f in ((42, 44, BL), (78, 40, OR), (60, 30, GR)):
        s += f'<path d="M{cx} {cy + 22} Q{cx + 4} 80 60 100" fill="none" stroke="{T}" stroke-width="2"/>'
        s += f'<ellipse cx="{cx}" cy="{cy}" rx="16" ry="20" fill="{f}"/><ellipse cx="{cx - 6}" cy="{cy - 8}" rx="4" ry="6" fill="#fff" opacity=".5"/><path d="M{cx - 3} {cy + 20} h6 l-3 5z" fill="{f}"/>'
    return s


def gluecksrad():
    s = kreis_bg(HG)
    farben = [OR, '#fff', BL, GE, GR, '#fff', HB, GE]
    for i in range(8):
        a0, a1 = math.radians(i * 45 - 90), math.radians((i + 1) * 45 - 90)
        s += f'<path d="M60 58 L{60 + 38 * math.cos(a0):.1f} {58 + 38 * math.sin(a0):.1f} A38 38 0 0 1 {60 + 38 * math.cos(a1):.1f} {58 + 38 * math.sin(a1):.1f} Z" fill="{farben[i]}"/>'
    s += f'<circle cx="60" cy="58" r="38" fill="none" stroke="{T}" stroke-width="4"/><circle cx="60" cy="58" r="6" fill="{T}"/>'
    return s + f'<path d="M60 12 l-7 -6 h14z" fill="{T}"/><path d="M54 104 h12 l-2 -10 h-8z" fill="{T}"/>'


def dosenwerfen():
    s = kreis_bg(HB)
    s += f'<rect x="18" y="96" width="84" height="8" rx="2" fill="{T}"/>'
    for (x, y) in ((28, 74), (48, 74), (68, 74), (38, 52), (58, 52), (48, 30)):
        s += f'<rect x="{x}" y="{y}" width="18" height="22" rx="2" fill="{SI}"/><rect x="{x}" y="{y + 7}" width="18" height="8" fill="{OR}"/>'
    return s + f'<circle cx="92" cy="40" r="10" fill="{GE}"/><path d="M84 36 q8 4 16 0" stroke="{OR}" stroke-width="2" fill="none"/>'


def zuckerwatte():
    s = kreis_bg(GE)
    s += f'<rect x="57" y="62" width="6" height="46" rx="3" fill="#fff" stroke="{T}" stroke-width="2"/>'
    for cx, cy, r in ((48, 50, 18), (72, 48, 18), (60, 36, 18), (56, 60, 14), (68, 60, 14)):
        s += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{RO}"/>'
    return s + '<circle cx="54" cy="34" r="6" fill="#fff" opacity=".45"/>'


def feuerwerk():
    s = f'<circle cx="60" cy="60" r="52" fill="{T}"/>'
    for cx, cy, r, f in ((44, 44, 22, GE), (80, 56, 18, OR), (56, 84, 14, HB)):
        for a in range(0, 360, 30):
            x1, y1 = cx + r * .35 * math.cos(math.radians(a)), cy + r * .35 * math.sin(math.radians(a))
            x2, y2 = cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))
            s += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{f}" stroke-width="3" stroke-linecap="round"/>'
    return s


# Bäckerei (Beispiele)
def backofen():
    s = kreis_bg(GE)
    s += f'<path d="M20 100 V58 Q20 26 60 26 Q100 26 100 58 V100Z" fill="#fff"/><path d="M36 100 V70 Q36 50 60 50 Q84 50 84 70 V100Z" fill="{T}"/>'
    s += f'<path d="M48 96 q4 -14 12 -16 q-2 8 4 10 q4 -10 0 -18 q14 8 10 24z" fill="{OR}"/><rect x="14" y="98" width="92" height="8" rx="3" fill="{SI}"/>'
    return s + ''.join(f'<rect x="{x}" y="34" width="8" height="5" rx="2" fill="{SI}"/>' for x in (40, 56, 72))


def brezel_kl():
    s = kreis_bg(HB)
    return s + (f'<path d="M60 74 C30 104 14 60 34 42 C52 26 72 46 60 74 C48 46 68 26 86 42 C106 60 90 104 60 74 Z" fill="none" stroke="#b46a2a" stroke-width="11" stroke-linejoin="round"/>'
                + ''.join(f'<circle cx="{x}" cy="{y}" r="1.8" fill="#fff"/>' for x, y in ((34, 48), (48, 36), (72, 36), (86, 50), (40, 80), (80, 80), (60, 70))))


def torte():
    s = kreis_bg(HG)
    s += f'<rect x="26" y="66" width="68" height="30" rx="4" fill="{RO}"/><rect x="34" y="44" width="52" height="24" rx="4" fill="#fff"/><rect x="18" y="94" width="84" height="8" rx="3" fill="{SI}"/>'
    s += ''.join(f'<circle cx="{x}" cy="66" r="4" fill="#fff"/>' for x in range(30, 94, 9))
    return s + ''.join(f'<rect x="{x}" y="28" width="5" height="16" rx="2" fill="{c}"/><path d="M{x + 2.5} 20 q4 5 0 8 q-4 -3 0 -8z" fill="{OR}"/>' for x, c in ((44, BL), (58, GE), (72, OR)))


def baeckermuetze():
    s = kreis_bg(OR)
    s += ''.join(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff"/>' for cx, cy, r in ((44, 46, 18), (60, 36, 20), (76, 46, 18)))
    return s + f'<rect x="34" y="50" width="52" height="34" fill="#fff"/><rect x="32" y="80" width="56" height="14" rx="3" fill="#fff" stroke="{SI}" stroke-width="2"/>'


# Spielwaren (Beispiele)
def teddy():
    s = kreis_bg(GE)
    braun, hell = '#b7793a', '#e2b57c'
    s += f'<circle cx="40" cy="34" r="10" fill="{braun}"/><circle cx="80" cy="34" r="10" fill="{braun}"/><ellipse cx="60" cy="84" rx="26" ry="22" fill="{braun}"/><circle cx="60" cy="48" r="22" fill="{braun}"/>'
    s += f'<ellipse cx="60" cy="56" rx="10" ry="8" fill="{hell}"/><circle cx="52" cy="44" r="3" fill="{T}"/><circle cx="68" cy="44" r="3" fill="{T}"/><circle cx="60" cy="53" r="3" fill="{T}"/>'
    return s + f'<ellipse cx="60" cy="86" rx="14" ry="12" fill="{hell}"/><path d="M50 66 h20 l-10 8z" fill="{BL}"/>'


def kreisel():
    s = kreis_bg(HB)
    return s + (f'<path d="M24 52 Q60 30 96 52 L60 104 Z" fill="{OR}"/><path d="M24 52 Q60 30 96 52 Q60 62 24 52Z" fill="{GE}"/>'
                f'<path d="M42 52 L60 104 L50 54Z" fill="#fff" opacity=".6"/><rect x="56" y="18" width="8" height="22" rx="3" fill="{T}"/>')


def rakete():
    s = kreis_bg(T)
    s += ''.join(f'<circle cx="{x}" cy="{y}" r="1.6" fill="#fff"/>' for x, y in ((24, 40), (92, 30), (86, 84), (30, 88), (100, 60)))
    return s + (f'<path d="M60 14 Q82 34 76 78 H44 Q38 34 60 14Z" fill="#fff"/><path d="M44 60 L30 84 H46Z M76 60 L90 84 H74Z" fill="{OR}"/>'
                f'<circle cx="60" cy="48" r="9" fill="{HB}" stroke="{BL}" stroke-width="3"/><path d="M50 80 Q60 106 70 80Z" fill="{GE}"/>')


def wuerfel():
    s = kreis_bg(HG)
    s += f'<path d="M30 46 L60 30 L90 46 L60 62Z" fill="#fff"/><path d="M30 46 V82 L60 98 V62Z" fill="#eef1f4"/><path d="M90 46 V82 L60 98 V62Z" fill="#dfe5ec"/>'
    return s + ''.join(f'<circle cx="{x}" cy="{y}" r="3.5" fill="{c}"/>' for x, y, c in ((60, 46, T), (42, 62, OR), (48, 76, OR), (72, 70, BL), (80, 58, BL), (78, 82, BL)))



def brot():
    s = kreis_bg(HB)
    s += '<path d="M18 80 Q18 40 60 40 Q102 40 102 80 Q102 92 90 92 H30 Q18 92 18 80Z" fill="#c98a45"/>'
    s += ''.join(f'<path d="M{x} 50 q8 14 0 30" stroke="#8a5a26" stroke-width="4" fill="none" stroke-linecap="round"/>' for x in (40, 58, 76))
    return s + '<path d="M28 58 Q40 44 60 44" stroke="#e8b878" stroke-width="5" fill="none" stroke-linecap="round"/>'


def croissant_kl():
    s = kreis_bg(GE)
    # Hörnchen: fünf Segmente, außen breit, die Spitzen nach unten gebogen
    segmente = [(22, 82, 34, 58, -38), (38, 58, 50, 44, -18), (52, 44, 68, 44, 0), (70, 44, 82, 58, 18), (86, 58, 98, 82, 38)]
    for x0, y0, x1, y1, dreh in segmente:
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        breit = 16 if dreh == 0 else 13
        s += f'<ellipse cx="{cx}" cy="{cy}" rx="{breit}" ry="{22 if dreh == 0 else 17}" fill="#d98c3a" stroke="#9a5418" stroke-width="2.5" transform="rotate({dreh} {cx} {cy})"/>'
    return s + '<ellipse cx="60" cy="38" rx="8" ry="5" fill="#f6c785" opacity=".7"/>'


def nudelholz():
    s = kreis_bg(HG)
    s += f'<rect x="22" y="50" width="76" height="22" rx="11" fill="#e2b36c"/><rect x="8" y="56" width="18" height="10" rx="5" fill="#b97d34"/><rect x="94" y="56" width="18" height="10" rx="5" fill="#b97d34"/>'
    return s + '<path d="M30 56 H90" stroke="#fff" stroke-width="3" opacity=".5" stroke-linecap="round"/><ellipse cx="60" cy="92" rx="30" ry="6" fill="#fff"/>'


def aehren():
    s = kreis_bg(OR)
    for dx, dreh in ((-16, -12), (0, 0), (16, 12)):
        g = f'<line x1="60" y1="104" x2="60" y2="30" stroke="{GE}" stroke-width="3"/>' + ''.join(
            f'<ellipse cx="{60 + sx * 6}" cy="{y}" rx="4" ry="8" fill="{GE}" transform="rotate({sx * 30} {60 + sx * 6} {y})"/>' for y in (36, 48, 60) for sx in (-1, 1)) + f'<ellipse cx="60" cy="28" rx="4" ry="8" fill="{GE}"/>'
        s += f'<g transform="translate({dx} 0) rotate({dreh} 60 104)">{g}</g>'
    return s


def mehlsack():
    s = kreis_bg(HB)
    s += '<path d="M30 40 Q28 32 38 30 L44 22 L50 30 L70 30 L76 22 L82 30 Q92 32 90 40 L94 96 Q94 104 84 104 H36 Q26 104 26 96Z" fill="#fff" stroke="#c5ccd3" stroke-width="2"/>'
    return s + f'<rect x="38" y="58" width="44" height="22" rx="4" fill="{BL}"/><text x="60" y="74" text-anchor="middle" font-family="Helvetica Neue, Arial" font-weight="700" font-size="13" fill="#fff">MEHL</text>'


def plaetzchen():
    s = kreis_bg(GE)
    s += f'<rect x="18" y="44" width="84" height="44" rx="4" fill="{SI}"/><rect x="18" y="84" width="84" height="6" rx="2" fill="#9aa5b1"/>'
    for cx, cy, f in ((36, 58, '#e2b36c'), (60, 58, '#c98a45'), (84, 58, '#e2b36c'), (48, 74, '#c98a45'), (72, 74, '#e2b36c')):
        s += f'<circle cx="{cx}" cy="{cy}" r="9" fill="{f}"/><circle cx="{cx - 2}" cy="{cy - 2}" r="2" fill="#5a3418"/>'
    return s


def gugelhupf():
    s = kreis_bg(HG)
    s += '<path d="M24 92 Q22 52 60 46 Q98 52 96 92Z" fill="#c98a45"/>'
    s += ''.join(f'<path d="M{x} 50 Q{x + 2} 70 {x} 92" stroke="#8a5a26" stroke-width="3" fill="none"/>' for x in (40, 52, 64, 76))
    s += '<path d="M28 60 Q34 46 60 44 Q86 46 92 60 Q84 70 78 58 Q70 68 62 56 Q54 68 46 58 Q38 70 28 60Z" fill="#fff"/><ellipse cx="60" cy="46" rx="8" ry="4" fill="#8a5a26"/>'
    return s + f'<rect x="18" y="90" width="84" height="8" rx="3" fill="{SI}"/>'


def kaffeetasse():
    s = kreis_bg(OR)
    s += '<path d="M28 50 H84 V76 Q84 96 56 96 Q28 96 28 76Z" fill="#fff"/><path d="M84 56 Q100 56 100 68 Q100 80 84 80" fill="none" stroke="#fff" stroke-width="7"/>'
    s += f'<ellipse cx="56" cy="50" rx="28" ry="6" fill="#7a4a24"/><ellipse cx="56" cy="102" rx="38" ry="6" fill="{SI}"/>'
    return s + ''.join(f'<path d="M{x} 40 q-6 -8 0 -16 q6 -8 0 -14" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round" opacity=".8"/>' for x in (46, 60))


def roboter():
    s = kreis_bg(GE)
    s += f'<rect x="38" y="30" width="44" height="34" rx="6" fill="{SI}"/><circle cx="50" cy="46" r="6" fill="{BL}"/><circle cx="70" cy="46" r="6" fill="{BL}"/><rect x="50" y="56" width="20" height="4" rx="2" fill="{T}"/>'
    s += f'<line x1="60" y1="30" x2="60" y2="20" stroke="{T}" stroke-width="3"/><circle cx="60" cy="18" r="4" fill="{OR}"/>'
    s += f'<rect x="34" y="66" width="52" height="30" rx="6" fill="{BL}"/><rect x="48" y="72" width="24" height="12" rx="3" fill="{HB}"/>'
    return s + f'<rect x="22" y="68" width="10" height="24" rx="5" fill="{SI}"/><rect x="88" y="68" width="10" height="24" rx="5" fill="{SI}"/><rect x="40" y="96" width="14" height="10" rx="3" fill="{T}"/><rect x="66" y="96" width="14" height="10" rx="3" fill="{T}"/>'


def segelboot():
    s = kreis_bg(HB)
    s += f'<path d="M58 22 V80" stroke="{T}" stroke-width="3"/><path d="M62 24 L92 74 H62Z" fill="#fff"/><path d="M54 32 L30 74 H54Z" fill="{OR}"/>'
    s += f'<path d="M24 80 H96 L86 96 H34Z" fill="{BL}"/><path d="M14 100 q12 -6 24 0 t24 0 t24 0 t24 0" stroke="#fff" stroke-width="3" fill="none"/>'
    return s


def baukloetze():
    s = kreis_bg(HG)
    kl = [(26, 72, OR, 'A'), (60, 72, BL, 'B'), (43, 40, GE, 'C')]
    for x, y, f, b in kl:
        s += f'<rect x="{x}" y="{y}" width="32" height="32" rx="4" fill="{f}"/><text x="{x + 16}" y="{y + 24}" text-anchor="middle" font-family="Helvetica Neue, Arial" font-weight="700" font-size="20" fill="#fff">{b}</text>'
    return s


def trommel():
    s = kreis_bg(OR)
    s += f'<rect x="28" y="48" width="64" height="40" fill="{BL}"/><ellipse cx="60" cy="88" rx="32" ry="10" fill="{BL}"/><ellipse cx="60" cy="48" rx="32" ry="10" fill="#fff"/>'
    s += ''.join(f'<path d="M{x} 56 L{x + 12} 86" stroke="{GE}" stroke-width="3"/>' for x in (32, 50, 68))
    return s + f'<path d="M40 26 L54 42 M82 22 L68 40" stroke="{T}" stroke-width="4" stroke-linecap="round"/><circle cx="40" cy="26" r="5" fill="#fff"/><circle cx="82" cy="22" r="5" fill="#fff"/>'


def flugzeug():
    s = kreis_bg(HB)
    s += f'<path d="M20 64 Q20 56 30 56 H88 Q102 56 104 64 Q102 72 88 72 H30 Q20 72 20 64Z" fill="#fff"/><path d="M54 58 L40 26 H50 L74 58Z" fill="{OR}"/><path d="M54 70 L40 98 H50 L74 70Z" fill="{OR}"/>'
    s += f'<path d="M24 58 L16 40 H24 L34 58Z" fill="{BL}"/>' + ''.join(f'<circle cx="{x}" cy="62" r="3" fill="{BL}"/>' for x in (66, 74, 82))
    return s + f'<path d="M96 60 Q102 64 96 68" stroke="{BL}" stroke-width="3" fill="none"/>'


def dino():
    s = kreis_bg(GE)
    s += f'<path d="M22 86 Q20 60 42 56 Q52 54 60 60 L70 40 Q74 28 86 30 Q98 32 96 42 Q94 50 84 48 L80 66 Q84 88 70 92 L64 92 L64 104 L56 104 L56 92 L42 92 L42 104 L34 104 L34 90 Q24 92 14 100 Q16 90 22 86Z" fill="{GR}"/>'
    s += f'<circle cx="88" cy="38" r="3" fill="{T}"/>' + ''.join(f'<path d="M{x} {y} l6 -8 6 8z" fill="{HG}"/>' for x, y in ((36, 58), (48, 56), (60, 58)))
    return s


def schaukelpferd():
    s = kreis_bg(HG)
    s += f'<path d="M16 96 Q60 120 104 96" stroke="#b46a2a" stroke-width="7" fill="none" stroke-linecap="round"/>'
    s += f'<path d="M34 98 L40 74 M50 102 L52 76 M74 102 L72 76 M88 98 L82 74" stroke="#b46a2a" stroke-width="5"/>'
    s += f'<path d="M30 58 Q30 74 50 76 H76 Q88 76 88 62 Q88 52 80 52 H42 Q30 52 30 58Z" fill="#fff" stroke="{T}" stroke-width="2"/>'
    s += f'<path d="M76 54 L84 26 Q86 20 92 22 L102 34 L96 40 L88 36 L86 54Z" fill="#fff" stroke="{T}" stroke-width="2"/><circle cx="92" cy="28" r="2" fill="{T}"/>'
    return s + f'<path d="M84 24 Q76 30 78 44" stroke="{OR}" stroke-width="5" fill="none"/><rect x="50" y="48" width="22" height="8" rx="2" fill="{OR}"/><path d="M30 60 Q18 62 16 76" stroke="{OR}" stroke-width="5" fill="none"/>'


def kran():
    s = kreis_bg(HB)
    s += f'<rect x="40" y="30" width="10" height="66" fill="{GE}"/>' + ''.join(f'<path d="M40 {y} L50 {y + 10}" stroke="{T}" stroke-width="2"/>' for y in range(32, 92, 10))
    s += f'<rect x="22" y="26" width="82" height="8" fill="{GE}"/><rect x="18" y="24" width="14" height="14" fill="{T}"/><line x1="88" y1="34" x2="88" y2="62" stroke="{T}" stroke-width="2"/>'
    s += f'<rect x="78" y="62" width="20" height="16" rx="2" fill="{OR}"/><rect x="30" y="94" width="34" height="12" rx="3" fill="{T}"/>'
    return s + f'<circle cx="38" cy="106" r="4" fill="{SI}"/><circle cx="56" cy="106" r="4" fill="{SI}"/>'


ALBEN = {
    'kirmes': [('Riesenrad', riesenrad), ('Karussell', karussell), ('Autoscooter', autoscooter), ('Kettenkarussell', kettenkarussell),
               ('Achterbahn', achterbahn), ('Schiffschaukel', schiffschaukel), ('Losbude', losbude), ('Luftballons', luftballons),
               ('Glücksrad', gluecksrad), ('Dosenwerfen', dosenwerfen), ('Zuckerwatte', zuckerwatte), ('Feuerwerk', feuerwerk)],
    'baeckerei': [('Backofen', backofen), ('Brezel', brezel_kl), ('Torte', torte), ('Bäckermütze', baeckermuetze),
                  ('Brot', brot), ('Croissant', croissant_kl), ('Nudelholz', nudelholz), ('Ähren', aehren),
                  ('Mehlsack', mehlsack), ('Plätzchen', plaetzchen), ('Gugelhupf', gugelhupf), ('Kaffeetasse', kaffeetasse)],
    'spielwaren': [('Teddy', teddy), ('Kreisel', kreisel), ('Rakete', rakete), ('Würfel', wuerfel),
                   ('Roboter', roboter), ('Segelboot', segelboot), ('Bauklötze', baukloetze), ('Trommel', trommel),
                   ('Flugzeug', flugzeug), ('Dino', dino), ('Schaukelpferd', schaukelpferd), ('Kran', kran)],
}


def aufkleber(fn):
    return (f'<svg viewBox="0 0 120 120" class="aufkleber-svg" aria-hidden="true"><rect x="2" y="2" width="116" height="116" rx="18" fill="#fff"/>{fn()}'
            f'<path d="M118 92 V100 Q118 118 100 118 H92 Q96 100 118 92Z" fill="#eef1f4"/></svg>')


def main():
    app = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    daten = {k: [[t, aufkleber(fn)] for t, fn in m] for k, m in ALBEN.items()}
    assert all(len(m) == 12 for m in daten.values())
    js = '// Erzeugt mit werkzeuge/aufkleber.py – nicht von Hand ändern.\nwindow.AUFKLEBER = ' + json.dumps(daten, ensure_ascii=False) + ';\n'
    open(os.path.join(app, 'aufkleber.js'), 'w', encoding='utf-8').write(js)
    print(f'aufkleber.js: {sum(len(m) for m in daten.values())} Aufkleber, {len(js) // 1024} KB')


if __name__ == '__main__':
    main()
