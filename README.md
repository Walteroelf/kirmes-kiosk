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
| `ton/` | Ansagen mit der Thorsten-Stimme (AAC), `ton/index.json` ordnet Text → Datei zu |
| `werkzeuge/ansagen.py` | Erzeugt die Ansagen neu (siehe „Vorlesen“) |
| `symbole.js` | Die 12 Bilder, mit denen sich die Kinder auf einem Gerät erkennen (statt Namen) |
| `aufkleber.js`, `werkzeuge/aufkleber.py` | Aufkleber für das Sammelalbum und das Skript, das sie zeichnet |
| `laeden/`, `werkzeuge/laeden.py` | Die drei gezeichneten Läden (SVG) und das Skript, das sie erzeugt (`python3 werkzeuge/laeden.py`); Preise und Markierungen setzt die App selbst ein |
| `schriften/` | Schriften Andika und Grandstander (SIL Open Font License), lokal eingebunden |
| `tests/` | Automatischer Test mit künstlichen Szenen und eine Prüfseite für echte Fotos |

## Drei Läden

**Aufgabenseite ohne Scrollen:** Auf dem iPad quer stehen links „Das möchte ich kaufen“ (Sachen untereinander, ab 4 Sachen kleiner) und der Knopf „Zum Laden“, rechts die Kasse mit Zahlteller, Geldschublade und „Fertig“. Auf dem iPad hoch stehen die Sachen als kleine Kacheln oben, die Kasse darunter. „Aufgabe 3 von 10“ steht in der Kopfzeile. Auf dem Handy wird wie gewohnt gescrollt.

**Startbildschirm:** Beim Öffnen geht ein roter Vorhang mit dem Schild „Einkaufen!“ auf (knapp 2 Sekunden; Tippen überspringt ihn; bei „Bewegung reduzieren“ entfällt er). Dann wählt das Kind den Laden (große Karten nur mit Bild und Name) oder tippt darunter auf **„Weiter wie zuletzt“**. Der Knopf **ⓘ Info** zeigt den mathematischen Anspruch jedes Ladens und die aktuelle Stufe (ohne Code, nur zum Lesen). Im Lehrkraft-Bereich lässt sich die freie Wahl abschalten (*Laden & Schwierigkeit* → „Immer derselbe Laden“); dann gibt es nur „Los geht's“ im eingestellten Laden. Nach einer Runde führt **„Anderer Laden“** zurück zum Start.

**Schwierigkeit je Laden (Lehrkraft):** Im Lehrkraft-Bereich unter *Laden & Schwierigkeit*; „Schwierigkeit festlegen (Lehrkraft)“ auf dem Startbildschirm öffnet (mit Code) direkt diesen Abschnitt. Für jeden Laden wird eine der 8 Stufen gewählt (Liste untereinander, mit Namen). Dazu: **Steigert sich** (nächste Stufe nach gelösten Aufgaben) oder **Bleibt** (übt auf der gewählten Stufe). Die Wahl gilt sofort. Mit `…?start=0` startet die App ohne Startbildschirm.

Im Lehrkraft-Bereich ist der feste Laden unter **„Immer derselbe Laden“** (oder per Link `…?laden=…`) einstellbar. Jeder Laden hat eigene Waren, eigene Stufen, eigenen Fortschritt und eine eigene Auswertung.

| Laden | Zahlenraum | Geld im Vorrat | Geld legen |
|---|---|---|---|
| **Kirmes-Kiosk** (`laden=kirmes`, Standard) | ganze Euro bis ca. 30 € | 1 €, 2 €, 5 €, 10 €, 20 € | fotografieren oder ziehen |
| **Spielwarenladen** (`laden=spielwaren`) | ganze Euro bis ca. 200 € | zusätzlich 50 € und 100 € | ziehen |
| **Bäckerei** (`laden=baeckerei`) | Euro und Cent bis ca. 10 € | 10 ct, 20 ct, 50 ct, 1 €, 2 €, 5 € | ziehen |

**Spielwarenladen** – 20 Spielsachen von 3 € (Seifenblasen) bis 149 € (Fahrrad). Stufen: 2 Spielsachen bis 30 € → bis 60 € → 3 bis 100 € → Große Scheine (bis 150 €) → 4 bis 200 € → Rückgeld von 50 € → Rückgeld von 100 € → Reicht das Geld? (100 €).

**Bäckerei** – 20 Backwaren und Getränke von 0,40 € (Brötchen) bis 4,20 € (Vollkornbrot), alle Preise in 10-Cent-Schritten. Stufen: 1 Sache (bis 2 €) → 2 Sachen (bis 3 €) → 3 (bis 5 €) → 4 (bis 8 €) → 5 (bis 10 €) → Rückgeld von 5 € → Rückgeld von 10 € → Reicht das Geld? (5 €).

Die Kamera-Erkennung kennt nur 1-€-/2-€-Münzen und 5-/10-/20-€-Scheine; darum wird in Spielwarenladen und Bäckerei das Geld immer auf dem Gerät auf den Zahlteller gezogen.

## Auf dem iPad einrichten

1. Die App-Adresse in Safari öffnen.
2. **Teilen → Zum Home-Bildschirm**. Danach startet die App wie ein normales Programm und läuft auch ohne WLAN.
3. Beim ersten Foto fragt das iPad, ob die App die Kamera benutzen darf: **Erlauben**.
4. Auf das **Zahnrad** oben rechts tippen und den angezeigten **Code** eintippen → Lehrkraft-Bereich (siehe unten).

## Was das Kind macht

Es gibt zwei Wege, das Geld zu legen (umschaltbar im Lehrkraft-Bereich unter **„Geld & Kamera“**):

- **Spielgeld legen und fotografieren** (haptisch, mit echtem Spielgeld und Kamera).
- **Geld auf dem Gerät auf den Zahlteller ziehen** (virtuell, ohne Kamera): Unter dem **Zahlteller** (in der Ladenfarbe) liegt das Geld in einer **Geldschublade** mit einem Fach je Münze und Schein (Kirmes: 1 €, 2 €, 5 €, 10 €, 20 €). Das Kind zieht es mit dem Finger auf den Teller oder tippt es einfach an (leichter bei motorischen Schwierigkeiten). Geld auf dem Teller antippen oder herunterziehen legt es zurück. Die Rückmeldung („Super!“ / „Das passt noch nicht.“ mit „Noch einmal“) erscheint auf dem Teller – nichts verschiebt sich. Münzen und Scheine sind möglichst echt gezeichnet (Rändelung, Bimetall, Hologrammstreifen), aber mit eigenen Motiven und dem Aufdruck „SPIELGELD“ (`geld.js`, keine Abbildungen echter Banknoten). Mit **Fertig** prüft die App. Gilt „höchstens zwei 1-€-Stücke“, zeigt die 1-€-Münze, wie viele noch übrig sind. Alles andere (Stufen, Preis-Schild, Hilfen, Auswertung) funktioniert genauso wie beim Fotografieren.

- **Einkaufen**: Sachen ansehen, Preise zusammenrechnen, Geld legen, Foto.
- **Rückgeld**: „Ich bezahle mit 10 €“ – das Rückgeld legen und fotografieren.
- **Reicht das Geld?**: „Ich habe 10 €“ – mit großem Knopf *Ja, das reicht* / *Nein, zu wenig* antworten.
- **Gesamtbetrag wählen** (Schalter im Lehrkraft-Bereich unter *Aufgaben*, unabhängig von Stufe und Schwierigkeit): Am Ende wählt das Kind den Gesamtbetrag bzw. das Rückgeld aus 4 Preis-Schildern. Solange der Schalter an ist, nennt die App vorher keinen Betrag.
- Knopf oben: **Vorlesen** (Lautsprecher).
- **Wunschzettel** (Lehrkraft-Bereich → Aufgaben, an/aus): Jede 3. Aufgabe einer Runde sucht das Kind die Sachen selbst im Laden aus. Die Anzahl gibt die Stufe vor; die App nennt den **Höchstbetrag** („Du darfst höchstens 12 € ausgeben.“ – auf der Karte, im Korb und gesprochen); Sachen, die ihn sprengen würden, sind blass und lassen sich nicht wählen („Das ist zu teuer.“). Gewähltes landet unten im **Korb** (antippen = zurücklegen); ist er voll, geht es mit **Fertig ausgesucht** wie gewohnt weiter (rechnen, Geld legen). Link: `…&wunsch=0` schaltet ihn aus.
- **Sammelalbum** („Mein Album“ auf der Startseite und nach jeder Runde): Nach jeder geschafften Runde gibt es einen Aufkleber für die Seite des Ladens – 12 je Laden (Kirmes: Riesenrad, Karussell …; Bäckerei: Backofen, Brezel …; Spielwaren: Teddy, Rakete …), flach im Stil München 72 (`aufkleber.js`, erzeugt mit `werkzeuge/aufkleber.py`). Unabhängig von Fehlern, ohne Punkte oder Vergleich.
- **Zum Laden** (großer Knopf in der Ladenfarbe bei „Das möchte ich kaufen“): öffnet den gezeichneten Laden über den ganzen Bildschirm (Ausschnitt nah am Laden, schmale Kopfzeile, Einkaufszettel und „← Zurück“ in einer Leiste unten) – Kirmes-Bude, Bäckerei oder Spielwarenladen mit allen 20 Waren und großen weißen Preisschildern (in der Bäckerei direkt am Korb, am Brot und vor jeder Reihe der Vitrine), einer **Wanduhr** (zeigt die echte Zeit; Antippen: „Es ist 10 Uhr 25.“) und **Lampen** zum An- und Ausschalten (Antippen; an = warmer Lichtschein unter der Lampe), Theke, Kasse und Verkäufer/in. **Antippen** einer Ware: Sie leuchtet auf, ihr Preisschild blinkt, Thorsten sagt z. B. „Ein Kakao kostet 1 Euro 90.“ **Einkaufszettel** unten: jede gesuchte Sache einzeln, auch doppelte (zwei Donuts = zwei Posten nebeneinander); Antippen eines Postens zeigt die Ware im Laden. Jedes Antippen einer gesuchten Ware im Laden **hakt einen Posten ab**, sein Preis steht dann auf dem Zettel („Alles gefunden!“). **Markierung** der gesuchten Waren (grüner Rahmen mit Korb) je nach Einstellung *als Hilfe nach einem Fehlversuch* (Standard), *immer* oder *nie* (Lehrkraft-Bereich → Hilfen; Link: `…&markieren=immer`). Mit dem Taster wandert die Markierung über die Waren, den Zettel und „Zurück“.

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

## Stufen in Themen

Jeder Laden hat feine Stufen in 6 Themen (Kirmes 26, Bäckerei 23, Spielwaren 21). Kirmes-Kiosk:

| Thema | Stufen |
|---|---|
| 1 · Geld kennen | eine Sache nur mit 1-€-Münzen · mit 1 € und 2 € · auch mit 5 € |
| 2 · Zusammenrechnen | 2 Sachen bis 10 € · 3 Sachen bis 12 € · 3 Sachen über 10 € (Zehnerübergang) · 4 Sachen bis 15 € · 5 Sachen bis 20 € |
| 3 · Geschickt legen | höchstens zwei 1-€-Stücke · 5 Sachen mit zwei 1-€-Stücken · größere Beträge · **mit möglichst wenig Geld** (die App prüft auch die Zahl der Stücke) · **Betrag anders legen** (z. B. 10 € ohne den 10-€-Schein – das Stück fehlt in der Schublade) |
| 4 · Mehrmals und Ergänzen | **zweimal dasselbe** · **dreimal dasselbe** (immer mit „2×“, „3×“) · **Wie viel fehlt noch?** („Ich habe schon 3 €“, die Ware kostet 5 €) |
| 5 · Rückgeld und Budget | Rückgeld von 5 € · von 10 € · von 20 € · Reicht das Geld? · Reicht das Geld? – knapp · **Wunschzettel mit Budget** (jede Aufgabe selbst aussuchen, höchstens 15 €) |
| 6 · Verkäufer sein | Thorsten ist der **Kunde**, das Kind verkauft: **Reicht das Geld vom Kunden?** (Ja/Nein; der Kunde gibt passend, etwas zu viel oder zu wenig) · **Rückgeld geben** (Kunde zahlt mit 5 € oder 10 €) · **Kunde gibt mehrere Stücke** (z. B. 5 € + 2 € für 6 €) · **Erst den Preis, dann Rückgeld** (Gesamtpreis aus 4 Schildern wählen, dann das Rückgeld legen). Preise sind beim Verkaufen immer sichtbar. |

Bäckerei: *Euro und Cent kennen* (unter 1 € mit 10/20 ct, mit 50 ct, über 1 €), *Zusammenrechnen* (2 Sachen bis 2 € … 5 Sachen bis 10 €), *Geschickt legen* (möglichst wenig Münzen, Betrag anders legen), *Mehrmals und Ergänzen* (zweimal dasselbe, **bis zum vollen Euro**, wie viel fehlt noch?), *Rückgeld und Budget* (von 1 €, 5 €, 10 €, Reicht das Geld?, knapp, Wunschzettel mit 5 €), *Verkäufer sein* (wie beim Kiosk, mit Cent; Kunde zahlt mit 1 €, 2 €, 5 € oder 10 €). Spielwarenladen: *Große Scheine kennen* (eine Spielsache bis 20 €, 50 €, 100 €), *Zusammenrechnen* (2 Spielsachen bis 30 € … 4 bis 200 €), *Geschickt legen* (möglichst wenig Scheine, 50 €/100 € anders legen), *Mehrmals und Ergänzen* (zweimal dasselbe, wie viel fehlt noch?), *Rückgeld und Budget* (von 50 €, 100 €, Reicht das Geld?, knapp, Wunschzettel mit 100 €), *Verkäufer sein* (Kunde zahlt mit 20 €, 50 € oder 100 €). In Stufen wie „nur 1-€-Münzen“ liegt nur dieses Geld in der Schublade. Jede Stufe hat eine feste Kennung (Link: `…&st=k-2-3`); der Stand von vor Version 4.7 wird übernommen, alte Links mit `stufe=1–8` gehen weiter.

**Wechsel werden erklärt:** Bei jeder neuen Stufe erscheint eine Karte, die Thorsten vorliest („Neu ab hier“, bei einem neuen Thema „Neues Thema: …“ mit Lob). Neue Aufgabenarten und neues Geld (z. B. erstes Rückgeld, „Reicht das Geld?“, 2-€-Münze, 1 € = 100 Cent) werden zusätzlich **vorgemacht** („Zeig es mir“: Sachen mit Preis, das Geld fällt Stück für Stück auf den Teller, dazu die Rechnung); danach folgt eine **Probeaufgabe**, die nicht zählt, mit sichtbaren Preisen. In den ersten 3 Aufgaben nach einem Wechsel steht oben „Neu: …“ (antippen = Erklärung noch einmal) und die Hilfe kommt schon nach dem 1. Fehlversuch. Geht es eine Stufe zurück, heißt es freundlich „Wir üben das noch ein bisschen“. Setzt die Lehrkraft eine Stufe, wird sie beim nächsten Start ebenso erklärt.

Nach einer einstellbaren Zahl gelöster Aufgaben (Standard 8; gezählt werden Aufgaben mit höchstens 2 Fotos und ohne Hilfe) erscheint die Karte **„Neu ab hier“** mit Lob, und die nächste Stufe beginnt. **Wenn eine Stufe nicht klappt** (Einstellung unter *Laden & Schwierigkeit*):
- *weitergehen, später wiederholen* (Standard): nach 12 Aufgaben ohne Aufstieg geht es zur nächsten Stufe („Das üben wir später noch einmal …“); die Stufe wird **gemerkt**.
- *eine Stufe zurück*: nach 3 schweren Aufgaben in Folge (frühere Einstellung „Eine Stufe zurück“ wird übernommen).
- *auf der Stufe bleiben*.

**Stand je Stufe:** In der Stufenliste und in der Auswertung steht bei jeder geübten Stufe *sicher* (grün: mind. 4 Aufgaben, davon 80 % ohne Hilfe oder die letzten 3 ohne Hilfe), *im Aufbau* (gelb), *noch schwierig* (orange: gemerkt oder unter 50 %) oder *ausgelassen* (grau). Gezählt werden die letzten 10 Aufgaben der Stufe. Mit **„auslassen“** neben jeder Stufe nimmt die Lehrkraft eine Stufe aus dem automatischen Ablauf (Aufstieg, Weitergehen und Zurück springen darüber); steht das Kind gerade darauf, geht es zur nächsten Stufe.

**Wiederholung in jeder Runde** (Schalter, Standard an): In jeder 4. Aufgabe kommt eine gemerkte Stufe dran, in jeder 5. eine sichere frühere Stufe – angekündigt mit „Weißt du noch? Das üben wir noch einmal.“ Diese Aufgaben zählen für den Stand ihrer Stufe, nicht für den Aufstieg. Klappt eine gemerkte Stufe wieder (sicher), wird sie nicht mehr gemerkt.

Statt Stufen lässt sich im Lehrkraft-Bereich unter *Laden & Schwierigkeit* (eingeklappt) eine **„Eigene Aufgabe statt Stufen“** einschalten (Aufgabe, Anzahl Sachen, gerade/ungerade, Höchstbetrag, Bezahlen mit, 1-€-Münzen); sie gilt im Laden, in dem gerade geübt wird. Ob am Ende der Gesamtbetrag aus 4 Möglichkeiten gewählt wird, stellt ein eigener Schalter ein – er gilt für jede Stufe und für die eigene Aufgabe.

## Lehrkraft-Bereich

**Öffnen:** Zahnrad oben rechts antippen. Es erscheint ein Code aus vier Zahlen, **als Wörter geschrieben** (z. B. „acht · drei · fünf · neun“), der mit dem Zahlenfeld eingetippt wird (also 8 3 5 9). Der Code ist jedes Mal neu; bei einer falschen Eingabe kommt sofort ein neuer. Kinder, die (noch) nicht lesen, können den Bereich so nicht öffnen.

**Übung abbrechen:** Oben im Lehrkraft-Bereich führt „Zur Ladenauswahl“ während einer Übung direkt zurück zum Startbildschirm (die angefangene Runde zählt nicht).

**Aufbau:** Links eine Seitenleiste mit neun Abschnitten (wie die iPad-Einstellungen), unter jedem eine Zeile mit dem aktuellen Stand (z. B. „Kind wählt · steigt nach 8“); rechts der Inhalt. Auf dem Handy erst die Liste, dann der Abschnitt mit „‹ Übersicht“. **Jede Änderung gilt sofort**; „Fertig“ schließt. Wurden Laden, Stufe oder Aufgabe geändert, zeigt ein Hinweis unten: Mit „Fertig“ beginnt eine neue Runde. Sonst läuft die angefangene Aufgabe weiter.

*Üben*
- **Kinder**: Mehrere Kinder können ein Gerät nutzen. Jedes Kind bekommt ein **Bild** (Igel, Rakete, Blume, Sonne, Fisch, Auto, Katze, Baum, Stern, Schiff, Apfel, Eule) – Namen werden nicht gespeichert. Beim Öffnen der App fragt sie „Wer übt heute?“, das Kind tippt auf sein Bild (auf der Ladenauswahl führt „Anderes Kind“ zurück). **Einstellungen, Stufen, Auswertung und Album gelten je Kind.** Im Lehrkraft-Bereich: Kind auswählen (die Einstellungen gelten dann für dieses Kind; oben steht, für welches), Bild ändern, Kind hinzufügen (beginnt mit den Einstellungen des gerade gewählten Kindes, aber bei Stufe 1) und löschen (mit Rückfrage). Mit nur einem Kind ändert sich nichts; der bisherige Lernstand gehört dem ersten Kind.
- **Laden & Schwierigkeit**: Kind wählt den Laden selbst oder immer derselbe Laden; Stufe je Laden (die 8 Stufen untereinander mit ihrem Namen, Erklärung des Anspruchs hinter dem „i“); *steigert sich* oder *bleibt*, nächste Stufe nach 5/8/10/15 Aufgaben, eine Stufe zurück nach 3 schweren Aufgaben; eingeklappt die *eigene Aufgabe statt Stufen*.
- **Aufgaben**: Aufgaben pro Runde, Wunschzettel, Gesamtbetrag aus 4 wählen (Link: `…&schild=1`), gleiche Sachen mehrmals – und wie sie erscheinen: *einzeln nebeneinander* (Standard) oder *zusammengefasst* mit „2×“, „3×“ auf der Karte, auf dem Einkaufszettel und an der Markierung im Laden (schwerer: das Kind muss den Preis mehrmals nehmen; Link: `…&mengen=zusammen`).
- **Hilfen**: Preise unter den Sachen, Hilfe nach Fehlversuchen, gelegtes Geld als Betrag, im Laden zeigen, was gekauft werden soll.
- **Geld & Kamera**: fotografieren oder auf dem Gerät ziehen (Link: `…?geld=ziehen`), Kamera in der App, Vorschaubilder im Protokoll.
- **Ton & Bedienung**: Name (optional, nur auf diesem Gerät), Töne und Vorlesen, Stimme, *Ansagen stumm*, **Bedienung mit einem Taster**: Eine blaue Markierung wandert von Knopf zu Knopf (1,5 / 2,5 / 4 Sekunden). Auswählen mit Leertaste/Enter (viele Taster für das iPad senden diese Tasten) oder durch Tippen irgendwo auf den Bildschirm. Alternativ hat das iPad selbst die „Schaltersteuerung“ (Einstellungen → Bedienungshilfen).

*Auswerten & Material*
- **Auswertung** für den Förderplan, je Laden umschaltbar, für 7 Tage, 30 Tage oder alles: Zusammenfassung („… davon 85 % ohne Hilfe gelöst. Sicher: bis 10 €. Noch schwierig: 16–20 €.“), **häufigster Fehler mit Förder-Tipp** und Tabelle der Fehlerarten (*eine Sache vergessen*, *eine Sache doppelt gezählt*, *Preis statt Rückgeld gelegt*, *bezahlten Betrag gelegt*, *Zehner/Stellenwert*, *knapp verzählt*, *anderer Fehler*); aufklappbar Tabellen nach Stufe, Betrag und Anzahl der Sachen. **Drucken** (alle Tabellen) oder **Als Tabelle speichern** (CSV, öffnet in Excel/Numbers). Darunter der **Lernstand aller Läden** (Stufe, Aufgaben, ohne Hilfe gelöst, zuletzt geübt; *Übersicht als Tabelle* je Stufe) und das **Foto-Protokoll** (Einträge zum Aufklappen, auf Wunsch mit Vorschaubild).
- **Material**: **Druckvorlagen** (DIN A4, zum Ausschneiden): *Preisschilder* aller Waren eines Ladens (Bild, Name, Preis) für den Klassen-Kaufladen und *Betrags-Schilder* (Bereich wählbar, z. B. 1–30 € oder 0,10–10,00 €) für „Gesamtbetrag aus 4 wählen“ am Tisch. Am iPad öffnet sich das Drucken-Fenster (auch „als PDF sichern“). Außerdem der **Link mit diesen Einstellungen** für TaskCards oder einen QR-Code, z. B.
  `…/kirmes-kiosk/?modus=stufen&stufe=4&aufstieg=8&runde=10`
  oder mit eigener Aufgabe: `…/kirmes-kiosk/?modus=fest&art=kaufen&anzahl=4&betrag=ungerade&max=15&einer=2&schild=1&runde=10`
  Der Name kommt absichtlich nicht in den Link.
- **Daten**: *Lernstand als Datei sichern* (JSON mit **allen Kindern**: Stufen, Einstellungen, Auswertung, Protokoll und Album) und *Datei laden* (z. B. auf einem anderen Gerät; ersetzt den Stand dort nach Rückfrage; ältere Dateien mit einem Kind ersetzen nur das gewählte Kind). **Erinnerung:** Wurde 14 Tage nicht gesichert (oder noch nie, ab 20 Aufgaben), steht oben im Lehrkraft-Bereich „Lernstand sichern“ mit „Jetzt sichern“, in der Seitenleiste „Sicherung fällig“. Die App bittet den Browser außerdem, ihren Speicher nicht zu löschen; am sichersten ist sie über „Zum Home-Bildschirm“ geöffnet – der Name und Vorschaubilder kommen nicht in die Dateien; Hinweise zum Datenschutz; **Löschen** (Protokoll und Auswertung oder alle Daten, jeweils mit Rückfrage); unten Versionsnummer, ob die App offline verfügbar ist und wie viele Ansagen offline gespeichert sind.

- **Wenn die Erkennung sich irrt**: unter dem Foto *Erkennung korrigieren* → Markierung antippen wechselt 1 € → 2 € → 5 € → 10 € → 20 € → entfernen; leere Stelle antippen fügt 1 € hinzu.

## Vorlesen

Standard ist die **Thorsten-Stimme** (Piper, Modell `de_DE-thorsten-high`, Sprachdaten von Thorsten Müller unter CC0). Lob („Super!“, „Richtig!“, „Geschafft!“, „Das klappt schon super!“) kommt aus der emotionalen Thorsten-Stimme (`de_DE-thorsten_emotional-medium`, Stimmung „amused“, ebenfalls CC0). Die Ansagen sind fertige Tondateien im Ordner `ton/` (ca. 4.400 Bausteine, alle gleich laut): Sätze mit Betrag komplett (z. B. „Das sind genau 3 Euro 40.“), Waren je nach Platz im Satz („Ich möchte eine Brezel, …“ / „…, eine Brezel, …“ / „… und eine Brezel kaufen.“), alle festen Sätze sowie Zahlen und Satzteile als Rückfall. Die App setzt jeden Text aus den längsten passenden Bausteinen zusammen – offline, ohne Server. Die App selbst ist nach dem ersten Öffnen sofort offline nutzbar. Die Ansagen (ca. 62 MB) lädt sie danach im Hintergrund in einen eigenen Offline-Speicher, solange sie geöffnet ist (einige Minuten im WLAN). Dieser Speicher bleibt bei neuen Versionen erhalten – nachgeladen wird nur, was neu ist; ein abgebrochenes Laden geht beim nächsten Öffnen weiter. Den Stand zeigt der Lehrkraft-Bereich unter *Daten* („Ansagen offline: alle“). Bis dahin liest die Gerätestimme Sätze, deren Ansagen noch fehlen und die nicht aus dem Netz geladen werden können. Jede Ansage hat vorn und hinten 0,15 s Stille, damit kein Gerät Wortenden abschneidet. **Stumm-Knopf** (durchgestrichener Lautsprecher oben, auf jeder Seite): Das Kind kann die Ansagen selbst aus- und wieder einschalten (orange = stumm); der Knopf „Vorlesen“ liest auch dann auf Wunsch vor, Jubel-Töne bleiben. Die Lehrkraft sieht und ändert das unter *Ton & Bedienung*. Nur der **Name des Kindes** wird mit der Stimme des Geräts gesprochen. Fehlt für einen Text ein Baustein, liest die Gerätestimme den ganzen Satz. Umschalten im Lehrkraft-Bereich unter *Ton & Bedienung* (Link: `…&stimme=geraet`).

**Ansagen neu erzeugen** (nach Änderungen an Vorlese-Texten, Waren oder Stufen): Piper installieren (`python3 -m venv venv && venv/bin/pip install piper-tts`), die Modelle `de_DE-thorsten-high.onnx` und `de_DE-thorsten_emotional-medium.onnx` (jeweils + `.json`) von huggingface.co/rhasspy/piper-voices laden, dann
`python3 werkzeuge/ansagen.py --piper venv/bin/python --modell de_DE-thorsten-high.onnx --lob-modell de_DE-thorsten_emotional-medium.onnx` (Stimmung fürs Lob ändern: `--lob-stimmung surprised`). Aussprache von Lehnwörtern (Burger, Muffin, Donut, Croissant, Erdbeertörtchen …) steht als Umschreibung oder Lautschrift in `AUSSPRACHE` am Anfang des Skripts (braucht macOS wegen `afconvert`). Danach VERSION erhöhen.

## Tipps für gute Fotos

- Weißes Blatt als Unterlage (die „Unterlage für Geld“ funktioniert gut)
- Münzen mit etwas Abstand; Scheine nebeneinander, nicht übereinander
- Kein Schatten, keine Spiegelung; möglichst von oben
- Kein Preisschild mit aufs Foto (das Schild wählt das Kind in der App)

## Design

Angelehnt an das Erscheinungsbild der Olympischen Spiele München 1972 (Otl Aicher): helle, heitere Farben – Hellblau, Blau, Hellgrün, Grün, Gelb, Orange, Silber, viel Weiß –, flache Flächen ohne Schatten, kleine Rundungen, bewusst ohne Rot und Schwarz (Schrift in Dunkelblau). Ruhig gehalten, damit wenig ablenkt.

**Farbleitsystem:** Jeder Laden hat eine Leitfarbe – Kirmes-Kiosk Orange, Bäckerei Gelb, Spielwarenladen Hellblau. Sie zieht sich durch die Startkarte, den Kopf (Band unten und Kante links), die Preisschilder, die Nummer des Arbeitsschritts und den Zahlteller. „Richtig“ ist immer Grün, „Schau noch mal“ Orange. Überschriften in einer schlichten Groteskschrift des Geräts (Helvetica Neue), Texte weiter in der Leseschrift Andika. Beim Start fährt ein Vorhang aus Farbstreifen auseinander.

## Bilder und Rechte

Alle Produktbilder (je 20 für Kirmes-Kiosk, Spielwarenladen und Bäckerei) und das App-Symbol wurden eigens für diese App neu gezeichnet (SVG-Vektorgrafiken im Ordner `bilder/`). Sie enthalten keine Bilder aus anderen Programmen oder Sammlungen (z. B. Worksheet Crafter), deren Lizenz eine Veröffentlichung in einer App oder auf einer Website nicht erlaubt. Die Schriften stehen unter der SIL Open Font License.

## Datenschutz

- **Fotos** werden nur im Browser ausgewertet, nicht hochgeladen und nicht gespeichert. Ausnahme: Ist „Vorschaubilder im Protokoll speichern“ eingeschaltet, bleibt ein kleines Vorschaubild im Browser-Speicher dieses Geräts (standardmäßig aus).
- **Name, Einstellungen, Stufe, Protokoll und Auswertung** liegen nur im Browser-Speicher dieses Geräts. Name nicht im Link, nicht im Protokoll, nicht in der Auswertung.
- **Keine fremden Server**: keine Google-Schriften, keine Statistik, keine Cookies, keine Werbung.
- **Vorlesen**: fertige Tondateien aus der App (Thorsten-Stimme) oder Stimmen, die auf dem Gerät installiert sind. Online-Stimmen werden bewusst nicht verwendet.
- **Löschen**: im Lehrkraft-Bereich unter *Daten* → „Alle Daten auf diesem Gerät“.

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
