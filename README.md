
# Patient Management System (Flask)

Simple Patient Management System written in Python using Flask and SQLite.

## Run locally

1. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # mac/linux
   venv\Scripts\activate    # windows
   ```

2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   python app.py
   ```

4. Visit `http://127.0.0.1:5000` in your browser.

## Features
- Add, edit, delete patients
- Uses SQLite (patients.db created automatically)
- Minimal templates for demonstration and submission

## To deploy
- Deploy to any Python-supporting host (Heroku, Render, Railway). You'll need to add a `Procfile` or follow provider instructions.
