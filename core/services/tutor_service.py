from core.rag.rag import get_rag_chain
from core.services.log_service import LogService
from utils.logger import logger
from db.memory import DatabaseConversationMemory
from db.database import get_db 

class TutorService:
    def __init__(self, db_session_factory):
        self.db_session_factory = db_session_factory

    def generate_answer(self, question, session_id, persona="default"):
        db = self.db_session_factory()
        try:
            memory = DatabaseConversationMemory(
                session_id=session_id,
                db=db,
                return_messages=True
            )
            
            # Get messages directly from memory
            chat_history = memory.load_memory_variables({})["chat_history"]
            
            chain = get_rag_chain(persona=persona, memory=memory)
            
            result = chain.invoke({
                "input": question,
                "chat_history": chat_history
            })
            
            if "answer" not in result:
                logger.error(f"'answer' key not in result: {result}")
                return "Sorry, no answer could be generated."
                
            LogService().log_question_answer(question, result["answer"])
            return result["answer"]
        except Exception as e:
            db.rollback()
            logger.error(f"Error generating answer: {e}")
            return "Sorry, I couldn't process your question right now."
        finally:
            db.close()