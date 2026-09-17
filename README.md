# AI Smart Interview Analyzer

An AI-powered platform that helps users practice, record, and analyze mock interviews — with performance history, analytics, and coaching feedback.

## Features

- User registration & login
- Interactive mock interview sessions
- Interview history tracking
- Performance analytics dashboard
- AI-powered coaching feedback
- User settings

## Tech Stack

**Backend:** FastAPI, SQLAlchemy, SQLite
**Frontend:** HTML, CSS, JavaScript
**Auth:** JWT (python-jose)
**AI:** OpenAI API

## Project Structure

```
AI-Smart-Interview-Analyzer/
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── routes/
│   ├── services/
│   └── requirements.txt
├── frontend/
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── interview.html
│   ├── interview-room.html
│   ├── history.html
│   ├── analytics.html
│   ├── coach.html
│   └── settings.html
└── README.md
```

## Getting Started

### Prerequisites
- Python 3.10+
- pip

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/AI-Smart-Interview-Analyzer.git
cd AI-Smart-Interview-Analyzer
```

2. Create and activate a virtual environment
```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux
```

3. Install dependencies
```bash
pip install -r backend/requirements.txt
```

4. Set up environment variables

Create a `.env` file inside `backend/`:
```
OPENAI_API_KEY=your-key-here
```

5. Run the server
```bash
uvicorn backend.main:app --reload
```

6. Open in browser
```
http://127.0.0.1:8000/login.html
```

## Available Pages

| Route | Description |
|---|---|
| `/login.html` | User login |
| `/register.html` | New user registration |
| `/dashboard.html` | Main dashboard |
| `/interview.html` | Start a mock interview |
| `/interview-room.html` | Live interview session |
| `/history.html` | Past interview history |
| `/analytics.html` | Performance analytics |
| `/coach.html` | AI coaching feedback |
| `/settings.html` | User settings |


