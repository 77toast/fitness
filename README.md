# Fitness Tracker

Persönlicher Meal-Prep- und Trainings-Tracker als statische Single-Page-Webseite. Kein Backend, kein Build-Step – reines HTML/CSS/JS in einer `index.html`.

## Zweck

Günstiger, high-protein Meal-Prep-Plan (Magerquark, Skyr, Whey, Reis, Hähnchen, Eier, Kichererbsen etc.) mit täglicher Abhak-Funktion, mehreren Mahlzeit-Varianten pro Slot, Makro-Tracking (Kcal/Protein/Carbs/Fett), frei hinzufügbaren Extras mit automatischer Nährwert-Suche, einem Vorrats-System (Pantry), einer automatisch generierten Einkaufsliste und einem Push/Pull/Legs-Trainingsplan mit Satz-Tracking und Verlauf.

## Tech-Stack

- Reines HTML/CSS/JS, eine einzige Datei (`index.html`)
- Kein Framework, kein Build-Tool, keine Dependencies
- Nährwert-Suche über die [Open Food Facts API](https://world.openfoodfacts.org/data) (kostenlos, kein API-Key, CORS erlaubt, läuft clientseitig)
- Persistenz über `localStorage` im Browser (client-seitig, kein Server, kein Account)
- Gehostet über **GitHub Pages** unter `77toast.github.io/fitness`

## Wichtig: Repo-Trennung wegen Privacy Policy

Der Haupt-GitHub-Account hostet unter `<username>.github.io` bereits die **Privacy Policy für eine TikTok-API-Anbindung** (separates Content-Automation-Projekt). Der Fitness Tracker läuft deshalb bewusst in einem **eigenen, separaten Repo** (`fitness` unter dem Account `77toast`), NICHT im `<username>.github.io`-Hauptrepo, damit sich beide Pages-Deployments nicht überschneiden oder gegenseitig beeinflussen.

- Haupt-Repo `<username>.github.io` → Privacy Policy (TikTok API) – nicht anfassen
- Separates Repo `77toast/fitness` → dieser Tracker, läuft unter `77toast.github.io/fitness`

**Niemals Dateien im Haupt-`.github.io`-Repo verändern**, alles bleibt im `fitness`-Repo isoliert.

## Datenmodell (in `index.html`, im `<script>`-Teil)

- `POOLS` – Objekt mit drei Kategorien (`breakfast`, `snack`, `main`), jede enthält mehrere Mahlzeit-Optionen mit `id`, `title`, `short`, `kcal`, `protein`, `carbs`, `fat`, `ingredients[]` (inkl. `pantryKey` zur Verknüpfung mit dem Vorrat) und `steps[]` (Zubereitung).
- `SLOTS` – 5 feste Tages-Slots (Frühstück, Snack, Mittag, Snack, Abend), jeder verweist auf einen Pool.
- `DEFAULT_PANTRY` – Standard-Vorratsliste mit `key`, `name`, `unit`, `qty`, `low` (Schwellenwert für "wird knapp").
- `WORKOUTS` – drei Trainingstage (`push`, `pull`, `legs`), je mit `exercises[]` aus `id`, `name`, `sets` (Ziel-Sätze) und `reps` (Ziel-Wiederholungsbereich).

## State / Storage-Keys (localStorage)

| Key | Inhalt | Reset |
| --- | --- | --- |
| `mealtracker_day2_<Jahr>-<Monat>-<Tag>` | Tagesstatus: gewählte Option + abgehakt pro Slot, plus `extras[]` | täglich (`cleanupOldDayKeys`) |
| `fitnesstracker_workout_<YYYY-MM-DD>` | welcher Trainingstag heute gewählt ist | täglich (`cleanupOldDayKeys`) |
| `fitnesstracker_history` | `{ übungsId: [ { date, sets: [{kg, reps}] } ] }` – gesamte Trainingshistorie | nie |
| `mealtracker_pantry` | dauerhafter Vorrat | nie |
| `mealtracker_shop_manual` | manuell hinzugefügte Einkaufslisten-Einträge | nie |
| `mealtracker_shop_checked` | abgehakte Einkaufslisten-Einträge | nie |
| `mealtracker_expanded` / `mealtracker_switchopen` | UI-State (offene Rezepte/Auswahl-Panels) | nie |
| `fitnesstracker_unlocked` | Passwort-Flag (gesetzter Hash), schaltet die Seite ohne erneute Eingabe frei | bei Passwortwechsel |

Die Trainings**historie** liegt bewusst nicht im Tages-Key – sie überlebt den täglichen Reset, nur die Auswahl des Trainingstags nicht.

## Aktueller Funktionsumfang

**Heute**
- Pro Mahlzeit: mehrere austauschbare Varianten ("Andere Option"), volle Rezepte mit Zutaten & Zubereitungsschritten
- Live-Makro-Balken (Kcal/Protein/Carbs/Fett): "gegessen" vs. "Tagesplan"
- **Extras**: beliebige, nicht geplante Lebensmittel für den Tag hinzufügen
  - Tab "Suchen": Name eintippen → Open Food Facts liefert Treffer mit Nährwerten pro 100g → Menge in Gramm eingeben → Makros werden automatisch skaliert
  - Tab "Manuell": Name + Kcal/P/C/F direkt eintragen (Fallback, wenn die API nichts findet oder offline ist – Netzwerkfehler werden abgefangen und gemeldet)
  - Extras erhöhen nur den "gegessen"-Wert, nicht den Tagesplan-Zielwert; die Balken deckeln visuell bei 100 %, der Zahlenwert läuft weiter (z.B. `2150 / 1770`)

**Training**
- Drei Tage: Push, Pull, Legs mit je 6 Übungen (Ziel-Sätze und Ziel-Wiederholungsbereich)
- Pro Übung Sätze mit **kg × Wiederholungen** eintragen, einzeln löschbar
- "Letztes Mal (06.08.): 57.5kg × 8, 57.5kg × 6" pro Übung, plus aufklappbarer Verlauf der letzten 6 Sessions
- Eingabefelder sind mit dem letzten Satz vorbelegt
- Fortschrittsbalken über absolvierte vs. geplante Sätze des Tages

**Vorrat / Liste**
- Vorrat mit +/- Steppern und "wird knapp"-Markierung, die automatisch in die Einkaufsliste wandert
- Einkaufsliste aus Auto-Einträgen + manuellen Einträgen, mit Badge für offene Posten

**Reset**
- Täglich um Mitternacht: Tagesauswahl, Abhak-Status, Extras und gewählter Trainingstag. Vorrat, Liste und Trainingshistorie bleiben bestehen.

## Passwort einrichten

Die Seite startet gesperrt. Der Schutz ist rein clientseitig: `index.html` enthält den **SHA-256-Hash** des Passworts, nicht das Klartext-Passwort.

1. Seite öffnen – solange `PASSWORD_HASH` leer ist, zeigt die Startmaske einen Generator
2. Wunschpasswort eintippen → "Hash erzeugen" → angezeigten Hex-String kopieren
3. In `index.html` oben im `<script>`-Teil einsetzen: `const PASSWORD_HASH = "<hash>";`
4. Committen und pushen

Danach fragt die Seite beim ersten Aufruf pro Gerät nach dem Passwort und merkt sich die Freigabe in `localStorage`. Solange kein Hash gesetzt ist, gibt es zusätzlich den Link "Ohne Passwort öffnen".

**Das ist kein echter Zugriffsschutz.** GitHub Pages liefert die Datei an jeden aus, der die URL kennt; wer den Quelltext liest, sieht die Struktur der Seite, und die Daten liegen ohnehin nur lokal im Browser. Es hält neugierige Blicke ab, mehr nicht.

Wenn echter Schutz gewünscht ist: statt GitHub Pages auf **Netlify** oder **Vercel** deployen (beide kostenlos, beide bieten serverseitigen Passwortschutz/Basic Auth, Deploy direkt aus dem GitHub-Repo). Dann ist die URL allerdings nicht mehr `77toast.github.io/fitness`.

## Bekannte Einschränkungen

- Daten sind rein lokal im Browser (`localStorage`) – kein Sync zwischen Geräten, kein Backup
- Keine Nutzerkonten/Auth (siehe Passwort-Abschnitt oben)
- Keine Kalorien-/Makro-**Ziele** einstellbar, nur der Ist-Wert aus der Tagesauswahl als Referenz
- Übungen im Trainingsplan sind fest im Code (`WORKOUTS`), nicht über die UI editierbar
- Open Food Facts ist eine Community-Datenbank: Nährwerte einzelner Produkte können fehlen oder ungenau sein

## Mögliche weitere Ausbauideen

- Wochenübersicht/Historie (letzte 7 Tage, z.B. Streak oder Durchschnittswerte) für den Meal Tracker
- Eigene Tagesziele für Kcal/Makros einstellbar machen, Balken relativ dazu färben
- Export der Einkaufsliste (z.B. als Text zum Teilen/Copy)
- Übungen über die UI hinzufügen/umbenennen/löschen
- Progressions-Graph statt Textliste im Übungsverlauf
- Barcode-Scan für Extras (Open Food Facts unterstützt Lookup per EAN)

## Deployment

Einfache statische Seite, kein Build nötig:

1. Repo `fitness` unter dem Account `77toast` anlegen – **nicht** das `.github.io`-Hauptrepo
2. `index.html` ins Repo-Root pushen
3. Settings → Pages → Branch `main` → Save
4. Live unter `77toast.github.io/fitness`

Bei Änderungen: `index.html` committen und pushen, Pages baut automatisch neu.

### Lokal testen

`localStorage` und die Passwortprüfung (`crypto.subtle`) brauchen einen echten Origin – per Doppelklick über `file://` geöffnet funktioniert die Seite nicht. Stattdessen:

```bash
python -m http.server 8777 --directory .
```

Dann `http://localhost:8777` im Browser öffnen.
