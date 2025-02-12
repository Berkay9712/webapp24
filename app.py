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

# Benutzer-Modell
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Umfrage-Modell
class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    questions = db.Column(db.Text, nullable=False)  # Gespeichert als JSON-String
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Null, wenn kein User angemeldet

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

# Startseite mit Login
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Erfolgreich eingeloggt!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Falscher Nutzername oder Passwort!', 'danger')

    return render_template('index.html')

# Registrierung
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash('Nutzername bereits vergeben!', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)  # Direkt einloggen nach Registrierung
        flash('Registrierung erfolgreich! Du bist jetzt eingeloggt.', 'success')
        return redirect(url_for('dashboard'))

    return render_template('register.html')

# Dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    surveys = Survey.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', user=current_user, surveys=surveys)

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Erfolgreich ausgeloggt!', 'info')
    return redirect(url_for('home'))

# Umfrage erstellen
@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        questions = request.form.getlist('questions[]')

        # Falls keine Fragen eingegeben wurden, leere Liste speichern
        questions_json = json.dumps(questions, ensure_ascii=False) if questions else "[]"

        new_survey = Survey(
            title=title,
            questions=questions_json,  # Immer als JSON speichern
            user_id=current_user.id
        )
        db.session.add(new_survey)
        db.session.commit()

        flash('Umfrage erfolgreich erstellt!', 'success')
        return redirect(url_for('created', survey_id=new_survey.id))

    return render_template('create.html', user=current_user)

@app.route('/created/<int:survey_id>')
@login_required
def created(survey_id):
    survey = Survey.query.get_or_404(survey_id)
    survey_link = f"{request.url_root}survey/{survey_id}"  # Erzeugt den vollständigen Link
    return render_template('created.html', survey=survey, survey_link=survey_link)

# Umfrage löschen
@app.route('/delete_survey/<int:survey_id>', methods=['POST'])
@login_required
def delete_survey(survey_id):
    survey = Survey.query.get_or_404(survey_id)

    # Überprüfen, ob der aktuelle Nutzer der Ersteller ist
    if survey.user_id != current_user.id:
        flash("Du kannst nur deine eigenen Umfragen löschen!", "danger")
        return redirect(url_for('dashboard'))

    db.session.delete(survey)
    db.session.commit()
    flash("Umfrage erfolgreich gelöscht!", "success")

    return redirect(url_for('dashboard'))

# Umfragelink aufrufen
@app.route('/survey/<int:survey_id>', methods=['GET', 'POST'])
def show_survey(survey_id):
    survey = Survey.query.get_or_404(survey_id)  # Holt die Umfrage oder gibt 404 zurück

    # JSON in eine Python-Liste umwandeln
    try:
        questions = json.loads(survey.questions) if survey.questions else []
    except json.JSONDecodeError as e:
        flash("Fehler beim Laden der Fragen!", "danger")
        questions = []

    return render_template('survey.html', survey=survey, questions=questions)

# Auswertung
@app.route('/results/<int:survey_id>')
@login_required
def results(survey_id):
    survey = Survey.query.get_or_404(survey_id)
    
    # JSON in eine Python-Liste umwandeln
    try:
        questions = json.loads(survey.questions) if survey.questions else []
    except json.JSONDecodeError as e:
        flash("Fehler beim Laden der Fragen!", "danger")
        questions = []
    
    return render_template('results.html', survey=survey, questions=questions)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

