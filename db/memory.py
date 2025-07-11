from langchain_core.memory import BaseMemory
from langchain_core.messages import AIMessage, HumanMessage
from pydantic import Field
from db.models import ChatMemoryModel
from sqlalchemy.orm import Session
from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass
class ChatMemory:
    messages: List[Any]

class DatabaseConversationMemory(BaseMemory):
    session_id: str = Field(..., description="Unique session identifier")
    db: Session = Field(..., description="Database session")
    return_messages: bool = Field(default=True)
    
    class Config:
        arbitrary_types_allowed = True

    @property
    def memory_variables(self) -> List[str]:
        return ["chat_history"]

    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        return {"chat_history": self.get_messages()}

    def get_messages(self) -> List[Any]:
        """Helper method to get messages from database"""
        rows = self.db.query(ChatMemoryModel).filter_by(
            session_id=self.session_id
        ).order_by(ChatMemoryModel.timestamp).all()

        messages = []
        for row in rows:
            if row.role == "human":
                messages.append(HumanMessage(content=row.content))
            elif row.role == "ai":
                messages.append(AIMessage(content=row.content))
        return messages

    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
        if "input" not in inputs or "answer" not in outputs:
            return

        self.db.add_all([
            ChatMemoryModel(
                session_id=self.session_id,
                role="human",
                content=inputs["input"]
            ),
            ChatMemoryModel(
                session_id=self.session_id,
                role="ai",
                content=outputs["answer"]
            )
        ])
        self.db.commit()

    def clear(self) -> None:
        self.db.query(ChatMemoryModel).filter_by(
            session_id=self.session_id
        ).delete()
        self.db.commit()