from fastapi import APIRouter, Depends, HTTPException, Query
from core.services.content_service import ContentService
from core.services.feedback_service import FeedbackService
from core.services.tutor_service import TutorService
from core.services.log_service import LogService
from core.schemas.request import UploadContentRequest, AskQuestionRequest,FeedbackRequest
from core.schemas.response import UploadContentResponse, AnswerResponse, MetricsResponse, TopicListResponse, FeedbackResponse,QALogListResponse
from utils.logger import logger
from sqlalchemy.orm import Session
from db.models import SessionModel
from db.models import ChatMemoryModel
from db.database import get_db
import uuid


router = APIRouter()

@router.post("/start-session")
async def start_session(db: Session = Depends(get_db)):
    session_id = str(uuid.uuid4())
    db.add(SessionModel(id=session_id))
    db.commit()
    return {"session_id": session_id}

@router.post("/upload-content", response_model=UploadContentResponse)
async def upload_content(
    request: UploadContentRequest,
    service: ContentService = Depends()
):
    result = service.upload_content(request)
    return result


@router.post("/ask", response_model=AnswerResponse)
async def ask_question(
    request: AskQuestionRequest,
    session_id: str = Query(..., description="Unique session ID"),
    persona: str = Query("default"),
    db: Session = Depends(get_db),
):
    session_exists = db.query(SessionModel).filter_by(id=session_id).first()
    if not session_exists:
        raise HTTPException(status_code=400, detail="Invalid session ID")

    service = TutorService(lambda: db)
    answer = service.generate_answer(request.question, session_id=session_id, persona=persona)
    return {"answer": answer}



@router.get("/topics", response_model=TopicListResponse)
async def get_topics(
    grade: str = Query(None, description="Filter by grade"),
    topic: str = Query(None, description="Filter by topic"),
    service: ContentService = Depends()
):
    results = service.get_filtered_topics(grade=grade, topic=topic)
    return {"topics": results}


@router.get("/metrics",response_model=MetricsResponse)
async def get_metrics(service: ContentService = Depends()):
    metrics = service.get_system_metrics()
    return metrics

@router.post("/feedback",response_model=FeedbackResponse)
async def submit_feedback(
    request: FeedbackRequest,
    service: FeedbackService = Depends()
):
    result = service.submit_feedback(request.question, request.answer, request.rating, request.comment)
    return result

@router.get("/logs", response_model=QALogListResponse)
def get_logs(service: LogService = Depends()):
    logs = service.get_logs()
    return {"logs": logs}

