from flask import Flask, render_template, request, redirect, url_for, session, send_file
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = "geheimespasswort"  # Geheimschlüssel für die Session

data_file = "survey_results.xlsx"

# Login-Daten für Gebietsleiter
USER_CREDENTIALS = {
    "gebietsleiter": "passwort123"
}

@app.route('/')
def home():
    if "user" in session:
        return f"Willkommen {session['user']}! <a href='/survey'>Zur Umfrage</a> | <a href='/download'>Ergebnisse</a> | <a href='/logout'>Logout</a>"
    return "Willkommen zu NTCHECKS! <a href='/login'>Login</a>"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            session["user"] = username
            return redirect(url_for('survey'))  # Nutzer zur Umfrage weiterleiten
        else:
            return "Falsche Login-Daten! <a href='/login'>Erneut versuchen</a>"

    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for('home'))

@app.route('/survey', methods=['GET', 'POST'])
def survey():
    if "user" not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        filiale = request.form['filiale']
        sauberkeit = request.form['sauberkeit']
        produktqualität = request.form['produktqualität']

        new_data = pd.DataFrame([[filiale, sauberkeit, produktqualität]], 
                                columns=["Filiale", "Sauberkeit", "Produktqualität"])
        
        if os.path.exists(data_file):
            existing_data = pd.read_excel(data_file)
            new_data = pd.concat([existing_data, new_data], ignore_index=True)
        
        new_data.to_excel(data_file, index=False)
        
        return render_template("thank_you.html")  # Nach Absenden zur Bestätigungsseite weiterleiten

    return render_template("survey.html")

@app.route('/download')
def download():
    if os.path.exists(data_file):
        return send_file(data_file, as_attachment=True)
    else:
        return "Keine Ergebnisse vorhanden."

if __name__ == '__main__':
    app.run(debug=True)
