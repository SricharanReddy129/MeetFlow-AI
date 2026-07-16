from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from services.validate_jwt import verify_clerk_session
from services.user_dashboard_service import get_user_dashboard_logic

router = APIRouter()

@router.get("/api/users/me")
def get_dashboard(
    clerk_id: str = Depends(verify_clerk_session),
    db: Session = Depends(get_db)
):
    data = get_user_dashboard_logic(db, clerk_id)
    
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
        
    return data