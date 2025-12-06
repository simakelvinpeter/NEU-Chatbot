# NEU Virtual Assistant Chatbot

A production-ready university chatbot interface built with React + TypeScript (frontend) and FastAPI (backend).

## 🏗️ Project Structure

```
NEU-Chatbot/
├── frontend/                 # React + TypeScript frontend
│   ├── public/              # Static assets
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/          # Page components
│   │   ├── utils/          # Utility functions
│   │   ├── types/          # TypeScript type definitions
│   │   └── App.tsx         # Main App component
│   └── package.json
│
├── backend/                 # FastAPI backend
│   ├── app.py              # FastAPI entry point
│   ├── routes/             # API endpoints
│   ├── services/           # Business logic
│   ├── models/             # Pydantic models
│   ├── core/               # Configuration
│   └── requirements.txt
│
└── README.md
```

## ✨ Features

- **Modern UI**: Based on Near East University design with Tailwind CSS
- **Responsive Design**: Works seamlessly on desktop and mobile
- **Real-time Chat**: Dynamic message rendering with typing indicators
- **File Attachments**: Support for uploading files
- **Quick Links Sidebar**: Easy access to university resources
- **Accessibility**: High contrast, keyboard navigation, ARIA labels
- **Type Safety**: Full TypeScript support
- **API Integration**: RESTful API with FastAPI backend

## 🚀 Getting Started

### Prerequisites

- Node.js 16+ and npm/yarn
- Python 3.8+
- pip

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend will run on `http://localhost:5173`

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python app.py
```

The backend API will run on `http://localhost:8000`

## 📖 API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🔧 Configuration

### Frontend Environment Variables

Create a `.env` file in the `frontend` directory:

```env
VITE_API_URL=http://localhost:8000
```

### Backend Environment Variables

Create a `.env` file in the `backend` directory:

```env
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
DEBUG=True
```

## 🧪 Testing

### Frontend Tests
```bash
cd frontend
npm run test
```

### Backend Tests
```bash
cd backend
pytest
```

## 📦 Production Build

### Frontend
```bash
cd frontend
npm run build
```

### Backend
```bash
cd backend
uvicorn app:app --host 0.0.0.0 --port 8000
```

## 🎨 Design System

- **Primary Color**: #d41111 (NEU Red)
- **Font Family**: Lexend (headings), Noto Sans (body)
- **Icons**: Material Symbols
- **Framework**: Tailwind CSS

## 📝 License

This project is licensed under the MIT License.

## 👥 Contributors

- Development Team
- Near East University

## 🔗 Links

- [GitHub Repository](https://github.com/simakelvinpeter/NEU-Chatbot)
- [Near East University](https://neu.edu.tr)
