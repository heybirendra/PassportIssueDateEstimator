from flask import Flask, render_template, request
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

app = Flask(__name__)

# Load country rules
COUNTRY_RULES = pd.read_csv("country_rules.csv").set_index("country").to_dict(orient="index")

def calculate_age(dob, expiry_date):
    age = expiry_date.year - dob.year
    if (expiry_date.month, expiry_date.day) < (dob.month, dob.day):
        age -= 1
    return age

def estimate_issue_date(expiry_date, dob, nationality):
    nationality = nationality.upper()
    if nationality not in COUNTRY_RULES:
        return None
    rules = COUNTRY_RULES[nationality]
    age = calculate_age(dob, expiry_date)
    validity = rules["adult_validity"] if age >= rules["adult_age"] else rules["minor_validity"]
    # Handle exceptions (e.g., UK pre-2018)
    if nationality == "UK" and expiry_date < datetime(2018, 1, 1):
        validity = 9.5
    return expiry_date - relativedelta(years=validity)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        expiry_date = datetime.strptime(request.form["expiry_date"], "%Y-%m-%d")
        dob = datetime.strptime(request.form["dob"], "%Y-%m-%d")
        nationality = request.form["nationality"]
        issue_date = estimate_issue_date(expiry_date, dob, nationality)
        return render_template("index.html", issue_date=issue_date)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)