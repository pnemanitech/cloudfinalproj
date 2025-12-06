# Cloud TODO App
A simple Python Flask + vanilla JS TODO app ready for cloud deployment experiments.

## Backend setup
1. `cd backend`
2. `python -m venv venv`
3. `source venv/bin/activate` (Windows: `venv\\Scripts\\activate`)
4. `pip install -r requirements.txt`
5. `python app.py`

Backend runs at `http://localhost:5000`.

## Frontend usage
- Open `frontend/index.html` in a browser via a simple static server (e.g., VS Code Live Server).
- `API_BASE_URL` in `frontend/app.js` is set to `http://localhost:5000`; update it if your backend is hosted elsewhere.

## API endpoints
- `GET /api/health` — health check.
- `GET /api/todos` — list todos.
- `POST /api/todos` — create a todo (`{ "title": "..." }`).
- `PATCH /api/todos/<id>` — update fields like `title` or `completed`.
- `DELETE /api/todos/<id>` — remove a todo.
