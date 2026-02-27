# 🚦 Traffic Violation Detection API

A production-grade REST API for real-time traffic violation detection using **YOLOv7**, **DeepSORT**, and **Tesseract OCR**.

Based on published research: *"Advancing Road Safety: A Comprehensive Analysis of an Enhanced Traffic Violation Detection"* — IJISAE, Vol. 12, Issue 19s, 2024.

---

## Published Metrics

| Metric | Score |
|--------|-------|
| mAP (Violation Detection) | **98.09%** |
| License Plate Recognition | **99.41%** |
| Real-World Detection Rate | **82.8%** (77/93) |
| False Positive Rate | **0%** |

## What It Detects

- 🪖 **Helmet violations** — riders without helmets on two-wheelers
- 🚦 **Traffic signal violations** — running red lights
- 🏎️ **Speed limit violations** — exceeding posted limits
- 👥 **Triple riding** — three persons on a two-wheeler
- 📱 **Phone usage** — using phone while riding

---

## Tech Stack

- **Detection Model:** YOLOv7 (custom-trained)
- **Object Tracking:** DeepSORT
- **License Plate OCR:** Tesseract
- **API Framework:** FastAPI
- **Containerization:** Docker
- **Language:** Python 3.11
- **CV Library:** OpenCV

## Project Structure

```
traffic-violation-detection-api/
├── app/
│   ├── __init__.py
│   ├── main.py            # FastAPI application & endpoints
│   ├── detector.py         # YOLOv7 detection engine
│   └── config.py           # Environment-based configuration
├── tests/
│   └── test_api.py         # Pytest test suite
├── models/                  # YOLOv7 weights (not tracked in git)
├── Dockerfile               # Production container
├── docker-compose.yml       # Docker Compose config
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variable template
└── README.md
```

## Quick Start

### Option 1: Local Development

```bash
# Clone the repo
git clone https://github.com/AIArjun/traffic-violation-detection-api.git
cd traffic-violation-detection-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Run the API
uvicorn app.main:app --reload --port 8000
```

### Option 2: Docker

```bash
# Build and run
docker-compose up --build

# Or build manually
docker build -t traffic-api .
docker run -p 8000:8000 traffic-api
```

### Access the API

- **Landing Page:** http://localhost:8000
- **Interactive Docs (Swagger):** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## API Endpoints

### `GET /health`
Health check endpoint.

```bash
curl http://localhost:8000/health
```

### `GET /model/info`
Get model architecture details and published metrics.

### `POST /detect`
Detect violations in a single image.

```bash
curl -X POST http://localhost:8000/detect \
  -F "file=@traffic_image.jpg" \
  -F "confidence_threshold=0.5" \
  -F "detect_plates=true"
```

**Response:**
```json
{
  "request_id": "a1b2c3d4",
  "timestamp": "2024-03-15T10:30:00",
  "image_size": {"width": 1920, "height": 1080},
  "inference_time_ms": 45.2,
  "total_violations": 2,
  "violations": [
    {
      "violation_id": "a1b2c3d4-0",
      "violation_type": "no_helmet",
      "confidence": 0.9412,
      "bounding_box": {"x1": 245, "y1": 180, "x2": 410, "y2": 395},
      "license_plate": "KA01AB1234",
      "plate_confidence": 0.9673
    }
  ],
  "summary": {"no_helmet": 1, "red_light": 1}
}
```

### `POST /detect/batch`
Process multiple images in a single request (max 10).

```bash
curl -X POST http://localhost:8000/detect/batch \
  -F "files=@image1.jpg" \
  -F "files=@image2.jpg"
```

---

## Running Tests

```bash
pip install pytest httpx
pytest tests/ -v
```

---

## Using Custom YOLOv7 Weights

1. Train YOLOv7 on your traffic violation dataset
2. Place the `.pt` weights file in the `models/` directory
3. Set the environment variable:
   ```bash
   export MODEL_PATH=models/yolov7-traffic.pt
   ```
4. Restart the API — it will load real weights instead of demo mode

---

## Architecture

```
Client (Image Upload)
        │
        ▼
   FastAPI Server
        │
        ├──► Input Validation (file type, size)
        │
        ├──► Image Preprocessing (OpenCV)
        │
        ├──► YOLOv7 Inference (violation detection)
        │
        ├──► DeepSORT Tracking (multi-object)
        │
        ├──► Tesseract OCR (license plate extraction)
        │
        └──► JSON Response (violations + metadata)
```

---

## Author

**Arjun Ponnaganti**
- MSc Image Analysis & Machine Learning — Uppsala University, Sweden
- 4 peer-reviewed publications including IEEE
- [LinkedIn](https://linkedin.com/in/arjun-ponnaganti)
- [GitHub](https://github.com/AIArjun)

## License

MIT License
