from core.rag.rag import get_rag_chain
from core.services.log_service import LogService
from utils.logger import logger
from db.memory import DatabaseConversationMemory
from db.database import get_db
from langchain_core.messages import HumanMessage, AIMessage 

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
            
            # Load chat history from memory
            chat_history = memory.load_memory_variables({})["chat_history"]
            
            # Pass the memory object to the RAG chain
            chain = get_rag_chain(persona=persona, memory=memory)
            
            # Invoke the chain with the current input and loaded chat history
            result = chain.invoke({
                "input": question,
                "chat_history": chat_history # Ensure chat_history is passed here
            })
            
            if "answer" not in result:
                logger.error(f"'answer' key not in result: {result}")
                return "Sorry, no answer could be generated."
            
            answer = result["answer"]

            # Explicitly save the current turn (human question and AI answer) to memory
            # The save_context method in DatabaseConversationMemory will handle DB persistence
            memory.save_context(
                inputs={"input": question},
                outputs={"answer": answer}
            )

            # Log the question and answer for general logs (separate from chat memory)
            LogService().log_question_answer(question, answer, session_id=session_id)
            
            return answer
        except Exception as e:
            db.rollback()
            logger.error(f"Error generating answer: {e}")
            return "Sorry, I couldn't process your question right now."
        finally:
            db.close()