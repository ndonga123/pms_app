
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / 'patients.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS patients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    dob TEXT,
                    phone TEXT,
                    address TEXT,
                    notes TEXT
                )''')
    conn.commit()
    conn.close()

app = Flask(__name__)
app.secret_key = 'dev-secret-key'  # change for production
init_db()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    patients = conn.execute('SELECT * FROM patients ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('index.html', patients=patients)

@app.route('/add', methods=('GET','POST'))
def add():
    if request.method == 'POST':
        first = request.form['first_name'].strip()
        last = request.form['last_name'].strip()
        dob = request.form.get('dob','').strip()
        phone = request.form.get('phone','').strip()
        address = request.form.get('address','').strip()
        notes = request.form.get('notes','').strip()
        if not first or not last:
            flash('First and last name are required.')
            return redirect(url_for('add'))
        conn = get_db_connection()
        conn.execute('INSERT INTO patients (first_name,last_name,dob,phone,address,notes) VALUES (?,?,?,?,?,?)',
                     (first,last,dob,phone,address,notes))
        conn.commit()
        conn.close()
        flash('Patient added.')
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=('GET','POST'))
def edit(id):
    conn = get_db_connection()
    patient = conn.execute('SELECT * FROM patients WHERE id = ?', (id,)).fetchone()
    if not patient:
        conn.close()
        flash('Patient not found.')
        return redirect(url_for('index'))
    if request.method == 'POST':
        first = request.form['first_name'].strip()
        last = request.form['last_name'].strip()
        dob = request.form.get('dob','').strip()
        phone = request.form.get('phone','').strip()
        address = request.form.get('address','').strip()
        notes = request.form.get('notes','').strip()
        if not first or not last:
            flash('First and last name are required.')
            return redirect(url_for('edit', id=id))
        conn.execute('UPDATE patients SET first_name=?, last_name=?, dob=?, phone=?, address=?, notes=? WHERE id=?',
                     (first,last,dob,phone,address,notes,id))
        conn.commit()
        conn.close()
        flash('Patient updated.')
        return redirect(url_for('index'))
    conn.close()
    return render_template('edit.html', patient=patient)

@app.route('/delete/<int:id>', methods=('POST',))
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM patients WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Patient deleted.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
