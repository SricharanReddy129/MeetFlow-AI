from sqlalchemy.orm import Session
from models.models import Users

class UserRepository:
    @staticmethod
    def get_by_clerk_id(db: Session, clerk_id: str) -> Users | None:
        return db.query(Users).filter(Users.clerk_user_id == clerk_id).first()