from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# Nutzer-Modell
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)  
    surveys = db.relationship('Survey', backref='creator', lazy=True)

# Umfrage-Modell
class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  
    questions = db.relationship('Question', backref='survey', cascade="all, delete-orphan", lazy=True)
    responses = db.relationship('Response', backref='survey', cascade="all, delete-orphan", lazy=True)

# Frage-Modell
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'), nullable=False)

# Antwort-Modell 
class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'), nullable=False)
    answers = db.Column(db.Text, nullable=False)  # JSON-String mit Antworten

