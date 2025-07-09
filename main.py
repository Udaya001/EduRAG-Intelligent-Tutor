from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.logger import logger
from core.config import settings
from api.v1 import router

app = FastAPI(
    title="EduRAG Backend",
    description="DocBot – Intelligent Tutor Using RAG and LangChain",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def get_homepage():
    return {"messgae": "Welcome to the EduRAG"}

app.include_router(router,prefix="/api/v1/router",tags=['Endpoints'])

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting App.....")
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)



