from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from flask import Flask, jsonify, request
from database import init_db
import sqlite3

app = Flask(__name__)
app.config["SECRET_KEY"] = "tanisha-super-secret-key-2026"
init_db()

def get_conn():
    return sqlite3.connect("tasks.db")
@app.route("/register", methods=["POST"])
def register():
    data = request.json

    username = data["username"]
    password = generate_password_hash(data["password"])

    conn = get_conn()

    try:
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()

    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": "Username already exists"}), 400

    conn.close()

    return jsonify({"message": "Registration successful"})
    @app.route("/login", methods=["POST"])
def login():
    data = request.json

    username = data["username"]
    password = data["password"]

    conn = get_conn()

    user = conn.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    ).fetchone()

    conn.close()

    if not user:
        return jsonify({"error": "Invalid username or password"}), 401

    if not check_password_hash(user[2], password):
        return jsonify({"error": "Invalid username or password"}), 401

    token = jwt.encode(
        {
            "user_id": user[0],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
        },
        app.config["SECRET_KEY"],
        algorithm="HS256"
    )

    return jsonify({"token": token})
    def get_current_user():
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return None

    try:
        token = auth_header.replace("Bearer ", "")

        data = jwt.decode(
            token,
            app.config["SECRET_KEY"],
            algorithms=["HS256"]
        )

        return data["user_id"]

    except:
        return None
@app.route("/tasks", methods=["GET"])
def get_tasks():
    conn = get_conn()
   user_id = get_current_user()

if not user_id:
    return jsonify({"error": "Unauthorized"}), 401

tasks = conn.execute(
    "SELECT * FROM tasks WHERE user_id = ?",
    (user_id,)
).fetchall()
    conn.close()
    task_list = [
        {"id": t[0], "task": t[2], "done": t[3], "due_date": t[4]}
        for t in tasks
    ]
    return jsonify(task_list)

@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.json
    task_text = data["task"]
    due_date = data.get("due_date", None)
    user_id = get_current_user()

if not user_id:
    return jsonify({"error": "Unauthorized"}), 401
    conn = get_conn()
   conn.execute(
    """
    INSERT INTO tasks (user_id, task, due_date)
    VALUES (?, ?, ?)
    """,
    (user_id, task_text, due_date)
)
    conn.commit()
    conn.close()
    return jsonify({"message": "Task added!"})

@app.route("/tasks/<int:task_id>/toggle", methods=["PUT"])
def toggle_task(task_id):
    conn = get_conn()
    conn.execute("""
        UPDATE tasks
        SET done = CASE WHEN done = 0 THEN 1 ELSE 0 END
        WHERE id = ?
    """, (task_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Task updated!"})

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = get_conn()
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Task deleted!"})

import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
