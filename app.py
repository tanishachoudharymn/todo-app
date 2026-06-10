from flask import Flask, jsonify, request
from database import init_db
import sqlite3

app = Flask(__name__)
init_db()

def get_conn():
    return sqlite3.connect("tasks.db")

@app.route("/tasks", methods=["GET"])
def get_tasks():
    conn = get_conn()
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    task_list = [
        {"id": t[0], "task": t[1], "done": t[2], "due_date": t[3]}
        for t in tasks
    ]
    return jsonify(task_list)

@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.json
    task_text = data["task"]
    due_date = data.get("due_date", None)
    conn = get_conn()
    conn.execute(
        "INSERT INTO tasks (task, due_date) VALUES (?, ?)",
        (task_text, due_date)
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

app.run(port=5000)
