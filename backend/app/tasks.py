import logging
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
    - Returns structured errors instead of crashing the worker
    """
    try:
        # Import ML only inside worker process
        from backend.app.ml.processor import process_image

        logger.info(f"[TASK] Processing image: {image_path}")
        return process_image(image_path)

    except Exception as e:
        logger.exception(f"[TASK] Failed processing image: {image_path}")
        return {
            "status": "failed",
            "error": str(e),
        }
