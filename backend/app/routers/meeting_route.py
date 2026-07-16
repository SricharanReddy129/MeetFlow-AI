from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import meeting_service
from app.services.validate_jwt import verify_clerk_session
from app.services.validate_jwt import get_current_user
from fastapi.responses import Response

router = APIRouter(prefix="/api/meetings", tags=["meetings"])


@router.post("/new")
def new_meeting(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    clerk_user_id: str = Depends(get_current_user),
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
    
@router.get("")
def get_meetings(
    db: Session = Depends(get_db),
    clerk_user_id: str = Depends(get_current_user),
):
    try:
        meetings = meeting_service.list_meetings(db, clerk_user_id)
        return [
            {
                "id": str(m.id),
                "title": m.title,
                "summary": m.summary,
                "action_items": m.action_items.get("items", []),
                "transcript_word_count": m.transcript_word_count,
                "created_at": m.created_at.isoformat(),
            }
            for m in meetings
        ]
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{meeting_id}")
def get_meeting(
    meeting_id: str,
    db: Session = Depends(get_db),
    clerk_user_id: str = Depends(get_current_user),
):
    try:
        meeting = meeting_service.get_meeting(db, clerk_user_id, meeting_id)
        return {
            "id": str(meeting.id),
            "title": meeting.title,
            "summary": meeting.summary,
            "action_items": meeting.action_items.get("items", []),
            "transcript_word_count": meeting.transcript_word_count,
            "created_at": meeting.created_at.isoformat(),
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{meeting_id}")
def delete_meeting(
    meeting_id: str,
    db: Session = Depends(get_db),
    clerk_user_id: str = Depends(get_current_user),
):
    try:
        meeting_service.delete_meeting_by_id(db, clerk_user_id, meeting_id)
        return {"status": "deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    
@router.get("/{meeting_id}/pdf")
def download_meeting_pdf(
    meeting_id: str,
    db: Session = Depends(get_db),
    clerk_user_id: str = Depends(get_current_user),
):
    try:
        meeting = meeting_service.get_meeting(db, clerk_user_id, meeting_id)
        pdf_bytes = meeting_service.generate_meeting_pdf(meeting)
        filename = f"{meeting.title[:50].strip().replace(' ', '_') or 'meeting'}.pdf"
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))