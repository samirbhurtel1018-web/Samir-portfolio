from flask import Flask, render_template, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = "samir_secret_key"

# SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# -------------------------
# DATABASE MODEL
# -------------------------
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    message = db.Column(db.String(500))

# -------------------------
# ROUTES
# -------------------------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/skills")
def skills():
    return render_template("skills.html")

@app.route("/projects")
def projects():
    return render_template("projects.html")

@app.route("/resume")
def resume():
    return render_template("resume.html")

# -------------------------
# CONTACT PAGE (PRIVATE MESSAGES)
# -------------------------
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message_text = request.form["message"]

        # Save to database
        new_message = Message(name=name, email=email, message=message_text)
        db.session.add(new_message)
        db.session.commit()

        # Optional: also save to message.txt (private)
        with open("message.txt", "a") as f:
            f.write(f"Name: {name}\nEmail: {email}\nMessage: {message_text}\n---\n")

        flash("Your message has been sent!")  # Show confirmation to user
        return redirect("/contact")

    # Render contact page (no messages visible)
    return render_template("contact.html")

# -------------------------
# ADMIN LOGIN AND DASHBOARD
# -------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":
            session["admin"] = True
            return redirect("/dashboard")
        else:
            flash("Incorrect username or password")

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "admin" not in session:
        return redirect("/login")

    messages = Message.query.all()  # Only admin can see this
    return render_template("dashboard.html", messages=messages)

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/")

# -------------------------
# CREATE DATABASE
# -------------------------
with app.app_context():
    db.create_all()
    # Ensure message.txt exists
    if not os.path.exists("message.txt"):
        open("message.txt", "w").close()

if __name__ == "__main__":
    app.run(debug=True)
