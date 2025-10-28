from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patients.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    diagnosis = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

# Home page - show all patients
@app.route('/')
def index():
    patients = Patient.query.all()
    return render_template('index.html', patients=patients)

# Add patient
@app.route('/add', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        diagnosis = request.form['diagnosis']

        new_patient = Patient(name=name, age=age, gender=gender, diagnosis=diagnosis)
        db.session.add(new_patient)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add.html')

# Edit patient
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_patient(id):
    patient = Patient.query.get_or_404(id)
    if request.method == 'POST':
        patient.name = request.form['name']
        patient.age = request.form['age']
        patient.gender = request.form['gender']
        patient.diagnosis = request.form['diagnosis']
        patient.address = request.form['address']
        patient. contact = request.form['contact']
        patient.email = request.form['email']
       
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', patient=patient)

# Delete patient
@app.route('/delete/<int:id>', methods=['POST'])
def delete_patient(id):
    patient = Patient.query.get_or_404(id)
    db.session.delete(patient)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
