import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

# Create table if it doesn't exist
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS registrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    event TEXT
)
""")

conn.commit()
conn.close()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/events")
def events():
    return render_template("events.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        event = request.form["event"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO registrations (name, email, event) VALUES (?, ?, ?)",
            (name, email, event)
        )

        conn.commit()
        conn.close()

        return render_template(
            "success.html",
            name=name,
            email=email,
            event=event
        )

    return render_template("register.html")


@app.route("/admin")
def admin():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM registrations")

    students = cursor.fetchall()

    conn.close()

    return render_template(
        "admin.html",
        students=students
    )


if __name__ == "__main__":
    app.run(debug=True)