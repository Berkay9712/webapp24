from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///surveys.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mein_geheimer_schlüssel'  # Wähle einen sicheren Schlüssel

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Benutzer-Modell für Authentifizierung
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Umfrage-Modelle
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

# Benutzerauthentifizierung laden
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Datenbanktabellen erstellen (nur einmal notwendig)
with app.app_context():
    db.create_all()

# Startseite
@app.route('/')
def home():
    return render_template('index.html')

# Registrierung
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Prüfen, ob der Nutzername bereits existiert
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Nutzername bereits vergeben!', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registrierung erfolgreich! Bitte logge dich ein.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Falsche Anmeldedaten!', 'danger')

    return render_template('login.html')

# Dashboard für eingeloggte Nutzer
@app.route('/dashboard')
@login_required
def dashboard():
    surveys = Survey.query.all()  # Falls Benutzer nur eigene Umfragen sehen sollen: Survey.query.filter_by(user_id=current_user.id)
    return render_template('dashboard.html', user=current_user, surveys=surveys)

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Erfolgreich ausgeloggt!', 'info')
    return redirect(url_for('home'))

# Umfrage erstellen (nur eingeloggte Nutzer)
@app.route('/create', methods=['GET', 'POST'])
@login_required
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
        return render_template('created.html', survey_link=survey_link, survey_id=new_survey.id)

    return render_template('create.html')

# Umfrage anzeigen & ausfüllen
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

#  Ergebnisse einer Umfrage anzeigen
@app.route('/results/<int:survey_id>')
def results(survey_id):
    survey = Survey.query.get_or_404(survey_id)
    return render_template('results.html', survey=survey)

#  Flask-App starten
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) # Zugrif auch von anderen Geräten erlauben



