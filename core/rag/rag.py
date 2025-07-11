from langchain.chains import (
    create_history_aware_retriever,
    create_retrieval_chain,
)
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

from .llm import get_llm
from .vector_store import get_vectorstore
from .prompts import DEFAULT_PROMPT, PERSONA_PROMPTS
from utils.logger import logger


def get_rag_chain(persona: str = "default", memory=None):
    logger.info("Initializing vector store...")
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    logger.info("Loading LLM...")
    llm = get_llm()
    logger.info(f"Loaded LLM of type: {type(llm)}")

    # Select prompt template based on persona
    prompt_template = PERSONA_PROMPTS.get(persona.lower(), DEFAULT_PROMPT)
    qa_prompt = PromptTemplate.from_template(prompt_template)

    # Create document QA chain
    qa_chain = create_stuff_documents_chain(llm=llm, prompt=qa_prompt)

    # Initialize memory if not provided
    if memory is None:
        logger.info("No memory provided. Using ConversationBufferMemory.")
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

    # Create history-aware retriever
    logger.info("Creating context-aware retriever...")
    contextualize_q_prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "Given a chat history and the latest user question, "
            "which might reference context in the chat history, "
            "rephrase the question to be a standalone question."
        )),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"), 
    ])
    
    try:
        history_aware_retriever = create_history_aware_retriever(
            llm=llm,
            retriever=retriever,
            prompt=contextualize_q_prompt
        )
    except Exception as e:
        logger.error(f"Failed to create history-aware retriever: {e}")
        raise 

    # Build the full retrieval chain
    logger.info("Assembling final retrieval chain...")
    chain = create_retrieval_chain(
        retriever=history_aware_retriever,
        combine_docs_chain=qa_chain
    )

    logger.info("Retrieval-augmented generation (RAG) chain is ready.")
    return chain
