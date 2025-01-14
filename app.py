from flask import Flask, render_template, request, redirect, url_for
from models import db, Survey, Question, Response

app = Flask(__name__)

# SQL Datenbank
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///surveys.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Datenbank mit Flask-App
db.init_app(app)

with app.app_context():
    db.create_all()
@app.route('/')
def index():
    surveys = Survey.query.all()
    return render_template('index.html', surveys=surveys)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        questions = request.form.getlist('questions[]')

        # Titel darf nicht leer 
        if not title:
            return "Bitte geben Sie einen Titel an", 400
        
        # mindestens eine Frage erforderlich
        valid_questions = [q.strip() for q in questions if q.strip()]
        if not valid_questions:
            return "Bitte stellen Sie eine Frage", 400

        # Umfrage und Fragen erstellen
        try:
            new_survey = Survey(title=title)
            db.session.add(new_survey)
            db.session.flush()  # damit `new_survey.id` verfügbar ist

            for question_text in valid_questions:
                new_question = Question(text=question_text, survey_id=new_survey.id)
                db.session.add(new_question)

            db.session.commit()
            return redirect('/')
        except Exception as e:
            db.session.rollback()
            return f"An error occurred: {e}", 500 # zur Fehlererkennung

    return render_template('create.html')


@app.route('/survey/<int:survey_id>', methods=['GET', 'POST'])
def take_survey(survey_id):
    survey = Survey.query.get_or_404(survey_id)
    if request.method == 'POST':
        for question in survey.questions:
            answer = request.form.get(f'question_{question.id}')
            if answer:
                new_response = Response(question_id=question.id, answer=answer)
                db.session.add(new_response)
        db.session.commit()
        return redirect(url_for('results', survey_id=survey_id))
    return render_template('survey.html', survey=survey)

@app.route('/results/<int:survey_id>')
def results(survey_id):
    survey = Survey.query.get_or_404(survey_id)
    return render_template('results.html', survey=survey)

if __name__ == '__main__':
    app.run(debug=True)
