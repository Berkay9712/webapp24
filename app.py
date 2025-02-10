from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///surveys.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    questions = db.relationship('Question', backref='survey', lazy=True)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'), nullable=False)

class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    answer = db.Column(db.String, nullable=False)
    question = db.relationship('Question', backref=db.backref('responses', lazy=True))

# Datenbanktabellen erstellen (innerhalb eines Anwendungskontexts)
with app.app_context():
    db.create_all()

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        questions_text = request.form.getlist('questions[]')

        new_survey = Survey(title=title)
        db.session.add(new_survey)
        db.session.commit()

        for question_text in questions_text:
            question = Question(text=question_text, survey_id=new_survey.id)
            db.session.add(question)
        
        db.session.commit()

        survey_link = url_for('survey', survey_id=new_survey.id, _external=True)
        return render_template('created.html', survey_link=survey_link)

    return render_template('create.html')

@app.route('/survey/<int:survey_id>', methods=['GET', 'POST'])
def survey(survey_id):
    survey = Survey.query.get_or_404(survey_id)

    if request.method == 'POST':
        responses = request.form.getlist('responses[]')
        questions = survey.questions

        for i, question in enumerate(questions):
            response = Response(question_id=question.id, answer=responses[i])
            db.session.add(response)

        db.session.commit()
        return redirect(url_for('results', survey_id=survey.id))

    return render_template('survey.html', survey=survey)

@app.route('/results/<int:survey_id>')
def results(survey_id):
    survey = Survey.query.get_or_404(survey_id)
    return render_template('results.html', survey=survey)

if __name__ == '__main__':
    app.run(debug=True)

