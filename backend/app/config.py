import os
from decimal import Decimal

RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")

if not RAZORPAY_KEY_ID or not RAZORPAY_KEY_SECRET:
    raise ValueError("RAZORPAY_KEY_ID or RAZORPAY_KEY_SECRET environment variable is missing")

PRO_PLAN_AMOUNT_RUPEES = Decimal("499.00")  # change to your actual price

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is missing")

FREE_DAILY_LIMIT = 3
FREE_WORD_LIMIT = 3000
FREE_MEETING_CAP = 10