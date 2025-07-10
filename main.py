from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.logger import logger
from core.config import settings
from db.models import ContentModel
from db.database import engine

from api.v1.router import router
import uvicorn

app = FastAPI(
    title="EduRAG Backend",
    description="EduRAG – Intelligent Tutor Using RAG and LangChain",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure tables exist
ContentModel.metadata.create_all(bind=engine)


@app.get("/")
def get_homepage():
    return {"messgae": "Welcome to the EduRAG"}

app.include_router(router,prefix="/api/v1/router",tags=['Endpoints'])

if __name__ == "__main__":
    logger.info("Starting App.....")
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)



