---
title: Design Decisions
nav_order: 3
---

{: .label }
[Nurdan Turan]

{: .label }
[Berkay Olmaz]

{: .no_toc }
# Design decisions

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## 01: routes & app.py trennen

### Meta

Status
: Work in progress - **Decided** - Obsolete

Updated
: 14-02-2025

### Problem statement

Das Problem alle Routen in einer py zu speichern und von der app.py zu trennen.

### Decision

Da die Aufwendigkeit mit blueprints zu arbeiten zu hoch war und die App eine, noch, übersichtliche Anzahl an Routen hatte, wurde die Entscheidung getroffen, diese nicht zu trennen.

### Regarded options

Da die routes mit einem Präfix versehen werden müssen, wenn diese in einer gesonderten py gespeichert werden, war es nahe die routen einheitlich in die app.py zu setzen.

---
## 02: einfache Loginverwaltung

### Meta

Status
: Work in progress - **Decided** - Obsolete

Updated
: 12-02-2025

### Problem statement

Nutzer, die auf ihre Umfragen zugreifen wollen, benötigen die Möglichkeit einer Anmeldung.

### Decision

Flask-Login nutzen, da die Anwendung bereits auf Flask basiert.

### Regarded options

Sie bietet eine einfache Integration und automatisiert im selben Zug die Nutzung.

---
## 03: Aufbau der Datenbank

### Meta

Status
: Work in progress - **Decided** - Obsolete

Updated
: 14-02-2025

### Problem statement

Umfragen sollten mit mehreren Fragen gespeichert werden können und für die Ersteller zugänglich sein.

### Decision

SQL Alchemy mit relationaler Datenbank.

### Regarded options

Durch die Nutzung von SQL Alchemy konnten wir den Aufbau und die Strukturierung innerhalb des Codes gut planen.

---
## 04: erweiterte UI

### Meta

Status
: Work in progress - Decided - **Obsolete**

Updated
: 14-02-2025

### Problem statement

Ersteller der Umfragen sollten die Möglichkeit haben, ihre Fragen mit Hinweisen beschriften zu können (Beispiel: kleines i an einem Rand der Frage, für Informationsgebung)

### Decision

Da wir die simple Gestaltung und zeitsparende value propostion einhalten möchten, haben die Nutzer die Möglichkeit nähere Infos zu den Fragen bereits in der Frage mitzugeben. 

### Regarded options

+schöneres Design
-Nutzung fragwürdig, da Vorteil der App das Zeit sparen ist

---
## 05: Umsetzung Umfrage ohne Anmeldung

### Meta

Status
: Work in progress - **Decided** - Obsolete

Updated
: 12-02-2025

### Problem statement

Umfragen, die ohne Login erstellt werden, müssen in der gleichen Datenbank gespeichert werden.

### Decision

Das Feld für die ID in der Datenbank kann leer bleiben.

### Regarded options

+keine separate Benutzerverwaltung nötig
+Zuordnung bleibt erhalten
+es wird kein Platzhalter verwendet

---
## UI Komponenten der Webanwendung


### Layout

`body {
    font-family: Arial, sans-serif;
    background-color: #f5f5f5;
    text-align: center;
    margin: 0;
    padding: 0;
}`

- Schriftart: Arial, sans-serif
- background-color: #f5f5f5; - Helle Hintergrundfarbe
- text-align: center; - zentriert den Text.

---

### Header

`.header-bar {
    background-color: #007BFF;
    color: white;
    text-align: center;
    padding: 15px 0;
    font-size: 24px;
    font-weight: bold;
}`

- background-color: #007BFF; - blaue Farbe für die Kopfzeile (inspiriert vo Social Media Plattformen)
- font-size: 24px; font-weight: bold; - große und fette Schrift

---

### Container

`.container {
    max-width: 600px;
    background: white;
    padding: 20px;
    margin: 30px auto;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}`

- border-radius: 10px; - abgerundete Ecken
- box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); - Schatten für schwebende Optik

### Eingabefelder

`.form-container {
    text-align: center;
    margin: 20px 0;
}
label {
    display: block;
    margin: 10px 0 5px;
    font-weight: bold;
}
.input-field {
    width: 100%;
    padding: 12px;
    margin-top: 5px;
    border: 1px solid #ccc;
    border-radius: 8px;
    font-size: 16px;
    box-sizing: border-box;
}`

- border-radius: 8px; erneut abgerundete Felder
- font-size: 16px; - Schriftgröße

---

### Flash-Meldungen

`.flash-messages {
    margin: 20px auto;
    padding: 10px;
    width: 50%;
    text-align: center;
}
.flash-success {
    background-color: #28a745;
    color: white;
    padding: 10px;
    border-radius: 5px;
}
.flash-danger {
    background-color: #dc3545;
    color: white;
    padding: 10px;
    border-radius: 5px;
}`

- background-color: #28a745; - grüne Erfolgsmeöldung
- background-color: #dc3545; - rote Fehlermeldung

---

### Buttons

`.button {
    background-color: #007BFF;
    color: white;
    border: none;
    padding: 12px 24px;
    font-size: 16px;
    border-radius: 25px;
    cursor: pointer;
    display: inline-block;
    margin: 10px;
    transition: background-color 0.3s;
    text-decoration: none;
}
.button:hover {
    background-color: #0056b3;
}`

- border-radius: 25px; - runde Buttons
- transition: background-color 0.3s; - Hover-Effekt

---

### Frage & Antwortfelder

`.question-box {
    background-color: #f9f9f9;
    padding: 15px;
    margin-bottom: 15px;
    border-radius: 8px;
    border: 1px solid #ddd;
}
.question-text {
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 10px;
}`

- border-radius: 8px; - aberundete Felder
- background-color: #f9f9f9; - heller Hintergrund

### Umfragen / Ergebnisse

`.survey-list, .results-list {
    list-style: none;
    padding: 0;
}
.survey-list li, .results-list li {
    background: white;
    padding: 15px;
    margin: 10px 0;
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}`

- box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); - schwebende Optik
- border-radius: 8px; - Abrundung 
  
---

### Logout & Löschen

`.logout-btn {
    background-color: #dc3545;
}
.logout-btn:hover {
    background-color: #a71d2a;
}
.remove-btn {
    background-color: #dc3545;
    color: white;
    border: none;
    padding: 8px 15px;
    font-size: 14px;
    border-radius: 5px;
    cursor: pointer;
    margin-top: 5px;
}
.remove-btn:hover {
    background-color: #a71d2a;
}`

- background-color: #dc3545; - rote Buttons für kritische Aktionen
- hover: background-color: #a71d2a; - wird dunkler beim Hovern
