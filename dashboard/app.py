from flask import Flask, render_template, request, redirect, session
from database.db_connection import get_connection

app = Flask(__name__)

app.secret_key = "secret123"


# ---------- LOGIN CHECK FUNCTION ----------

def check_login():

    if "user" not in session:
        return False

    return True


# ---------- HOME ----------

@app.route("/")
def home():

    if not check_login():
        return redirect("/login")

    return render_template("base.html")


# ---------- LOGIN ----------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        user = request.form["user"]
        pw = request.form["pass"]

        if user == "admin" and pw == "admin":

            session["user"] = user

            return redirect("/devices")

        else:
            return "Wrong login"

    return render_template("login.html")


# ---------- LOGOUT ----------

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# ---------- DEVICES ----------

@app.route("/devices")
def devices():

    if not check_login():
        return redirect("/login")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM devices")

    data = cursor.fetchall()

    conn.close()

    return render_template(
        "devices.html",
        devices=data
    )


# ---------- HEALTH ----------

@app.route("/health")
def health():

    if not check_login():
        return redirect("/login")

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT devices.device_name,
           health_score.score,
           health_score.health_status,
           health_score.last_update
    FROM health_score
    JOIN devices
    ON devices.device_id = health_score.device_id
    """

    cursor.execute(query)

    data = cursor.fetchall()

    conn.close()

    return render_template(
        "health.html",
        data=data
    )


# ---------- ALERTS ----------

@app.route("/alerts")
def alerts():

    if not check_login():
        return redirect("/login")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM alerts ORDER BY alert_time DESC"
    )

    data = cursor.fetchall()

    conn.close()

    return render_template(
        "alerts.html",
        alerts=data
    )


if __name__ == "__main__":
    app.run(debug=True)