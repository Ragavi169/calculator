from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ragavi_31",
    database="calculator_db"
)
cursor = db.cursor(dictionary=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/calculate", methods=["POST"])
def calculate():
    num1 = float(request.form["num1"])
    num2 = float(request.form["num2"])
    op = request.form["operation"]

    if op == "add":
        result = num1 + num2
    elif op == "sub":
        result = num1 - num2
    elif op == "mul":
        result = num1 * num2
    elif op == "div":
        result = num1 / num2
    else:
        result = num1 % num2

    cursor.execute("""
        INSERT INTO calculator_history (num1, num2, operation, result)
        VALUES (%s, %s, %s, %s)
    """, (num1, num2, op, result))
    db.commit()

    return render_template("index.html", result=result)


@app.route("/history")
def history():
    cursor.execute("SELECT * FROM calculator_history ORDER BY id DESC")
    data = cursor.fetchall()
    return render_template("history.html", history=data)


@app.route("/clear")
def clear():
    cursor.execute("DELETE FROM calculator_history")
    db.commit()
    return redirect("/history")


if __name__ == "__main__":
    app.run(debug=True)
