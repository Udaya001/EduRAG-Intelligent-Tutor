from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from .llm import get_llm
from .vector_store import get_vectorstore
from .prompts import DEFAULT_PROMPT, PERSONA_PROMPTS
from utils.logger import logger

def get_rag_chain(persona="default", memory=None):
    vectorstore = get_vectorstore()

    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

 
    prompt_template = PERSONA_PROMPTS.get(persona.lower(), DEFAULT_PROMPT)
    prompt = PromptTemplate.from_template(prompt_template)

    if memory is None:
        logger.info("Creating in-memory buffer...")
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, output_key="answer")

    logger.info("Getting LLM...")
    llm = get_llm()

    logger.info("Building ConversationalRetrievalChain...")
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True,
        condense_question_prompt=prompt,
        output_key="answer",
    )

    logger.info("Chain successfully built.")
    return chain



