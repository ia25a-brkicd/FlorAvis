import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from dotenv import load_dotenv # Lädt .env Datei
from config import DevelopmentConfig, ProductionConfig
from db import close_db, init_db
from services import auth_service
from repository import postgresql_repo as user_repo

# 1. .env laden (macht lokal Variablen verfügbar, auf Render passiert nichts)
load_dotenv()

app = Flask(__name__)

# 2. Config wählen
if os.environ.get('FLASK_ENV') == 'development':
    app.config.from_object(DevelopmentConfig)
else:
    app.config.from_object(ProductionConfig)

app.teardown_appcontext(close_db)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/init-db')
def initialize():
    try:
        init_db()
        return "Datenbank Tabelle 'users' erstellt."
    except Exception as e:
        return f"Fehler: {e}"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        action = request.form['action']
        username = request.form['username']
        password = request.form['password']

        if action == 'register':
            if user_repo.create_user(username, password):
                flash('Registriert! Jetzt einloggen.')
            else:
                flash('Username vergeben.')
            
        elif action == 'login':
            user_id = auth_service.authenticate(username, password)
            if user_id:
                session['user_id'] = user_id
                return redirect(url_for('profile'))
            else:
                flash('Falsche Daten.')

    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = user_repo.get_user_by_id(session['user_id'])
    return render_template('profile.html', username=user[1], user_id=user[0])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    # Lokal starten
    app.run(port=5000)