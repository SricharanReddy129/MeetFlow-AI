import datetime
from sqlalchemy.orm import Session
from sqlalchemy import asc
from app.models.models import Meetings, Users

def get_user_by_clerk_id(db: Session, clerk_user_id: str) -> Users | None:
    return db.query(Users).filter(Users.clerk_user_id == clerk_user_id).first()

def reset_daily_usage_if_new_day(db: Session, user: Users) -> None:
    today = datetime.date.today()
    if user.last_usage_date != today:
        user.daily_usage = 0
        user.last_usage_date = today
        db.commit()

def increment_daily_usage(db: Session, user: Users) -> None:
    user.daily_usage += 1
    db.commit()

def count_user_meetings(db: Session, user_id) -> int:
    return db.query(Meetings).filter(Meetings.user_id == user_id).count()

def get_oldest_meeting(db: Session, user_id) -> Meetings | None:
    return (
        db.query(Meetings)
        .filter(Meetings.user_id == user_id)
        .order_by(asc(Meetings.created_at))
        .first()
    )

def delete_meeting(db: Session, meeting: Meetings) -> None:
    db.delete(meeting)
    db.commit()

def create_meeting(
    db: Session,
    user_id,
    title: str,
    transcript: str,
    summary: str,
    action_items: dict,
    word_count: int,
) -> Meetings:
    meeting = Meetings(
        user_id=user_id,
        title=title,
        transcript=transcript,
        summary=summary,
        action_items=action_items,
        transcript_word_count=word_count,
    )
    db.add(meeting)
    db.commit()
    db.refresh(meeting)
    return meeting