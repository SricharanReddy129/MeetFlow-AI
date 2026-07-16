import razorpay
import hmac
import hashlib
from sqlalchemy.orm import Session
from app import config
from app.repositories import payment_repo

client = razorpay.Client(auth=(config.RAZORPAY_KEY_ID, config.RAZORPAY_KEY_SECRET))

def create_order(db: Session, clerk_user_id: str) -> dict:
    user = payment_repo.get_user_by_clerk_id(db, clerk_user_id)
    if not user:
        raise ValueError("User not found")

    amount_paise = int(config.PRO_PLAN_AMOUNT_RUPEES * 100)

    order = client.order.create({
        "amount": amount_paise,
        "currency": "INR",
        "payment_capture": 1,
    })

    payment_repo.create_payment_record(db, user.id, order["id"], config.PRO_PLAN_AMOUNT_RUPEES)

    return {
        "order_id": order["id"],
        "amount": amount_paise,
        "currency": "INR",
        "key_id": config.RAZORPAY_KEY_ID,
    }

def verify_and_upgrade(db: Session, clerk_user_id: str, order_id: str, payment_id: str, signature: str) -> None:
    body = f"{order_id}|{payment_id}"
    expected_signature = hmac.new(
        config.RAZORPAY_KEY_SECRET.encode(),
        body.encode(),
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(expected_signature, signature):
        raise ValueError("Invalid payment signature")

    user = payment_repo.get_user_by_clerk_id(db, clerk_user_id)
    if not user:
        raise ValueError("User not found")

    payment_repo.mark_payment_paid(db, order_id, payment_id)
    payment_repo.upgrade_user_to_pro(db, user.id)