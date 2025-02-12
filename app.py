from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///surveys.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mein_geheimer_schlüssel'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "home"

# Modelle
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    questions = db.Column(db.Text, nullable=False)  # JSON-Format
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'), nullable=False)
    answers = db.Column(db.Text, nullable=False)

    survey = db.relationship('Survey', backref=db.backref('responses', lazy=True))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

# Hilfsfunktionen
def parse_json(data, default=[]):
    try:
        return json.loads(data) if data else default
    except json.JSONDecodeError:
        return default

# Routen
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            flash('Erfolgreich eingeloggt!', 'success')
            return redirect(url_for('dashboard'))
        flash('Falscher Nutzername oder Passwort!', 'danger')
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if User.query.filter_by(username=request.form['username']).first():
            flash('Nutzername bereits vergeben!', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(request.form['password'])
        new_user = User(username=request.form['username'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        flash('Registrierung erfolgreich!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    surveys = Survey.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', surveys=surveys)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Erfolgreich ausgeloggt!', 'info')
    return redirect(url_for('home'))

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        questions_json = json.dumps(request.form.getlist('questions[]'))
        new_survey = Survey(title=request.form['title'], questions=questions_json, user_id=current_user.id)
        db.session.add(new_survey)
        db.session.commit()
        flash('Umfrage erfolgreich erstellt!', 'success')
        return redirect(url_for('created', survey_id=new_survey.id))
    return render_template('create.html')

@app.route('/created/<int:survey_id>')
@login_required
def created(survey_id):
    survey = Survey.query.get_or_404(survey_id)
    survey_link = f"{request.url_root}survey/{survey_id}"
    return render_template('created.html', survey=survey, survey_link=survey_link)

@app.route('/delete_survey/<int:survey_id>', methods=['POST'])
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

@app.route('/survey/<int:survey_id>', methods=['GET', 'POST'])
def show_survey(survey_id):
    survey = Survey.query.get_or_404(survey_id)
    questions = parse_json(survey.questions)

    if request.method == 'POST':
        answers_json = json.dumps(request.form.getlist('answers[]'))
        new_response = Response(survey_id=survey.id, answers=answers_json)
        db.session.add(new_response)
        db.session.commit()
        return redirect(url_for('submitted', survey_id=survey.id, response_id=new_response.id))

    return render_template('survey.html', survey=survey, questions=questions)

@app.route('/submitted/<int:survey_id>/<int:response_id>')
def submitted(survey_id, response_id):
    response = Response.query.get_or_404(response_id)
    survey = Survey.query.get_or_404(survey_id)

    questions = json.loads(survey.questions) if survey.questions else []
    answers = json.loads(response.answers) if response.answers else []

    # Kombiniere Fragen und Antworten
    combined = list(zip(questions, answers))

    return render_template('submitted.html', survey_id=survey_id, combined=combined)


@app.route('/results/<int:survey_id>')
@login_required
def results(survey_id):
    survey = Survey.query.get_or_404(survey_id)
    responses = Response.query.filter_by(survey_id=survey.id).all()
    all_answers = [parse_json(response.answers) for response in responses]
    return render_template('results.html', survey=survey, all_answers=all_answers)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
