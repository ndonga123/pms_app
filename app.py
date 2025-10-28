from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Use SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patients.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
@app.before_first_request
def create_tables():
    db.create_all()


# Define the patient model (table)
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    condition = db.Column(db.String(200), nullable=False)

# Homepage – list patients
@app.route('/')
def home():
    patients = Patient.query.all()
    return render_template('index.html', patients=patients)

# Add patient form
@app.route('/add', methods=['POST'])
def add_patient():
    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    condition = request.form['condition']

    new_patient = Patient(name=name, age=age, gender=gender, condition=condition)
    db.session.add(new_patient)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
