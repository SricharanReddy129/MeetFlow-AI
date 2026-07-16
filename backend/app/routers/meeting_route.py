from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import meeting_service
from app.services.validate_jwt import verify_clerk_session

router = APIRouter(prefix="/api/meetings", tags=["meetings"])


@router.post("/new")
def new_meeting(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    clerk_user_id: str = Depends(verify_clerk_session),
):
    try:
        meeting = meeting_service.create_meeting(db, clerk_user_id, file)
        return {
            "id": str(meeting.id),
            "title": meeting.title,
            "summary": meeting.summary,
            "action_items": meeting.action_items.get("items", []),
            "transcript_word_count": meeting.transcript_word_count,
            "created_at": meeting.created_at.isoformat(),
        }
    except meeting_service.DailyLimitExceededError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except meeting_service.WordLimitExceededError as e:
        raise HTTPException(status_code=413, detail=str(e))
    except meeting_service.UnsupportedFileTypeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))