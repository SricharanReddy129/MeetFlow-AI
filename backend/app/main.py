from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth_middleware import ClerkAuthMiddleware   # NEW

from routers import user_signup_route, user_dashboard_route, payment_route, meeting_route

from sqlalchemy import inspect

from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db


app = FastAPI(
    title="MeetFlow AI API",
    description="Backend API service for MeetFlow AI SaaS application",
    version="1.0.0"
)

origins = [
    "http://localhost:3000",
    "https://meet-flow-ai-chi.vercel.app",
]

# NEW: auth middleware added first, so CORS (added next) wraps it and stays outermost
app.add_middleware(ClerkAuthMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_signup_route.router)
app.include_router(user_dashboard_route.router)
app.include_router(payment_route.router)
app.include_router(meeting_route.router)

@app.get("/", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "message": "MeetFlow AI API is running smoothly."
    }