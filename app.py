from flask import Flask, render_template, request
import re
import hashlib
import requests

app = Flask(__name__)

# Load dictionary words
with open("dictionary.txt") as f:
    dictionary_words = set(word.strip().lower() for word in f)

def check_strength(password):
    score = 100
    tips = []

    # Length check
    if len(password) < 12:
        tips.append("Make your password at least 12 characters long.")
        score -= 25

    # Character variety check
    if not re.search(r'[A-Z]', password):
        tips.append("Add uppercase letters.")
        score -= 10
    if not re.search(r'[a-z]', password):
        tips.append("Add lowercase letters.")
        score -= 10
    if not re.search(r'[0-9]', password):
        tips.append("Add numbers.")
        score -= 10
    if not re.search(r'[^A-Za-z0-9]', password):
        tips.append("Add symbols.")
        score -= 10

    # Dictionary word check
    lower_pass = password.lower()
    for word in dictionary_words:
        if word in lower_pass:
            tips.append(f"Remove dictionary word: '{word}'")
            score -= 15
            break

    # Breach check using HaveIBeenPwned API
    sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix, suffix = sha1_hash[:5], sha1_hash[5:]
    res = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")
    if res.status_code == 200:
        hashes = (line.split(":") for line in res.text.splitlines())
        for h, count in hashes:
            if h == suffix:
                tips.append(f"Found in {count} breaches — change it immediately!")
                score -= 50
                break

    return max(score, 0), tips

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        password = request.form["password"]
        score, tips = check_strength(password)
        return render_template("result.html", score=score, tips=tips)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
