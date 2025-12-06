const API_BASE_URL = "http://localhost:5050";

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("todo-form");
  const input = document.getElementById("todo-input");
  const list = document.getElementById("todo-list");

  const loadTodos = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/api/todos`);
      const todos = await res.json();
      list.innerHTML = "";
      todos.forEach((todo) => renderTodo(todo));
    } catch (err) {
      console.error("Failed to load todos", err);
    }
  };

  const renderTodo = (todo) => {
    const li = document.createElement("li");

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = Boolean(todo.completed);
    checkbox.addEventListener("change", async () => {
      await updateTodo(todo.id, { completed: checkbox.checked });
      await loadTodos();
    });

    const title = document.createElement("span");
    title.textContent = todo.title;
    title.className = `todo-title${todo.completed ? " completed" : ""}`;

    const deleteBtn = document.createElement("button");
    deleteBtn.textContent = "Delete";
    deleteBtn.addEventListener("click", async () => {
      await deleteTodo(todo.id);
      await loadTodos();
    });

    li.append(checkbox, title, deleteBtn);
    list.appendChild(li);
  };

  const addTodo = async (title) => {
    await fetch(`${API_BASE_URL}/api/todos`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title }),
    });
  };

  const updateTodo = async (id, fields) => {
    await fetch(`${API_BASE_URL}/api/todos/${id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(fields),
    });
  };

  const deleteTodo = async (id) => {
    await fetch(`${API_BASE_URL}/api/todos/${id}`, {
      method: "DELETE",
    });
  };

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const title = input.value.trim();
    if (!title) return;
    await addTodo(title);
    input.value = "";
    await loadTodos();
  });

  loadTodos();
});
