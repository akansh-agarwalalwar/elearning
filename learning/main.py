from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from config.connection import init_db
from middleware.logging_middleware import LoggingMiddleware
from middleware.error_handler import setup_error_handlers
from config.logging_config import log_system_event
from pathlib import Path
from routers.auth.admin import router as admin_router
from routers.auth.auth import router as auth_router
from routers.instructor.instructor import router as instructor_router
from routers.admin.privileges import router as privilege_router
from routers.course.courses import router as course_router

app = FastAPI(
    title="E-Learning API",
    description="A comprehensive e-learning platform API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add logging middleware
app.add_middleware(LoggingMiddleware)

# Setup error handlers
setup_error_handlers(app)

# Mount static files for serving banner images
uploads_path = Path("uploads")
if uploads_path.exists():
    app.mount("/static", StaticFiles(directory="uploads"), name="static")

@app.on_event("startup")
def startup():
    try:
        log_system_event("STARTUP", "Application starting up")
        init_db()
        log_system_event("STARTUP", "Database initialized successfully")
    except Exception as e:
        log_system_event("STARTUP_ERROR", f"Failed to start application: {str(e)}")
        raise

@app.on_event("shutdown")
def shutdown():
    try:
        log_system_event("SHUTDOWN", "Application shutting down")
        log_system_event("SHUTDOWN", "Database connection closed")
    except Exception as e:
        log_system_event("SHUTDOWN_ERROR", f"Error during shutdown: {str(e)}")

# Import routers after database setup
app.include_router(admin_router, prefix='/api/v1/admin', tags=["Admin routes"])
app.include_router(auth_router, prefix='/api/v1/auth', tags=["Authentication routes"])
app.include_router(instructor_router, prefix='/api/v1/instructor', tags=["Instructor routes"])
app.include_router(privilege_router, prefix='/api/v1', tags=["Privilege Management"])
app.include_router(course_router, prefix='/api/v1', tags=["Course Management"])

@app.get("/")
async def getapi():
    log_system_event("HEALTH_CHECK", "Root endpoint accessed")
    return {"message":" Welcome to the E-Learning API 🎈 "}
