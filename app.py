from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import json
import csv
import io

from models import db, User, Survey, Question, Response  # db von models importieren

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///circumsdata.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mein_geheimer_schlüssel'

# Datenbank mit App verknüpfen
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# alle routen

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and check_password_hash(user.password, request.form.get('password')):
            login_user(user)
            flash('Erfolgreich eingeloggt!', 'success')
            return redirect(url_for('dashboard'))
        flash('Falscher Nutzername oder Passwort!', 'danger')
    return render_template('index.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if User.query.filter_by(username=username).first():
            flash('Nutzername bereits vergeben!', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        flash('Registrierung erfolgreich!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('register.html')

@app.route("/dashboard")
@login_required
def dashboard():
    surveys = Survey.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html", user=current_user, surveys=surveys)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Erfolgreich ausgeloggt!', 'info')
    return redirect(url_for("home"))

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == 'POST':
        title = request.form['title']
        questions_list = request.form.getlist('questions[]')

        if not title or not questions_list:
            flash("Titel und mindestens eine Frage erforderlich!", "danger")
            return redirect(url_for('create'))

        user_id = current_user.id if current_user.is_authenticated else None
        new_survey = Survey(title=title, user_id=user_id)
        db.session.add(new_survey)
        db.session.commit()

        for question_text in questions_list:
            new_question = Question(text=question_text, survey_id=new_survey.id)
            db.session.add(new_question)

        db.session.commit()
        flash('Umfrage erfolgreich erstellt!', 'success')
        return redirect(url_for('created', survey_id=new_survey.id))

    return render_template('create.html')

@app.route("/created/<int:survey_id>")
def created(survey_id):
    survey = Survey.query.get_or_404(survey_id)
    survey_link = f"{request.url_root}survey/{survey_id}"
    return render_template('created.html', survey=survey, survey_link=survey_link)

@app.route("/delete_survey/<int:survey_id>", methods=['POST', 'DELETE'])
@login_required
def delete_survey(survey_id):
    survey = Survey.query.get_or_404(survey_id)
    if survey.user_id != current_user.id:
        flash("Du kannst nur deine eigenen Umfragen löschen!", "danger")
    else:
        db.session.delete(survey)
        db.session.commit()
        flash("Umfrage erfolgreich gelöscht!", "success")
    return redirect(url_for('dashboard'))

@app.route("/survey/<int:survey_id>", methods=['GET', 'POST'])
def show_survey(survey_id):
    survey = Survey.query.get_or_404(survey_id)
    
    if request.method == 'POST':
        answers_json = json.dumps(request.form.getlist('answers[]'))
        new_response = Response(survey_id=survey.id, answers=answers_json)
        db.session.add(new_response)
        db.session.commit()
        return redirect(url_for('submitted', survey_id=survey.id, response_id=new_response.id))

    questions = [q.text for q in survey.questions]
    return render_template('survey.html', survey=survey, questions=questions)

@app.route('/submitted/<int:survey_id>/<int:response_id>')
def submitted(survey_id, response_id):
    response = Response.query.get_or_404(response_id)
    survey = Survey.query.get_or_404(survey_id)

    questions = [q.text for q in survey.questions]
    answers = json.loads(response.answers) if response.answers else []

    combined = list(zip(questions, answers))
    return render_template('submitted.html', survey_id=survey_id, combined=combined)

@app.route('/results/<int:survey_id>')
def results(survey_id):
    survey = Survey.query.get_or_404(survey_id)
    responses = Response.query.filter_by(survey_id=survey.id).all()

    questions = [q.text for q in survey.questions]
    all_answers = [json.loads(response.answers) for response in responses]

    return render_template('results.html', survey=survey, questions=questions, all_answers=all_answers)

@app.route("/download_csv/<int:survey_id>")
def download_csv(survey_id):
    survey = Survey.query.get_or_404(survey_id)
    responses = Response.query.filter_by(survey_id=survey.id).all()

    output = io.StringIO()
    writer = csv.writer(output, delimiter=";")
    
    questions = [q.text for q in survey.questions]
    writer.writerow(["ID"] + questions)

    for i, response in enumerate(responses, 1):
        answers = json.loads(response.answers)
        writer.writerow([i] + answers)

    output.seek(0)
    return send_file(io.BytesIO(output.getvalue().encode()), mimetype="text/csv", as_attachment=True, download_name=f"Umfrage_{survey.title}.csv")

with app.app_context():        # DB erstellen
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
