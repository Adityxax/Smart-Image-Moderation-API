# 🧠 Smart Image Moderation & Analysis API

*A full-stack, async, Dockerized, ML-powered image analysis platform*

A production-style system that allows users to upload an image and receive real-time insights including NSFW detection, face counting, OCR text extraction, and image quality metrics — all backed by an asynchronous, containerized ML pipeline and a modern frontend dashboard.

---

## 🚀 Features

### Image Analysis

* 🔞 **NSFW / Sensitive Content Detection** (HSV-based heuristic)
* 🧍 **Face Detection** (OpenCV DNN – SSD Caffe model)
* 🔤 **OCR Text Extraction** (EasyOCR)
* 🌀 **Blur Detection** (Laplacian variance)
* 📐 **Image Quality Scoring** (resolution + sharpness)
* ⚡ **Processing Time Tracking**
* 🧪 **Model Metadata Reporting**

### System Capabilities

* 🔁 **Asynchronous ML Processing** (Celery + Redis)
* 🗄️ **Persistent Analysis History** (PostgreSQL)
* 📦 **Fully Dockerized Architecture**
* 🖥️ **Frontend Dashboard** (Next.js + Tailwind)
* 🛠️ **Dev / Prod Environment Separation**
* 🚦 **Health Checks + Service Orchestration**

---

## 🧩 The Idea

Build a **hosted API + frontend dashboard** where users can upload an image and receive:

* NSFW / sensitive content flag
* Face count
* OCR-extracted text
* Image quality metrics (blur + resolution)
* Processing time and model metadata

---

## 🏗️ Architecture Overview

### 🔹 Frontend (Next.js + Tailwind)

* Upload UI with image preview
* Polling-based live status updates
* Styled results dashboard
* Custom fonts (Bungee + Roboto Condensed)
* Themed UI with blur, glow, gradients, and purple-glass cards

### 🔹 Backend (FastAPI)

* REST API:

  * `POST /upload` → Upload image and queue job
  * `GET /result/{job_id}` → Fetch processing status/results
  * `GET /health` → Service health check

### 🔹 Async Task System

* **Celery** → Background ML processing
* **Redis** → Message broker + result backend
* ML runs in workers, not in the API thread

### 🔹 ML Pipeline (CPU-Only, Production-Safe)

* OpenCV DNN → Face detection
* EasyOCR → Text extraction
* Heuristic NSFW scoring → HSV skin-tone detection
* Blur detection → Laplacian variance
* Quality scoring → Resolution + sharpness formula

### 🔹 Docker

Multi-container setup:

* `smart_api` → FastAPI server
* `smart_worker` → Celery ML worker
* `smart_redis` → Redis broker
* `smart_db` → PostgreSQL database
* Dev + Prod Docker Compose configs

---

## 🔄 Processing Flow

### Upload Flow

1. User uploads an image
2. FastAPI:

   * Saves file to `/uploads`
   * Generates a `job_id`
   * Queues a Celery task
3. Returns `job_id` instantly

### Worker Flow

1. Celery worker:

   * Lazy-loads ML models
   * Runs:

     * Face detection
     * OCR
     * Blur scoring
     * NSFW heuristic
2. Packages result as JSON
3. Stores output in Redis

### Result Flow

Frontend polls:

```http
GET /result/{job_id}
```

Until:

```json
status = "success"
```

Then renders:

* NSFW status
* Faces detected
* OCR text
* Blur score
* Quality score
* Processing time
* Model metadata

---

## 🧪 ML Pipeline Design

### Face Detection

* OpenCV SSD (Caffe model)
* Confidence thresholding
* Lightweight and CPU-friendly

### OCR

* EasyOCR (English)
* Auto model caching via Docker volume

### Blur Detection

* Laplacian variance

  * High = sharp
  * Low = blurry

### NSFW Heuristic

* HSV skin-tone masking (H: 0-20, S: 20-255, V: 70-255)
* Pixel ratio scoring
* Threshold-based classification (> 0.25)

### Quality Score

* Combines:

  * Resolution
  * Sharpness
* Normalized and capped at `1.0`

---

## 🎨 Frontend Evolution

### Started As

> “Choose file. Button. Black screen.”

### Ended As

* Themed galaxy-style background
* Gradient + blur overlay
* Purple-glass cards
* Image preview panel
* Hover-glow buttons
* Clean results dashboard

### UX Features

* Upload preview
* Disabled + loading states
* Error handling
* Structured result layout

This turned a backend tool into a **demo-ready product**.

---

## 🐳 DevOps & Docker

### Containers

* API (FastAPI)
* Worker (Celery)
* Broker (Redis)
* Database (PostgreSQL)

### Volumes

* OCR model caching
* Upload persistence

### Health Checks

* Redis health monitoring
* API `/health` endpoint

### Environments

* Separate dev and prod compose files
* Local dev supports hot reload + async workers

---

## ⚡ One-Command Full Stack Startup

Added:

```json
"dev:full": "concurrently \"npm run dev\" \"npm run backend\""
```

Now:

```bash
npm run dev:full
```

Starts:

* Next.js frontend
* Docker backend
* Redis
* Celery workers

---

## 🔀 Git & GitHub Workflow

### Flow Used

* Feature branch: `feature/frontend-dashboard`
* Pull Request into `main`
* Clean merge
* Branch deleted after success

### PR Included

* Frontend dashboard
* Dev / prod Docker setup
* Concurrent startup scripts
* Backend integration updates

---

## 📋 Features Checklist

### Backend

* Async ML processing
* REST API (FastAPI)
* Redis queue & Result backend
* PostgreSQL data persistence
* CPU-safe ML pipeline
* Dockerized deployment
* Health checks & Orchestration

### Frontend

* Upload UI
* Live job polling
* Results dashboard
* Image preview
* Styled cards
* Custom fonts
* Glow effects
* Themed background

### Dev Experience

* One-command startup
* Dev / prod separation
* Clean Git history
* Release-ready structure

---

## 🧠 What This Project Demonstrates

* ✅ Distributed systems
* ✅ Async task queues
* ✅ ML pipeline design
* ✅ Docker orchestration
* ✅ API architecture
* ✅ Frontend integration
* ✅ DevOps workflows
* ✅ GitHub collaboration

Built a **Mini SaaS platform for ML image moderation**.

---

## 🔮 Future Upgrades

* JWT / API Key authentication
* Rate limiting
* GPU worker support (CUDA containers)
* Cloud deployment (Fly.io / Railway / AWS)
* Public demo URL

---

## 👤 Author

**Adi**
Backend, DevOps & ML Engineer

---

## ⭐ Star This Repo

If this project helped you or inspired you, consider giving it a star. It helps others discover the project and keeps the motivation flowing.

---

## 🏷️ Tech Stack Badges


![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=next.js&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)


---

## 🗺️ System Architecture Diagram

```text
+---------------------+
|     Frontend       |
|  Next.js + UI      |
+----------+----------+
           |
           | HTTP (Upload / Poll)
           v
+---------------------+
|      FastAPI       |
|  /upload /result  |
+----------+----------+
           |
           | Task Queue
           v
+---------------------+
|       Redis        |
| Broker + Results  |
+----------+----------+
           |          |
           | Consume  +------> +-------------------+
           v                   |   PostgreSQL      |
+---------------------+        |   Result Data     |
|   Celery Worker     | <------+-------------------+
|  ML Pipeline        |
+----------+----------+
           |
           | Models / Files
           v
+---------------------+
| Volumes / Models  |
| uploads / OCR /  |
| face models       |
+---------------------+
```
