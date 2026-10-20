# Kirmes-Kiosk

Eine Lern-App für den Mathe-Unterricht (Förderschwerpunkt GG): Das Kind sieht Sachen vom Kirmes-Kiosk, rechnet die Preise zusammen, legt das passende Spielgeld auf ein weißes Blatt und fotografiert es. Die App erkennt Münzen und Scheine auf dem Foto und sagt, ob der Betrag stimmt. Schreiben ist nicht nötig.

Alles läuft im Browser: kein Server, kein Konto, keine KI-Dienste. Die Fotos verlassen das Gerät nicht. Die App funktioniert nach dem ersten Öffnen auch offline.

**App:** https://walteroelf.github.io/kirmes-kiosk/

## Dateien

| Datei | Inhalt |
|---|---|
| `index.html` | Die App (Oberfläche, Aufgaben, Stufen, Einstellungen, Auswertung) |
| `erkennung.js` | Die Geld-Erkennung und der Fotocheck |
| `worker.js` | Führt die Erkennung im Hintergrund aus, damit nichts einfriert |
| `sw.js`, `manifest.webmanifest`, `icons/` | Offline-Fähigkeit und App-Symbol für den Home-Bildschirm |
| `bilder/` | Produktbilder: eigens für diese App gezeichnete Vektorgrafiken (SVG), keine fremden Bilder; `bilder/spielwaren/` und `bilder/baeckerei/` für die weiteren Läden |
| `schriften/` | Schriften Andika und Grandstander (SIL Open Font License), lokal eingebunden |
| `tests/` | Automatischer Test mit künstlichen Szenen und eine Prüfseite für echte Fotos |

## Drei Läden

Im Lehrkraft-Bereich unter **„Laden“** (oder per Link `…?laden=…`) wählbar. Jeder Laden hat eigene Waren, eigene Stufen, eigenen Fortschritt und eine eigene Auswertung.

| Laden | Zahlenraum | Geld im Vorrat | Geld legen |
|---|---|---|---|
| **Kirmes-Kiosk** (`laden=kirmes`, Standard) | ganze Euro bis ca. 30 € | 1 €, 2 €, 5 €, 10 €, 20 € | fotografieren oder ziehen |
| **Spielwarenladen** (`laden=spielwaren`) | ganze Euro bis ca. 200 € | zusätzlich 50 € und 100 € | ziehen |
| **Bäckerei** (`laden=baeckerei`) | Euro und Cent bis ca. 10 € | 10 ct, 20 ct, 50 ct, 1 €, 2 €, 5 € | ziehen |

**Spielwarenladen** – 20 Spielsachen von 3 € (Seifenblasen) bis 149 € (Fahrrad). Stufen: 2 Spielsachen bis 30 € → bis 60 € → 3 bis 100 € → Große Scheine (bis 150 €) → 4 bis 200 € → Rückgeld von 50 € → Rückgeld von 100 € → Reicht das Geld? (100 €).

**Bäckerei** – 20 Backwaren und Getränke von 0,40 € (Brötchen) bis 4,20 € (Vollkornbrot), alle Preise in 10-Cent-Schritten. Stufen: 1 Sache (bis 2 €) → 2 Sachen (bis 3 €) → 3 (bis 5 €) → 4 (bis 8 €) → 5 (bis 10 €) → Rückgeld von 5 € → Rückgeld von 10 € → Reicht das Geld? (5 €).

Die Kamera-Erkennung kennt nur 1-€-/2-€-Münzen und 5-/10-/20-€-Scheine; darum wird in Spielwarenladen und Bäckerei das Geld immer auf dem Gerät ins Feld gezogen.

## Auf dem iPad einrichten

1. Die App-Adresse in Safari öffnen.
2. **Teilen → Zum Home-Bildschirm**. Danach startet die App wie ein normales Programm und läuft auch ohne WLAN.
3. Beim ersten Foto fragt das iPad, ob die App die Kamera benutzen darf: **Erlauben**.
4. Auf das **Zahnrad** oben rechts tippen und den angezeigten **Code** eintippen → Lehrkraft-Bereich (siehe unten).

## Was das Kind macht

Es gibt zwei Wege, das Geld zu legen (umschaltbar im Lehrkraft-Bereich unter **„Geld legen“**):

- **Spielgeld legen und fotografieren** (haptisch, mit echtem Spielgeld und Kamera).
- **Geld auf dem Gerät ins Feld ziehen** (virtuell, ohne Kamera): Links liegen 1-€- und 2-€-Münzen sowie 5-, 10- und 20-€-Scheine. Das Kind zieht sie mit dem Finger in das große Feld oder tippt sie einfach an (leichter bei motorischen Schwierigkeiten). Geld im Feld antippen oder herausziehen legt es zurück. Mit **Fertig** prüft die App. Gilt „höchstens zwei 1-€-Stücke“, zeigt die 1-€-Münze, wie viele noch übrig sind. Alles andere (Stufen, Preis-Schild, Hilfen, Auswertung) funktioniert genauso wie beim Fotografieren.

- **Einkaufen**: Sachen ansehen, Preise zusammenrechnen, Geld legen, Foto.
- **Rückgeld**: „Ich bezahle mit 10 €“ – das Rückgeld legen und fotografieren.
- **Reicht das Geld?**: „Ich habe 10 €“ – mit großem Knopf *Ja, das reicht* / *Nein, zu wenig* antworten.
- **Gesamtbetrag wählen** (per Haken im Lehrkraft-Bereich, unabhängig von Stufe und Schwierigkeit): Am Ende wählt das Kind den Gesamtbetrag bzw. das Rückgeld aus 4 Preis-Schildern. Solange der Haken gesetzt ist, nennt die App vorher keinen Betrag.
- Knöpfe oben: **Vorlesen** (Lautsprecher), **Preisliste** (Preisschild-Symbol).

### Kamera mit Rahmen

„Foto vom Geld“ öffnet ein Kamerabild mit Rahmen („Das weiße Blatt in den Rahmen“). Unten liegt eine feste Leiste mit dem großen gelben **Auslöser** (aktiv, sobald ein Kamerabild da ist), **Zurück** und **Kamera-App**. Gezeigt wird immer das ganze Kamerabild – genau das kommt aufs Foto.

Wird die Kamera nicht erlaubt oder kommt nach 6 Sekunden kein Bild, sagt die App „Tippe auf Kamera-App“ und merkt sich das für dieses Gerät: Danach öffnet „Foto vom Geld“ direkt die normale Kamera-App des iPads. Im Lehrkraft-Bereich lässt sich die Kamera in der App ab- und wieder einschalten (das setzt die Merkung zurück).

### Rückmeldungen

- Richtig: Lob (mit Namen, falls eingetragen) und ein kurzer Ton.
- Falsch: „Das passt noch nicht. Rechne noch einmal und zähle dein Geld.“ – bewusst **ohne** „zu viel / zu wenig“, damit nicht geraten wird.
- Unsicher (verschmolzene Münzen, starker Glanz): Stellen werden mit **?** markiert, die App bittet um ein neues Foto, statt zu korrigieren.
- **Fotocheck**: Ist das Foto zu dunkel, verwackelt oder ist kein weißes Blatt zu sehen, sagt die App das konkret („Halte das Tablet ganz ruhig …“). Solche Fotos zählen nicht als Fehlversuch.

### Gestufte Hilfe

Nach dem **2. Fehlversuch** erscheint *Hilfe: Preise zeigen*, nach dem **3.** *Hilfe: Schritt für Schritt* (z. B. „3 € + 2 € + 1 € = ?“). Die Lösung wird nie verraten. Abschaltbar.

## Stufen (wie die „Neu ab hier“-Karten auf TaskCards)

| Stufe | Inhalt |
|---|---|
| 1 | 2 Sachen einkaufen (bis 10 €) |
| 2 | 3 Sachen (bis 12 €) |
| 3 | 4 Sachen (bis 15 €) |
| 4 | Weniger 1-€-Stücke: höchstens zwei 1 € (Bündeln) |
| 5 | 5 Sachen einkaufen (bis 15 €, höchstens zwei 1 €) |
| 6 | Größere Beträge bis 20 € |
| 7 | Rückgeld (bezahlt mit 10 €) |
| 8 | Reicht das Geld? (10 € dabei) |

Nach einer einstellbaren Zahl gelöster Aufgaben (Standard 8; gezählt werden Aufgaben mit höchstens 2 Fotos und ohne Hilfe) erscheint die Karte **„Neu ab hier“** mit Lob, und die nächste Stufe beginnt. Optional geht es nach 3 schweren Aufgaben in Folge eine Stufe zurück. Statt Stufen kann im Lehrkraft-Bereich auch **„Feste Einstellungen“** gewählt werden (Aufgabe, Anzahl Sachen, gerade/ungerade, Höchstbetrag, Bezahlen mit, 1-€-Münzen). Ob am Ende der Gesamtbetrag aus 4 Möglichkeiten gewählt wird, stellt ein eigener Haken ein – er gilt für jede Stufe und für feste Einstellungen.

## Lehrkraft-Bereich

**Öffnen:** Zahnrad oben rechts antippen. Es erscheint ein Code aus vier Zahlen, **als Wörter geschrieben** (z. B. „acht · drei · fünf · neun“), der mit dem Zahlenfeld eingetippt wird (also 8 3 5 9). Der Code ist jedes Mal neu; bei einer falschen Eingabe kommt sofort ein neuer. Kinder, die (noch) nicht lesen, können den Bereich so nicht öffnen.

- **Geld legen**: fotografieren oder auf dem Gerät ziehen (auch per Link: `…?geld=ziehen`)
- **Gesamtbetrag wählen**: Haken an/aus – am Ende den Gesamtbetrag aus 4 Möglichkeiten wählen (Link: `…&schild=1`)

- Name (optional, nur auf diesem Gerät), Ablauf (Stufen oder fest), Aufgaben pro Runde
- Hilfen, Töne und Vorlesen, Kamera mit Rahmen, Vorschaubilder im Protokoll
- **Bedienung mit einem Taster**: Eine blaue Markierung wandert von Knopf zu Knopf (1,5 / 2,5 / 4 Sekunden). Auswählen mit Leertaste/Enter (viele Taster für das iPad senden diese Tasten) oder durch Tippen irgendwo auf den Bildschirm. Alternativ hat das iPad selbst die „Schaltersteuerung“ (Einstellungen → Bedienungshilfen).
- **Link mit diesen Einstellungen** für TaskCards oder einen QR-Code, z. B.
  `…/kirmes-kiosk/?modus=stufen&stufe=4&aufstieg=8&runde=10`
  oder fest: `…/kirmes-kiosk/?modus=fest&art=kaufen&anzahl=4&betrag=ungerade&max=15&einer=2&schild=1&runde=10`
  Der Name kommt absichtlich nicht in den Link.
- **Auswertung für den Förderplan**: Zusammenfassung („… davon 85 % ohne Hilfe gelöst. Sicher: bis 10 €. Noch schwierig: 16–20 €.“) und Tabellen nach Stufe, Betrag und Anzahl der Sachen, für 7 Tage, 30 Tage oder alles. **Drucken** oder **Als Tabelle speichern** (CSV, öffnet in Excel/Numbers).
- **Protokoll der Fotos** mit Ergebnis, auf Wunsch mit Vorschaubild.
- **Wenn die Erkennung sich irrt**: unter dem Foto *Erkennung korrigieren* → Markierung antippen wechselt 1 € → 2 € → 5 € → 10 € → 20 € → entfernen; leere Stelle antippen fügt 1 € hinzu.
- Unten: Versionsnummer und ob die App offline verfügbar ist.

## Tipps für gute Fotos

- Weißes Blatt als Unterlage (die „Unterlage für Geld“ funktioniert gut)
- Münzen mit etwas Abstand; Scheine nebeneinander, nicht übereinander
- Kein Schatten, keine Spiegelung; möglichst von oben
- Kein Preisschild mit aufs Foto (das Schild wählt das Kind in der App)

## Bilder und Rechte

Alle Produktbilder (je 20 für Kirmes-Kiosk, Spielwarenladen und Bäckerei) und das App-Symbol wurden eigens für diese App neu gezeichnet (SVG-Vektorgrafiken im Ordner `bilder/`). Sie enthalten keine Bilder aus anderen Programmen oder Sammlungen (z. B. Worksheet Crafter), deren Lizenz eine Veröffentlichung in einer App oder auf einer Website nicht erlaubt. Die Schriften stehen unter der SIL Open Font License.

## Datenschutz

- **Fotos** werden nur im Browser ausgewertet, nicht hochgeladen und nicht gespeichert. Ausnahme: Ist „Vorschaubilder im Protokoll speichern“ eingeschaltet, bleibt ein kleines Vorschaubild im Browser-Speicher dieses Geräts (standardmäßig aus).
- **Name, Einstellungen, Stufe, Protokoll und Auswertung** liegen nur im Browser-Speicher dieses Geräts. Name nicht im Link, nicht im Protokoll, nicht in der Auswertung.
- **Keine fremden Server**: keine Google-Schriften, keine Statistik, keine Cookies, keine Werbung.
- **Vorlesen** nutzt nur Stimmen, die auf dem Gerät installiert sind. Online-Stimmen werden bewusst nicht verwendet.
- **Löschen**: „Alle Daten auf diesem Gerät löschen“ im Lehrkraft-Bereich.

GitHub Pages ist der Webhoster: Beim Aufruf verarbeitet GitHub wie jeder Webserver technisch die IP-Adresse. Der Ordner kann genauso auf den Schulserver gelegt werden (nötig ist nur https).

## Wie die Erkennung arbeitet

0. **Weißabgleich über das Papier**: gleicht Farbstich (Glühbirne, Neonröhre) und Schatten aus.
1. Alles, was sich vom hellen Papier abhebt, wird als Fläche ausgeschnitten.
2. Ovale Flächen sind Münzen. **1 €**: Ring golden, Mitte silbern. **2 €**: Mitte golden, Ring silbern.
3. Sich berührende Münzen werden an der engsten Stelle getrennt.
4. Große rechteckige, bedruckte Flächen sind Scheine; die Farbe entscheidet: 5 € grau-grün, 10 € rot, 20 € blau, 50 € orange. Ein Schein ist etwa 18-mal so groß wie eine Münze – deutlich größere Flächen oder zwei Scheinfarben in einer Fläche gelten als „überlappende Scheine“ → neues Foto.
5. **Münzen auf Scheinen** werden über ihre goldenen Teile gefunden.
   Einfarbig goldene Kreise (gedruckte Münz-Bildchen auf der Unterlage, Cent-Münzen) werden ignoriert – die Aufgaben rechnen nur mit ganzen Euro.
   Nah fotografierte Münzen: Die App erkennt die Münzgröße und passt den Weißabgleich daran an.
6. Farben werden als Median gemessen; Glanzlichter zählen nicht. Verdeckt Glanz die Mitte, entscheidet der Ring.
7. Unsichere Stellen → **?** und Bitte um ein neues Foto.

## Tests

**Automatisch (bei jeder Änderung auf GitHub):** `node tests/test.js` erzeugt rund 150 künstliche Szenen (normal, 5-/10-/20-€-Scheine, zwei Scheine, überlappende Scheine, Münze auf Schein, sich berührende Münzen, warmes und kaltes Licht, Schattenverlauf, Schattenkante, Spiegelungen, dunkel, unscharf, viele Münzen, **nah fotografiert** – auch mit Schein, Tischkante, warmem Licht und **Kopfzeile der Unterlage mit gedruckten Münz-Bildchen** und Preisschild) und prüft den Fotocheck. Stand Version 2.0.2: 140 von 146 Szenen richtig, 5-mal Bitte um neues Foto, 1 falsches Urteil (bei überlappenden Scheinen).

**Echte Fotos:** `tests/pruefen.html` öffnen (z. B. `…/kirmes-kiosk/tests/pruefen.html`), Fotos hineinziehen. Steht der richtige Betrag im Dateinamen (`12euro.jpg`), wird automatisch verglichen. Nichts wird hochgeladen. Bitte keine Fotos mit Kindern ins Repository legen.

Bisher an 15 echten Spielgeld-Fotos geprüft (14 richtig, 1-mal neues Foto, auch bei warmem, kaltem und grünlichem Licht). 10-€- und 20-€-Scheine sowie Münzen auf Scheinen sind bisher nur an künstlichen Szenen getestet.

## Neue Version veröffentlichen

In `index.html` (`VERSION`) und `sw.js` (`VERSION`) die Versionsnummer erhöhen, dann hochladen. Geräte holen sich die neue Fassung beim nächsten Öffnen mit Internet.
