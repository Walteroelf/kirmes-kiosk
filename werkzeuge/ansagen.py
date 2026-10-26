#!/usr/bin/env python3
"""
Erzeugt die Ansagen (Ordner ton/) mit Piper und der Thorsten-Stimme (Datensätze CC0):
  - de_DE-thorsten-high            für alles
  - de_DE-thorsten_emotional-medium für das Lob („Super!“, „Richtig!“ …) in fröhlicher Stimmung

Die App setzt jeden Vorlese-Text aus den längsten passenden Bausteinen zusammen. Damit die
Satzmelodie stimmt, gibt es möglichst große Bausteine:
  - Sätze mit Betrag komplett („Das sind genau 3 Euro 40.“) für alle vorkommenden Beträge
  - Waren je nach Platz im Satz: „Ich möchte eine Brezel, …“ / „…, eine Brezel, …“ /
    „… und eine Brezel kaufen.“ / „Ich möchte eine Brezel kaufen.“
  - alle festen Sätze
Was fehlt, liest die Stimme des Geräts (z. B. der Name des Kindes).

Aufruf (Piper muss installiert sein, siehe README):
  python3 werkzeuge/ansagen.py --piper venv/bin/python --modell de_DE-thorsten-high.onnx \
      --lob-modell de_DE-thorsten_emotional-medium.onnx

Nach Änderungen an Vorlese-Texten, Waren oder Stufen neu ausführen und die VERSION in index.html/sw.js erhöhen.
"""
import argparse, array, hashlib, json, math, os, re, subprocess, sys, tempfile, wave

HIER = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(HIER)
ZIEL = os.path.join(APP, 'ton')
TON_STAND = '3'   # erhöhen, wenn sich die Aufbereitung ändert (dann wird alles neu erzeugt)


# Aussprache von Lehnwörtern: Umschreibung oder Lautschrift ([[ … ]] geht direkt an Piper).
# Der Artikel steht mit in der Lautschrift, sonst wird „ein“ betont.
AUSSPRACHE = [
    (r'\b[Ee]in Schokocroissant\b', '[[ aɪn ʃˌoːkokroasˈaŋ ]]'),
    (r'\bSchokocroissants\b', '[[ ʃˌoːkokroasˈaŋs ]]'),
    (r'\b[Ee]in Croissant\b', '[[ aɪn kroasˈaŋ ]]'),
    (r'\bCroissants\b', '[[ kroasˈaŋs ]]'),
    (r'\b[Ee]in Erdbeertörtchen\b', '[[ aɪn ˈeːɾtbeːɾtˌœɾtçən ]]'),
    (r'\bErdbeertörtchen\b', '[[ ˈeːɾtbeːɾtˌœɾtçən ]]'),
    (r'\b[Ee]in Rosinenbrötchen\b', '[[ aɪn roːzˈiːnənbrˌøːtçən ]]'),   # espeak: „ROsi-NEN-brötchen“
    (r'\bRosinenbrötchen\b', '[[ roːzˈiːnənbrˌøːtçən ]]'),
    (r'\bBurger\b', 'Börger'),
    (r'\bMuffins\b', 'Maffins'), (r'\bMuffin\b', 'Maffin'),
    (r'\bDonuts\b', 'Dohnatts'), (r'\bDonut\b', 'Dohnatt'),
]


def aussprache(text):
    for muster, ersatz in AUSSPRACHE:
        text = re.sub(muster, ersatz, text)
    return text


def schluessel(text):
    """Wie tonSchluessel() in index.html: Wörter klein, Satzzeichen am Rand weg."""
    woerter = text.replace('€', 'Euro').split()
    return ' '.join(w for w in (re.sub(r'^[\W_]+|[\W_]+$', '', w.lower()) for w in woerter) if w)


def saetze(text):
    return [t for t in re.split(r'(?<=[.!?:])\s+', text.replace('€', 'Euro').strip()) if t]


def euro_text(n):
    """Wie sprichBetrag() für ganze Euro: Text in der App und gesprochene Form („ein Euro“, „hundertein Euro“)."""
    sprich = f'{n} Euro'
    if n % 100 == 1:
        sprich = ('hundert' if n > 100 else '') + 'ein Euro'
    return f'{n} Euro', sprich


def cent_text(v):
    """Wie sprichBetrag() in der Bäckerei (v in Cent)."""
    e, c = divmod(v, 100)
    if e == 0:
        return f'{c} Cent', f'{c} Cent'
    ea, es = euro_text(e)
    return (ea, es) if c == 0 else (f'{ea} {c}', f'{es} {c}')


def sammle(lob_stimme):
    html = open(os.path.join(APP, 'index.html'), encoding='utf-8').read()
    teile = []  # (Text in der App, gesprochener Text, Stimme)

    def satz(*texte, stimme='normal'):
        for t in texte:
            for s in saetze(t):
                teile.append((s, s, stimme))

    def teil(anzeige, sprich=None, stimme='normal'):
        teile.append((anzeige, sprich or anzeige, stimme))

    # Lob in fröhlicher Stimmung (zuerst, damit diese Fassung gewinnt)
    satz('Super!', 'Richtig!', 'Geschafft!', 'Das klappt schon super!', stimme=lob_stimme)

    # Waren je nach Platz im Satz: „Ich möchte A, B und C kaufen.“
    for ein, mehr in re.findall(r"\['([^']+)', '([^']+)'\]", html[html.index('const SPRECH'):html.index('const ZAHL_SPRECH')]):
        for f in [ein, f'zwei {mehr}', f'drei {mehr}']:
            teil(f'Ich möchte {f} kaufen.')
            teil(f'Ich möchte {f}', f'Ich möchte {f},')
            teil(f, f + ',')
            teil(f'und {f} kaufen.')
        teil(mehr)   # Rückfall für „vier …“, „fünf …“
    for w in ['zwei', 'drei', 'vier', 'fünf', 'sechs', 'und', 'Ich möchte', 'kaufen.']:
        teil(w)

    # Sätze mit Betrag – komplett
    euro = [euro_text(n) for n in range(1, 201)]
    cent10 = [cent_text(v) for v in range(10, 1001, 10)]      # Lösungen in der Bäckerei bis 10 €
    cent20 = [cent_text(v) for v in range(10, 2001, 10)]      # hingelegtes Geld bis 20 €
    rahmen = ['Das sind genau {}.', 'Das sind genau {} Rückgeld.', 'Du bekommst {} zurück.', 'Zusammen kostet es {}.']
    for r in rahmen:
        for a, s in euro + cent10:
            teil(r.format(a), r.format(s))
    for r in ['Du hast {} hingelegt.', 'Ich sehe {}.']:
        for a, s in euro + cent20:
            teil(r.format(a), r.format(s))
    bezahlt = [euro_text(n) for n in [5, 10, 15, 20, 50, 100, 200]]
    scheine = [(f'einem {n}-Euro-Schein', f'einem {w}-Euro-Schein') for n, w in
               [(5, 'Fünf'), (10, 'Zehn'), (20, 'Zwanzig'), (50, 'Fünfzig'), (100, 'Hundert')]]
    for a, s in bezahlt + scheine:
        teil(f'Ich bezahle mit {a}.', f'Ich bezahle mit {s}.')
    for a, s in bezahlt:
        teil(f'Ich habe {a} dabei.', f'Ich habe {s} dabei.')
        teil(f'Dann zieh das von {a} ab.', f'Dann zieh das von {s} ab.')

    # Stufen-Texte und Hinweise zur Fotoqualität (aus index.html)
    for block in ['STUFEN_KIRMES', 'STUFEN_SPIELWAREN', 'STUFEN_BAECKEREI']:
        a = html.index(f'const {block}'); b = html.index('];', a)
        for t in re.findall(r"text: '([^']+)'", html[a:b]):
            satz(t)
    a = html.index('const QUALITAET'); b = html.index('};', a)
    for t in re.findall(r"'([^']+\.)'", html[a:b]):
        satz(t)

    # Feste Sätze
    satz('Wie viel kostet das?', 'Wie viel kostet das zusammen?', 'Wie viel Geld bekomme ich zurück?',
         'Zieh das Geld in das Feld und tippe dann auf Fertig.', 'Zieh das Rückgeld in das Feld und tippe dann auf Fertig.',
         'Leg das Geld hin und mach ein Foto.', 'Leg das Rückgeld hin und mach ein Foto.', 'Reicht mein Geld?',
         'Wo möchtest du einkaufen?', 'Im Kirmes-Kiosk, in der Bäckerei oder im Spielwarenladen?', "Tippe auf Los geht's.",
         'Heute kaufst du am Kirmes-Kiosk ein.', 'Heute kaufst du in der Bäckerei ein.', 'Heute kaufst du im Spielwarenladen ein.',
         'Hier stehen die Preise.', 'Rechne noch einmal.', 'Rechne zuerst alle Preise zusammen.',
         'Rechne die Preise Schritt für Schritt zusammen.', 'Tippe auf Kamera-App.',
         'Halte das weiße Blatt in den Rahmen.', 'Dann drück auf den gelben Knopf.',
         'Ich sehe kein Geld.', 'Leg das Geld auf ein weißes Blatt und fotografiere von oben.', 'Der Betrag stimmt.',
         'Aber du hast zu viele Ein-Euro-Münzen.', 'Tausche zwei Ein-Euro-Münzen gegen ein Zwei-Euro-Stück.',
         'Ich bin mir nicht sicher.', 'Leg die Münzen mit etwas Abstand, ohne Schatten und ohne Spiegelung.',
         'Mach bitte noch ein Foto.', 'Dein Rückgeld passt genau.', 'Dein Geld passt genau.', 'Das passt noch nicht.',
         'Rechne noch einmal und zähle dein Geld.', 'Zieh zuerst Geld in das Feld.', 'Welches Schild passt zum Rückgeld?',
         'Welches Preis-Schild passt?', 'Schau noch mal.', 'Zähle dein Geld im Feld.', 'Zähle dein Geld auf dem Foto.',
         'Das Geld reicht.', 'Das Geld reicht nicht.', 'Schau noch einmal.', 'Rechne die Preise zusammen und vergleiche mit deinem Geld.',
         'Du hast alle Aufgaben geschafft.', 'Wir üben das noch ein bisschen.', 'Du bist bereit für eine Neuerung:',
         'Tippe auf eine Sache, dann hörst du den Preis.', 'Du hast alles gefunden.',
         'Was möchtest du kaufen?', 'Das ist zu teuer.', 'Dein Korb ist voll. Tippe auf Fertig.', 'Ein neuer Aufkleber für dein Album.',
         'Such dir eine Sache im Laden aus.', 'Such dir zwei Sachen im Laden aus.', 'Such dir drei Sachen im Laden aus.',
         'Such dir vier Sachen im Laden aus.', 'Such dir fünf Sachen im Laden aus.')

    # Laden-Ansicht: „Ein Kakao kostet 1 Euro 90.“ (wie satzPreis() in index.html: Nominativ, Betrag wie sprichBetrag)
    sprech = dict((m[0].strip("'"), m[1]) for m in re.findall(r"('?[\w-]+'?): \['([^']+)', '[^']+'\]", html[html.index('const SPRECH'):html.index('const ZAHL_SPRECH')]))
    for liste, cent in [('PRODUKTE_KIRMES', False), ('PRODUKTE_SPIELWAREN', False), ('PRODUKTE_BAECKEREI', True)]:
        a = html.index(f'const {liste}'); b = html.index('];', a)
        for pid, name, preis in re.findall(r"id: '([^']+)', name: '([^']+)', preis: (\d+)", html[a:b]):
            f = re.sub(r'^einen ', 'ein ', sprech.get(pid, name)); f = f[0].upper() + f[1:]
            anzeige, sprich = cent_text(int(preis)) if cent else euro_text(int(preis))
            teil(f'{f} kostet {anzeige}.', f'{f} kostet {sprich}.')
    # Satzteile als Rückfall (Name, ungewöhnliche Beträge, Anzahl der Aufgaben)
    for t in ['Hallo', 'Ich bezahle mit', 'Ich habe', 'dabei.', 'Das sind genau', 'Rückgeld.', 'Du hast', 'hingelegt.',
              'Ich sehe', 'Du bekommst', 'zurück.', 'Zusammen kostet es', 'Dann zieh das von', 'ab.',
              'Aufgaben geschafft.', 'davon ganz ohne Hilfe!']:
        teil(t)
    for n in range(0, 101):
        teil(str(n), 'eins' if n == 1 else str(n))
    for a, s in euro:
        teil(a, s)
    for c in range(10, 100, 10):
        teil(f'{c} Cent')
    for a, s in scheine:
        teil(a, s)

    # doppelte Schlüssel entfernen (erster gewinnt)
    gesehen, liste = set(), []
    for anzeige, sprich, stimme in teile:
        k = schluessel(anzeige)
        if k and k not in gesehen:
            gesehen.add(k); liste.append((k, aussprache(sprich), stimme))
    return liste


PUFFER = 0.15   # Sekunden Stille vorn und hinten (wie TON_RAND in index.html)


def aufbereiten(pfad_ein, pfad_aus, ziel_rms=3200):
    """Stille am Rand kürzen, alle Bausteine gleich laut, vorn und hinten PUFFER Stille.
    Der Puffer schützt die Wortenden: manche Geräte schneiden beim Entpacken von AAC
    am Anfang oder Ende ein Stück ab – dann trifft es nur die Stille."""
    with wave.open(pfad_ein) as w:
        p = w.getparams(); d = array.array('h', w.readframes(p.nframes))
    r = p.framerate
    spitze0 = max((abs(v) for v in d), default=1) or 1
    schwelle = max(80, int(spitze0 * 0.012))   # leise Laute (s, n, ch) am Wortende behalten
    laut = [i for i, v in enumerate(d) if abs(v) > schwelle]
    if laut:
        d = d[max(0, laut[0] - int(r * 0.04)):min(len(d), laut[-1] + int(r * 0.09))]
    stimmhaft = [v for v in d if abs(v) > schwelle] or [1]
    rms = math.sqrt(sum(v * v for v in stimmhaft) / len(stimmhaft))
    spitze = max(abs(v) for v in d) or 1
    faktor = min(ziel_rms / rms, 30000 / spitze)
    blende = int(r * 0.008)
    n = len(d)
    d = array.array('h', (max(-32767, min(32767, int(v * faktor * min(1, (i + 1) / blende, (n - i) / blende)))) for i, v in enumerate(d)))
    stille = array.array('h', [0] * int(r * PUFFER))
    d = stille + d + stille
    with wave.open(pfad_aus, 'wb') as w:
        w.setparams(p); w.writeframes(d.tobytes())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--piper', required=True, help='Python mit installiertem piper-tts')
    ap.add_argument('--modell', required=True, help='de_DE-thorsten-high.onnx')
    ap.add_argument('--lob-modell', required=True, help='de_DE-thorsten_emotional-medium.onnx')
    ap.add_argument('--lob-stimmung', default='amused', help='amused, surprised, neutral …')
    ap.add_argument('--tempo', type=float, default=1.12, help='length_scale: größer = langsamer')
    a = ap.parse_args()

    stimmen = {'normal': (a.modell, None), 'lob': (a.lob_modell, a.lob_stimmung)}
    liste = sammle('lob')
    os.makedirs(ZIEL, exist_ok=True)
    index, auftrag = {}, {'normal': [], 'lob': []}
    for k, sprich, stimme in liste:
        datei = hashlib.sha1(f'{TON_STAND}|{stimmen[stimme]}|{a.tempo}|{sprich}'.encode()).hexdigest()[:12] + '.m4a'
        index[k] = datei
        if not os.path.exists(os.path.join(ZIEL, datei)):
            auftrag[stimme].append((sprich, datei))
    print(f'{len(liste)} Bausteine, {sum(map(len, auftrag.values()))} neu zu erzeugen', flush=True)

    code = (
        'import sys, json, wave\n'
        'from piper import PiperVoice, SynthesisConfig\n'
        'v = PiperVoice.load(sys.argv[1]); sm = v.config.speaker_id_map\n'
        'cfg = SynthesisConfig(length_scale=float(sys.argv[3]), normalize_audio=False,\n'
        '                      speaker_id=sm[sys.argv[5]] if sys.argv[5] != "-" else None)\n'
        'for i, t in enumerate(json.load(open(sys.argv[2]))):\n'
        '    with wave.open(f"{sys.argv[4]}/{i}.wav", "wb") as w: v.synthesize_wav(t, w, syn_config=cfg)\n'
        '    if i % 200 == 0: print("  ", i, flush=True)\n'
    )
    for stimme, jobs in auftrag.items():
        if not jobs:
            continue
        modell, stimmung = stimmen[stimme]
        with tempfile.TemporaryDirectory() as tmp:
            json.dump([s for s, _ in jobs], open(os.path.join(tmp, 'texte.json'), 'w'))
            subprocess.run([a.piper, '-c', code, modell, os.path.join(tmp, 'texte.json'), str(a.tempo), tmp, stimmung or '-'], check=True)
            for i, (_, datei) in enumerate(jobs):
                roh, fertig = os.path.join(tmp, f'{i}.wav'), os.path.join(tmp, f'{i}k.wav')
                aufbereiten(roh, fertig)
                subprocess.run(['afconvert', '-f', 'm4af', '-d', 'aac', '-b', '32000', fertig, os.path.join(ZIEL, datei)], check=True)

    # nicht mehr benutzte Dateien entfernen
    for f in os.listdir(ZIEL):
        if f.endswith('.m4a') and f not in index.values():
            os.remove(os.path.join(ZIEL, f))
    json.dump(index, open(os.path.join(ZIEL, 'index.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'), sort_keys=True)
    groesse = sum(os.path.getsize(os.path.join(ZIEL, f)) for f in os.listdir(ZIEL))
    print(f'fertig: {len(index)} Dateien, {groesse / 1e6:.1f} MB')


if __name__ == '__main__':
    sys.exit(main())
