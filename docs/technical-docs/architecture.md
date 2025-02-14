---
title: Architecture
parent: Technical Docs
nav_order: 1
---

{: .label }
[Nuran Turan]

{: .label }
[Berkay Olmaz]

{: .no_toc }
# Architecture
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }


## Overview

Circumspectis ist eine benutzerfreundliche Plattform zur Erstellung, Verwaltung und Analyse von Umfragen. Sie ermöglicht es Nutzern, schnell und unkompliziert Umfragen zu erstellen – mit oder ohne Anmeldung. Die Teilnehmer können ihre Antworten über einen generierten Link abgeben und dem Ersteller werden di Ergebnisse übersichtlich dargestellt. 
Ein besonderes Feature ist der Export der Ergebnisse als CSV-Datei, welches die Analyse der Umfrage erleichtern soll. Die App basiert auf Flask und verwendet SQLAlchemy für die Datenbankverwaltung. Die Benutzerverwaltung erfolgt über Flask-Login, und enthält Passwort-Hashing als eine Sicherheitsfunktion. Die App ist übersichtlich aufgebaut, sodass Mitentwickler leicht neue Features hinzufügen oder bestehende Funktionen erweitern können.

## Codemap

Unsere App basiert auf dem Flask-Framework und ist unterteilt in:

**Datenbank (models.py):**
Die App verwendet SQLAlchemy zur Verwaltung der Datenbank. Es gibt vier zentrale Modelle:

- User (für registrierte Nutzer mit Login)
- Survey (für Umfragen)
- Question (Fragen einer Umfrage)
- Response (gespeicherte Antworten)
  
Die App verwendet SQLite als Datenbank

**Routen und Views (app.py):**

- Authentifizierung: Registrierung, Login und Logout über Flask-Login
- Dashboard: Übersicht der eigenen Umfragen
- Umfrage-Erstellung: Nutzer können Umfragen mit mehreren Fragen erstellen
- Umfrage-Teilnahme: Teilnehmer können ohne Anmeldung antworten
- Ergebnisanzeige: Ergebnisse werden aggregiert und visualisiert
- CSV-Export: Antworten können als CSV-Datei heruntergeladen werden

**Templates (style.css mit Jinja2)** 

- Benutzerfreundliche, einfache Oberfläche zur Interaktion mit den Umfragen
- Dynamische Templates für Formulare, Dashboards und Ergebnisanzeigen


## Cross-cutting concerns

**1. Datenbank & Modelle (models.py)**

User: Speichert Nutzerdaten (z. B. Username, Passwort).
Survey: Enthält die Umfrage-Metadaten (Titel, Ersteller).
Question: Fragen, die einer Umfrage zugeordnet sind.
Response: Antworten der Teilnehmer, gespeichert als JSON.

Die Beziehungen zwischen den Modellen werden über Fremdschlüssel verwaltet.

SQLote Datenbank: `(sqlite:///circumsdata.db)`

**2. Routing & Views (app.py)**

Startseite `(/)` - Login & Registrierung
Dashboard `(/dashboard)` - Übersicht der eigenen Umfragen
Umfrage erstellen `(/create)` - Titel & Fragen eingeben
Umfrage anzeigen `(/survey/<int:survey_id>)` - Teilnahme an Umfragen
Ergebnisse anzeigen `(/results/<int:survey_id>)` - Antworten auswerten
Umfrage löschen `(/delete_survey/<int:survey_id>)`
CSV-Download `(/download_csv/<int:survey_id>)` - Ergebnisse als CSV speichern

