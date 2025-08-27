from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector as mysql

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database connection
db = mysql.connect(
    host="localhost",
    user="root",
    password="Varun@1505",
    database="user_detail"
)

@app.route("/")
def home():
    return render_template("login.html")   # Default: show login page

@app.route("/login", methods=["POST"])
def login():
    username = request.form["email"]
    password = request.form["password"]

    cursor = db.cursor()
    cursor.execute("SELECT * FROM details WHERE email=%s AND password=%s", (username, password))
    user = cursor.fetchone()

    if user:
        return redirect(url_for("welcome", email=username))
    else:
        flash("Invalid username or password")
        return redirect(url_for("home"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name =request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        cursor = db.cursor()
        cursor.execute("INSERT INTO details (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
        db.commit()
        flash("Registration successful! Please login.")
        return redirect(url_for("home"))
    return render_template("register.html")

@app.route("/welcome")
def welcome():
    name = request.args.get("name", "Guest")
    return render_template("welcome.html", username=name)

if __name__ == "__main__":
    app.run(debug=True)
