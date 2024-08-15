#server.py for register service
import os
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from passlib.hash import pbkdf2_sha256



app = Flask(__name__)

# MySQL configuration
app.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
app.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
app.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
app.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
app.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")

mysql = MySQL(app)

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    cur = mysql.connection.cursor()
    res = cur.execute("SELECT COUNT(*) FROM users WHERE email = %s", (email,))
    

    if res > 0:
        return jsonify({"message": "Email already in use"}), 400


    cur.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "User registered successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5001)