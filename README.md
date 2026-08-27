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

## Scope

Der Fitness Tracker lebt vollständig im Repo `77toast/fitness` und ist unter `77toast.github.io/fitness` erreichbar. Alles zu diesem Projekt gehört ausschließlich hierher — **niemals Dateien im `<username>.github.io`-Hauptrepo oder in einem anderen Repo des Accounts anfassen.**

## Datenmodell (in `index.html`, im `<script>`-Teil)

- `POOLS` – Objekt mit drei Kategorien (`breakfast`, `snack`, `main`), jede enthält mehrere Mahlzeit-Optionen mit `id`, `title`, `short`, `kcal`, `protein`, `carbs`, `fat`, `ingredients[]` (inkl. `pantryKey` zur Verknüpfung mit dem Vorrat) und `steps[]` (Zubereitung).
- `SLOTS` – 5 feste Tages-Slots (Frühstück, Snack, Mittag, Snack, Abend), jeder verweist auf einen Pool.
- Der Vorrat hat **keine** Standardliste – er startet leer und wird ausschließlich manuell befüllt. Einträge haben `key`, `name`, `unit`, `qty`, `low` (Schwellenwert für "wird knapp", bei manuell angelegten Einträgen `0`).
- `pantryKeyFor(name, existing)` leitet den `key` aus dem eingegebenen Namen ab (kleingeschrieben, Umlaute transliteriert, Sonderzeichen raus): "Hähnchen" → `haehnchen`. Genau diese Slugs stehen als `pantryKey` an den Zutaten in `POOLS`, dadurch greift die "vorhanden"/"wenig da"-Anzeige in den Rezepten, sobald du die Zutat unter ihrem normalen Namen anlegst. Zutaten ohne passenden Vorratseintrag zeigen einfach kein Label.
- `WORKOUTS` – drei Trainingstage (`push`, `pull`, `legs`), je mit `exercises[]` aus `id`, `name`, `sets` (Ziel-Sätze), `reps` (Ziel-Wiederholungsbereich), `mg` (Muskelgruppe, Basis für die Wochenvolumen-Auswertung) und `alts[]` (alternative Übungen für denselben Slot, je mit eigener `id` und `name`).

## State / Storage-Keys (localStorage)

| Key | Inhalt | Reset |
| --- | --- | --- |
| `mealtracker_day2_<Jahr>-<Monat>-<Tag>` | Tagesstatus: gewählte Option + abgehakt pro Slot, plus `extras[]` | täglich (`cleanupOldDayKeys`) |
| `fitnesstracker_workout_<YYYY-MM-DD>` | welcher Trainingstag heute gewählt ist | täglich (`cleanupOldDayKeys`) |
| `fitnesstracker_history` | `{ übungsId: [ { date, sets: [{kg, reps, rpe?}] } ] }` – gesamte Trainingshistorie, `rpe` optional | nie |
| `mealtracker_pantry_v2` | dauerhafter Vorrat (startet leer) | nie |
| `mealtracker_shop_manual` | manuell hinzugefügte Einkaufslisten-Einträge als `{id, name}` | nie |
| `mealtracker_shop_checked` | abgehakte Einkaufslisten-Einträge | nie |
| `mealtracker_expanded` / `mealtracker_switchopen` | UI-State (offene Rezepte/Auswahl-Panels) | nie |
| `fitnesstracker_unlocked` | Passwort-Flag (gesetzter Hash), schaltet die Seite ohne erneute Eingabe frei | bei Passwortwechsel / "Seite sperren" |
| `fitnesstracker_goals` | eigene Tagesziele für Kcal/P/C/F und Wasser | nie |
| `fitnesstracker_weight` | `[{ date, kg }]` – Gewichtsverlauf | nie |
| `fitnesstracker_extra_recent` | die letzten 10 Extras für die Schnellauswahl-Chips | nie |
| `fitnesstracker_daylog` | `{ "YYYY-MM-DD": { kcal, protein, meals } }` – Tageszusammenfassungen für die Wochenübersicht, auf 60 Tage begrenzt | rollierend |
| `fitnesstracker_measurements` | `[{ date, waist?, chest?, hips?, arm?, thigh? }]` – Körpermaße | nie |
| `fitnesstracker_best_streak` | längster je erreichter Streak (Zahl), Basis für die Streak-Badges | nie |
| `fitnesstracker_bar_weight` | zuletzt genutztes Stangengewicht im Platten-/Warm-up-Rechner | nie |
| `fitnesstracker_ex_choice` | `{ slotId: variantenId }` – gewählte Übungs-Variante pro Slot, Standard-Übung wird nicht gespeichert | nie |
| `fitnesstracker_calc_inputs` | zuletzt genutzte Eingaben des TDEE-Rechners (ohne Gewicht, das kommt vom Gewichts-Tracking) | nie |

Die Trainings**historie** liegt bewusst nicht im Tages-Key – sie überlebt den täglichen Reset, nur die Auswahl des Trainingstags nicht.

## Aktueller Funktionsumfang

**Heute**
- Pro Mahlzeit: mehrere austauschbare Varianten ("Andere Option"), volle Rezepte mit Zutaten & Zubereitungsschritten
- Neben den Meal-Prep-Gerichten auch schnelle Toast-Optionen ohne Kochen: 2 Eier auf Vollkorntoast, Erdnussbutter-Marmeladen-Toast, Vollkorntoast mit Putenbrust, Erdnussbutter-Banane-Toast, Thunfisch-Sandwich
- Schnelle Hauptgerichte ohne großen Aufwand: Pasta mit Thunfisch-Quark-Sauce, Airfryer-Hähnchen mit Reis (Fertigbeutel, kein Topf), Mikro-Kartoffel mit Quark-Thunfisch-Dip
- Baked Oats als Frühstück: gemahlene Haferflocken + Banane + Ei + Whey + Backpulver, 20-25 Min bei 180°C — Porridge-Zutaten, Kuchen-Ergebnis (540 kcal, 43g Protein)
- Live-Makro-Balken (Kcal/Protein/Carbs/Fett): "gegessen" vs. "Tagesplan" bzw. gegen die eigenen Ziele, darunter der Rest ("Noch 735 kcal · 52g Protein")
- **Extras**: beliebige, nicht geplante Lebensmittel für den Tag hinzufügen
  - Tab "Suchen": Name eintippen → Open Food Facts liefert Treffer mit Nährwerten pro 100g → Menge in Gramm eingeben → Makros werden automatisch skaliert
  - Tab "Manuell": Name + Kcal/P/C/F direkt eintragen (Fallback, wenn die API nichts findet oder offline ist – Netzwerkfehler werden abgefangen und gemeldet)
  - Extras erhöhen nur den "gegessen"-Wert, nicht den Tagesplan-Zielwert; die Balken deckeln visuell bei 100 %, der Zahlenwert läuft weiter (z.B. `2150 / 1770`)
  - Schnellauswahl-Chips ("Zuletzt gegessen") für die letzten 10 Extras – ein Tap statt erneut suchen
  - Barcode-Scan: Button erscheint nur, wenn der Browser `BarcodeDetector` kann (Chrome auf Android), sonst bleibt es bei Suche und manueller Eingabe
- Wasser-Zähler in Gläsern à 250ml, ebenfalls Teil des Tagesstates

**Training**
- Drei Tage: Push, Pull, Legs mit je 6 Übungen (Ziel-Sätze und Ziel-Wiederholungsbereich)
- **Trainingstag wird vorgeschlagen**: aus der Historie wird der zuletzt absolvierte Tag ermittelt und der nächste der Rotation Push → Pull → Legs vorgewählt, mit Hinweis "Zuletzt Push am 12.08. — Pull ist dran". Tippst du selbst auf einen Tag, gilt deine Wahl für heute
- **Alternativen pro Übung** ("Andere Übung", analog zu "Andere Option" bei den Mahlzeiten): z.B. Bankdrücken ↔ Kurzhantel ↔ Brustpresse, Klimmzug ↔ Latzug. Jede Variante hat eine eigene ID, die Historie bleibt also getrennt — die Wochenvolumen-Auswertung zählt aber alle Varianten eines Slots auf dieselbe Muskelgruppe. Die Wahl gilt dauerhaft (`fitnesstracker_ex_choice`), nicht nur für heute
- Pro Übung Sätze mit **kg × Wiederholungen** eintragen, einzeln löschbar; Eingabefelder sind mit dem letzten Satz vorbelegt
- **RPE pro Satz** (optional, 5-10 in 0,5er-Schritten): wird mitgespeichert, in Satzliste und Verlauf als "@RPE 8" angezeigt (Feature aus Strong/Hevy)
- "Letztes Mal (06.08.): 57.5kg × 8, 57.5kg × 6" pro Übung, plus aufklappbarer Verlauf der letzten 6 Sessions
- Fortschrittsbalken über absolvierte vs. geplante Sätze des Tages
- Satzpausen-Timer (90s / 2min / 3min), startet automatisch beim Eintragen eines Satzes, mit Signalton am Ende
- Bestleistung pro Übung, "PR"-Marke wenn der heutige Top-Satz die bisherige Bestleistung schlägt
- Progressionsvorschlag aus der letzten Session: oberes Ende des Wiederholungsbereichs erreicht → +2,5kg, sonst eine Wiederholung mehr
- Im Verlauf pro Übung: Graph über das geschätzte 1RM (Epley: `kg × (1 + reps/30)`) plus aktueller Schätzwert und Differenz zur Vorsession. Damit sind Sessions vergleichbar, in denen sich Gewicht *und* Wiederholungen unterscheiden
- Sätze pro Muskelgruppe der letzten 7 Tage als Balken (`mg`-Feld an jeder Übung)
- **Platten- & Warm-up-Rechner** pro Übung: Zielgewicht + Stangengewicht → Scheiben pro Seite (Greedy-Algorithmus über 25/20/15/10/5/2.5/1.25kg) plus eine Warm-up-Ramp (40/60/80/90 % des Zielgewichts mit Wiederholungsvorschlag). Stangengewicht wird gemerkt (`fitnesstracker_bar_weight`) — Idee von den kostenlosen Tools der Stronger-App

**Vorrat / Liste**
- Vorrat startet leer und wird manuell befüllt – es wird nichts vorgegeben, was du gar nicht hast
- +/- Stepper pro Eintrag; steht ein Eintrag auf 0, gilt er als "knapp" und wandert automatisch in die Einkaufsliste
- Einkaufsliste aus Auto-Einträgen + manuellen Einträgen, mit Badge für offene Posten und Kopieren als Text
- Alte Installationen hatten eine vorbefüllte Standard-Vorratsliste unter `mealtracker_pantry`. Der Key wurde auf `mealtracker_pantry_v2` gezogen und der alte beim Start gelöscht – der Vorrat ist also einmalig leer, egal was vorher drinstand.

**Mehr**
- Wochenübersicht der letzten 7 Tage: Training (💪), abgehakte Mahlzeiten, Streak, Ø Kcal und Ø Protein
- **Aktivitäts-Heatmap** (12 Wochen): Contribution-Graph im GitHub-Stil, Zellfarbe zeigt Mahlzeiten geloggt / trainiert / beides an einem Tag
- **Auszeichnungen**: Badges für Streak-Meilensteine (3/7/14/30/100 Tage, gegen den bisher längsten Streak in `fitnesstracker_best_streak`) und Trainings-Meilensteine (10/25/50/100 Einheiten)
- Gewicht eintragen mit 7-Tage-Schnitt, Trend gegen die Vorwoche und Sparkline über die letzten 30 Einträge
- **Körpermaße**: Taille/Brust/Hüfte/Oberarm/Oberschenkel eintragen, zeigt jeweils den letzten Wert und den Trend zum Eintrag von vor ca. 3 Wochen (`fitnesstracker_measurements`)
- Eigene Tagesziele für Kcal/P/C/F und Wasser – sind welche gesetzt, vergleichen die Balken im Heute-Tab dagegen statt gegen den Tagesplan
- **TDEE-Rechner** (Mifflin-St-Jeor) direkt bei den Tageszielen: Alter/Größe/Gewicht/Aktivitätslevel/Ziel (Abnehmen/Halten/Aufbauen) → befüllt die Kcal-/Protein-/Carbs-/Fett-Zielfelder, Eingaben werden gemerkt (`fitnesstracker_calc_inputs`)
- Backup: Export als JSON-Datei, Import stellt alles wieder her (der Passwort-Flag wird bewusst nicht mitgesichert). Das Datum des letzten Exports steht in `fitnesstracker_last_export` und wird im Panel angezeigt – ab 30 Tagen als Alter statt als Datum
- "Seite sperren" verwirft die Freigabe, danach fragt die Seite wieder nach dem Passwort

**Als App installieren**
- `manifest.json` + `sw.js` machen die Seite zur PWA: über "Zum Startbildschirm hinzufügen" bekommst du ein App-Icon, Vollbild ohne Browserleiste und Offline-Betrieb
- Der Service Worker läuft **network-first** – ein neuer Push kommt sofort an, der Cache springt nur ein, wenn kein Netz da ist. Anfragen an Open Food Facts werden nie gecacht.
- Icons (`icon-192.png`, `icon-512.png`) werden von `tools/make_icons.py` erzeugt

**Reset**
- Täglich um Mitternacht: Tagesauswahl, Abhak-Status, Extras, Wasser und gewählter Trainingstag. Vorrat, Liste, Trainingshistorie, Gewicht, Ziele und Wochenlog bleiben bestehen.

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

- Daten sind rein lokal im Browser (`localStorage`) – kein Sync zwischen Geräten. Ein Backup gibt es nur manuell über Export/Import im "Mehr"-Tab, nichts passiert automatisch
- Keine Nutzerkonten/Auth (siehe Passwort-Abschnitt oben)
- Übungen im Trainingsplan sind fest im Code (`WORKOUTS`), nicht über die UI editierbar
- Open Food Facts ist eine Community-Datenbank: Nährwerte einzelner Produkte können fehlen oder ungenau sein

## Mögliche weitere Ausbauideen

- Übungen über die UI hinzufügen/umbenennen/löschen (aktuell fest in `WORKOUTS`)
- Eigene Rezepte über die UI anlegen statt in `POOLS`
- Trainingsplan-Varianten (Upper/Lower, Ganzkörper) neben PPL
- Supersätze/Drop-Sets als eigene Satz-Typen (JEFIT-Feature)
- Fortschrittsfotos (wie bei JEFIT) — technisch machbar über `localStorage`/IndexedDB, aber Speicherplatz im Browser ist begrenzt
- Sparklines pro Körpermaß statt nur Zahl + Trend

## Deployment

Einfache statische Seite, kein Build nötig:

1. Repo `fitness` unter dem Account `77toast` anlegen
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
