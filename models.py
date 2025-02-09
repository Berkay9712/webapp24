from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    questions = db.relationship('Question', backref='survey', lazy=True)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)  # text darf nicht NULL sein
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'), nullable=False)

class Response(db.Model):
    __tablename__ = 'response'
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)  # Frage ID
    answer = db.Column(db.String, nullable=False)

    question = db.relationship('Question', backref=db.backref('responses', lazy=True))




