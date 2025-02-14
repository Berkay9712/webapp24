---
title: Reference
parent: Technical Docs
nav_order: 3
---

{: .label }
[Nurdan Turan]

{: .label }
[Berkay Olmaz]

{: .no_toc }
# Reference documentation


## Authorisierung


### `home()`

**Route:** `/`

**Methods:** `POST` `GET`

**Purpose:** Zeigt die Startseite an und verarbeitet die Anmeldung eines Nutzers. Wenn die Anmeldedaten korrekt sind, wird der Nutzer zum Dashboard weitergeleitet. Andernfalls wird eine Fehlermeldung angezeigt.

**Output:**
- Erfolgreiche Anmeldung - "Erfolgreich eingeloggt!" und Weiterleitung zum Dashboard
- Fehlgeschlagene Anmeldung - "Falscher Nutzername oder Passwort!"
---


### `register()`

**Route:** `/register/`

**Methods:** `POST` `GET`

**Purpose:** Registriert einen neuen Nutzer. Falls der Benutzername bereits existiert, wird eine Fehlermeldung angezeigt. Bei erfolgreicher Registrierung wird der Nutzer automatisch eingeloggt.

**Output:**
- Erfolgreiche Registrierung - "Registrierung erfolgreich!"
- Benutzername existiert bereits - "Nutzername bereits vergeben!"
---


### `logout()`

**Route:** `/logout/`

**Methods:** `GET`

**Purpose:** Meldet den Nutzer ab und leitet ihn zur Startseite weiter.

**Output:**
- Erfolgreiches Logout - "Erfolgreich ausgeloggt!"

---

## Dashboard & Surveys


### `dashboard()`

**Route:** `/dashboard/`

**Methods:** `GET`

**Purpose:** Zeigt das Dashboard des Nutzers mit einer Übersicht aller erstellten Umfragen.

**Output:**
- Liste eigener Umfragen mit Links zur Verwaltung
---


### `create()`

**Route:** `/create/`

**Methods:** `GET`, `POST`

**Purpose:** Die Erstellung einer neuen Umfrage mit einem Titel und mindestens einer Frage. Falls kein Nutzer angemeldet ist, wird die Umfrage anonym gespeichert.

**Output:**
- Erfolgreiche Umfrage-Erstellung - "Umfrage erfolgreich erstellt!" mit generiertem Link
- Fehler - "Titel und mindestens eine Frage erforderlich!"
---


### `created()`

**Route:** `/created/`

**Methods:** `GET`

**Purpose:** Zeigt eine Bestätigungsseite nach der Umfrageerstellung und gibt den Umfragelink aus.

**Output:**
- Umfragelink: http://127.0.0.1:5000/survey/123
---


### `delete_survey(survey_id)`

**Route:** `/delete_survey/<int:survey_id>/`

**Methods:** `POST`, `DELETE`

**Purpose:** Löscht eine Umfrage, falls der aktuelle Nutzer der Ersteller ist. Andernfalls wird eine Fehlermeldung ausgegeben.

**Output:**
- Erfolgreiche Löschung - "Umfrage erfolgreich gelöscht!"
---


### `show_survey(survey_id)`

**Route:** `/survey/<int:survey_id>/`

**Methods:** `POST`, `GET`

**Purpose:** Zeigt die Umfrage mit ihren Fragen an und ermöglicht es Teilnehmern, Antworten einzureichen. Die Antworten werden als JSON gespeichert.

**Output:**
- Erfolgreiche Teilnahme - Weiterleitung zur Bestätigungsseite mit "Antwort gespeichert!"
---


### `submitted(survey_id, response_id)`

**Route:** `/submitted/<int:survey_id>/<int:response_id>/`

**Methods:** `GET`

**Purpose:** Zeigt die Bestätigungsseite nach der Teilnahme an einer Umfrage mit den eingereichten Antworten.

**Output:**
- Liste der Fragen und Antworten des Nutzers

---

## Survey Results & Data Export


### `results(survey_id)`

**Route:** `/results/<int:survey_id>/`

**Methods:** `GET`

**Purpose:** Zeigt die gesammelten Antworten einer Umfrage an, aufgeteilt nach Fragen.

**Output:**
- Tabelle mit allen Antworten zu einer Umfrage
---


### `download_csv(survey_id)`

**Route:** `/download_csv/<int:survey_id>/`

**Methods:** `GET`

**Purpose:** Download der Umfrageergebnisse als CSV-Datei.

**Output:**
ID;  Frage 1;  Frage 2;  Frage 3
1;  Antwort 1;  Antwort 2;  Antwort 3
2;  Antwort A;  Antwort B;  Antwort C




  

