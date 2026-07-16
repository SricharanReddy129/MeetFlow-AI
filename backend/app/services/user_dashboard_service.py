from sqlalchemy.orm import Session
from repositories.user_dashboard_repo import UserRepository

def get_user_dashboard_logic(db: Session, clerk_id: str) -> dict | None:
    user = UserRepository.get_by_clerk_id(db, clerk_id)
    
    if not user:
        return None

    # Business Logic: Prepare data structure based on Plan
    plan_value = user.plan.value if hasattr(user.plan, 'value') else user.plan
    
    payload = {
        "name": user.name,
        "plan": plan_value,
    }

    if plan_value == "FREE":
        payload["daily_usage"] = user.daily_usage
        # We can calculate remaining usage here if the limit is defined globally
        payload["remaining_attempts"] = 50 - user.daily_usage 

    return payload