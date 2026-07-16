from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.services import payment_service
from app.services.validate_jwt import verify_clerk_session

router = APIRouter(prefix="/api/payments", tags=["payments"])

class VerifyPaymentRequest(BaseModel):
    order_id: str
    payment_id: str
    signature: str

@router.post("/create-order")
def create_order(db: Session = Depends(get_db), clerk_user_id: str = Depends(verify_clerk_session)):
    try:
        return payment_service.create_order(db, clerk_user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/verify")
def verify_payment(
    payload: VerifyPaymentRequest,
    db: Session = Depends(get_db),
    clerk_user_id: str = Depends(verify_clerk_session),
):
    try:
        payment_service.verify_and_upgrade(
            db, clerk_user_id, payload.order_id, payload.payment_id, payload.signature
        )
        return {"status": "success", "plan": "PRO"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))