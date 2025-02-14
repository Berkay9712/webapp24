---
title: Design Decisions
nav_order: 3
---

{: .label }
[Jane Dane]

{: .no_toc }
# Design decisions

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## 01: [Title]

### Meta

Status
: **Work in progress** - Decided - Obsolete

Updated
: DD-MMM-YYYY

### Problem statement

[Describe the problem to be solved or the goal to be achieved. Include relevant context information.]

### Decision

[Describe **which** design decision was taken for **what reason** and by **whom**.]

### Regarded options

[Describe any possible design decision that will solve the problem. Assess these options, e.g., via a simple pro/con list.]

---

## [Example, delete this section] 01: How to access the database - SQL or SQLAlchemy 

### Meta

Status
: Work in progress - **Decided** - Obsolete

Updated
: 30-Jun-2024

### Problem statement

Should we perform database CRUD (create, read, update, delete) operations by writing plain SQL or by using SQLAlchemy as object-relational mapper?

Our web application is written in Python with Flask and connects to an SQLite database. To complete the current project, this setup is sufficient.

We intend to scale up the application later on, since we see substantial business value in it.



Therefore, we will likely:
Therefore, we will likely:
Therefore, we will likely:

+ Change the database schema multiple times along the way, and
+ Switch to a more capable database system at some point.

### Decision

We stick with plain SQL.

Our team still has to come to grips with various technologies new to us, like Python and CSS. Adding another element to our stack will slow us down at the moment.

Also, it is likely we will completely re-write the app after MVP validation. This will create the opportunity to revise tech choices in roughly 4-6 months from now.
*Decision was taken by:* github.com/joe, github.com/jane, github.com/maxi

### Regarded options

We regarded two alternative options:

+ Plain SQL
+ SQLAlchemy

| Criterion | Plain SQL | SQLAlchemy |
| --- | --- | --- |
| **Know-how** | ✔️ We know how to write SQL | ❌ We must learn ORM concept & SQLAlchemy |
| **Change DB schema** | ❌ SQL scattered across code | ❔ Good: classes, bad: need Alembic on top |
| **Switch DB engine** | ❌ Different SQL dialect | ✔️ Abstracts away DB engine |

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
