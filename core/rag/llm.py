from langchain_google_vertexai import ChatVertexAI

def get_llm():
    return ChatVertexAI(
        model_name="gemini-2.5-flash",
        temperature=0.3,
        location="us-central1",
    )


