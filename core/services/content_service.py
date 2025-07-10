from db.models import ContentModel
from db.database import SessionLocal
from core.rag.vector_store import get_vectorstore, save_vectorstore, embeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from core.config import settings
from utils.logger import logger
import os



def add_to_vectorstore(texts):
    if not texts:
        logger.warning("No texts provided to add to vector store")
        return

    logger.info("Adding texts to vector store")
    vectorstore = get_vectorstore()

    for text in texts:
        vectorstore.add_texts(texts=[text])  # Send one text at a time

    save_vectorstore(vectorstore)
    logger.debug("Vector store updated")




class ContentService:
    def __init__(self):
        self.db = SessionLocal()

    def upload_content(self, request):
        #Uploads content and metadata to the database and vector store.
        #Returns success message and content ID.

        logger.info(f"Uploading content for topic: {request.metadata.get('topic')}")
        try:
            content = ContentModel(
                topic=request.metadata.get("topic"),
                title=request.metadata.get("title"),
                grade=request.metadata.get("grade"),
                content=request.content,
                metadata_=request.metadata
            )
            self.db.add(content)
            self.db.commit()
            self.db.refresh(content)

            # Split content and add to FAISS
            splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            texts = splitter.split_text(request.content)
            add_to_vectorstore(texts)

            logger.info(f"Content uploaded successfully (ID: {content.id})")
            return {"message": "Content uploaded", "content_id": content.id}
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error uploading content: {str(e)}")
            raise
        finally:
            self.db.close()

    def get_filtered_topics(self, grade: str = None, topic: str = None):
        #Fetches topics filtered by grade or topic name.
        #Returns list of dictionaries containing topic info.

        logger.info(f"Fetching topics (grade={grade}, topic={topic})")
        try:
            query = self.db.query(ContentModel)

            if grade:
                query = query.filter(ContentModel.grade == grade)
            if topic:
                query = query.filter(ContentModel.topic.ilike(f"%{topic}%"))

            results = query.all()
            logger.debug(f"Found {len(results)} matching topics")
            return [{"topic": c.topic, "grade": c.grade, "title": c.title} for c in results]
        except Exception as e:
            logger.error(f"Error fetching topics: {str(e)}")
            raise
        finally:
            self.db.close()

    def get_system_metrics(self):
        #Returns system metrics like total topics, files uploaded, and vector store size.

        logger.info("Fetching system metrics")
        try:
            total_topics = self.db.query(ContentModel.topic).distinct().count()
            total_files = self.db.query(ContentModel).count()
            vectorstore = get_vectorstore()
            vector_store_size = len(vectorstore.index_to_docstore_id) if vectorstore else 0

            metrics = {
                "total_topics": total_topics,
                "total_files_uploaded": total_files,
                "vector_store_size": vector_store_size
            }
            logger.debug(f"Metrics: {metrics}")
            return metrics
        except Exception as e:
            logger.error(f"Error fetching metrics: {str(e)}")
            raise
        finally:
            self.db.close()



