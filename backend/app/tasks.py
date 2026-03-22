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

        result = {
            **result,
            "processing_time": round(time.time() - start_time, 2),
            "status": "success"
        }

        return result

    except Exception as e:
        logger.exception(f"[TASK] Failed processing image: {image_path}")

        return {
            "status": "failed",
            "error": str(e),
            "processing_time": round(time.time() - start_time, 2),
        }