# 🧠 Smart Image Moderation & Analysis API (Mini SaaS)

A **containerized, asynchronous image analysis platform** that lets users upload images and receive automated moderation and insight results through a clean, production-style API.

Think **AWS Rekognition, but student-budget and engineer-brain powered**.

This system follows real-world backend and DevOps patterns including microservice-style architecture, background job processing, persistent model caching, and health-based startup orchestration.

---

## 🚀 Features

* 🔞 **NSFW Content Detection** (lightweight heuristic-based)
* 🧍 **Face Detection** (OpenCV DNN)
* 🔤 **OCR Text Extraction** (EasyOCR)
* 🌀 **Blur Detection** (Laplacian variance)
* 📐 **Image Quality Scoring** (resolution-based)
* ⚡ **Processing Time Tracking**
* 🔁 **Asynchronous Job Handling** (FastAPI + Celery)
* 📦 **Fully Containerized Deployment** (Docker + Docker Compose)

---

## 🏗️ System Architecture

This project follows a **microservices-style, asynchronous processing pipeline** designed for scalability, reliability, and fast API response times.

### Core Components

### 1️⃣ FastAPI (API Service)

* Accepts image uploads
* Returns a `job_id` immediately
* Exposes `/result/{job_id}` for result retrieval
* Serves OpenAPI documentation at `/docs`
* Health endpoint for service orchestration

### 2️⃣ Celery (Worker Service)

* Runs ML tasks asynchronously
* Loads models once per worker
* Processes images from shared volumes
* Stores results in Redis

### 3️⃣ Redis

* Message broker for Celery
* Result backend for job storage
* Health dependency for startup order

---

## 🔄 Processing Pipeline

### Upload Flow

1. User uploads an image via `POST /upload`
2. API stores the image in `/uploads`
3. API pushes a job to Redis
4. Celery worker picks up the task
5. ML pipeline processes the image
6. Results are stored in Redis
7. User polls `GET /result/{job_id}` to retrieve output

---

## 🧠 ML & Computer Vision Stack

### Face Detection

* **OpenCV DNN (SSD-based Caffe Model)**
* Lightweight and CPU-friendly
* No GPU or PyTorch dependency

**Model Files:**

* `deploy.prototxt`
* `res10_300x300_ssd_iter_140000.caffemodel`

### OCR

* **EasyOCR**
* CPU mode
* Persistent model cache via Docker volumes

### Image Quality Analysis

* Blur detection using **Laplacian variance**
* Resolution-based quality scoring
* End-to-end processing time measurement

### NSFW Detection

* **HSV-based skin ratio heuristic**
* Lightweight placeholder for future ML-based classifiers

---

## 🐳 Containerization Strategy

### Docker Architecture

### Base Image (`Dockerfile.base`)

Pre-installs all heavy dependencies once:

* Python 3.11
* OpenCV
* EasyOCR
* NumPy
* System libraries (Tesseract, GL, build tools)

This prevents repeated downloads of large ML packages during rebuilds.

### App Image (`Dockerfile`)

* Inherits from `smart-ml-base:cpu`
* Installs lightweight app dependencies
* Copies backend source code
* Creates runtime directories
* Runs the FastAPI server

---

## 🧩 Docker Compose Services

### Services

| Service  | Role                            |
| -------- | ------------------------------- |
| `api`    | FastAPI server (port `8000`)    |
| `worker` | Celery background processor     |
| `redis`  | Message broker + result backend |

### Health-Based Startup

* API and Worker wait for Redis to become healthy
* Prevents race conditions during system startup

---

## 📂 Persistent Volumes

| Directory   | Purpose                      |
| ----------- | ---------------------------- |
| `uploads/`  | Stores uploaded images       |
| `.easyocr/` | OCR model cache              |
| `models/`   | OpenCV face detection models |

### Benefits

* No re-downloading of models
* Faster cold starts
* Images persist across container restarts

---

## 🌐 API Endpoints

### Upload Image

**POST** `/upload`

**Response**

```json
{
  "job_id": "uuid",
  "status": "processing"
}
```

### Get Result

**GET** `/result/{job_id}`

**Response**

```json
{
  "status": "success",
  "result": {
    "nsfw": false,
    "faces_detected": 0,
    "ocr_text": "Detected text",
    "blur_score": 907.64,
    "quality_score": 1.0,
    "processing_time": 1.62,
    "model": {
      "face": "opencv-dnn",
      "ocr": "easyocr",
      "nsfw": "heuristic-v1",
      "device": "cpu"
    }
  }
}
```

---

## 🛠️ DevOps Highlights

* **Health-Based Startup Ordering**
* **Layered Docker Builds**
* **Asynchronous Job Queue**
* **Horizontally Scalable Workers**
* **Persistent Model Caching**
* **Clean OpenAPI Interface**

---

## ▶️ How to Run

### First-Time Setup

```bash
docker build -t smart-ml-base:cpu -f Dockerfile.base .
docker compose up --build
```

### Daily Startup

```bash
docker compose up
```

### Stop System

```bash
docker compose down
```

---

## 💪 System Design Strengths

* ✅ Fully containerized
* ✅ Asynchronous ML processing
* ✅ Production-style architecture
* ✅ Persistent model caching
* ✅ Scalable worker system
* ✅ Clean API interface
* ✅ Student-budget infrastructure

---

## 🌱 Future Upgrade Paths

* Replace NSFW heuristic with **CLIP / ViT-based classifier**
* Add **GPU workers** using CUDA containers
* Store results in **PostgreSQL** instead of Redis
* Add **authentication and API keys**
* Deploy with **Docker Swarm / Kubernetes**
* Add **rate limiting & usage analytics**

---

## 👤 Author

**Adi**
Backend, DevOps & Computer Vision Engineer

---

## ⭐ Star This Repo

If this saved you from Docker-induced emotional damage, drop a star. The algorithm and my sanity both appreciate it.
