"""Tests for the status endpoint."""

from fastapi import status


def test_healthcheck_endpoint(client):
    """Test the healthcheck endpoint returns the expected information."""
    response = client.get("/api/v1/healthcheck")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "status" in data
    assert "timestamp" in data
    assert data["status"] == "OK"
    assert data["timestamp"] is not None
