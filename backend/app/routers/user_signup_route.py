# user_signup_route.py

import os
import logging
from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlalchemy.orm import Session
from svix.webhooks import Webhook
from svix.exceptions import WebhookVerificationError

# Adjust these imports to match your actual project structure
from database import get_db 
from services.user_signup_service import UserSignUpService

logger = logging.getLogger(__name__)

# The prefix groups this under your application's onboarding flow
router = APIRouter(prefix="/api/onboarding", tags=["User Onboarding"])

# The endpoint describes the specific action
@router.post("/clerk-sync", status_code=status.HTTP_200_OK)
async def sync_clerk_signup(request: Request, db: Session = Depends(get_db)):
    """
    Endpoint for Clerk webhooks. 
    Verifies the svix signature and processes the user.created event.
    """
    clerk_secret = os.getenv("CLERK_SECRET_KEY")
    if not clerk_secret:
        logger.error("CLERK_SECRET_KEY is missing from environment variables.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Server configuration error."
        )

    # 1. Extract Svix headers
    headers = request.headers
    svix_id = headers.get("svix-id")
    svix_timestamp = headers.get("svix-timestamp")
    svix_signature = headers.get("svix-signature")

    if not svix_id or not svix_timestamp or not svix_signature:
        logger.warning("Incoming webhook missing Svix headers.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Missing required Svix headers."
        )

    # 2. Get raw request body
    payload = await request.body()
    wh = Webhook(clerk_secret)

    # 3. Verify the payload against the signature
    try:
        # We pass headers as a dict to satisfy the svix verification method
        event = wh.verify(payload, dict(headers))
    except WebhookVerificationError as e:
        logger.error(f"Webhook signature verification failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid webhook signature."
        )

    # 4. Pass the verified payload to the Service Layer
    try:
        result = UserSignUpService.process_clerk_webhook(db, event)
        return result  # Returns the success/ignored dict with 200 OK
        
    except ValueError as e:
        # Catches our strict validation errors (missing name, email, or clerk_id)
        logger.error(f"Validation error during user sync: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail=str(e)
        )
        
    except RuntimeError as e:
        # Catches our database insertion failures
        logger.error(f"Database error during user sync: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Failed to sync user to database."
        )