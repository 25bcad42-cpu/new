from flask import Flask, render_template, request, redirect
import pymysql
import os

app = Flask(__name__)

# Railway MySQL Connection
connection = pymysql.connect(
    host=os.getenv("MYSQLHOST"),
    user=os.getenv("MYSQLUSER"),
    password=os.getenv("MYSQLPASSWORD"),
    database=os.getenv("MYSQLDATABASE"),
    port=int(os.getenv("MYSQLPORT"))
)

# HOME PAGE (Fetch Data)
@app.route("/")
def home():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM contacts ORDER BY id DESC")
    contacts = cursor.fetchall()
    cursor.close()

    return render_template("index.html", contacts=contacts)


# INSERT DATA
@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    cursor = connection.cursor()

    sql = "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)"
    cursor.execute(sql, (name, email, message))
    connection.commit()

    cursor.close()

    return redirect("/")


# RUN
if __name__ == "__main__":
    app.run(debug=True)