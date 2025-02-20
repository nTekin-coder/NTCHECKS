from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import datetime

app = Flask(__name__)

# **Hier sind jetzt ALLE 22 Fragen korrekt**
questions = [
    {"text": "Plunder- & Gebäckvitrine: A-Fläche richtig bestückt?", "points": [40, 27, 13, 0]},
    {"text": "Brotregal: A-Fläche richtig bestückt?", "points": [40, 27, 13, 0]},
    {"text": "Kühlvitrine (Kondi & Snack): Farb- und Formenspiel, tageszeitliche Präsentation?", "points": [40, 27, 13, 0]},
    {"text": "Handelswaren & HW-Kühlregal: lt. Vorgabe befüllt, ohne Kartons, Etiketten lesbar?", "points": [20, 13, 7, 0]},
    {"text": "Produkte entsprechen vorgegebener Geier-Qualität?", "points": [50, 33, 17, 0]},
    {"text": "Ladenbackliste wird korrekt geführt?", "points": [40, 27, 13, 0]},
    {"text": "Frische ist gegeben (Semmel & Salzstangerl nicht älter als 4 Stunden)?", "points": [50, 33, 17, 0]},
    {"text": "Menge und Auswahl sind angemessen für die Uhrzeit?", "points": [50, 33, 17, 0]},
    {"text": "Snacks sehen frisch und unwiderstehlich aus?", "points": [50, 33, 17, 0]},
    {"text": "Kaffeekultur wird systemgetreu gelebt?", "points": [60, 40, 20, 0]},
    {"text": "Begrüßung findet statt?", "points": [30, 20, 10, 0]},
    {"text": "W-Fragen werden benutzt?", "points": [40, 27, 13, 0]},
    {"text": "Haben Sie eine GEIER-Karte gefragt?", "points": [20, 13, 7, 0]},
    {"text": "Kassiervorgaben werden eingehalten?", "points": [20, 13, 7, 0]},
    {"text": "Herzliche Verabschiedung findet statt?", "points": [40, 27, 33, 0]},
    {"text": "Es wird aktiv, herzlich, kompetent und flott verkauft", "points": [30, 20, 10, 0]},
    {"text": "Hat der Kunde Vorrang (ab 2 wartenden Kunden, Kollegin rufen)?", "points": [30, 20, 10, 0]},
    {"text": "Hygienisches Arbeiten (Gebäckzange, Brotsackerl, Handschuhe)?", "points": [80, 53, 27, 0]},
    {"text": "Berufskleidung sauber & vollständig?", "points": [50, 33, 17, 0]},
    {"text": "Außen: Eindruck für Grundordnung und Sauberkeit tadellos?", "points": [60, 40, 20, 0]},
    {"text": "Innen: Eindruck für Grundordnung und Sauberkeit tadellos?", "points": [80, 53, 27, 0]},
    {"text": "Preisauszeichnung vollständig & korrekt, Plakate ordentlich platziert?", "points": [60, 40, 20, 0]},
    {"text": "Bemerkungen (Freitext)", "type": "text"},
]

@app.route("/", methods=["GET", "POST"])
def survey():
    if request.method == "POST":
        filialnummer = request.form.get("filialnummer")
        unterschrift = request.form.get("unterschrift")

        gesamtpunkte = sum(int(request.form.get(f"q{i}", 0)) for i, q in enumerate(questions) if "points" in q)

        data = {
            "Monat": datetime.date.today().strftime("%Y-%m"),
            "Filialnummer": filialnummer,
            "Ergebnis": gesamtpunkte
        }

        df = pd.DataFrame([data])
        excel_datei = "Umfrage_Ergebnisse.xlsx"

        try:
            existing_df = pd.read_excel(excel_datei)
            df = pd.concat([existing_df, df], ignore_index=True)
        except FileNotFoundError:
            pass

        df.to_excel(excel_datei, index=False)

        return redirect(url_for("thank_you"))

    return render_template("survey.html", questions=questions)

@app.route("/thank-you")
def thank_you():
    return "<h2>Danke für die Teilnahme!</h2> <a href='/'>Neue Umfrage starten</a>"

if __name__ == "__main__":
    app.run(debug=True)
