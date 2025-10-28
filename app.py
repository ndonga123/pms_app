from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Use Render's writable directory (/tmp) for SQLite
db_path = os.path.join("/tmp", "patients.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    diagnosis = db.Column(db.String(200))

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    patients = Patient.query.all()
    return render_template("index.html", patients=patients)

@app.route("/add", methods=["POST"])
def add_patient():
    name = request.form.get("name")
    age = request.form.get("age")
    diagnosis = request.form.get("diagnosis")

    if name:
        new_patient = Patient(name=name, age=age, diagnosis=diagnosis)
        db.session.add(new_patient)
        db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:id>")
def delete_patient(id):
    patient = Patient.query.get(id)
    if patient:
        db.session.delete(patient)
        db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
