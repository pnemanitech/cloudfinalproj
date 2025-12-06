from flask import Flask, jsonify, request
from flask_cors import CORS

from db import add_todo, delete_todo, get_todos, update_todo

app = Flask(__name__)
CORS(app)


@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/api/todos")
def list_todos():
    return jsonify(get_todos())


@app.post("/api/todos")
def create_todo():
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    if not title:
        return jsonify({"error": "Title is required"}), 400
    todo = add_todo(title)
    return jsonify(todo), 201


@app.patch("/api/todos/<int:todo_id>")
def edit_todo(todo_id: int):
    data = request.get_json(silent=True) or {}
    fields = {}
    if "title" in data:
        fields["title"] = data["title"]
    if "completed" in data:
        fields["completed"] = data["completed"]

    updated = update_todo(todo_id, **fields)
    if not updated:
        return jsonify({"error": "Not found"}), 404
    return jsonify(updated)


@app.delete("/api/todos/<int:todo_id>")
def remove_todo(todo_id: int):
    deleted = delete_todo(todo_id)
    if not deleted:
        return jsonify({"error": "Not found"}), 404
    return jsonify({"success": True})


if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
