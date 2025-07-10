from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from .llm import get_llm
from .vector_store import get_vectorstore
from .prompts import DEFAULT_PROMPT, PERSONA_PROMPTS


memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

def get_rag_chain(persona="default"):
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    prompt_template = PERSONA_PROMPTS.get(persona.lower(), DEFAULT_PROMPT)
    prompt = PromptTemplate.from_template(prompt_template)

    chain = ConversationalRetrievalChain.from_llm(
        llm=get_llm(),
        retriever=retriever,
        memory=memory,
        return_source_documents=True,
        condense_question_prompt=prompt
    )
    return chain


rag_chain = get_rag_chain()

def generate_answer(question: str):
    result = rag_chain.invoke({"question": question})
    return result["answer"]
