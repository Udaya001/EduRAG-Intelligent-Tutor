from langchain.memory import ConversationBufferMemory
from core.rag.rag import get_rag_chain
from utils.logger import logger

class TutorService:
    def generate_answer(self, question, persona="default"):
        logger.info(f"Generating answer for persona: {persona}")

        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, output_key="answer")

        chain = get_rag_chain(persona=persona, memory=memory)

        try:
            result = chain.invoke({"question": question})
        except Exception as e:
            logger.error(f"Chain invocation failed: {e}")
            raise
        logger.info(f"Chain result: {result}")


        return result["answer"]
