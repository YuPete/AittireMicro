import os
from flask import Flask, render_template, request, url_for, session, abort, flash, redirect
import requests

app = Flask(__name__)
app.secret_key = "QwE8hFg4JkLm9Np0QrStUvWx"  # Secret key used for session management

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL")
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL")

@app.route("/")
def landing():
    return render_template("landing.html", email=session.get("email"))

@app.route("/forget")
def forget():
    return render_template("forget.html")

@app.route("/clear")
def clear():
    session.clear()
    return redirect(url_for("landing"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email").lower()
        password = request.form.get("password")

        response = requests.post(f"{AUTH_SERVICE_URL}/login", json={"email": email, "password": password})

        if response.status_code == 200:
            session["email"] = email  # Store the user's email in the session
            return redirect(url_for("landing"))
        else:
            flash("Incorrect email or password.")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email").lower()
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-password")

        if password == confirm_password:
            response = requests.post(f"{USER_SERVICE_URL}/register", json={"email": email, "password": password})

            if response.status_code == 200:
                flash("Successfully signed up.")
                return redirect(url_for("login"))
            elif response.status_code == 400:
                flash("Email already in use, login?")
        else:
            flash("Passwords don't match")
    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)