# Meal Tracker

Persönlicher Meal-Prep-Tracker als statische Single-Page-Webseite. Kein Backend, kein Build-Step – reines HTML/CSS/JS in einer `index.html`.

## Zweck

Günstiger, high-protein Meal-Prep-Plan (Magerquark, Skyr, Whey, Reis, Hähnchen, Eier, Kichererbsen etc.) mit täglicher Abhak-Funktion, mehreren Mahlzeit-Varianten pro Slot, Makro-Tracking (Kcal/Protein/Carbs/Fett), einem Vorrats-System (Pantry) und einer automatisch generierten Einkaufsliste.

## Tech-Stack

- Reines HTML/CSS/JS, eine einzige Datei (`index.html`)
- Kein Framework, kein Build-Tool, keine Dependencies
- Persistenz über `localStorage` im Browser (client-seitig, kein Server, kein Account)
- Gehostet über **GitHub Pages**

## Wichtig: Repo-Trennung wegen Privacy Policy

Mein Haupt-GitHub-Account hostet unter `<username>.github.io` bereits die **Privacy Policy für eine TikTok-API-Anbindung** (separates Content-Automation-Projekt). Der Meal Tracker läuft deshalb bewusst in einem **eigenen, separaten Repo** (z.B. `meal-tracker`), NICHT im `<username>.github.io`-Hauptrepo, damit sich beide Pages-Deployments nicht überschneiden oder gegenseitig beeinflussen.

- Haupt-Repo `<username>.github.io` → Privacy Policy (TikTok API) – nicht anfassen
- Separates Repo `meal-tracker` → dieser Tracker, läuft unter `<username>.github.io/meal-tracker`

Falls hier mit Claude Code weitergearbeitet wird: **niemals Dateien im Haupt-`.github.io`-Repo verändern**, alles bleibt im `meal-tracker`-Repo isoliert.

## Datenmodell (in `index.html`, im `<script>`-Teil)

- `POOLS` – Objekt mit drei Kategorien (`breakfast`, `snack`, `main`), jede enthält mehrere Mahlzeit-Optionen mit `id`, `title`, `short`, `kcal`, `protein`, `carbs`, `fat`, `ingredients[]` (inkl. `pantryKey` zur Verknüpfung mit dem Vorrat) und `steps[]` (Zubereitung).
- `SLOTS` – 5 feste Tages-Slots (Frühstück, Snack, Mittag, Snack, Abend), jeder verweist auf einen Pool.
- `DEFAULT_PANTRY` – Standard-Vorratsliste mit `key`, `name`, `unit`, `qty`, `low` (Schwellenwert für "wird knapp").

## State / Storage-Keys (localStorage)

- `mealtracker_day2_<Jahr>-<Monat>-<Tag>` – Tagesstatus (gewählte Option + abgehakt pro Slot), wird täglich neu erzeugt, alte Tage werden automatisch aufgeräumt (`cleanupOldDayKeys`)
- `mealtracker_pantry` – dauerhafter Vorrat (übersteht Tageswechsel)
- `mealtracker_shop_manual` – manuell hinzugefügte Einkaufslisten-Einträge
- `mealtracker_shop_checked` – abgehakte Einkaufslisten-Einträge
- `mealtracker_expanded` / `mealtracker_switchopen` – UI-State (welche Rezepte/Auswahl-Panels offen sind)

## Aktueller Funktionsumfang

- 3 Tabs: **Heute** (Tracker + Makros), **Vorrat** (Pantry mit +/- Steppern), **Liste** (auto-generierte + manuelle Einkaufsliste)
- Pro Mahlzeit: mehrere austauschbare Varianten ("Andere Option"), volle Rezepte mit Zutaten & Zubereitungsschritten
- Live-Makro-Balken (Kcal/Protein/Carbs/Fett): "gegessen" vs. "Tagesplan"
- Vorrat mit "wird knapp"-Markierung, die automatisch in die Einkaufsliste wandert
- Täglicher Reset um Mitternacht (Tagesauswahl + Abhak-Status), Vorrat & Liste bleiben bestehen

## Bekannte Einschränkungen

- Daten sind rein lokal im Browser (`localStorage`) – kein Sync zwischen Geräten, kein Backup
- Keine Nutzerkonten/Auth
- Keine Kalorien-/Makro-**Ziele** einstellbar, nur der Ist-Wert aus der Tagesauswahl als Referenz

## Offene Aufgaben für Claude Code (nächster Ausbauschritt)

Der Rest wird lokal mit Claude Code weitergebaut. Hier die vollständigen Anforderungen:

### 1. Automatisiertes Macro-Tracking für individuelle/extra gegessene Sachen

Aktuell zeigt der "Heute"-Tab nur "gegessen vs. Tagesplan" basierend auf den abgehakten Standard-Slots. Zusätzlich soll man:

- Frei beliebige, nicht im Plan enthaltene Lebensmittel/Mahlzeiten als "Extra" für den aktuellen Tag hinzufügen können (z.B. spontane Snacks, Restaurantbesuch, Abweichung vom Plan)
- Diese Extras sollen automatisch in die Tagesmakros (Kcal/Protein/Carbs/Fett) mit einfließen, die oben im Macro-Panel angezeigt werden
- **Automatisierte Makro-Ermittlung, falls möglich**: beim Eintippen eines Lebensmittelnamens automatisch Nährwerte nachschlagen, nicht nur manuell eintragen. Empfehlung: [Open Food Facts API](https://world.openfoodfacts.org/data) nutzen — kostenlos, kein API-Key nötig, unterstützt CORS, funktioniert clientseitig direkt aus dem Browser (Suche z.B. über `https://world.openfoodfacts.org/cgi/search.pl?search_terms=<query>&search_simple=1&action=process&json=1&page_size=5`, liefert Nährwerte pro 100g zurück). Nutzer gibt dann nur noch die verzehrte Menge in Gramm ein, Rest wird automatisch skaliert und berechnet.
- Manuelle Eingabe (Name + Kcal/Protein/Carbs/Fett direkt) muss als Fallback erhalten bleiben, falls die API nichts findet oder nicht erreichbar ist (Netzwerkfehler abfangen)
- Extras sollen wie die Standard-Mahlzeiten in einer Liste im "Heute"-Tab erscheinen, mit Lösch-Möglichkeit
- Extras zählen NICHT in den "Tagesplan"-Zielwert rein (der bleibt die Summe der 5 geplanten Slots), sondern erhöhen nur den "gegessen"-Ist-Wert — die Balken dürfen dabei über 100% des Ziels gehen (visuell z.B. bei 100% deckeln, aber den echten Zahlenwert weiter anzeigen)
- Persistenz: Extras gehören zum Tagesstate (`mealtracker_day2_<datum>`), setzen sich also wie der Rest automatisch um Mitternacht zurück

### 2. Trainingsplan (Push/Pull/Legs) mit Tracking

Neuer Tab/Bereich für einen PPL-Trainingsplan, analog zum Hevy-Plan der bereits existiert (siehe Kontext: Nutzer hat bereits einen PPL-Plan für die Hevy-App gebaut — als Ausgangsbasis nutzen bzw. beim Nutzer nachfragen, welche genauen Übungen/Sätze/Wiederholungsbereiche übernommen werden sollen).

Anforderungen:

- 3 Trainingstage: Push, Pull, Legs, jeweils mit fester Übungsliste (Übungsname, Ziel-Sätze, Ziel-Wiederholungsbereich)
- Pro Übung UI zum Eintragen der tatsächlich absolvierten Sätze: **Kilogramm** und **Wiederholungen** pro Satz
- Tracking-Historie: welches Gewicht/welche Wiederholungen wurden an welchem Datum pro Übung geschafft — mindestens die letzte Session pro Übung anzeigen (z.B. "letztes Mal: 40kg x 8"), im Idealfall eine kleine Verlaufsansicht/Progression pro Übung
- Persistenz analog zum restlichen Projekt über `localStorage`, eigene Storage-Keys (z.B. `fitnesstracker_workout_<datum>`, `fitnesstracker_history`)
- Design/UI-Stil an das bestehende dunkle Card-Design des Meal Trackers anlehnen (gleiche Farbpalette/Komponenten wiederverwenden), damit es sich wie eine App anfühlt

### 3. Passwortschutz für die Seite

Die Seite (Meal Tracker + neuer Trainingsplan) soll nicht öffentlich einsehbar sein, da es sich um private Gesundheits-/Trainingsdaten handelt.

- Da GitHub Pages selbst (auch mit privatem Repo) keine echte Zugriffskontrolle bietet (siehe Hinweis oben zu Free/Pro-Plan-Limitierungen), reicht ein reiner client-seitiger Passwortschutz NICHT für echte Sicherheit aus (Quellcode ist im Browser einsehbar) — für dieses private, nicht-kritische Anwendung (Ernährungs-/Trainingsdaten, kein Login mit echten Konsequenzen) ist das aber ein akzeptabler Kompromiss, sofern das dem Nutzer bewusst ist
- Einfachste Umsetzung: eine simple Passwort-Eingabemaske vor dem Zugriff auf den Inhalt, die z.B. einen gehashten Wert (nicht das Klartext-Passwort im Code) mit der Eingabe vergleicht, und den Zugriff dann per `sessionStorage`/`localStorage`-Flag freischaltet
- Empfehlung, falls echte Sicherheit gewünscht ist: stattdessen auf Netlify oder Vercel umziehen (beide kostenlos, beide bieten echten Passwortschutz/Basic-Auth ohne Umweg über clientseitigen JS-Check) — das dem Nutzer als Option nennen/anbieten

### 4. Rebranding: Umzug zu `77toast.github.io/fitness`

- Das Projekt soll künftig unter dem GitHub-Account/Repo-Namen `77toast` laufen, konkret unter `77toast.github.io/fitness` erreichbar sein
- Das heißt: neues bzw. umbenanntes Repo `fitness` unter dem Account `77toast`, `index.html` (und alle weiteren Dateien) dort hinein
- Bestehender Hinweis zur Repo-Trennung wegen der Privacy Policy (siehe oben) bleibt unverändert gültig — die Privacy Policy liegt weiterhin im `<username>.github.io`-Hauptrepo, der Fitness-/Meal-Tracker läuft komplett separat unter `77toast.github.io/fitness`
- Titel/Branding auf der Seite selbst (aktuell "Meal Tracker") entsprechend anpassen, sobald der neue Trainingsplan-Bereich dazukommt (z.B. neuer Oberbegriff wie "77toast Fitness" o.ä. — Nutzer nach gewünschtem Namen fragen, falls nicht klar)

## Bereits vorhandene, mögliche weitere Ausbauideen (niedrigere Priorität)

- Wochenübersicht/Historie (letzte 7 Tage, z.B. Streak oder Durchschnittswerte) für den Meal Tracker
- Eigene Tagesziele für Kcal/Makros einstellbar machen, Balken relativ dazu färben
- Export der Einkaufsliste (z.B. als Text zum Teilen/Copy)

## Deployment

Einfache statische Seite, kein Build nötig:

1. Neues, separates GitHub-Repo anlegen (z.B. `meal-tracker`) – **nicht** das `.github.io`-Hauptrepo
2. `index.html` ins Repo-Root hochladen
3. Settings → Pages → Branch `main` → Save
4. Live unter `<username>.github.io/meal-tracker`

Bei Änderungen: `index.html` einfach im Repo überschreiben/committen, Pages baut automatisch neu.
