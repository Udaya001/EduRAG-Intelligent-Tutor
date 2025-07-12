from db.models import LogModel
from db.database import SessionLocal
from typing import Optional

class LogService:
    def log_question_answer(self, question: str, answer: str, session_id: Optional[str] = None):
        db = SessionLocal()
        try:
            log_entry = LogModel(
                question=question,
                answer=answer,
                session_id=session_id
            )
            db.add(log_entry)
            db.commit()
        finally:
            db.close()

    def get_logs(self, session_id: Optional[str] = None):
        db = SessionLocal()
        try:
            query = db.query(LogModel).filter(LogModel.timestamp.isnot(None))
            if session_id:
                query = query.filter(LogModel.session_id == session_id)
            return query.order_by(LogModel.timestamp).all()
        finally:
            db.close()
