from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Helper function to open a database connection
def get_db_connection():
    conn = sqlite3.connect("workouts.db")
    conn.row_factory = sqlite3.Row  # Access columns by name like a dictionary
    return conn

@app.route("/")
def index():
    conn = get_db_connection()
    # Fetch all records ordered by newest first
    workouts = conn.execute("SELECT * FROM workouts ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("index.html", workouts=workouts)

@app.route("/add", methods=["POST"])
def add_workout():
    # Retrieve form input values
    exercise = request.form["exercise"]
    sets = request.form["sets"]
    reps = request.form["reps"]
    weight = request.form["weight"]
    date = datetime.now().strftime("%Y-%m-%d")

    # Insert entry into database
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO workouts (exercise, sets, reps, weight, date) VALUES (?, ?, ?, ?, ?)",
        (exercise, sets, reps, weight, date)
    )
    conn.commit()
    conn.close()

    # Redirect user back to home page
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)