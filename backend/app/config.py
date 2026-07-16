import os
from decimal import Decimal

RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")

if not RAZORPAY_KEY_ID or not RAZORPAY_KEY_SECRET:
    raise ValueError("RAZORPAY_KEY_ID or RAZORPAY_KEY_SECRET environment variable is missing")

PRO_PLAN_AMOUNT_RUPEES = Decimal("499.00")  # change to your actual price