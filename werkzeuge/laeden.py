#!/usr/bin/env python3
"""
Zeichnet die Laden-Ansichten (laeden/kirmes.svg, laeden/baeckerei.svg, laeden/spielwaren.svg).

Jeder Laden ist ein zusammenhängendes Bild (Format 1200 × 780) mit einheitlicher Perspektive.
Die Produktbilder aus bilder/ werden eingesetzt; jede Ware steckt in einer Gruppe
  <g class="artikel" data-id="…" data-box="x y b h"> … </g>
Die Preisschilder liegen in einer eigenen obersten Ebene (<g class="schilder">, je <g class="schild" data-id="…">
mit <text class="preis"/>), damit kein Teil des Bildes sie verdeckt.
Die App trägt die Preise selbst ein (aus PRODUKTE_… in index.html) und zeichnet die
Markierung („im Korb“, „2×“) über data-box. Preise ändern = nur index.html ändern.

Aufruf:  python3 werkzeuge/laeden.py
"""
import os, re

HIER = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(HIER)
ZIEL = os.path.join(APP, 'laeden')
T = '#1d3a5c'          # Dunkelblau statt Schwarz
W, H = 1200, 780


def ids_aus_index():
    s = open(os.path.join(APP, 'index.html'), encoding='utf-8').read()
    erg = {}
    for laden, name in [('kirmes', 'PRODUKTE_KIRMES'), ('spielwaren', 'PRODUKTE_SPIELWAREN'), ('baeckerei', 'PRODUKTE_BAECKEREI')]:
        a = s.index(f'const {name}'); b = s.index('];', a)
        erg[laden] = re.findall(r"id: '([^']+)'", s[a:b])
    return erg


class Szene:
    def __init__(self, laden, ordner, praefix):
        self.laden, self.ordner, self.k = laden, ordner, praefix
        self.teile, self.ids, self.schilder = [], [], []

    def __iadd__(self, svg):
        self.teile.append(svg); return self

    def u(self, name):            # Verweis auf eine Füllung aus den defs
        return f'url(#{self.k}{name})'

    # ---------- Bausteine
    def bild(self, i, cx, boden, h, extra='', drehen=0):
        """Produktbild (200×200, Standfläche bei 85 % der Höhe) mit Mitte cx, stehend auf y = boden."""
        t = f' transform="rotate({drehen} {cx:.1f} {boden - .43 * h:.1f})"' if drehen else ''
        return (f'<image href="{self.ordner}{i}.svg" x="{cx - h / 2:.1f}" y="{boden - 0.85 * h:.1f}" width="{h:.1f}" height="{h:.1f}" '
                f'preserveAspectRatio="xMidYMax meet"{t} {extra}/>')

    def schild(self, i, cx, y, w=72, hh=25, haken=True):
        oben = f'<rect x="{cx - 4}" y="{y - 6}" width="8" height="9" rx="1.5" fill="#9aa5b1"/>' if haken else ''
        return (f'<g class="schild" data-id="{i}">{oben}<rect x="{cx - w / 2}" y="{y}" width="{w}" height="{hh}" rx="3" fill="#fff" stroke="{T}" stroke-width="2.2"/>'
                f'<text x="{cx}" y="{y + hh - 7}" text-anchor="middle" class="preis"></text></g>')

    def artikel(self, i, inhalt, box, schild_xy, schild_haken=True):
        x, y, w, h = box
        self.ids.append(i)
        erg = (f'<g class="artikel" data-id="{i}" data-box="{x:.0f} {y:.0f} {w:.0f} {h:.0f}">'
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="transparent"/>{inhalt}</g>')
        self.schilder.append(self.schild(i, schild_xy[0], schild_xy[1], haken=schild_haken))
        return erg

    def person(self, P, Ky, haende_y, hemd='#fff', schuerze='#ffd200', kappe='schiffchen', kappe_farbe='#fff',
               haare='#7a5233', jacke=None):
        """Freundliche Verkäuferin/freundlicher Verkäufer – steht hinter der Theke, Hände auf der Theke."""
        k = []
        k.append(f'<path d="M{P - 78} 700 V{Ky + 92} q0 -42 42 -46 h72 q42 4 42 46 V700z" fill="{jacke or hemd}"/>')   # Oberkörper
        if jacke:   # Strickjacke offen über hellem Shirt
            k.append(f'<path d="M{P - 30} 700 V{Ky + 60} h60 V700z" fill="{hemd}"/>'
                     f'<path d="M{P - 30} {Ky + 60} l30 36 30 -36" fill="none" stroke="{jacke}" stroke-width="6"/>'
                     f'<rect x="{P + 36}" y="{Ky + 104}" width="30" height="18" rx="3" fill="#fff" stroke="#c5ccd3" stroke-width="2"/>')   # Namensschild
        if schuerze:
            k.append(f'<path d="M{P - 50} 700 V{Ky + 104} q0 -14 14 -14 h72 q14 0 14 14 V700z" fill="{schuerze}"/>'
                     f'<path d="M{P - 36} {Ky + 90} L{P - 14} {Ky + 52} M{P + 36} {Ky + 90} L{P + 14} {Ky + 52}" stroke="{schuerze}" stroke-width="8" stroke-linecap="round"/>')
        k.append(f'<path d="M{P - 16} {Ky + 46} l16 18 16 -18" fill="none" stroke="#e3e7eb" stroke-width="5" stroke-linejoin="round"/>')
        k.append(f'<rect x="{P - 12}" y="{Ky + 26}" width="24" height="24" fill="{self.u("haut")}"/>')
        arm = jacke or hemd
        tiefe = haende_y - (Ky + 92)
        k.append(f'<path d="M{P - 78} {Ky + 92} q-14 {tiefe * .4:.0f} -12 {tiefe - 10:.0f} l4 20 h28 l2 -{tiefe * .55:.0f} q0 -30 10 -{tiefe * .4:.0f}z" fill="{arm}"/>')
        k.append(f'<path d="M{P + 78} {Ky + 92} q14 {tiefe * .4:.0f} 12 {tiefe - 10:.0f} l-4 20 h-28 l-2 -{tiefe * .55:.0f} q0 -30 -10 -{tiefe * .4:.0f}z" fill="{arm}"/>')
        k.append(f'<ellipse cx="{P - 74}" cy="{haende_y}" rx="17" ry="11" fill="{self.u("haut")}"/><ellipse cx="{P + 74}" cy="{haende_y}" rx="17" ry="11" fill="{self.u("haut")}"/>')
        k.append(f'<ellipse cx="{P}" cy="{Ky - 2}" rx="36" ry="38" fill="{haare}"/>')
        k.append(f'<ellipse cx="{P}" cy="{Ky + 6}" rx="31" ry="34" fill="{self.u("haut")}"/>')
        k.append(f'<path d="M{P - 33} {Ky - 4} q8 -26 33 -26 q25 0 33 26 q-14 -12 -33 -12 q-19 0 -33 12z" fill="{haare}"/>')
        if kappe == 'schiffchen':
            k.append(f'<path d="M{P - 30} {Ky - 20} q30 -26 60 0 l-4 -18 q-26 -12 -52 0z" fill="{kappe_farbe}" stroke="#dfe4e9" stroke-width="2"/>'
                     f'<path d="M{P - 26} {Ky - 30} q26 -8 52 0" fill="none" stroke="#ffd200" stroke-width="3"/>')
        elif kappe == 'schirm':
            k.append(f'<path d="M{P - 33} {Ky - 12} q2 -32 33 -32 q31 0 33 32z" fill="{kappe_farbe}"/>'
                     f'<path d="M{P - 36} {Ky - 12} h86 q6 0 6 5 q-40 6 -92 2z" fill="{kappe_farbe}"/><circle cx="{P}" cy="{Ky - 44}" r="4" fill="{kappe_farbe}"/>')
        k.append(f'<ellipse cx="{P - 11}" cy="{Ky + 6}" rx="3.5" ry="4.5" fill="#2a2a2a"/><ellipse cx="{P + 11}" cy="{Ky + 6}" rx="3.5" ry="4.5" fill="#2a2a2a"/>'
                 f'<path d="M{P - 17} {Ky - 3} q6 -4 12 0 M{P + 5} {Ky - 3} q6 -4 12 0" stroke="#5a3a22" stroke-width="2.5" fill="none" stroke-linecap="round"/>'
                 f'<path d="M{P - 2} {Ky + 10} q2 6 4 0" stroke="#c98e6a" stroke-width="2.5" fill="none" stroke-linecap="round"/>'
                 f'<path d="M{P - 12} {Ky + 20} q12 11 24 0" stroke="#a5523f" stroke-width="3.2" fill="none" stroke-linecap="round"/>'
                 f'<circle cx="{P - 20}" cy="{Ky + 17}" r="6" fill="#f2998a" opacity=".35"/><circle cx="{P + 20}" cy="{Ky + 17}" r="6" fill="#f2998a" opacity=".35"/>'
                 f'<ellipse cx="{P - 31}" cy="{Ky + 8}" rx="5" ry="8" fill="#eab991"/><ellipse cx="{P + 31}" cy="{Ky + 8}" rx="5" ry="8" fill="#eab991"/>')
        return '<g pointer-events="none">' + ''.join(k) + '</g>'

    def korb(self, cx, boden, breite=168, tief=36):
        b2 = breite / 2
        return (f'<path d="M{cx - b2 + 2} {boden - tief + 2}h{breite - 4}l-12 {tief}h-{breite - 28}z" fill="{self.u("korb")}"/>'
                f'<path d="M{cx - b2 + 2} {boden - tief + 2}h{breite - 4}l-12 {tief}h-{breite - 28}z" fill="{self.u("geflecht")}"/>'
                f'<rect x="{cx - b2}" y="{boden - tief - 2}" width="{breite}" height="7" rx="3" fill="#b97d34"/>')

    def korb_vorn(self, cx, boden, breite=152):
        b2 = breite / 2
        return (f'<path d="M{cx - b2} {boden - 16}h{breite}l-6 18h-{breite - 12}z" fill="{self.u("korb")}"/>'
                f'<path d="M{cx - b2} {boden - 16}h{breite}l-6 18h-{breite - 12}z" fill="{self.u("geflecht")}"/>')

    def svg(self, defs):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" class="laden-svg" data-laden="{self.laden}">'
                f'<defs>{defs}</defs>' + '\n'.join(self.teile) + '<g class="schilder">' + ''.join(self.schilder) + '</g></svg>')


def gemeinsame_defs(k, wand=('#fdf6e1', '#f6e7c1'), wandL=('#e9d39c', '#f3e3b8'), wandR=('#e6cf96', '#f1e0b2'),
                    front=('#ffdb2e', '#f2c400')):
    return f'''
<linearGradient id="{k}wand" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{wand[0]}"/><stop offset="1" stop-color="{wand[1]}"/></linearGradient>
<linearGradient id="{k}wandL" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{wandL[0]}"/><stop offset="1" stop-color="{wandL[1]}"/></linearGradient>
<linearGradient id="{k}wandR" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="{wandR[0]}"/><stop offset="1" stop-color="{wandR[1]}"/></linearGradient>
<linearGradient id="{k}decke" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f7f3ea"/><stop offset="1" stop-color="#fffdf7"/></linearGradient>
<radialGradient id="{k}lichtfleck" cx=".5" cy=".3" r=".6"><stop offset="0" stop-color="#fff8d6" stop-opacity=".9"/><stop offset="1" stop-color="#fff8d6" stop-opacity="0"/></radialGradient>
<linearGradient id="{k}holz" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#c88a42"/><stop offset=".5" stop-color="#dba45c"/><stop offset="1" stop-color="#c3843c"/></linearGradient>
<linearGradient id="{k}holzBrett" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e8b871"/><stop offset="1" stop-color="#b8782f"/></linearGradient>
<linearGradient id="{k}rueckwandRegal" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ead1a0"/><stop offset="1" stop-color="#f2dfb6"/></linearGradient>
<linearGradient id="{k}schatten" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3b2a12" stop-opacity=".28"/><stop offset="1" stop-color="#3b2a12" stop-opacity="0"/></linearGradient>
<linearGradient id="{k}korb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d9a24e"/><stop offset="1" stop-color="#a8702a"/></linearGradient>
<pattern id="{k}geflecht" width="12" height="10" patternUnits="userSpaceOnUse"><path d="M0 5h12M6 0v10" stroke="#8a5a1e" stroke-opacity=".35" stroke-width="2"/></pattern>
<linearGradient id="{k}front" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{front[0]}"/><stop offset="1" stop-color="{front[1]}"/></linearGradient>
<linearGradient id="{k}platte" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#e9edf1"/></linearGradient>
<linearGradient id="{k}metall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#eef1f4"/><stop offset=".5" stop-color="#b8c1ca"/><stop offset="1" stop-color="#dfe4e9"/></linearGradient>
<linearGradient id="{k}metallS" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#aeb8c2"/><stop offset=".45" stop-color="#eef1f4"/><stop offset="1" stop-color="#b3bdc7"/></linearGradient>
<linearGradient id="{k}glas" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e8f5fc" stop-opacity=".55"/><stop offset=".25" stop-color="#d6ecf8" stop-opacity=".18"/><stop offset="1" stop-color="#cfe6f4" stop-opacity=".28"/></linearGradient>
<linearGradient id="{k}innen" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fffaf0"/><stop offset="1" stop-color="#f3ead8"/></linearGradient>
<linearGradient id="{k}led" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff6c9"/><stop offset="1" stop-color="#fff6c9" stop-opacity="0"/></linearGradient>
<linearGradient id="{k}kuehl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#eaf6fd"/><stop offset="1" stop-color="#d4ebf7"/></linearGradient>
<linearGradient id="{k}himmel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#bfe3f7"/><stop offset="1" stop-color="#e6f4fb"/></linearGradient>
<linearGradient id="{k}haut" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f6cfae"/><stop offset="1" stop-color="#eab991"/></linearGradient>
<filter id="{k}weich" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>'''


# ======================================================================================== Raum (für Innenräume)
def raum(sz, vp=(600, 280), boden='fliesen', boden_farben=('#e7eaee', '#d6dce3'), lampen=(330, 600, 870)):
    k = sz.k
    def x_auf(xb, y):
        return vp[0] + (xb - vp[0]) * (y - vp[1]) / (480 - vp[1])
    sz += f'<rect width="{W}" height="{H}" fill="{sz.u("decke")}"/>'
    sz += f'<polygon points="0,0 150,70 150,480 0,547" fill="{sz.u("wandL")}"/>'
    sz += f'<polygon points="1200,0 1050,70 1050,480 1200,547" fill="{sz.u("wandR")}"/>'
    sz += f'<rect x="150" y="70" width="900" height="410" fill="{sz.u("wand")}"/>'
    for x in lampen:
        sz += f'<ellipse cx="{x}" cy="150" rx="170" ry="120" fill="{sz.u("lichtfleck")}"/>'
    sz += '<g opacity=".16" fill="#4a3a1a"><polygon points="150,70 166,74 166,480 150,480"/><polygon points="1050,70 1034,74 1034,480 1050,480"/><rect x="150" y="70" width="900" height="6"/></g>'
    teile = []
    if boden == 'fliesen':
        reihen = [480, 491, 504, 520, 540, 566, 600, 646, 708, 790]
        spalten = list(range(150 - 75 * 10, 1050 + 75 * 11, 75))
        for r in range(len(reihen) - 1):
            y0, y1 = reihen[r], reihen[r + 1]
            for c in range(len(spalten) - 1):
                a, b = spalten[c], spalten[c + 1]
                pts = f'{x_auf(a, y0):.1f},{y0} {x_auf(b, y0):.1f},{y0} {x_auf(b, y1):.1f},{y1} {x_auf(a, y1):.1f},{y1}'
                teile.append(f'<polygon points="{pts}" fill="{boden_farben[(r + c) % 2]}"/>')
    else:   # Parkett: Dielen laufen in die Tiefe
        teile.append(f'<rect x="0" y="480" width="{W}" height="300" fill="{boden_farben[0]}"/>')
        for i, xb in enumerate(range(150 - 45 * 30, 1050 + 45 * 31, 45)):
            if i % 2:
                teile.append(f'<polygon points="{xb},480 {xb + 45},480 {x_auf(xb + 45, 790):.0f},790 {x_auf(xb, 790):.0f},790" fill="{boden_farben[1]}"/>')
        for y in [494, 512, 536, 568, 612, 672, 750]:
            for j, xb in enumerate(range(150 - 45 * 30, 1050 + 45 * 31, 90)):
                off = 45 if (y // 2) % 2 else 0
                xa = x_auf(xb + off, y)
                teile.append(f'<line x1="{xa:.0f}" y1="{y}" x2="{x_auf(xb + off + 45, y):.0f}" y2="{y}" stroke="#a7834f" stroke-opacity=".25" stroke-width="2"/>')
        for xb in range(150 - 45 * 30, 1050 + 45 * 31, 45):
            teile.append(f'<line x1="{xb}" y1="480" x2="{x_auf(xb, 790):.0f}" y2="790" stroke="#a7834f" stroke-opacity=".3" stroke-width="1.5"/>')
    sz += (f'<clipPath id="{k}bodenClip"><polygon points="150,480 1050,480 1200,547 1200,780 0,780 0,547"/></clipPath>'
           f'<g clip-path="url(#{k}bodenClip)">{"".join(teile)}<rect x="0" y="480" width="1200" height="300" fill="{sz.u("lichtfleck")}" opacity=".35"/></g>')
    sz += '<rect x="150" y="474" width="900" height="8" fill="#c9b78f" opacity=".8"/>'
    for x in (250, 600, 950):
        sz += f'<ellipse cx="{x}" cy="{18 if x == 600 else 26}" rx="26" ry="6" fill="#fff" stroke="#e0dccf" stroke-width="2"/>'


def fenster_links(sz, draussen=True):
    sz += (f'<clipPath id="{sz.k}fensterClip"><polygon points="24,140 118,160 118,372 24,398"/></clipPath>'
           f'<g clip-path="url(#{sz.k}fensterClip)"><rect x="0" y="120" width="140" height="300" fill="{sz.u("himmel")}"/>'
           '<circle cx="60" cy="330" r="46" fill="#8cc63f"/><circle cx="104" cy="350" r="34" fill="#6fae34"/><rect x="0" y="372" width="140" height="40" fill="#c5ccd3"/></g>'
           '<polygon points="24,140 118,160 118,372 24,398" fill="none" stroke="#fff" stroke-width="10" stroke-linejoin="round"/>'
           '<line x1="71" y1="150" x2="71" y2="385" stroke="#fff" stroke-width="7"/>'
           '<polygon points="16,398 126,372 126,382 16,410" fill="#fff"/>')


def uhr_rechts(sz):
    sz += f'<ellipse cx="1126" cy="172" rx="29" ry="34" fill="#fff" stroke="{T}" stroke-width="5"/><path d="M1126 172v-19M1126 172l12 8" stroke="{T}" stroke-width="4" stroke-linecap="round"/>'


def kasse_bildschirm(x, y):
    """Kassen-Bildschirm mit Kartenterminal; (x, y) = linke untere Ecke des Fußes."""
    return (f'<g transform="translate({x - 1052} {y - 648})"><rect x="1052" y="636" width="60" height="12" rx="3" fill="#9aa5b1"/><rect x="1076" y="590" width="12" height="48" fill="#9aa5b1"/>'
            f'<rect x="1030" y="540" width="104" height="66" rx="6" fill="{T}"/><rect x="1038" y="548" width="88" height="50" rx="3" fill="#9fd3f0"/>'
            '<rect x="1046" y="556" width="40" height="8" rx="2" fill="#fff" opacity=".8"/><rect x="1046" y="570" width="64" height="8" rx="2" fill="#fff" opacity=".6"/>'
            '<rect x="996" y="616" width="34" height="32" rx="5" fill="#3a4a5c"/><rect x="1001" y="621" width="24" height="10" rx="2" fill="#8cc63f"/></g>')


def theke(sz, x0, x1, platte_y, unten=780, felder=4, deko=None):
    """Theke parallel zur Rückwand: Platte (platte_y … +32), Front mit Feldern in der Leitfarbe."""
    f = platte_y + 32
    t = [f'<rect x="{x0}" y="{f}" width="{x1 - x0}" height="{unten - f}" fill="{sz.u("front")}"/>']
    breite = (x1 - x0) / felder
    t += [f'<rect x="{x0 + 10 + i * breite:.0f}" y="{f + 10}" width="{breite - 20:.0f}" height="{unten - f - 44}" rx="4" fill="none" stroke="#000" stroke-opacity=".08" stroke-width="3"/>' for i in range(felder)]
    if deko:
        t += [deko(x0 + breite * (i + .5), f + (unten - f - 24) / 2) for i in range(felder)]
    t.append(f'<rect x="{x0}" y="{unten - 24}" width="{x1 - x0}" height="24" fill="#000" opacity=".14"/>')
    t.append(f'<polygon points="{x0 + 14},{platte_y} {x1 - 14},{platte_y} {x1 + 4},{f} {x0 - 4},{f}" fill="{sz.u("platte")}"/><rect x="{x0 - 4}" y="{f - 4}" width="{x1 - x0 + 8}" height="6" fill="#d5dbe1"/>')
    sz += ''.join(t)


def aehre(cx, cy, farbe='#c99a00'):
    return (f'<g stroke="{farbe}" stroke-width="3.5" fill="none" stroke-linecap="round"><path d="M{cx} {cy + 24} V{cy - 24}"/>'
            + ''.join(f'<path d="M{cx} {y} l-11 -9 M{cx} {y} l11 -9"/>' for y in (cy - 14, cy - 3, cy + 8)) + '</g>')


# ======================================================================================== Bäckerei
def baeckerei():
    sz = Szene('baeckerei', 'bilder/baeckerei/', 'b-')
    defs = gemeinsame_defs(sz.k)
    raum(sz)
    # Fliesenspiegel unten an der Rückwand
    fl = ['<rect x="150" y="330" width="900" height="150" fill="#fbfaf6"/>']
    fl += [f'<line x1="150" y1="{y}" x2="1050" y2="{y}"/>' for y in range(355, 480, 25)]
    fl += [f'<line x1="{x}" y1="330" x2="{x}" y2="480"/>' for x in range(175, 1050, 25)]
    sz += f'<g stroke="#d9d3c3" stroke-width="1.5">{"".join(fl)}</g><rect x="150" y="326" width="900" height="6" fill="#e4d6b0"/>'
    fenster_links(sz); uhr_rechts(sz)

    # Brotregal
    R0, R1 = 168, 562
    reg = [f'<rect x="{R0}" y="92" width="{R1 - R0}" height="388" fill="{sz.u("holz")}"/>',
           f'<rect x="{R0 - 6}" y="86" width="{R1 - R0 + 12}" height="16" fill="{sz.u("holzBrett")}"/>',
           f'<rect x="{R0 + 12}" y="102" width="{R1 - R0 - 24}" height="278" fill="{sz.u("rueckwandRegal")}"/>']
    reg += [f'<line x1="{x}" y1="102" x2="{x}" y2="380" stroke="#d9bd86" stroke-width="1.5"/>' for x in range(R0 + 40, R1 - 12, 30)]
    reg.append(f'<rect x="{(R0 + R1) / 2 - 6}" y="102" width="12" height="278" fill="{sz.u("holz")}"/>')
    for y in (196, 288, 380):
        reg.append(f'<rect x="{R0 + 12}" y="{y + 12}" width="{R1 - R0 - 24}" height="22" fill="{sz.u("schatten")}"/>'
                   f'<rect x="{R0 + 4}" y="{y}" width="{R1 - R0 - 8}" height="12" fill="{sz.u("holzBrett")}"/>')
    reg.append(f'<rect x="{R0 + 12}" y="392" width="{R1 - R0 - 24}" height="88" fill="#d4a25b"/>')
    for x0 in (R0 + 18, (R0 + R1) / 2 + 6):
        reg.append(f'<rect x="{x0}" y="420" width="{(R1 - R0) / 2 - 30}" height="54" rx="3" fill="#e2b36c" stroke="#b97d34" stroke-width="2"/>'
                   f'<rect x="{x0 + (R1 - R0) / 4 - 30}" y="442" width="30" height="7" rx="3" fill="{T}" opacity=".5"/>')
    sz += ''.join(reg)
    L1, L2 = (R0 + 12 + (R0 + R1) / 2 - 6) / 2, ((R0 + R1) / 2 + 6 + R1 - 12) / 2

    def stapel_brot(i, cx, boden, h):
        inhalt = sz.bild(i, cx - 38, boden, h) + sz.bild(i, cx + 38, boden, h) + sz.bild(i, cx, boden - h * .32, h)
        return sz.artikel(i, inhalt, (cx - 95, boden - h * .95, 190, h * .95), (cx, boden + 2))

    def korb_mit(i, cx, boden, h, n=5):
        lagen = [(-50, -22), (0, -26), (50, -22), (-25, -36), (25, -36)][:n]
        inhalt = sz.korb(cx, boden) + ''.join(sz.bild(i, cx + dx, boden + dy, h) for dx, dy in sorted(lagen, key=lambda d: d[1])) + sz.korb_vorn(cx, boden)
        return sz.artikel(i, inhalt, (cx - 88, boden - 30 - h * .8, 176, h * .8 + 30), (cx, boden + 2))

    sz += stapel_brot('brot', L1, 196, 76)
    sz += stapel_brot('vollkornbrot', L2, 196, 76)
    sz += korb_mit('broetchen', L1, 288, 54)
    sz += korb_mit('mohnbroetchen', L2, 288, 54)
    sz += korb_mit('rosinenbroetchen', L1, 380, 54)
    sz += korb_mit('laugenstange', L2, 380, 68, n=4)

    # Baguettes stehend im hohen Korb
    bx = 618
    bag = (f'<ellipse cx="{bx}" cy="478" rx="40" ry="7" fill="#000" opacity=".15"/>'
           + ''.join(sz.bild('baguette', bx + dx, 452, 150, drehen=-47 + dx / 3) for dx in (-16, 14, -2))
           + f'<path d="M{bx - 36} 372h72l-6 104h-60z" fill="{sz.u("korb")}"/><path d="M{bx - 36} 372h72l-6 104h-60z" fill="{sz.u("geflecht")}"/>'
           + f'<rect x="{bx - 39}" y="368" width="78" height="8" rx="3" fill="#b97d34"/>')
    sz += sz.artikel('baguette', bag, (bx - 48, 262, 96, 216), (bx, 392))

    # Ladenschild, Rückbuffet, Kaffeemaschine
    sz += (f'<rect x="690" y="140" width="230" height="46" rx="4" fill="#fff" stroke="{T}" stroke-width="3"/><rect x="690" y="140" width="230" height="9" fill="#ffd200"/>'
           f'<text x="805" y="178" text-anchor="middle" class="ladenschild">bäckerei</text>')
    sz += (f'<rect x="672" y="388" width="268" height="92" fill="#f4f1ea"/><rect x="666" y="378" width="280" height="12" fill="{sz.u("metall")}"/>'
           '<g stroke="#d6d0c0" stroke-width="2" fill="none"><rect x="682" y="398" width="76" height="72" rx="3"/><rect x="768" y="398" width="76" height="72" rx="3"/><rect x="854" y="398" width="76" height="72" rx="3"/></g>')
    sz += (f'<g><rect x="820" y="296" width="106" height="84" rx="8" fill="{sz.u("metallS")}"/><rect x="830" y="306" width="86" height="26" rx="4" fill="{T}"/>'
           '<circle cx="845" cy="319" r="5" fill="#8cc63f"/><rect x="858" y="314" width="48" height="10" rx="3" fill="#3d9ad6"/>'
           '<rect x="848" y="340" width="12" height="16" fill="#555"/><rect x="886" y="340" width="12" height="16" fill="#555"/><rect x="832" y="370" width="82" height="8" fill="#9aa5b1"/>'
           '<g fill="#fff" stroke="#c5ccd3" stroke-width="2"><path d="M826 296h18l-2 -14h-14z"/><path d="M850 296h18l-2 -14h-14z"/><path d="M874 296h18l-2 -14h-14z"/></g></g>')

    # Getränkekühlschrank
    K0, K1 = 958, 1046
    kuehl = [f'<rect x="{K0}" y="150" width="{K1 - K0}" height="330" rx="6" fill="#f7f9fb" stroke="#c5ccd3" stroke-width="3"/>',
             f'<rect x="{K0 + 8}" y="160" width="{K1 - K0 - 16}" height="44" rx="3" fill="{T}"/>',
             f'<text x="{(K0 + K1) / 2}" y="189" text-anchor="middle" class="kuehltext">kalt</text>',
             f'<rect x="{K0 + 8}" y="210" width="{K1 - K0 - 16}" height="256" fill="{sz.u("kuehl")}"/>']
    kuehl += [f'<rect x="{K0 + 8}" y="{y}" width="{K1 - K0 - 16}" height="5" fill="#c5ccd3"/>' for y in (298, 384, 462)]
    kuehl.append(''.join(sz.bild('apfelschorle', K0 + 24 + 20 * c, y, 62) for y in (298, 384) for c in range(3)))
    kuehl.append(f'<rect x="{K0 + 8}" y="210" width="{K1 - K0 - 16}" height="256" fill="#fff" opacity=".12"/><polygon points="{K0 + 14},216 {K0 + 30},216 {K0 + 18},460 {K0 + 12},460" fill="#fff" opacity=".45"/>'
                 f'<rect x="{K1 - 16}" y="300" width="5" height="60" rx="2" fill="#9aa5b1"/>')
    sz += sz.artikel('apfelschorle', ''.join(kuehl), (K0, 150, K1 - K0, 330), ((K0 + K1) / 2, 418))

    sz += sz.person(760, 300, 462)

    # Vitrine
    V0, V1, VT = 36, 806, 458
    theke(sz, V0, V1, 640, felder=4, deko=lambda cx, cy: aehre(cx, cy))
    v = [f'<rect x="{V0 + 18}" y="{VT}" width="{V1 - V0 - 36}" height="{640 - VT}" fill="{sz.u("innen")}" opacity=".92"/>',
         f'<rect x="{V0 + 18}" y="{VT + 6}" width="{V1 - V0 - 36}" height="26" fill="{sz.u("led")}"/>',
         f'<rect x="{V0 + 26}" y="624" width="{V1 - V0 - 52}" height="10" rx="3" fill="{sz.u("metall")}"/>',
         f'<rect x="{V0 + 26}" y="545" width="{V1 - V0 - 52}" height="9" rx="2" fill="#e8f4fb" stroke="#bcdcf0" stroke-width="2"/>']
    sz += ''.join(v)

    def reihe(i, cx, boden, h, n=3, abst=30):
        ox = [(-abst, -6), (abst, -6), (0, 0)] if n == 3 else [(-abst / 2, -5), (abst / 2, 0)]
        return ''.join(sz.bild(i, cx + dx, boden + dy, h) for dx, dy in ox)

    for i, cx, h in [('croissant', 118, 82), ('schokocroissant', 262, 82), ('zimtschnecke', 410, 76), ('berliner', 556, 76), ('amerikaner', 700, 78)]:
        sz += sz.artikel(i, reihe(i, cx, 549, h), (cx - 66, 549 - h * .72, 132, h * .72), (cx, 556))
    for i, cx, h in [('kaesekuchen', 122, 92), ('apfelkuchen', 268, 92), ('erdbeertoertchen', 414, 84), ('keks', 556, 78), ('belegtes-broetchen', 700, 86)]:
        sz += sz.artikel(i, reihe(i, cx, 628, h, n=2, abst=48), (cx - 66, 628 - h * .72, 132, h * .72), (cx, 636))
    sz += (f'<g pointer-events="none"><path d="M{V0 + 6} 640 V{VT + 54} Q{V0 + 6} {VT} {V0 + 60} {VT} H{V1 - 6} V640 Z" fill="{sz.u("glas")}"/>'
           f'<path d="M{V0 + 6} 640 V{VT + 54} Q{V0 + 6} {VT} {V0 + 60} {VT} H{V1 - 6}" fill="none" stroke="{sz.u("metall")}" stroke-width="7"/>'
           f'<rect x="{V1 - 12}" y="{VT}" width="9" height="{640 - VT}" fill="{sz.u("metallS")}"/>'
           f'<polygon points="{V0 + 70},{VT + 8} {V0 + 128},{VT + 8} {V0 + 58},632 {V0 + 24},632" fill="#fff" opacity=".28"/>'
           f'<polygon points="{V0 + 150},{VT + 8} {V0 + 170},{VT + 8} {V0 + 104},632 {V0 + 88},632" fill="#fff" opacity=".18"/></g>')

    # Kassentheke
    theke(sz, 830, 1204, 642, felder=2)
    sz += '<g><path d="M1152 660 l6 -66 h34 l6 66z" fill="#d8b47a"/><path d="M1146 664 l6 -60 h34 l6 60z" fill="#e3c38d"/><path d="M1152 612h34" stroke="#c9a46a" stroke-width="3"/></g>'
    sz += kasse_bildschirm(1078, 660)
    sz += sz.artikel('kakao', sz.bild('kakao', 904, 652, 82) + sz.bild('kakao', 866, 658, 96), (822, 658 - 84, 120, 86), (878, 680))
    bz = 990
    staender = (f'<rect x="{bz - 30}" y="652" width="60" height="9" rx="3" fill="{sz.u("metall")}"/><rect x="{bz - 3}" y="460" width="6" height="194" fill="{sz.u("metallS")}"/>'
                + ''.join(f'<path d="M{bz} {y} q-18 -2 -26 8 M{bz} {y} q18 -2 26 8" stroke="#9aa5b1" stroke-width="3" fill="none"/>' for y in (482, 542, 602))
                + ''.join(sz.bild('brezel', bz, y + 52, 70) for y in (482, 542, 602)))
    sz += sz.artikel('brezel', staender, (bz - 40, 460, 80, 200), (bz, 680))
    # Hängelampen vorn
    for x in (365, 600):
        sz += (f'<g pointer-events="none"><line x1="{x}" y1="0" x2="{x}" y2="34" stroke="#4a5a6a" stroke-width="3"/>'
               f'<path d="M{x - 54} 80 Q{x - 48} 34 {x} 34 Q{x + 48} 34 {x + 54} 80 Z" fill="#ffd200"/>'
               f'<ellipse cx="{x}" cy="80" rx="54" ry="8" fill="#fff4b3"/><ellipse cx="{x}" cy="86" rx="38" ry="9" fill="#fff8d0" filter="url(#{sz.k}weich)" opacity=".9"/></g>')
    return sz, defs


# ======================================================================================== Kirmes-Kiosk (Bude von außen)
def kirmes():
    sz = Szene('kirmes', 'bilder/', 'k-')
    defs = gemeinsame_defs(sz.k, wand=('#fff3df', '#f7e2bd'), front=('#f7a84a', '#e98a1f')) + f'''
<linearGradient id="k-abend" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9fd3f0"/><stop offset="1" stop-color="#e8f5fc"/></linearGradient>
<linearGradient id="k-bretter" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#b8752e"/><stop offset=".5" stop-color="#d4954b"/><stop offset="1" stop-color="#b06d28"/></linearGradient>
<clipPath id="k-dachClip"><polygon points="70,64 1130,64 1160,150 40,150"/></clipPath>
<radialGradient id="k-birne" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fffbe0"/><stop offset=".55" stop-color="#ffd200"/><stop offset="1" stop-color="#ffd200" stop-opacity="0"/></radialGradient>'''
    # Himmel, Riesenrad und Nachbarbude im Hintergrund
    sz += f'<rect width="{W}" height="{H}" fill="url(#k-abend)"/>'
    rr = ['<g opacity=".55" stroke="#8fb3cf" fill="none" stroke-width="6"><circle cx="70" cy="250" r="170"/><circle cx="70" cy="250" r="20"/>']
    import math
    for a in range(0, 360, 30):
        x, y = 70 + 170 * math.cos(math.radians(a)), 250 + 170 * math.sin(math.radians(a))
        rr.append(f'<line x1="70" y1="250" x2="{x:.0f}" y2="{y:.0f}" stroke-width="3"/><rect x="{x - 14:.0f}" y="{y:.0f}" width="28" height="22" rx="4" fill="#cfe6f4" stroke-width="3"/>')
    rr.append('</g>')
    sz += ''.join(rr)
    sz += '<g opacity=".5"><polygon points="1130,210 1200,180 1200,420 1130,420" fill="#f3d9a6"/><polygon points="1120,214 1200,176 1200,196 1120,226" fill="#3d9ad6"/></g>'
    # Boden (Pflaster)
    sz += ('<rect x="0" y="736" width="1200" height="44" fill="#cfd5dc"/>'
           + ''.join(f'<line x1="{x}" y1="736" x2="{x - 30}" y2="780" stroke="#b5bdc6" stroke-width="2"/>' for x in range(0, 1260, 60))
           + '<line x1="0" y1="756" x2="1200" y2="756" stroke="#b5bdc6" stroke-width="2"/>')
    # Bude: Rückwand innen
    sz += f'<rect x="100" y="140" width="1000" height="600" fill="{sz.u("wand")}"/>'
    sz += ''.join(f'<line x1="{x}" y1="150" x2="{x}" y2="600" stroke="#e8cfa2" stroke-width="2"/>' for x in range(140, 1100, 46))
    sz += '<rect x="100" y="140" width="1000" height="40" fill="#000" opacity=".06"/>'
    # Lebkuchenherzen hängen unter dem Dach
    herzen = ''
    for j, (x, y) in enumerate([(170, 220), (228, 232), (286, 216), (344, 234), (402, 222)]):
        herzen += f'<line x1="{x}" y1="166" x2="{x}" y2="{y - 48}" stroke="#c88a42" stroke-width="2"/>' + sz.bild('lebkuchen', x, y, 66)
    sz += sz.artikel('lebkuchen', herzen, (132, 160, 306, 80), (286, 238))
    # Regal links: Getränke und warme Getränke
    def regal(x0, x1, top, bretter):
        r = [f'<rect x="{x0}" y="{top}" width="{x1 - x0}" height="{bretter[-1] - top + 12}" fill="#f6e3bd" opacity=".9"/>',
             f'<rect x="{x0 - 8}" y="{top}" width="10" height="{bretter[-1] - top + 12}" fill="{sz.u("holz")}"/><rect x="{x1 - 2}" y="{top}" width="10" height="{bretter[-1] - top + 12}" fill="{sz.u("holz")}"/>']
        for y in bretter:
            r.append(f'<rect x="{x0}" y="{y + 12}" width="{x1 - x0}" height="18" fill="{sz.u("schatten")}"/><rect x="{x0 - 8}" y="{y}" width="{x1 - x0 + 16}" height="12" fill="{sz.u("holzBrett")}"/>')
        return ''.join(r)
    sz += regal(128, 476, 250, [336, 432])
    def facings(i, cx, boden, h, n=3, abst=26):
        ox = {1: [0], 2: [-abst / 2, abst / 2], 3: [-abst, abst, 0]}[n]
        return ''.join(sz.bild(i, cx + dx, boden - (4 if k < n - 1 and n == 3 else 0), h) for k, dx in enumerate(ox))
    for i, cx, h, n in [('cola', 178, 86, 3), ('limo', 290, 86, 3), ('saft', 404, 78, 2)]:
        sz += sz.artikel(i, facings(i, cx, 338, h, n), (cx - 52, 338 - h * .78, 104, h * .78), (cx, 340))
    for i, cx, h, n in [('tee', 186, 70, 2), ('kaffee', 296, 70, 2)]:
        sz += sz.artikel(i, facings(i, cx, 434, h, n, 40), (cx - 54, 434 - h * .7, 108, h * .7), (cx, 436))
    # Schokolade gestapelt
    schoko = ''.join(sz.bild('schokolade', 408 + dx, 434 + dy, 70) for dx, dy in [(-18, 0), (16, 0), (0, -16)])
    sz += sz.artikel('schokolade', schoko, (356, 434 - 70, 104, 70), (408, 436))
    # Regal rechts: Süßes, Zuckerwatte, Popcornmaschine
    sz += regal(724, 1072, 214, [312, 440])
    for i, cx, h, n in [('donut', 780, 66, 3), ('muffin', 884, 70, 2)]:
        sz += sz.artikel(i, facings(i, cx, 314, h, n, 30), (cx - 54, 314 - h * .7, 108, h * .7), (cx, 316))
    zw = (f'<rect x="980" y="294" width="56" height="20" rx="4" fill="#e9ecef" stroke="#c5ccd3" stroke-width="2"/>'
          + ''.join(sz.bild('zuckerwatte', 1008 + dx, 310 + dy, 98) for dx, dy in [(-20, -6), (20, -6), (0, 0)]))
    sz += sz.artikel('zuckerwatte', zw, (952, 214, 112, 98), (1008, 316))
    # Popcornmaschine
    pm = (f'<rect x="744" y="362" width="190" height="78" rx="6" fill="#fff" fill-opacity=".35" stroke="{sz.u("metall")}" stroke-width="7"/>'
          f'<rect x="736" y="350" width="206" height="16" rx="4" fill="#f39325"/><rect x="760" y="340" width="158" height="12" rx="4" fill="#ffd200"/>'
          + ''.join(sz.bild('popcorn', 790 + 44 * c, 438 - (6 if c == 1 else 0), 64) for c in range(3))
          + '<polygon points="760,368 790,368 770,434 752,434" fill="#fff" opacity=".35"/>')
    sz += sz.artikel('popcorn', pm, (740, 340, 202, 100), (839, 444))
    # Verkäufer mit Schirmmütze in Orange
    sz += sz.person(600, 330, 560, hemd='#fff', schuerze='#f39325', kappe='schirm', kappe_farbe='#f39325', haare='#4a3426')
    # Theke vorn: Holzbretter in Orange, Platte aus Edelstahl
    sz += ('<rect x="100" y="586" width="1000" height="150" fill="url(#k-bretter)"/>'
           + ''.join(f'<line x1="100" y1="{y}" x2="1100" y2="{y}" stroke="#9a5a1c" stroke-opacity=".45" stroke-width="2"/>' for y in range(616, 736, 30))
           + '<rect x="100" y="586" width="1000" height="150" fill="#f39325" opacity=".35"/>'
           + f'<polygon points="112,556 1088,556 1104,588 96,588" fill="{sz.u("platte")}"/><rect x="96" y="584" width="1008" height="7" fill="#c5ccd3"/>')
    wimpel = ['<path d="M108 640 Q600 690 1092 640" stroke="#4a5a6a" stroke-width="2.5" fill="none"/>']
    farben = ['#3d9ad6', '#ffd200', '#8cc63f', '#ffffff', '#9fd3f0', '#f7c35a']
    for j, x in enumerate(range(130, 1080, 46)):
        t = (x - 108) / 984; y = 640 + 50 * 4 * t * (1 - t) * .5 * 2 * .5
        y = (1 - t) ** 2 * 640 + 2 * (1 - t) * t * 690 + t ** 2 * 640
        wimpel.append(f'<polygon points="{x - 16},{y:.0f} {x + 16},{y + 2:.0f} {x},{y + 34:.0f}" fill="{farben[j % len(farben)]}" stroke="#000" stroke-opacity=".08"/>')
    sz += ''.join(wimpel)
    # Grill mit Würstchen, Hotdogs
    sz += (f'<rect x="120" y="532" width="200" height="26" rx="4" fill="#3a4a5c"/><rect x="126" y="526" width="188" height="10" rx="3" fill="{sz.u("metall")}"/>'
           + ''.join(f'<line x1="{x}" y1="528" x2="{x}" y2="534" stroke="#9aa5b1" stroke-width="2"/>' for x in range(134, 312, 12)))
    sz += sz.artikel('wurst', ''.join(sz.bild('wurst', cx, 540 + dy, 70) for cx, dy in [(160, -8), (220, -10), (280, -8), (190, 2), (250, 2)]), (122, 470, 196, 76), (220, 596))
    sz += sz.artikel('hotdog', f'<rect x="334" y="548" width="96" height="10" rx="3" fill="#c5ccd3"/>' + sz.bild('hotdog', 368, 552, 80) + sz.bild('hotdog', 392, 562, 84),
                     (330, 494, 104, 70), (382, 596))
    sz += sz.artikel('burger', sz.bild('burger', 470, 562, 88) + sz.bild('burger', 512, 566, 92), (436, 488, 112, 80), (492, 596))
    pommes = (f'<rect x="566" y="528" width="72" height="34" rx="4" fill="#e9ecef" stroke="#c5ccd3" stroke-width="2"/>'
              + ''.join(sz.bild('pommes', 584 + 36 * c, 548 + 8 * (c % 2), 82) for c in range(2)))
    sz += sz.artikel('pommes', pommes, (560, 478, 84, 88), (602, 596))
    sz += sz.artikel('pizza', '<ellipse cx="700" cy="562" rx="54" ry="10" fill="#fff" stroke="#dfe4e9" stroke-width="2"/>' + sz.bild('pizza', 686, 564, 74) + sz.bild('pizza', 716, 566, 78),
                     (646, 500, 108, 66), (700, 596))
    sz += sz.artikel('falaffel', sz.bild('falaffel', 774, 562, 80) + sz.bild('falaffel', 806, 566, 84), (748, 498, 92, 68), (790, 596))
    def tortenstaender(i, cx):
        return (f'<rect x="{cx - 6}" y="548" width="12" height="12" fill="{sz.u("metallS")}"/><ellipse cx="{cx}" cy="560" rx="34" ry="6" fill="{sz.u("metall")}"/>'
                f'<ellipse cx="{cx}" cy="548" rx="52" ry="8" fill="#fff" stroke="#dfe4e9" stroke-width="2"/>' + sz.bild(i, cx, 550, 80)
                + f'<path d="M{cx - 50} 548 V508 q0 -30 50 -30 q50 0 50 30 V548" fill="#e8f5fc" fill-opacity=".28" stroke="#fff" stroke-width="3"/>'
                + f'<path d="M{cx - 36} 512 q4 -20 26 -26" stroke="#fff" stroke-width="5" fill="none" opacity=".7" stroke-linecap="round"/>')
    sz += sz.artikel('kirschkuchen', tortenstaender('kirschkuchen', 876), (822, 474, 108, 90), (876, 596))
    sz += sz.artikel('schoko-kuchen', tortenstaender('schoko-kuchen', 976), (922, 474, 108, 90), (976, 596))
    # Brezel am Stab (vorn an der Ecke)
    bz = 1050
    sz += sz.artikel('brezel', f'<rect x="{bz - 3}" y="400" width="6" height="160" fill="{sz.u("metallS")}"/><rect x="{bz - 24}" y="554" width="48" height="8" rx="3" fill="{sz.u("metall")}"/>'
                     + ''.join(sz.bild('brezel', bz, y, 64) for y in (448, 498, 548)), (bz - 34, 392, 68, 168), (bz, 596))
    # Bude: Pfosten, Dach mit Streifen und Bogenkante, Lichterkette, Schild
    sz += f'<rect x="82" y="120" width="30" height="620" fill="url(#k-bretter)"/><rect x="1088" y="120" width="30" height="620" fill="url(#k-bretter)"/>'
    streifen = ''.join(f'<rect x="{x}" y="60" width="60" height="100" fill="{"#f39325" if (x // 60) % 2 == 0 else "#fff"}"/>' for x in range(0, 1200, 60))
    sz += f'<g clip-path="url(#k-dachClip)">{streifen}<rect x="0" y="60" width="1200" height="100" fill="url(#{sz.k}schatten)" opacity=".5" transform="rotate(180 600 110)"/></g>'
    sz += ''.join(f'<path d="M{x} 150 a30 22 0 0 0 60 0z" fill="{"#f39325" if ((x - 40) // 60) % 2 == 0 else "#fff"}"/>' for x in range(40, 1160, 60))
    sz += '<path d="M44 150 H1156" stroke="#d97a12" stroke-width="3"/>'
    birnen = ''.join(f'<circle cx="{x}" cy="{186 + 10 * math.sin((x - 120) / 70)}" r="12" fill="url(#k-birne)"/><circle cx="{x}" cy="{186 + 10 * math.sin((x - 120) / 70)}" r="4.5" fill="#fff8c4"/>' for x in range(470, 730, 40))
    sz += f'<path d="M460 180 Q600 206 740 180" stroke="#4a5a6a" stroke-width="2" fill="none"/>{birnen}'
    schild = (f'<rect x="420" y="8" width="360" height="54" rx="6" fill="#fff" stroke="{T}" stroke-width="3"/>'
              + ''.join(f'<circle cx="{x}" cy="{y}" r="4" fill="#ffd200" stroke="#e8b800"/>' for x in range(432, 780, 20) for y in (16, 54))
              + f'<text x="600" y="47" text-anchor="middle" class="ladenschild gross">kirmes-kiosk</text>')
    sz += schild
    return sz, defs


# ======================================================================================== Spielwarenladen
def spielwaren():
    sz = Szene('spielwaren', 'bilder/spielwaren/', 's-')
    defs = gemeinsame_defs(sz.k, wand=('#f4f9fd', '#e3f0f9'), wandL=('#cfe3f1', '#e4f0f8'), wandR=('#cbe0ef', '#e1eef7'), front=('#b6dcf3', '#8ec7ea'))
    raum(sz, boden='parkett', boden_farben=('#e6c99a', '#dcbb86'), lampen=(330, 600, 870))
    fenster_links(sz)
    # Poster/Schild an der rechten Rückwand
    sz += (f'<rect x="870" y="128" width="160" height="46" rx="4" fill="#fff" stroke="{T}" stroke-width="3"/><rect x="870" y="128" width="160" height="9" fill="#9fd3f0"/>'
           f'<text x="950" y="166" text-anchor="middle" class="ladenschild klein">spielwaren</text>')
    # Großes Wandregal (weiß lackiert, Kanten hellblau)
    R0, R1 = 168, 772
    reg = [f'<rect x="{R0}" y="96" width="{R1 - R0}" height="384" fill="#fbfdff" stroke="#d3e3ee" stroke-width="3"/>',
           f'<rect x="{R0 + 10}" y="106" width="{R1 - R0 - 20}" height="324" fill="#eef5fa"/>']
    reg += [f'<rect x="{x}" y="106" width="10" height="324" fill="#fbfdff"/>' for x in (R0 + (R1 - R0) / 3 - 5, R0 + 2 * (R1 - R0) / 3 - 5)]
    for y in (200, 316, 430):
        reg.append(f'<rect x="{R0 + 10}" y="{y + 12}" width="{R1 - R0 - 20}" height="20" fill="#2a4a6a" opacity=".1"/>'
                   f'<rect x="{R0 + 2}" y="{y}" width="{R1 - R0 - 4}" height="12" fill="#fbfdff"/><rect x="{R0 + 2}" y="{y + 8}" width="{R1 - R0 - 4}" height="5" fill="#9fd3f0"/>')
    reg.append(f'<rect x="{R0 + 10}" y="442" width="{R1 - R0 - 20}" height="38" fill="#fbfdff"/>'
               + ''.join(f'<rect x="{R0 + 18 + i * 150}" y="448" width="140" height="28" rx="3" fill="#e3eff8" stroke="#c7dcea" stroke-width="2"/>' for i in range(4)))
    sz += ''.join(reg)
    def f(i, cx, boden, h, ox=(0,)):
        return ''.join(sz.bild(i, cx + dx, boden - (5 if j < len(ox) - 1 else 0), h) for j, dx in enumerate(ox))
    oben = [('kuscheltier', 262, 92, (-26, 26)), ('puppe', 470, 98, (-24, 24)), ('bilderbuch', 676, 86, (-22, 0, 22))]
    for i, cx, h, ox in oben:
        sz += sz.artikel(i, f(i, cx, 202, h, ox), (cx - 74, 202 - h * .8, 148, h * .8), (cx, 214))
    mitte = [('puzzle', 236, 80, (-14, 14)), ('brettspiel', 380, 82, (-14, 14)), ('malkasten', 530, 74, (-18, 18)), ('xylophon', 680, 80, (0,))]
    for i, cx, h, ox in mitte:
        sz += sz.artikel(i, f(i, cx, 318, h, ox), (cx - 64, 318 - h * .78, 128, h * .78), (cx, 330))
    unten = [('seifenblasen', 232, 72, (-24, 0, 24)), ('jojo', 378, 66, (-22, 0, 22)), ('springseil', 530, 74, (-16, 16)), ('spielzeugauto', 680, 70, (-22, 22))]
    for i, cx, h, ox in unten:
        sz += sz.artikel(i, f(i, cx, 432, h, ox), (cx - 64, 432 - h * .75, 128, h * .75), (cx, 444))
    # Skateboards an der Wand (Halterung)
    sk = (''.join(f'<rect x="{x}" y="196" width="10" height="16" rx="2" fill="#9aa5b1"/><rect x="{x}" y="388" width="10" height="16" rx="2" fill="#9aa5b1"/>' for x in (806, 856))
          + sz.bild('skateboard', 814, 400, 196, drehen=-90 + 12) + sz.bild('skateboard', 860, 400, 196, drehen=-90 + 12))
    sz += sz.artikel('skateboard', sk, (790, 196, 104, 210), (836, 420))
    # Drachen hängt von der Decke
    dr = '<line x1="560" y1="0" x2="560" y2="48" stroke="#4a5a6a" stroke-width="2"/>' + sz.bild('drachen', 560, 190, 170, drehen=-12)
    sz += sz.artikel('drachen', dr, (494, 34, 132, 160), (600, 188), schild_haken=False)
    # Kassentheke rechts mit Verkäuferin (Strickjacke)
    sz += sz.person(1020, 300, 520, hemd='#fff', schuerze=None, kappe=None, haare='#3a2a20', jacke='#3d9ad6')
    theke(sz, 900, 1204, 530, felder=2)
    sz += kasse_bildschirm(1100, 548)
    sz += sz.artikel('rc-auto', sz.bild('rc-auto', 966, 548, 96) + f'<rect x="1010" y="520" width="34" height="28" rx="4" fill="#3a4a5c"/><rect x="1024" y="500" width="4" height="22" fill="#3a4a5c"/>',
                     (912, 470, 136, 80), (970, 572))
    # Spieltisch in der Mitte
    sz += (f'<rect x="300" y="610" width="470" height="100" fill="{sz.u("front")}"/><rect x="300" y="690" width="470" height="20" fill="#000" opacity=".12"/>'
           f'<polygon points="312,580 758,580 774,612 296,612" fill="#f2e2c4"/><rect x="296" y="608" width="478" height="6" fill="#d9c49c"/>'
           '<rect x="306" y="710" width="18" height="34" fill="#b7cfe0"/><rect x="746" y="710" width="18" height="34" fill="#b7cfe0"/>')
    # Schienen-Oval für die Eisenbahn
    sz += '<ellipse cx="560" cy="592" rx="92" ry="12" fill="none" stroke="#8a6a46" stroke-width="5"/><ellipse cx="560" cy="592" rx="80" ry="8" fill="none" stroke="#8a6a46" stroke-width="3"/>'
    sz += sz.artikel('puppenhaus', sz.bild('puppenhaus', 386, 596, 150), (322, 474, 128, 124), (386, 622))
    sz += sz.artikel('eisenbahn', sz.bild('eisenbahn', 562, 598, 118), (496, 520, 132, 80), (560, 622))
    sz += sz.artikel('bausteine', sz.bild('bausteine', 690, 596, 104) + sz.bild('bausteine', 724, 600, 70), (636, 514, 126, 86), (700, 622))
    # Ballkorb (Gitter) vorn links
    bk = (sz.bild('ball', 222, 668, 70) + sz.bild('ball', 268, 664, 72) + sz.bild('ball', 246, 642, 66)
          + '<path d="M184 652 h120 l-10 104 h-100z" fill="#cfe2f0" fill-opacity=".35" stroke="#7d93a8" stroke-width="4"/>'
          + ''.join(f'<line x1="{x}" y1="654" x2="{x + (244 - x) * .08:.0f}" y2="754" stroke="#7d93a8" stroke-width="2.5"/>' for x in range(196, 300, 16))
          + ''.join(f'<line x1="{186 + (y - 652) * .1:.0f}" y1="{y}" x2="{302 - (y - 652) * .1:.0f}" y2="{y}" stroke="#7d93a8" stroke-width="2.5"/>' for y in (680, 708, 734))
          + '<ellipse cx="244" cy="652" rx="60" ry="8" fill="none" stroke="#7d93a8" stroke-width="4"/>')
    sz += sz.artikel('ball', bk, (180, 600, 128, 160), (244, 700))
    # Fahrrad und Roller auf dem Boden
    sz += '<ellipse cx="96" cy="766" rx="96" ry="10" fill="#000" opacity=".12"/>'
    sz += sz.artikel('fahrrad', sz.bild('fahrrad', 96, 776, 210), (0, 610, 190, 166), (96, 714))
    sz += sz.artikel('roller', sz.bild('roller', 846, 776, 210), (782, 600, 128, 176), (846, 712))
    return sz, defs


def main():
    os.makedirs(ZIEL, exist_ok=True)
    soll = ids_aus_index()
    for bauen in (baeckerei, kirmes, spielwaren):
        sz, defs = bauen()
        fehlt = set(soll[sz.laden]) - set(sz.ids)
        doppelt = {i for i in sz.ids if sz.ids.count(i) > 1}
        assert not fehlt and not doppelt, (sz.laden, fehlt, doppelt)
        pfad = os.path.join(ZIEL, sz.laden + '.svg')
        open(pfad, 'w', encoding='utf-8').write(sz.svg(defs))
        print(f'{sz.laden}: {len(sz.ids)} Artikel, {os.path.getsize(pfad) // 1024} KB')


if __name__ == '__main__':
    main()
