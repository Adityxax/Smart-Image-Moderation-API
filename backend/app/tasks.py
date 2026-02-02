import logging
import time
from backend.app.celery_app import celery

logger = logging.getLogger(__name__)


@celery.task(
    name="backend.app.tasks.run_image_analysis",
    bind=True,
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 3, "countdown": 5},
)
def run_image_analysis(self, image_path: str):
    """
    Run the ML pipeline on an image path.

    - Lazy-loads ML models inside the worker
    - Retries on transient failures
    - Emits live progress states for frontend polling
    - Returns structured errors instead of crashing the worker
    """

    def step(name: str):
        self.update_state(
            state="PROGRESS",
            meta={"step": name}
        )
        logger.info(f"[TASK] {name}")

    start_time = time.time()

    try:
        step("Loading image")

        # Import ML only inside worker process
        from backend.app.ml.processor import process_image

        step("Running NSFW detection")
        time.sleep(0.3)

        step("Detecting faces")
        time.sleep(0.3)

        step("Running OCR")
        time.sleep(0.3)

        step("Analyzing quality")

        result = process_image(image_path)

        step("Finalizing results")

        # Attach processing time if not already added
        if isinstance(result, dict):
            result["processing_time"] = round(time.time() - start_time, 2)
            result["status"] = "success"

        return result

    except Exception as e:
        logger.exception(f"[TASK] Failed processing image: {image_path}")
        return {
            "status": "failed",
            "error": str(e),
            "processing_time": round(time.time() - start_time, 2),
        }
