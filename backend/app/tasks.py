import logging
import time
from backend.app.celery_app import celery

logger = logging.getLogger(__name__)


@celery.task(
    name="backend.app.tasks.run_image_analysis",
    bind=True,
    autoretry_for=(IOError, OSError, ConnectionError),
    retry_kwargs={"max_retries": 3, "countdown": 5},
    retry_backoff=True,
)
def run_image_analysis(self, image_path: str):

    def step(name: str):
        self.update_state(
            state="PROGRESS",
            meta={"step": name}
        )
        logger.info(f"[TASK] {name}")

    start_time = time.time()

    try:
        step("Loading image")

        # Lazy import inside worker
        from backend.app.ml.processor import process_image

        step("Running NSFW detection")
        time.sleep(0.2)

        step("Detecting faces")
        time.sleep(0.2)

        step("Running OCR")
        time.sleep(0.2)

        step("Analyzing quality")

        result = process_image(image_path)

        step("Finalizing results")

        # 🔥 IMPORTANT: enforce clean JSON-safe output
        if not isinstance(result, dict):
            raise ValueError("process_image must return dict")

        processing_time = round(time.time() - start_time, 2)
        
        # Save to PostgreSQL
        from backend.app.database import SessionLocal
        from backend.app.models import ImageAnalysisRecord
        
        db = SessionLocal()
        try:
            record = db.query(ImageAnalysisRecord).filter(ImageAnalysisRecord.id == self.request.id).first()
            if record:
                record.status = "success"
                record.processing_time = processing_time
                record.nsfw = result.get('nsfw')
                record.nsfw_score = result.get('nsfw_score')
                record.faces_detected = result.get('faces_detected')
                record.faces = result.get('faces')
                record.ocr_text = result.get('ocr_text')
                record.blur_score = result.get('blur_score')
                record.quality_score = result.get('quality_score')
                db.commit()
        finally:
            db.close()

        result = {
            **result,
            "processing_time": processing_time,
            "status": "success"
        }

        return result

    except Exception as e:
        logger.exception(f"[TASK] Failed processing image: {image_path}")

        try:
            from backend.app.database import SessionLocal
            from backend.app.models import ImageAnalysisRecord
            db = SessionLocal()
            record = db.query(ImageAnalysisRecord).filter(ImageAnalysisRecord.id == self.request.id).first()
            if record:
                record.status = "failed"
                record.processing_time = round(time.time() - start_time, 2)
                db.commit()
            db.close()
        except Exception as db_err:
            logger.error(f"[TASK] Failed to save error to DB: {db_err}")

        return {
            "status": "failed",
            "error": str(e),
            "processing_time": round(time.time() - start_time, 2),
        }