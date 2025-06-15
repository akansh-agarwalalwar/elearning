from fastapi import FastAPI
from database.db import init_db, close_db

app = FastAPI()

@app.on_event("startup")
async def startup():
    await init_db()

@app.on_event("shutdown")
async def shutdown():
    await close_db()

# Import routers after database setup
from routers.auth.admin import router as admin_router
from routers.auth.auth import router as auth_router

app.include_router(admin_router, prefix='/api/v1/admin', tags=["Admin routes"])
app.include_router(auth_router, prefix='/api/v1/auth', tags=["Authentication routes"])

@app.get("/")
async def getapi():
    return {"message":" Welcome to the E-Learning API 🎈 "}
