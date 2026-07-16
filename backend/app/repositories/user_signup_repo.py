# user_signup_repo.py

from sqlalchemy.orm import Session
from models.models import Users, PlanEnum

class UserSignUpRepository:
    @staticmethod
    def get_user_by_clerk_id(db: Session, clerk_id: str) -> Users | None:
        """
        Fetches a user from the database strictly using their Clerk User ID.
        Used for idempotency checks during sign-up and authentication during logins.
        """
        return db.query(Users).filter(Users.clerk_user_id == clerk_id).first()

    @staticmethod
    def create_user(db: Session, clerk_id: str, email: str, name: str) -> Users:
        """
        Inserts a new user record into the users table.
        The internal database UUID 'id' and default metrics are handled automatically.
        """
        new_user = Users(
            clerk_user_id=clerk_id,
            email=email,
            name=name,
            plan=PlanEnum.FREE,        # Explicit baseline alignment with your migration default
            daily_usage=0             # Starting baseline metrics
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)  # Refreshes the instance to capture the auto-generated Supabase UUID
        return new_user