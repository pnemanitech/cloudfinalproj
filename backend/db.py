"""
Extremely simple in-memory todo storage for demo purposes.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional


# Global in-memory list of todos with a couple of starting examples.
_todos: List[Dict[str, Any]] = [
    {
        "id": 1,
        "title": "Set up project structure",
        "completed": True,
        "created_at": datetime.utcnow().isoformat(),
    },
    {
        "id": 2,
        "title": "Build todo backend",
        "completed": False,
        "created_at": datetime.utcnow().isoformat(),
    },
]
_next_id: int = len(_todos) + 1


def get_todos() -> List[Dict[str, Any]]:
    """Return all todos."""
    return list(_todos)


def add_todo(title: str) -> Dict[str, Any]:
    """Add a new todo with an incrementing id and default fields."""
    global _next_id
    todo = {
        "id": _next_id,
        "title": title,
        "completed": False,
        "created_at": datetime.utcnow().isoformat(),
    }
    _todos.append(todo)
    _next_id += 1
    return todo


def update_todo(todo_id: int, **fields: Any) -> Optional[Dict[str, Any]]:
    """Update fields on a todo if it exists; return the updated todo or None."""
    for todo in _todos:
        if todo["id"] == todo_id:
            todo.update(fields)
            return todo
    return None


def delete_todo(todo_id: int) -> bool:
    """Delete a todo by id; return True if it was removed."""
    for idx, todo in enumerate(_todos):
        if todo["id"] == todo_id:
            del _todos[idx]
            return True
    return False
