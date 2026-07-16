# user_signup_service.py

from sqlalchemy.orm import Session
from repositories.user_signup_repo import UserSignUpRepository
import logging

logger = logging.getLogger(__name__)

class UserSignUpService:
    @staticmethod
    def process_clerk_webhook(db: Session, event: dict):
        """
        Parses the raw Clerk webhook payload and coordinates the database insertion.
        Ensures idempotency by checking if the user already exists.
        Enforces strict data validation for all required fields.
        """
        event_type = event.get("type")
        
        # We only care about user registration events
        if event_type != "user.created":
            return {"status": "ignored", "reason": "Not a user.created event"}

        data = event.get("data", {})
        
        # 1. Extract Clerk ID strictly
        clerk_id = data.get("id")
        if not clerk_id:
            logger.error("Clerk Webhook Missing User ID")
            raise ValueError("Missing required Clerk ID")
            
        # 2. Extract Email strictly
        email_addresses = data.get("email_addresses", [])
        email = email_addresses[0].get("email_address") if email_addresses else ""
        if not email:
            logger.error(f"Clerk Webhook Missing Email for User ID: {clerk_id}")
            raise ValueError("Missing required email address")
        
        # 3. Extract Name strictly (rejecting empty values entirely)
        first_name = data.get("first_name", "").strip()
        last_name = data.get("last_name", "").strip()
        
        # Combine and ensure neither part was just whitespace
        if not first_name or not last_name:
            logger.error(f"Clerk Webhook Name validation failed for User ID: {clerk_id}. First: '{first_name}', Last: '{last_name}'")
            raise ValueError("First and Last name are both required.")
            
        name = f"{first_name} {last_name}"
        
        if not name:
            logger.error(f"Clerk Webhook Missing Name for User ID: {clerk_id}")
            raise ValueError("Missing required name fields")

        # 4. Check Idempotency (Does the user already exist from a webhook retry?)
        existing_user = UserSignUpRepository.get_user_by_clerk_id(db, clerk_id)
        if existing_user:
            logger.info(f"User {clerk_id} already exists. Skipping insertion.")
            return {"status": "success", "message": "User already exists", "user_id": existing_user.id}
            
        # 5. Insert New User
        try:
            new_user = UserSignUpRepository.create_user(db, clerk_id, email, name)
            logger.info(f"Successfully created user {clerk_id} in database.")
            return {"status": "success", "message": "User created", "user_id": new_user.id}
        except Exception as e:
            logger.error(f"Database insertion failed for {clerk_id}: {str(e)}")
            # Raise exception so the router knows the transaction ultimately failed
            raise RuntimeError(f"Database insertion failed: {str(e)}") from e