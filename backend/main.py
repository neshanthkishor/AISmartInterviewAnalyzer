from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from backend.routes.auth_routes import router as auth_router
from backend.routes.interview_routes import router as interview_router


# ============================================================
# APPLICATION
# ============================================================

app = FastAPI(
    title="AI Smart Interview Analyzer",
    description=(
        "AI-powered interview practice, analysis, "
        "performance tracking and career intelligence platform."
    ),
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"


# ============================================================
# API ROUTES
# ============================================================

app.include_router(auth_router)
app.include_router(interview_router)


# ============================================================
# FRONTEND STATIC FILES
# ============================================================

if FRONTEND_DIR.exists():

    app.mount(
        "/frontend",
        StaticFiles(
            directory=str(FRONTEND_DIR)
        ),
        name="frontend"
    )


# ============================================================
# HELPER
# ============================================================

def serve_page(filename: str):

    file_path = FRONTEND_DIR / filename

    if file_path.exists():

        return FileResponse(
            str(file_path)
        )

    return {
        "status": "error",
        "message": f"{filename} not found."
    }


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {
        "status": "online",
        "application": "AI Smart Interview Analyzer",
        "version": "1.0.0",
        "message": "Backend is running successfully."
    }


# ============================================================
# LOGIN
# ============================================================

@app.get("/login.html")
def login_page():

    return serve_page("login.html")


# ============================================================
# REGISTER
# ============================================================

@app.get("/register.html")
def register_page():

    return serve_page("register.html")


# ============================================================
# APPLICATION
# ============================================================

@app.get("/app")
def application_page():

    return serve_page("login.html")


# ============================================================
# DASHBOARD
# ============================================================

@app.get("/dashboard")
def dashboard_page():

    return serve_page("dashboard.html")


@app.get("/dashboard.html")
def dashboard_html_page():

    return serve_page("dashboard.html")


# ============================================================
# NEW INTERVIEW
# ============================================================

@app.get("/interview")
def interview_page():

    return serve_page("interview.html")


@app.get("/interview.html")
def interview_html_page():

    return serve_page("interview.html")


# ============================================================
# INTERVIEW ROOM
# ============================================================

@app.get("/interview-room")
def interview_room_page():

    return serve_page("interview-room.html")


@app.get("/interview-room.html")
def interview_room_html_page():

    return serve_page("interview-room.html")


# ============================================================
# INTERVIEW HISTORY
# ============================================================

@app.get("/history")
def history_page():

    return serve_page("history.html")


@app.get("/history.html")
def history_html_page():

    return serve_page("history.html")


# ============================================================
# ANALYTICS
# ============================================================

@app.get("/analytics")
def analytics_page():

    return serve_page("analytics.html")


@app.get("/analytics.html")
def analytics_html_page():

    return serve_page("analytics.html")


# ============================================================
# AI COACH
# ============================================================

@app.get("/coach")
def coach_page():

    return serve_page("coach.html")


@app.get("/coach.html")
def coach_html_page():

    return serve_page("coach.html")


# ============================================================
# SETTINGS
# ============================================================

@app.get("/settings")
def settings_page():

    return serve_page("settings.html")


@app.get("/settings.html")
def settings_html_page():

    return serve_page("settings.html")


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "AI Smart Interview Analyzer",
        "version": "1.0.0"
    }


# ============================================================
# API INFORMATION
# ============================================================

@app.get("/api")
def api_information():

    return {
        "application": "AI Smart Interview Analyzer",
        "status": "online",
        "version": "1.0.0",

        "pages": {
            "login": "/login.html",
            "register": "/register.html",
            "dashboard": "/dashboard.html",
            "new_interview": "/interview.html",
            "interview_room": "/interview-room.html",
            "history": "/history.html",
            "analytics": "/analytics.html",
            "coach": "/coach.html",
            "settings": "/settings.html"
        },

        "modules": [
            "Authentication",
            "AI Interview Engine",
            "Question Generation",
            "Answer Evaluation",
            "Interview History",
            "Performance Analytics",
            "AI Coach",
            "User Settings"
        ]
    }


# ============================================================
# STARTUP MESSAGE
# ============================================================

@app.on_event("startup")
def startup_message():

    print("")
    print("=" * 60)
    print("       INTERVIEWIQ AI SMART INTERVIEW ANALYZER")
    print("=" * 60)
    print("Backend status : ONLINE")
    print(f"Frontend       : {FRONTEND_DIR}")
    print("")
    print("Available pages:")
    print("  /login.html")
    print("  /register.html")
    print("  /dashboard.html")
    print("  /interview.html")
    print("  /interview-room.html")
    print("  /history.html")
    print("  /analytics.html")
    print("  /coach.html")
    print("  /settings.html")
    print("=" * 60)
    print("")