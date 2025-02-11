from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'mein_geheimer_schlüssel'

# Datenbank initialisieren
db = SQLAlchemy(app)

# Flask-Login konfigurieren
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

#  Datenbankmodelle
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    surveys = db.relationship('Survey', backref='creator', lazy=True)

class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Optional für Gast-Umfragen

# Lade Nutzer für Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#  Startseite
@app.route("/")
def index():
    return render_template("index.html")

#  Registrierung eines neuen Nutzers
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        # Prüfen, ob der Nutzer bereits existiert
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Nutzername bereits vergeben!", "danger")
            return redirect(url_for("register"))
        
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash("Registrierung erfolgreich! Bitte logge dich ein.", "success")
        return redirect(url_for("login"))
    
    return render_template("register.html")

#  Login eines Nutzers (nur mit Nutzername und Passwort)
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            flash("Falscher Nutzername oder falsches Passwort!", "danger")
    
    return render_template("login.html")

#  Dashboard für eingeloggte Nutzer mit ihren Umfragen
@app.route("/dashboard")
@login_required
def dashboard():
    surveys = Survey.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html", user=current_user, surveys=surveys)

#  Logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Erstellt die Tabellen, falls sie nicht existieren
    app.run(debug=True)


