# NEU Virtual Assistant Chatbot

A production-ready chatbot for Near East University students. Ask questions about admissions, faculties, campus locations, dorms, and get instant answers with clickable map links.

## 🚀 Features

- 💬 171+ FAQ entries covering all NEU topics
- 🗺️ Interactive Google Maps integration with precise GPS coordinates
- 🔍 Smart web scraping from neu.edu.tr for unknown questions
- 📍 15+ campus building locations (faculties, banks, library, hospital)
- 🎨 NEU brand colors and professional design
- ⚡ Real-time responses with session management

## 🛠️ Tech Stack

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite 5.4** - Fast build tool
- **Tailwind CSS** - Styling
- **Axios** - HTTP client

### Backend
- **Python 3.14** - Programming language
- **FastAPI 0.104** - Web framework
- **Uvicorn** - ASGI server
- **BeautifulSoup4** - Web scraping
- **Pydantic** - Data validation

## 📋 Prerequisites

- **Node.js** (v18 or higher)
- **Python** (v3.10 or higher)
- **Git**

## 🔧 Installation & Setup

### 1. Clone the Repository
```bash

cd NEU-Chatbot
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install
```

## ▶️ Running the Bot

### Start Backend Server
```bash
cd backend
.\venv\Scripts\python.exe app.py
```
Backend runs on: **http://localhost:8000**

### Start Frontend Server
```bash
cd frontend
npm run dev
```
Frontend runs on: **http://localhost:5173**

## 🌐 Usage

1. Open browser to **http://localhost:5173**
2. Type your question in the chat input
3. Get instant answers with clickable links

### Example Questions:
- "Where is CIS faculty?"
- "Show me on map"
- "How to register?"
- "Where is Near East Bank?"
- "Who is the dean of CIS?"

## 📁 Project Structure

```
NEU-Chatbot/
├── backend/
│   ├── app.py              # FastAPI application
│   ├── services/
│   │   └── bot_logic.py    # Chatbot logic + FAQ
│   ├── routes/
│   │   └── chat.py         # API endpoints
│   ├── models/
│   │   └── message.py      # Pydantic models
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/         # Page components
│   │   ├── utils/         # API utilities
│   │   └── types/         # TypeScript types
│   ├── package.json
│   └── vite.config.ts
└── README.md
```

## 🎯 API Endpoints

- `POST /api/chat` - Send message, get bot response
- `GET /api/health` - Health check
- `POST /api/upload` - File upload (max 10MB)

## 🗺️ Map Integration

The bot provides precise Google Maps links for:
- Main campus
- 5 faculty buildings
- 2 bank locations
- Library, hospital, sports complex
- Student dormitories
- Administrative offices

## 📝 Configuration

### Backend (.env)
```
HOST=127.0.0.1
PORT=8000
DEBUG=True
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000
```

## 🧪 Testing

Ask the bot:
```
"show me on map"
"where is near east bank"
"who is nadire cavus"
"how to register"
```

## 📄 License

MIT License



## 🙏 Acknowledgments

- Near East University for institutional data
- NEU website (neu.edu.tr) for information source
