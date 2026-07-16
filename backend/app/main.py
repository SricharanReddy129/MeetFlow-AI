from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


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

# 4. Define a basic root health check endpoint to verify the server is live
@app.get("/", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "message": "MeetFlow AI API is running smoothly."
    }