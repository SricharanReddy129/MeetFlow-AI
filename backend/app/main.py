from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# signup routes
from routers import user_signup_route, user_dashboard_route, payment_route

# ro test db connection
from sqlalchemy import inspect

# testing models
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db


# 1. Initialize the FastAPI application instance
app = FastAPI(
    title="MeetFlow AI API",
    description="Backend API service for MeetFlow AI SaaS application",
    version="1.0.0"
)

# 2. Configure allowed origins for CORS
# Add both your local development URL and prepare for your eventual Vercel deployment URL
origins = [
    "http://localhost:3000",
    "https://your-vercel-domain.vercel.app",
]

# 3. Add CORS middleware to the application instance
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all standard HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all standard request headers
)

# 4. Include the user signup router for handling Clerk webhooks
app.include_router(user_signup_route.router)
app.include_router(user_dashboard_route.router)
app.include_router(payment_route.router)

# 4. Define a basic root health check endpoint to verify the server is live
@app.get("/", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "message": "MeetFlow AI API is running smoothly."
    }


# Dummy test route to verify SQLAlchemy models against Supabase
@app.get("/test-db-connection", tags=["Test"])
def test_db_connection(db: Session = Depends(get_db)):
    try:
        # Create an inspector bound to the current session's engine
        inspector = inspect(db.get_bind())
        
        # Fetch the list of table names
        table_names = inspector.get_table_names()
        
        return {
            "status": "success",
            "message": "Successfully connected to the database!",
            "tables_found": table_names
        }
    except Exception as e:
        return {
            "status": "error",
            "message": "Could not connect or reflect tables.",
            "details": str(e)
        }