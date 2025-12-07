"""
Firestore-backed todo storage for the cloud demo app.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from google.cloud import firestore

# Firestore client and collection reference
_db = firestore.Client()
_todos_collection = _db.collection("todos")


def get_todos() -> List[Dict[str, Any]]:
    """
    Return all todos from Firestore, ordered by created_at (newest first).
    Each todo is a dict with: id (int), title (str), completed (bool), created_at (ISO str).
    """
    docs = (
        _todos_collection.order_by("created_at", direction=firestore.Query.DESCENDING)
        .stream()
    )

    todos: List[Dict[str, Any]] = []
    for doc in docs:
        data = doc.to_dict() or {}
        todos.append(
            {
                "id": data.get("id"),
                "title": data.get("title", ""),
                "completed": data.get("completed", False),
                "created_at": data.get("created_at", datetime.utcnow().isoformat()),
            }
        )
    return todos


def _get_next_id() -> int:
    """
    Compute the next integer id by looking at existing todos.
    This is fine for a small demo app.
    """
    docs = _todos_collection.stream()
    max_id = 0
    for doc in docs:
        data = doc.to_dict() or {}
        try:
            current_id = int(data.get("id", 0))
            if current_id > max_id:
                max_id = current_id
        except (TypeError, ValueError):
            continue
    return max_id + 1


def add_todo(title: str) -> Dict[str, Any]:
    """
    Add a new todo document in Firestore with an incrementing integer id.
    """
    new_id = _get_next_id()
    todo = {
        "id": new_id,
        "title": title,
        "completed": False,
        "created_at": datetime.utcnow().isoformat(),
    }
    # Use an auto-generated document ID; the numeric id is stored as a field.
    _todos_collection.add(todo)
    return todo


def _get_doc_by_id(todo_id: int):
    """
    Helper: find the Firestore document whose 'id' field matches todo_id.
    Returns the document snapshot or None.
    """
    query = _todos_collection.where("id", "==", todo_id).limit(1).stream()
    for doc in query:
        return doc
    return None


def update_todo(todo_id: int, **fields: Any) -> Optional[Dict[str, Any]]:
    """
    Update fields on a todo in Firestore if it exists; return the updated todo or None.
    """
    doc = _get_doc_by_id(todo_id)
    if not doc:
        return None

    # Only update allowed fields
    updates: Dict[str, Any] = {}
    if "title" in fields:
        updates["title"] = fields["title"]
    if "completed" in fields:
        updates["completed"] = fields["completed"]

    if not updates:
        # Nothing to update; return current data
        data = doc.to_dict() or {}
        return {
            "id": data.get("id"),
            "title": data.get("title", ""),
            "completed": data.get("completed", False),
            "created_at": data.get("created_at", datetime.utcnow().isoformat()),
        }

    doc.reference.update(updates)

    # Return merged view
    data = doc.to_dict() or {}
    data.update(updates)
    return {
        "id": data.get("id"),
        "title": data.get("title", ""),
        "completed": data.get("completed", False),
        "created_at": data.get("created_at", datetime.utcnow().isoformat()),
    }


def delete_todo(todo_id: int) -> bool:
    """
    Delete a todo in Firestore by its integer id; return True if it was removed.
    """
    doc = _get_doc_by_id(todo_id)
    if not doc:
        return False
    doc.reference.delete()
    return True
