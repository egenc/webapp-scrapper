import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient
from app import get_jobs

@pytest.fixture
def client():
    app = FastAPI()
    client = TestClient(app)
    return client

def test_get_jobs_success(client):
    response = client.get("/jobs/")
    assert len(response.json()) > 0

def test_get_jobs_invalid_page(client):
    response = client.get("/jobs/?page=0")
    assert response.status_code == 404

def test_get_jobs_invalid_per_page(client):
    response = client.get("/jobs/?per_page=200")
    assert response.status_code == 404

def test_get_jobs_invalid_sort_by(client):
    response = client.get("/jobs/?sort_by=invalid_field")
    assert response.status_code == 404

def test_get_jobs_invalid_sort_order(client):
    response = client.get("/jobs/?sort_order=invalid_order")
    assert response.status_code == 404