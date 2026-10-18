# Kirmes-Kiosk

Eine Lern-App für den Mathe-Unterricht (Förderschwerpunkt GG): Das Kind sieht 1–5 Sachen vom Kirmes-Kiosk, rechnet die Preise zusammen, legt das passende Spielgeld auf ein weißes Blatt und fotografiert es. Die App erkennt die Münzen und Scheine auf dem Foto und sagt, ob der Betrag stimmt. Schreiben ist nicht nötig.

Alles läuft im Browser: kein Server, kein Konto, keine KI-Dienste. Die Fotos verlassen das Gerät nicht.

## Dateien

| Datei | Inhalt |
|---|---|
| `index.html` | Die App (Oberfläche, Aufgaben, Einstellungen, Protokoll) |
| `erkennung.js` | Die Geld-Erkennung |
| `bilder/` | Produktbilder |
| `schriften/` | Schriften Andika und Grandstander (SIL Open Font License), lokal eingebunden |

## Auf GitHub Pages veröffentlichen

1. Auf github.com ein neues Repository anlegen, z. B. `kirmes-kiosk` (öffentlich).
2. **Add file → Upload files**: `index.html`, `erkennung.js`, `README.md` und die Ordner `bilder` und `schriften` hineinziehen, dann **Commit changes**.
3. **Settings → Pages**: unter *Branch* `main` und `/ (root)` wählen, **Save**.
4. Nach etwa einer Minute ist die App erreichbar unter
   `https://DEIN-NAME.github.io/kirmes-kiosk/`

Die Kamera funktioniert nur über `https://` (bei GitHub Pages automatisch).

## Bedienung

- **Foto vom Geld**: öffnet auf Tablet/Handy direkt die Kamera.
- **Lautsprecher-Knopf**: liest die Aufgabe vor.
- **Preisschild-Knopf**: zeigt die Preisliste mit allen 20 Sachen.
- **Name** (optional, im Lehrkraft-Bereich): erscheint in Begrüßung und Lob, z. B. „Super, [Name]!“.
- **Zahnrad gedrückt halten** (gut 1 Sekunde): öffnet den Lehrkraft-Bereich. Kurz antippen reicht absichtlich nicht.

### Lehrkraft-Bereich

- Anzahl der Sachen (1–5), nur gerade / nur ungerade Beträge, Höchstbetrag, Aufgaben pro Runde
- **1-€-Münzen begrenzen** (Bündeln üben: „Ab jetzt hast du nur noch zwei 1-€-Stücke.“)
- **Preis-Schild wählen** als 2. Schritt: 4 Schilder zur Auswahl oder alle bis zum Höchstbetrag
- Hilfen: Preise anzeigen, gleiche Sachen mehrmals, Hinweis „zu viel / zu wenig“, Vorlesen und Töne
- **Link mit diesen Einstellungen**: für TaskCards oder einen QR-Code. Beispiel:
  `…/kirmes-kiosk/?anzahl=4&betrag=ungerade&max=15&runde=10&einer=2&schild=4`
  Der Name kommt absichtlich nicht in den Link. Er wird auf jedem Gerät einmal im Lehrkraft-Bereich eingetragen.
- **Protokoll**: jedes Foto mit Preis, erkanntem Betrag und Ergebnis, auf Wunsch mit Vorschaubild. Ohne Namen, nur auf diesem Gerät.

### Wenn die Erkennung sich irrt

Unter dem Foto auf **Erkennung korrigieren** tippen. Dann:
- Markierung antippen: Wert wechselt 1 € → 2 € → 5 € → 10 € → 20 € → entfernen
- leere Stelle antippen: fügt dort 1 € hinzu

Die App prüft danach sofort neu. Im Protokoll steht dann „von Hand korrigiert“.

## Tipps für gute Fotos

- Weißes Blatt als Unterlage (die „Unterlage für Geld“ funktioniert gut)
- Münzen nicht übereinander, mit etwas Abstand; Scheine nicht auf Münzen legen
- Möglichst von oben fotografieren, Blatt füllt das Bild
- Kein Preisschild mit aufs Foto (das Schild wählt das Kind in der App)

## Datenschutz

Die App ist so gebaut, dass keine personenbezogenen Daten das Gerät verlassen:

- **Fotos** werden nur im Browser ausgewertet. Sie werden nicht hochgeladen und nicht gespeichert. Ausnahme: Ist „Vorschaubilder im Protokoll speichern“ eingeschaltet, bleibt ein kleines Vorschaubild im Browser-Speicher dieses Geräts. Diese Einstellung ist standardmäßig aus.
- **Name**: optional, steht nur im Browser-Speicher dieses Geräts, nicht im Link und nicht im Protokoll. Am besten nur den Vornamen oder einen Spitznamen verwenden.
- **Keine fremden Server**: keine Google-Schriften, keine Statistik, keine Cookies, keine Werbung. Alles kommt aus dem eigenen Repository.
- **Vorlesen** nutzt nur Stimmen, die auf dem Gerät installiert sind. Online-Stimmen werden bewusst nicht verwendet, weil sie den Text an einen Server schicken. Gibt es auf dem Gerät keine deutsche Stimme, bleibt die App still.
- **Löschen**: Im Lehrkraft-Bereich löscht „Alle Daten auf diesem Gerät löschen“ Name, Einstellungen und Protokoll.

Zu beachten: GitHub Pages ist der Webhoster. Beim Aufruf der Seite verarbeitet GitHub wie jeder Webserver technisch die IP-Adresse (siehe Datenschutzerklärung von GitHub). Bei Bedarf kann der Ordner genauso auf den Schulserver oder in die Schul-Cloud gelegt werden. Die App braucht nur einen Webserver mit https.

Bitte keine Fotos auf GitHub hochladen, auf denen Kinder zu erkennen sind. Für die App selbst werden keine Fotos benötigt.

## Wie die Erkennung arbeitet

0. **Weißabgleich über das Papier**: Die App schätzt an jeder Stelle die Farbe des Blatts und rechnet sie auf neutrales Weiß um. Das gleicht Farbstich (Glühbirne, Neonröhre, Fensterlicht) und Schatten aus.
1. Alles, was sich vom hellen Papier abhebt, wird als Fläche ausgeschnitten.
2. Ovale Flächen sind Münzen. **1 €**: Ring golden, Mitte silbern. **2 €**: Mitte golden, Ring silbern. Einfarbig goldene Münzen sind Cent-Münzen und zählen 0 €.
3. Sich berührende Münzen werden an der engsten Stelle getrennt.
4. Große rechteckige, bedruckte Flächen sind Scheine, die Farbe entscheidet: 5 € grau-grün, 10 € rot, 20 € blau, 50 € orange.

5. Farben werden als Median gemessen; Glanzlichter und tiefe Schatten zählen nicht mit. Verdeckt ein Glanzfleck die Mitte, entscheidet der Ring allein.
6. **Unsichere Stellen** (verschmolzene Münzen, starker Glanz, scheinbar „ganz goldene“ Münzen) werden gestrichelt mit **?** markiert. Passt der Betrag dann nicht, sagt die App nicht „falsch“, sondern bittet um ein neues Foto.

Getestet mit 15 Fotos von Spielgeld auf der Unterlage, jeweils in 9 Lichtvarianten (Original, warmes, kaltes und grünliches Licht, dunkel mit Bildrauschen, Schattenverlauf, harte Schattenkante, Spiegelungen auf allen Münzen, alles zusammen). Von 135 Fällen: 119 richtig erkannt, 12-mal um ein neues Foto gebeten, 4-mal ein falsches Urteil (fast nur in der Extremvariante „alles zusammen“ oder wenn ein Preisschild mit im Bild lag). 1 € und 2 € wurden in keinem Fall vertauscht. 10-€- und 20-€-Scheine waren auf den Testfotos nicht dabei; ihre Erkennung ist deshalb noch nicht an echtem Spielgeld geprüft.
