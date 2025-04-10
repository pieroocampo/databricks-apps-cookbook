"""Tests for the main application."""

from fastapi import status


def test_root_endpoint(client):
    """Test the root endpoint returns the expected response."""
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "app" in data
    assert "message" in data
    assert "docs" in data
    assert data["app"] == "Databricks FastAPI Example"


def test_docs_endpoint(client):
    """Test the OpenAPI docs endpoint is accessible."""
    response = client.get("/docs")
    assert response.status_code == status.HTTP_200_OK
