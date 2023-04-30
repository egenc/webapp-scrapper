"""Unit test for web app"""
import psycopg2
import pytest
from starlette.testclient import TestClient
from app import app

@pytest.fixture
def client():
    return TestClient(app)

def test_get_jobs_success(client):
    response = client.get("/jobs/")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_get_jobs_invalid_page(client):
    response = client.get("/jobs/?page=0")
    assert response.status_code == 422

def test_get_jobs_invalid_per_page(client):
    response = client.get("/jobs/?per_page=200")
    assert response.status_code == 422

def test_get_jobs_invalid_sort_by(client):
    with pytest.raises(psycopg2.Error) as error:
        response = client.get("/jobs/?sort_by=invalid_field")
    assert "UndefinedColumn" in (str(error))

def test_get_jobs_invalid_sort_order(client):
    with pytest.raises(psycopg2.Error) as error:
        response = client.get("/jobs/?sort_order=invalid_order")
        print(response.json())
    assert "SyntaxError" in (str(error))
