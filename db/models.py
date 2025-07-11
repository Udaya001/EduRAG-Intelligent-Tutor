from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, Boolean
from db.database import Base
from datetime import datetime

class SessionModel(Base):
    __tablename__ = "sessions"
    id = Column(String, primary_key=True)  
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

class ContentModel(Base):
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, index=True)
    title = Column(String)
    grade = Column(String)
    content = Column(Text)
    metadata_ = Column("metadata", JSON)  

class ChatMemoryModel(Base):
    __tablename__ = "chat_memory"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True, nullable=False)
    role = Column(String, nullable=False)  # 'human' or 'ai'
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

class FeedbackModel(Base):
    __tablename__ = "feedback"


    id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)  
    comment = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)  

class LogModel(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String)
    answer = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow) 
