import os
import time
import cv2
import numpy as np
import easyocr

# -------------------------
# DEVICE (CPU ONLY)
# -------------------------
DEVICE = "cpu"
print(f"[ML] Running on {DEVICE}")

# -------------------------
# PATHS
# -------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")

PROTO_PATH = os.path.join(MODELS_DIR, "deploy.prototxt")
MODEL_PATH = os.path.join(MODELS_DIR, "res10_300x300_ssd_iter_140000.caffemodel")

EASYOCR_PATH = os.getenv("EASYOCR_MODULE_PATH", "/app/.easyocr")

os.makedirs(EASYOCR_PATH, exist_ok=True)

# -------------------------
# LOAD MODELS (ONCE PER WORKER)
# -------------------------
print("[ML] Loading EasyOCR (CPU)...")
reader = easyocr.Reader(
    ["en"],
    gpu=False,
    model_storage_directory=EASYOCR_PATH
)
print("[ML] EasyOCR loaded")

print("[ML] Loading OpenCV DNN face detector...")
if not os.path.exists(PROTO_PATH) or not os.path.exists(MODEL_PATH):
    raise RuntimeError(
        f"Face model files missing.\n"
        f"Expected:\n{PROTO_PATH}\n{MODEL_PATH}"
    )

face_net = cv2.dnn.readNetFromCaffe(PROTO_PATH, MODEL_PATH)
print("[ML] Face detector loaded")

# -------------------------
# HELPERS
# -------------------------
def detect_faces(image):
    h, w = image.shape[:2]
    blob = cv2.dnn.blobFromImage(
        cv2.resize(image, (300, 300)),
        1.0,
        (300, 300),
        (104.0, 177.0, 123.0)
    )
    face_net.setInput(blob)
    detections = face_net.forward()

    count = 0
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            count += 1
    return count


def blur_score(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return float(cv2.Laplacian(gray, cv2.CV_64F).var())


def nsfw_score(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    skin_mask = cv2.inRange(hsv, (0, 20, 70), (20, 255, 255))
    skin_ratio = np.sum(skin_mask > 0) / (image.shape[0] * image.shape[1])
    return float(skin_ratio)

# -------------------------
# MAIN PIPELINE
# -------------------------
def process_image(image_path: str) -> dict:
    start = time.time()

    if not os.path.exists(image_path):
        return {
            "status": "failed",
            "device": DEVICE,
            "error": "Image not found"
        }

    image = cv2.imread(image_path)
    if image is None:
        return {
            "status": "failed",
            "device": DEVICE,
            "error": "Invalid image"
        }

    # ---------- Resize for speed ----------
    max_dim = 1280
    h, w = image.shape[:2]
    if max(h, w) > max_dim:
        scale = max_dim / max(h, w)
        image = cv2.resize(image, (int(w * scale), int(h * scale)))

    # ---------- Face Detection ----------
    faces = detect_faces(image)

    # ---------- OCR ----------
    ocr_results = reader.readtext(image)
    text = " ".join([r[1] for r in ocr_results])

    # ---------- Blur ----------
    blur_val = blur_score(image)

    # ---------- NSFW ----------
    nsfw_val = nsfw_score(image)
    nsfw_flag = nsfw_val > 0.25

    # ---------- Quality ----------
    resolution_score = min(image.shape[0], image.shape[1]) / 1000
    quality_score = round(min((blur_val / 100) + resolution_score, 1.0), 2)

    return {
        "status": "success",
        "device": DEVICE,
        "image_path": image_path,
        "nsfw": nsfw_flag,
        "nsfw_score": round(nsfw_val, 3),
        "faces_detected": faces,
        "ocr_text": text,
        "blur_score": round(blur_val, 2),
        "quality_score": quality_score,
        "processing_time": round(time.time() - start, 2),
        "model": {
            "face": "opencv-dnn",
            "ocr": "easyocr",
            "nsfw": "heuristic-v1",
            "device": "cpu"
        }
    }
