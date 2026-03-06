# NEU Virtual Assistant

Simple full-stack chatbot for Near East University (NEU).

## What This Project Does
- Provides answers to common NEU questions (registration, faculties, dorms, campus services).
- Supports chat history by `session_id`.
- Uses a local NEU knowledge base and AI-assisted responses.
- Shows a branded landing page and chat UI.

## Tech Stack
- Backend: FastAPI, Pydantic, Uvicorn
- Frontend: Vanilla HTML/CSS/JavaScript, Node static server

## Requirements
- Python 3.10+
- Node.js 18+

## Quick Start (Windows PowerShell)

### 1. Initial setup
```powershell
cd NEU-chatbot-main
.\setup.ps1
```

### 2. Run backend (Terminal 1)
```powershell
cd backend
.\run.ps1
```
Backend URL: `http://localhost:8000`

### 3. Run frontend (Terminal 2)
```powershell
cd frontend
npm run start
```
Frontend URL: `http://127.0.0.1:5173`

## API Endpoints
- `POST /api/chat`
- `GET /api/health`
- `GET /api/chat/history/{session_id}`
- `DELETE /api/chat/session/{session_id}`

## Main Folders
```text
backend/
	app.py
	routes/
	services/
	models/
frontend/
	index.html
	styles.css
	script.js
assets/
```

## Notes
- No terminal windows are opened automatically by the app itself.
- If you need strict production behavior, pin dependencies after final testing.

## License
MIT


