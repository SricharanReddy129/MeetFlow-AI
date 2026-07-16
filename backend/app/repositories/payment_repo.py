from decimal import Decimal
from sqlalchemy.orm import Session
from app.models.models import Payments, Users, PaymentStatusEnum, PlanEnum, CurrencyEnum

def get_user_by_clerk_id(db: Session, clerk_user_id: str) -> Users | None:
    return db.query(Users).filter(Users.clerk_user_id == clerk_user_id).first()

def create_payment_record(db: Session, user_id, order_id: str, amount: Decimal) -> Payments:
    payment = Payments(
        user_id=user_id,
        razorpay_order_id=order_id,
        amount=amount,
        currency=CurrencyEnum.INR,
        status=PaymentStatusEnum.CREATED,
        plan=PlanEnum.PRO,
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment

def mark_payment_paid(db: Session, order_id: str, payment_id: str) -> Payments | None:
    payment = db.query(Payments).filter(Payments.razorpay_order_id == order_id).first()
    if not payment:
        return None
    payment.status = PaymentStatusEnum.PAID
    payment.razorpay_payment_id = payment_id
    payment.paid_at = datetime.utcnow()
    db.commit()
    return payment

def upgrade_user_to_pro(db: Session, user_id) -> Users | None:
    user = db.query(Users).filter(Users.id == user_id).first()
    if user:
        user.plan = PlanEnum.PRO
        db.commit()
    return user