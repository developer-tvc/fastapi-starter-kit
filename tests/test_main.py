"""Tests for the FastAPI Starter Kit application."""

from __future__ import annotations

from fastapi import status
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_returns_200():
    """GET / returns HTTP 200."""
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK


def test_root_returns_correct_message():
    """GET / returns the expected welcome message."""
    response = client.get("/")
    assert response.json() == {"message": "FastAPI Starter Kit"}
