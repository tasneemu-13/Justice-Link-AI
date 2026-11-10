"""
Unit tests for the FastAPI backend service.
"""

import pytest
import httpx
from justicelink.api import app


@pytest.mark.anyio
async def test_root_endpoint():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["project"] == "JusticeLink AI"


@pytest.mark.anyio
async def test_metrics_endpoint():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/metrics")
        assert response.status_code == 200
        data = response.json()
        assert "models" in data
        assert len(data["models"]) >= 5


@pytest.mark.anyio
async def test_prediction_endpoint():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "case_seq_no": 150,
            "filing_year": 2025,
            "filing_month": 5,
            "filing_day_of_year": 135,
        }
        response = await client.post("/api/v1/predict", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "estimated_duration_days" in data
        assert data["estimated_duration_days"] > 0
