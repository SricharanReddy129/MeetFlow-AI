import io
import json
from fastapi import UploadFile
from pypdf import PdfReader
import docx
from langchain_groq import ChatGroq
from sqlalchemy.orm import Session
from app import config
from app.repositories import meeting_repo
from app.models.models import PlanEnum


class DailyLimitExceededError(Exception):
    pass


class WordLimitExceededError(Exception):
    pass


class UnsupportedFileTypeError(Exception):
    pass


llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=config.GROQ_API_KEY, temperature=0.3)


def extract_text(file: UploadFile) -> str:
    filename = (file.filename or "").lower()
    content = file.file.read()

    if filename.endswith(".txt"):
        return content.decode("utf-8", errors="ignore")
    elif filename.endswith(".pdf"):
        reader = PdfReader(io.BytesIO(content))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    elif filename.endswith(".docx"):
        doc = docx.Document(io.BytesIO(content))
        return "\n".join(p.text for p in doc.paragraphs)
    else:
        raise UnsupportedFileTypeError("Only PDF, TXT, and DOCX files are supported.")


def summarize_transcript(transcript: str) -> dict:
    prompt = f"""You are a meeting summarization assistant. Given the meeting transcript below, respond with ONLY a valid JSON object (no markdown, no code fences, no extra text) in this exact structure:
{{
  "title": "short descriptive meeting title",
  "summary": "concise executive summary of the meeting, 3-5 sentences",
  "action_items": ["action item 1", "action item 2"]
}}

Transcript:
{transcript}
"""
    response = llm.invoke(prompt)
    raw = response.content.strip()

    if raw.startswith("```"):
        raw = raw.strip("`")
        if raw.startswith("json"):
            raw = raw[4:].strip()

    return json.loads(raw)


def create_meeting(db: Session, clerk_user_id: str, file: UploadFile) -> "Meetings":
    user = meeting_repo.get_user_by_clerk_id(db, clerk_user_id)
    if not user:
        raise ValueError("User not found")

    meeting_repo.reset_daily_usage_if_new_day(db, user)

    if user.plan == PlanEnum.FREE and user.daily_usage >= config.FREE_DAILY_LIMIT:
        raise DailyLimitExceededError(
            "Daily summary limit reached. Upgrade to Pro for unlimited summaries."
        )

    transcript = extract_text(file)
    word_count = len(transcript.split())

    if user.plan == PlanEnum.FREE and word_count > config.FREE_WORD_LIMIT:
        raise WordLimitExceededError(
            f"Transcript exceeds the {config.FREE_WORD_LIMIT}-word limit for the Free plan."
        )

    if user.plan == PlanEnum.FREE:
        existing_count = meeting_repo.count_user_meetings(db, user.id)
        if existing_count >= config.FREE_MEETING_CAP:
            oldest = meeting_repo.get_oldest_meeting(db, user.id)
            if oldest:
                meeting_repo.delete_meeting(db, oldest)

    result = summarize_transcript(transcript)

    meeting = meeting_repo.create_meeting(
        db,
        user.id,
        title=result["title"],
        transcript=transcript,
        summary=result["summary"],
        action_items={"items": result["action_items"]},
        word_count=word_count,
    )

    meeting_repo.increment_daily_usage(db, user)

    return meeting

def list_meetings(db: Session, clerk_user_id: str) -> list:
    user = meeting_repo.get_user_by_clerk_id(db, clerk_user_id)
    if not user:
        raise ValueError("User not found")
    return meeting_repo.get_meetings_by_user(db, user.id)


def get_meeting(db: Session, clerk_user_id: str, meeting_id: str):
    user = meeting_repo.get_user_by_clerk_id(db, clerk_user_id)
    if not user:
        raise ValueError("User not found")

    meeting = meeting_repo.get_meeting_by_id(db, meeting_id, user.id)
    if not meeting:
        raise ValueError("Meeting not found")
    return meeting


def delete_meeting_by_id(db: Session, clerk_user_id: str, meeting_id: str) -> None:
    user = meeting_repo.get_user_by_clerk_id(db, clerk_user_id)
    if not user:
        raise ValueError("User not found")

    meeting = meeting_repo.get_meeting_by_id(db, meeting_id, user.id)
    if not meeting:
        raise ValueError("Meeting not found")

    meeting_repo.delete_meeting(db, meeting)