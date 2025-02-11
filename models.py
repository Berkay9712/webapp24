from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

#  Nutzer-Modell für das Login-System
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), unique=True, nullable=False)  # Email-Feld hinzugefügt
    password = db.Column(db.String(150), nullable=False)
    
    # Beziehung: Ein Nutzer kann mehrere Umfragen erstellen
    surveys = db.relationship('Survey', backref='creator', lazy=True)

# Umfrage-Modell mit Verbindung zum Nutzer
class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Erstellungsdatum
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Optional für Gast-Umfragen

    # Beziehung zu den Fragen der Umfrage
    questions = db.relationship('Question', backref='survey', cascade="all, delete-orphan", lazy=True)

# Fragen-Modell mit Verbindung zur Umfrage
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'), nullable=False)

    # Beziehung zu den Antworten auf die Frage
    answers = db.relationship('Answer', backref='question', cascade="all, delete-orphan", lazy=True)

# Antwort-Modell für die Antworten der Nutzer
class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)




