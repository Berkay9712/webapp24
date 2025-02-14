---
title: Data Model
parent: Technical Docs
nav_order: 2
---

{: .label }
[Nurdan Turan]

{: .label }
[Berkay Olmaz]

{: .no_toc }
# Data model

**Nutzer-Modell**

`class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)  
    surveys = db.relationship('Survey', backref='creator', lazy=True)`

Das User-Modell speichert Informationen über registrierte Nutzer und ihre Umfragen.

- jeder Nutzer besitzt einen eindeutigen Benutzernamen und ein verschlüsseltes Passwort
- Nutzer können mehrere Umfragen erstellen, wodurch eine 1:N-Beziehung zwischen User und Survey entsteht (Verknüpfung erfolgt über die user_id in der Survey-Tabelle)
- falls keine Anmeldung erforderlich ist, kann eine Umfrage auch ohne Nutzer existieren


**Umfrage-Modell**

`class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  
    questions = db.relationship('Question', backref='survey', cascade="all, delete-orphan", lazy=True)
    responses = db.relationship('Response', backref='survey', cascade="all, delete-orphan", lazy=True)'`

Das Survey-Modell speichert eine Umfrage mit einem Titel und einer (optional) Verknüpfung zu einem Nutzer.

- jede Umfrage kann mehrere Fragen enthalten, wodurch eine 1:N-Beziehung zu Question entsteht
- Teilnehmer können Antworten auf eine Umfrage geben, die im Response-Modell gespeichert werden
Beziehung zu anderen Modellen:

**Frage-Modell**

`class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'), nullable=False)`

Das Question-Modell speichert die Fragen einer Umfrage.

- jede Frage gehört genau zu einer Umfrage, weshalb eine 1:N-Beziehung zu Survey besteht
- der Fragetext wird als Zeichenkette gespeichert

**Antwort-Modell**

`class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'), nullable=False)
    answers = db.Column(db.Text, nullable=False)  # JSON-String mit Antworten`

Das Response-Modell speichert die Antworten der Nutzer auf eine Umfrage.

- jede Antwort ist einer Umfrage zugeordnet
- eine Umfrage kann viele Antworten erhalten, weshalb eine 1:N-Beziehung zu Survey besteht

**alle Modellbeziehungen**

User zu Survey (1:N)
Survey zu Question (1:N)
Survey zu Response (1:N)
Question zu Survey (N:1)
Response zu Survey (N:1)


