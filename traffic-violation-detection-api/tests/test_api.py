"""
Tests for Traffic Violation Detection API
==========================================
Run: pytest tests/ -v
"""

import io
import pytest
import numpy as np
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestHealthEndpoint:
    def test_health_returns_200(self):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_response_structure(self):
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
        assert "model_loaded" in data
        assert "version" in data
        assert "timestamp" in data


class TestModelInfo:
    def test_model_info_returns_200(self):
        response = client.get("/model/info")
        assert response.status_code == 200

    def test_model_info_has_classes(self):
        response = client.get("/model/info")
        data = response.json()
        assert "detection_classes" in data
        assert "no_helmet" in data["detection_classes"]
        assert "red_light" in data["detection_classes"]

    def test_model_info_has_metrics(self):
        response = client.get("/model/info")
        data = response.json()
        assert "published_metrics" in data
        assert "mAP_violation_detection" in data["published_metrics"]


class TestDetectionEndpoint:
    @staticmethod
    def _create_test_image(width=640, height=480) -> bytes:
        """Generate a synthetic test image."""
        img = np.random.randint(0, 255, (height, width, 3), dtype=np.uint8)
        import cv2
        _, buffer = cv2.imencode(".jpg", img)
        return buffer.tobytes()

    def test_detect_returns_200(self):
        image_bytes = self._create_test_image()
        response = client.post(
            "/detect",
            files={"file": ("test.jpg", io.BytesIO(image_bytes), "image/jpeg")},
        )
        assert response.status_code == 200

    def test_detect_response_structure(self):
        image_bytes = self._create_test_image()
        response = client.post(
            "/detect",
            files={"file": ("test.jpg", io.BytesIO(image_bytes), "image/jpeg")},
        )
        data = response.json()
        assert "request_id" in data
        assert "timestamp" in data
        assert "inference_time_ms" in data
        assert "total_violations" in data
        assert "violations" in data
        assert "summary" in data
        assert "image_size" in data

    def test_detect_with_confidence_threshold(self):
        image_bytes = self._create_test_image()
        response = client.post(
            "/detect?confidence_threshold=0.9",
            files={"file": ("test.jpg", io.BytesIO(image_bytes), "image/jpeg")},
        )
        assert response.status_code == 200

    def test_detect_rejects_non_image(self):
        response = client.post(
            "/detect",
            files={"file": ("test.txt", io.BytesIO(b"not an image"), "text/plain")},
        )
        assert response.status_code == 400

    def test_detect_violations_have_required_fields(self):
        image_bytes = self._create_test_image()
        response = client.post(
            "/detect",
            files={"file": ("test.jpg", io.BytesIO(image_bytes), "image/jpeg")},
        )
        data = response.json()
        for v in data["violations"]:
            assert "violation_id" in v
            assert "violation_type" in v
            assert "confidence" in v
            assert "bounding_box" in v
            assert 0 <= v["confidence"] <= 1


class TestBatchEndpoint:
    def test_batch_detect(self):
        img = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        import cv2
        _, buf = cv2.imencode(".jpg", img)
        image_bytes = buf.tobytes()

        response = client.post(
            "/detect/batch",
            files=[
                ("files", ("img1.jpg", io.BytesIO(image_bytes), "image/jpeg")),
                ("files", ("img2.jpg", io.BytesIO(image_bytes), "image/jpeg")),
            ],
        )
        assert response.status_code == 200
        data = response.json()
        assert data["batch_size"] == 2
        assert len(data["results"]) == 2


class TestLandingPage:
    def test_root_returns_html(self):
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert "Traffic Violation" in response.text
