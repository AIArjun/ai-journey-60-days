"""
Traffic Violation Detection API
================================
A production-grade REST API for real-time traffic violation detection
using YOLOv7, DeepSORT, and Tesseract OCR.

Author: Arjun Ponnaganti
LinkedIn: https://linkedin.com/in/arjun-ponnaganti
Based on published research: IJISAE, Vol. 12, Issue 19s, 2024
"""

import io
import os
import time
import uuid
import logging
from datetime import datetime
from typing import Optional

import numpy as np
from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.detector import TrafficViolationDetector
from app.config import settings

# ─── Logging Setup ───
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("traffic-api")

# ─── FastAPI App ───
app = FastAPI(
    title="Traffic Violation Detection API",
    description=(
        "Real-time traffic violation detection using YOLOv7 + DeepSORT + OCR. "
        "Detects helmet violations, traffic signal violations, and speed limit infractions. "
        "Based on published research achieving 98.09% mAP and 99.41% plate recognition accuracy."
    ),
    version="1.0.0",
    contact={
        "name": "Arjun Ponnaganti",
        "url": "https://linkedin.com/in/arjun-ponnaganti",
    },
    docs_url="/docs",
    redoc_url="/redoc",
)

# ─── CORS ───
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Initialize Detector ───
detector = TrafficViolationDetector()

# ─── Request/Response Models ───
class HealthResponse(BaseModel):
    status: str = "healthy"
    version: str = "1.0.0"
    model_loaded: bool = True
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class ViolationDetail(BaseModel):
    violation_id: str
    violation_type: str
    confidence: float
    bounding_box: dict
    license_plate: Optional[str] = None
    plate_confidence: Optional[float] = None


class DetectionResponse(BaseModel):
    request_id: str
    timestamp: str
    image_size: dict
    inference_time_ms: float
    total_violations: int
    violations: list[ViolationDetail]
    summary: dict


class ModelInfoResponse(BaseModel):
    model_name: str = "YOLOv7-Traffic"
    framework: str = "PyTorch"
    detection_classes: list[str]
    input_size: str = "640x640"
    published_metrics: dict


# ─── Endpoints ───

@app.get("/", response_class=HTMLResponse)
async def root():
    """Landing page with API documentation link."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Traffic Violation Detection API</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: #0a0a1a;
                color: #e0e0e0;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .container {
                max-width: 700px;
                padding: 48px;
                text-align: center;
            }
            h1 {
                font-size: 2.2rem;
                color: #fff;
                margin-bottom: 8px;
            }
            .accent { color: #4fc3f7; }
            .subtitle {
                color: #888;
                font-size: 1rem;
                margin-bottom: 32px;
            }
            .metrics {
                display: flex;
                gap: 24px;
                justify-content: center;
                margin: 32px 0;
            }
            .metric {
                background: rgba(79, 195, 247, 0.08);
                border: 1px solid rgba(79, 195, 247, 0.2);
                border-radius: 12px;
                padding: 20px 28px;
            }
            .metric .value {
                font-size: 1.8rem;
                font-weight: 700;
                color: #4fc3f7;
            }
            .metric .label {
                font-size: 0.8rem;
                color: #888;
                margin-top: 4px;
            }
            .links {
                display: flex;
                gap: 16px;
                justify-content: center;
                margin-top: 32px;
            }
            a.btn {
                display: inline-block;
                padding: 12px 28px;
                border-radius: 8px;
                text-decoration: none;
                font-weight: 600;
                font-size: 0.95rem;
                transition: all 0.2s;
            }
            a.primary { background: #4fc3f7; color: #0a0a1a; }
            a.primary:hover { background: #81d4fa; }
            a.secondary {
                border: 1px solid #4fc3f7;
                color: #4fc3f7;
            }
            a.secondary:hover { background: rgba(79, 195, 247, 0.1); }
            .footer {
                margin-top: 48px;
                font-size: 0.85rem;
                color: #555;
            }
            .footer a { color: #4fc3f7; text-decoration: none; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚦 Traffic Violation <span class="accent">Detection API</span></h1>
            <p class="subtitle">
                Real-time detection using YOLOv7 + DeepSORT + Tesseract OCR
            </p>
            <div class="metrics">
                <div class="metric">
                    <div class="value">98.09%</div>
                    <div class="label">mAP (Violation Detection)</div>
                </div>
                <div class="metric">
                    <div class="value">99.41%</div>
                    <div class="label">Plate Recognition</div>
                </div>
                <div class="metric">
                    <div class="value">0</div>
                    <div class="label">False Positives</div>
                </div>
            </div>
            <div class="links">
                <a href="/docs" class="btn primary">API Documentation</a>
                <a href="/redoc" class="btn secondary">ReDoc</a>
            </div>
            <p class="footer">
                Built by <a href="https://linkedin.com/in/arjun-ponnaganti">Arjun Ponnaganti</a>
                &nbsp;|&nbsp; Based on research published in IJISAE, 2024
            </p>
        </div>
    </body>
    </html>
    """


@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """Check API health and model status."""
    logger.info("Health check requested")
    return HealthResponse(model_loaded=detector.is_loaded)


@app.get("/model/info", response_model=ModelInfoResponse, tags=["Model"])
async def model_info():
    """Get model architecture and performance metrics."""
    return ModelInfoResponse(
        detection_classes=detector.CLASSES,
        published_metrics={
            "mAP_violation_detection": "98.09%",
            "accuracy_plate_recognition": "99.41%",
            "real_world_detection_rate": "82.8% (77/93)",
            "false_positive_rate": "0%",
            "published_in": "IJISAE, Vol. 12, Issue 19s, 2024",
        },
    )


@app.post("/detect", response_model=DetectionResponse, tags=["Detection"])
async def detect_violations(
    file: UploadFile = File(..., description="Image file (JPEG/PNG) to analyze"),
    confidence_threshold: float = Query(
        default=0.5,
        ge=0.1,
        le=1.0,
        description="Minimum confidence score for detections",
    ),
    detect_plates: bool = Query(
        default=True,
        description="Enable license plate OCR extraction",
    ),
):
    """
    Detect traffic violations in an uploaded image.

    Analyzes the image for:
    - **Helmet violations** (riders without helmets)
    - **Traffic signal violations** (running red lights)
    - **Speed limit violations** (detected via context)

    Returns bounding boxes, confidence scores, violation types,
    and extracted license plate numbers (if enabled).
    """
    request_id = str(uuid.uuid4())[:8]
    logger.info(f"[{request_id}] Detection request: {file.filename}, threshold={confidence_threshold}")

    # Validate file type
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type: {file.content_type}. Expected image/jpeg or image/png.",
        )

    # Read and validate image
    try:
        contents = await file.read()
        if len(contents) > 10 * 1024 * 1024:  # 10MB limit
            raise HTTPException(status_code=413, detail="File too large. Maximum size: 10MB.")

        image = detector.preprocess_image(contents)
        h, w = image.shape[:2]
        logger.info(f"[{request_id}] Image loaded: {w}x{h}")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[{request_id}] Image processing error: {e}")
        raise HTTPException(status_code=400, detail=f"Could not process image: {str(e)}")

    # Run detection
    start_time = time.time()
    try:
        detections = detector.detect(
            image,
            confidence_threshold=confidence_threshold,
            detect_plates=detect_plates,
        )
        inference_time = (time.time() - start_time) * 1000
        logger.info(
            f"[{request_id}] Detection complete: {len(detections)} violations found "
            f"in {inference_time:.1f}ms"
        )
    except Exception as e:
        logger.error(f"[{request_id}] Detection error: {e}")
        raise HTTPException(status_code=500, detail=f"Detection failed: {str(e)}")

    # Format response
    violations = []
    violation_counts = {}
    for det in detections:
        v = ViolationDetail(
            violation_id=f"{request_id}-{len(violations)}",
            violation_type=det["class"],
            confidence=round(det["confidence"], 4),
            bounding_box={
                "x1": det["bbox"][0],
                "y1": det["bbox"][1],
                "x2": det["bbox"][2],
                "y2": det["bbox"][3],
            },
            license_plate=det.get("plate_text"),
            plate_confidence=det.get("plate_confidence"),
        )
        violations.append(v)
        violation_counts[det["class"]] = violation_counts.get(det["class"], 0) + 1

    return DetectionResponse(
        request_id=request_id,
        timestamp=datetime.utcnow().isoformat(),
        image_size={"width": w, "height": h},
        inference_time_ms=round(inference_time, 2),
        total_violations=len(violations),
        violations=violations,
        summary=violation_counts,
    )


@app.post("/detect/batch", tags=["Detection"])
async def detect_batch(
    files: list[UploadFile] = File(..., description="Multiple images to analyze"),
    confidence_threshold: float = Query(default=0.5, ge=0.1, le=1.0),
):
    """
    Batch detection endpoint for processing multiple images.
    Returns results for each image in the batch.
    """
    if len(files) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 images per batch.")

    results = []
    for file in files:
        try:
            contents = await file.read()
            image = detector.preprocess_image(contents)
            h, w = image.shape[:2]

            start = time.time()
            detections = detector.detect(image, confidence_threshold=confidence_threshold)
            elapsed = (time.time() - start) * 1000

            results.append({
                "filename": file.filename,
                "status": "success",
                "violations_found": len(detections),
                "inference_time_ms": round(elapsed, 2),
                "detections": detections,
            })
        except Exception as e:
            results.append({
                "filename": file.filename,
                "status": "error",
                "error": str(e),
            })

    return {"batch_size": len(files), "results": results}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
