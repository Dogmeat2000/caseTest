from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "super_secret_key" #Is this a sufficient secret key?

# -------------------
# Database setup
# -------------------
def get_db():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.close()

init_db()

# -------------------
# Home (protected)
# -------------------
@app.route("/")
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", username=session["username"])

# -------------------
# Register
# -------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        #username = request.form["username"]
        username = request.form.get('username')
        #password = generate_password_hash(request.form["password"])
        password = generate_password_hash(request.form.get('password'))
        print(password)

        conn = get_db()

        try:
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            flash("Registration successful! Please login.")
            return redirect(url_for("login"))
        except:
            flash("Username already exists.")
        finally:
            conn.close()

    return render_template("register.html")

# -------------------
# Login
# -------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        #username = request.form["username"]
        username = request.form.get('username')
        #password = generate_password_hash(request.form["password"])
        password = generate_password_hash(request.form.get('password'))

        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        # Why are get fetching all users with this name here? Why not just the one with the proper password hash?
        # Using the previous method, we would be fetching all users with the given name - not just the specific one we want...
        print(user)
        conn.close()

        if user and check_password_hash(user["password"], password):
        #    session.permanent = True
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("home"))
        else:
            flash("Invalid credentials")

    return render_template("login.html")

# -------------------
# Logout
# -------------------
@app.route("/logout")
def logout():
    #session.clear() <--- Should not be commented out.
    session.clear()
    return redirect(url_for("login"))

# -------------------
# Run app
# -------------------
if __name__ == "__main__":
    app.run(debug=True)