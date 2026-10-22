#!/usr/bin/env python3
"""
Erzeugt die Ansagen (Ordner ton/) mit Piper und der Thorsten-Stimme (de_DE-thorsten-high, Datensatz CC0).

Die App setzt jeden Vorlese-Text aus diesen Bausteinen zusammen: ganze Sätze, Satzteile,
Waren, Zahlen und Beträge. Was fehlt, liest die Stimme des Geräts (z. B. der Name des Kindes).

Aufruf (Piper muss installiert sein, siehe README):
  python werkzeuge/ansagen.py --piper /pfad/zu/venv/bin/python --modell /pfad/de_DE-thorsten-high.onnx

Nach Änderungen an Vorlese-Texten, Waren oder Stufen neu ausführen und die VERSION in index.html/sw.js erhöhen.
"""
import argparse, hashlib, json, os, re, subprocess, sys, tempfile, wave, array

HIER = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(HIER)
ZIEL = os.path.join(APP, 'ton')


def schluessel(text):
    """Wie tonSchluessel() in index.html: Wörter klein, Satzzeichen am Rand weg."""
    woerter = text.replace('€', 'Euro').split()
    return ' '.join(w for w in (re.sub(r'^[\W_]+|[\W_]+$', '', w.lower()) for w in woerter) if w)


def saetze(text):
    return [t for t in re.split(r'(?<=[.!?:])\s+', text.replace('€', 'Euro').strip()) if t]


def sammle():
    html = open(os.path.join(APP, 'index.html'), encoding='utf-8').read()
    teile = []  # (Text in der App, gesprochener Text)

    def satz(*texte):
        for t in texte:
            for s in saetze(t):
                teile.append((s, s))

    # Waren: Einzahl mit Artikel und Mehrzahl
    for ein, mehr in re.findall(r"\['([^']+)', '([^']+)'\]", html[html.index('const SPRECH'):html.index('const ZAHL_SPRECH')]):
        teile += [(ein, ein), (mehr, mehr)]
    for w in ['zwei', 'drei', 'vier', 'fünf', 'sechs', 'und', 'Ich möchte', 'kaufen.']:
        teile.append((w, w))

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
         'Welches Preis-Schild passt?', 'Richtig!', 'Schau noch mal.', 'Zähle dein Geld im Feld.', 'Zähle dein Geld auf dem Foto.',
         'Das Geld reicht.', 'Das Geld reicht nicht.', 'Schau noch einmal.', 'Rechne die Preise zusammen und vergleiche mit deinem Geld.',
         'Super!', 'Geschafft!', 'Du hast alle Aufgaben geschafft.', 'Wir üben das noch ein bisschen.',
         'Das klappt schon super!', 'Du bist bereit für eine Neuerung:')
    # Satzteile rund um Beträge, Zahlen und den Namen
    for t in ['Hallo', 'Ich bezahle mit', 'Ich habe', 'dabei.', 'Das sind genau', 'Rückgeld.', 'Du hast', 'hingelegt.',
              'Ich sehe', 'Du bekommst', 'zurück.', 'Zusammen kostet es', 'Dann zieh das von', 'ab.',
              'Aufgaben geschafft.', 'davon ganz ohne Hilfe!']:
        teile.append((t, t))

    # Zahlen und Beträge
    for n in range(0, 101):
        teile.append((str(n), 'eins' if n == 1 else str(n)))
    for n in range(1, 201):
        teile.append((f'{n} Euro', 'ein Euro' if n == 1 else f'{n} Euro'))
    for c in range(10, 100, 10):
        teile.append((f'{c} Cent', f'{c} Cent'))
    for n, wort in [(5, 'Fünf'), (10, 'Zehn'), (20, 'Zwanzig'), (50, 'Fünfzig'), (100, 'Hundert')]:
        teile.append((f'einem {n}-Euro-Schein', f'einem {wort}-Euro-Schein'))

    # doppelte Schlüssel entfernen (erster gewinnt)
    gesehen, liste = set(), []
    for anzeige, sprich in teile:
        k = schluessel(anzeige)
        if k and k not in gesehen:
            gesehen.add(k); liste.append((k, sprich))
    return liste


def beschneide(pfad_ein, pfad_aus, schwelle=400, rand_ms=25):
    """Stille am Anfang und Ende entfernen (die App setzt die Pausen selbst)."""
    with wave.open(pfad_ein) as w:
        p = w.getparams(); daten = array.array('h', w.readframes(p.nframes))
    laut = [i for i, v in enumerate(daten) if abs(v) > schwelle]
    if laut:
        rand = int(p.framerate * rand_ms / 1000)
        daten = daten[max(0, laut[0] - rand):min(len(daten), laut[-1] + rand)]
    with wave.open(pfad_aus, 'wb') as w:
        w.setparams(p); w.writeframes(daten.tobytes())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--piper', required=True, help='Python mit installiertem piper-tts')
    ap.add_argument('--modell', required=True, help='de_DE-thorsten-high.onnx')
    ap.add_argument('--tempo', type=float, default=1.12, help='length_scale: größer = langsamer')
    a = ap.parse_args()

    liste = sammle()
    os.makedirs(ZIEL, exist_ok=True)
    index, auftrag = {}, []
    for k, sprich in liste:
        datei = hashlib.sha1(k.encode()).hexdigest()[:10] + '.m4a'
        index[k] = datei
        if not os.path.exists(os.path.join(ZIEL, datei)):
            auftrag.append((sprich, datei))
    print(f'{len(liste)} Bausteine, {len(auftrag)} neu zu erzeugen')

    with tempfile.TemporaryDirectory() as tmp:
        if auftrag:
            # Piper einmal starten und alle Texte synthetisieren
            code = (
                'import sys, json, wave\n'
                'from piper import PiperVoice, SynthesisConfig\n'
                'v = PiperVoice.load(sys.argv[1]); cfg = SynthesisConfig(length_scale=float(sys.argv[3]))\n'
                'for i, t in enumerate(json.load(open(sys.argv[2]))):\n'
                '    with wave.open(f"{sys.argv[4]}/{i}.wav", "wb") as w: v.synthesize_wav(t, w, syn_config=cfg)\n'
            )
            json.dump([s for s, _ in auftrag], open(os.path.join(tmp, 'texte.json'), 'w'))
            subprocess.run([a.piper, '-c', code, a.modell, os.path.join(tmp, 'texte.json'), str(a.tempo), tmp], check=True)
            for i, (_, datei) in enumerate(auftrag):
                roh, kurz = os.path.join(tmp, f'{i}.wav'), os.path.join(tmp, f'{i}k.wav')
                beschneide(roh, kurz)
                subprocess.run(['afconvert', '-f', 'm4af', '-d', 'aac', '-b', '32000', kurz, os.path.join(ZIEL, datei)], check=True)

    # nicht mehr benutzte Dateien entfernen
    for f in os.listdir(ZIEL):
        if f.endswith('.m4a') and f not in index.values():
            os.remove(os.path.join(ZIEL, f))
    json.dump(index, open(os.path.join(ZIEL, 'index.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'), sort_keys=True)
    groesse = sum(os.path.getsize(os.path.join(ZIEL, f)) for f in os.listdir(ZIEL))
    print(f'fertig: {len(index)} Dateien, {groesse / 1e6:.1f} MB')


if __name__ == '__main__':
    sys.exit(main())
