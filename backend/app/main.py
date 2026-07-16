from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# signup routes
from routers import user_signup_route

# testing models
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
from models.models import Users, Meetings, Payments


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
    # "https://your-frontend-domain.vercel.app", # Uncomment and update during frontend deployment
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

# 4. Define a basic root health check endpoint to verify the server is live
@app.get("/", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "message": "MeetFlow AI API is running smoothly."
    }


# Dummy test route to verify SQLAlchemy models against Supabase
@app.get("/test-models", tags=["Test"])
def test_models(db: Session = Depends(get_db)):
    try:
        # Attempt to query the first record from each table to verify schema mapping
        user = db.query(Users).first()
        meeting = db.query(Meetings).first()
        payment = db.query(Payments).first()

        return {
            "status": "success",
            "message": "Models are perfectly mapped to Supabase!",
            "data": {
                "users_table_empty": user is None,
                "meetings_table_empty": meeting is None,
                "payments_table_empty": payment is None
            }
        }
    except Exception as e:
        # If there is a schema mismatch, SQLAlchemy will throw an error here
        return {
            "status": "error",
            "message": "Schema mismatch detected.",
            "details": str(e)
        }