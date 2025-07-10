import os
from langchain.vectorstores import Chroma
from langchain_google_vertexai import VertexAIEmbeddings

CHROMA_PERSIST_DIRECTORY = "chroma_db"

# embeddings to share
embeddings = VertexAIEmbeddings(
    project="vertex-ai-embedder",
    model_name="gemini-embedding-001"
)

def get_vectorstore():
    return Chroma(persist_directory=CHROMA_PERSIST_DIRECTORY, embedding_function=embeddings)

def save_vectorstore(vectorstore):
    vectorstore.persist()
