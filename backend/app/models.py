from sqlalchemy import Column, String, Boolean, Float, Integer
from sqlalchemy.dialects.postgresql import JSONB
from .database import Base

class ImageAnalysisRecord(Base):
    __tablename__ = "image_analyses"

    id = Column(String, primary_key=True, index=True) # Celery job_id
    image_path = Column(String, nullable=False)
    status = Column(String, default="pending") # pending, success, failed

    nsfw = Column(Boolean, nullable=True)
    nsfw_score = Column(Float, nullable=True)
    
    faces_detected = Column(Integer, nullable=True)
    faces = Column(JSONB, nullable=True)
    
    ocr_text = Column(String, nullable=True)
    
    blur_score = Column(Float, nullable=True)
    quality_score = Column(Float, nullable=True)
    
    processing_time = Column(Float, nullable=True)
