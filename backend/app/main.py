from fastapi import FastAPI, UploadFile, File, HTTPException
from celery.result import AsyncResult
import uuid
import os
import redis
from pydantic import BaseModel
from typing import Optional, Dict, Any

from backend.app.tasks import run_image_analysis
from backend.app.celery_app import celery

app = FastAPI(
    title="Smart Image Moderation API",
    version="1.0.0",
    description="Async image moderation API with OCR, face detection, NSFW scoring, and quality metrics (CPU mode)"
)

UPLOAD_DIR = "/app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = 6379


# -------------------------
# SCHEMAS
# -------------------------
class ImageResult(BaseModel):
    status: str
    device: Optional[str]
    image_path: str
    nsfw: bool
    nsfw_score: float
    faces_detected: int
    ocr_text: str
    blur_score: float
    quality_score: float
    processing_time: float
    model: Optional[Dict[str, Any]] = None


class ResultResponse(BaseModel):
    status: str
    result: Optional[ImageResult] = None
    error: Optional[str] = None


class UploadResponse(BaseModel):
    job_id: str
    status: str


# -------------------------
# ROUTES
# -------------------------
@app.get("/", tags=["system"])
def root():
    return {"status": "Smart Image Moderation API running", "mode": "cpu"}


@app.get("/health", tags=["system"])
def health():
    status = {
        "api": "ok",
        "redis": "unknown",
        "celery": "unknown",
    }

    # Check Redis
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, socket_connect_timeout=1)
        r.ping()
        status["redis"] = "ok"
    except Exception as e:
        status["redis"] = "error"
        status["redis_error"] = str(e)

    # Check Celery workers
    try:
        insp = celery.control.inspect(timeout=1)
        workers = insp.ping()
        status["celery"] = "ok" if workers else "error"
        status["workers"] = workers
    except Exception as e:
        status["celery"] = "error"
        status["celery_error"] = str(e)

    return status


@app.post("/upload", response_model=UploadResponse, tags=["jobs"])
async def upload_image(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Use JPG, PNG, or WEBP."
        )

    job_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{job_id}{ext}")

    try:
        with open(file_path, "wb") as f:
            f.write(await file.read())
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to save uploaded file")

    task = run_image_analysis.delay(file_path)

    return {
        "job_id": task.id,
        "status": "processing",
    }


@app.get("/result/{task_id}")
def get_result(task_id: str):
    task_result = AsyncResult(task_id, app=celery)

    if task_result.state == "PENDING":
        return {"status": "pending"}

    if task_result.state == "STARTED":
        return {"status": "running"}

    if task_result.state == "FAILURE":
        return {
            "status": "failed",
            "error": str(task_result.info),
        }

    if task_result.state == "SUCCESS":
        result = task_result.result

        # If worker returned a failure payload, pass it cleanly
        if isinstance(result, dict) and result.get("status") == "failed":
            return result

        return {
            "status": "success",
            "result": result,
        }

    return {"status": task_result.state}
