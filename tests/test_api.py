import pytest
import os
from io import BytesIO
import src.api as app_module
from src.api import app
from unittest.mock import patch


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_process_endpoint_no_file(client):
    """Test /process endpoint without file."""
    response = client.post('/process')
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "No file uploaded" in data["error"]


def test_result_endpoint_pending(client):
    """Test /result endpoint for pending task."""
    with patch.object(app_module, 'AsyncResult') as mock_async:
        mock_result = mock_async.return_value
        mock_result.state = "PENDING"

        response = client.get('/result/test-task-id')
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "pending"


def test_result_endpoint_success(client):
    """Test /result endpoint for successful task."""
    with patch('src.api.AsyncResult') as mock_async:
        mock_result = mock_async.return_value
        mock_result.state = "SUCCESS"
        mock_result.result = {"status": "success", "counts": {"A": 1, "T": 1, "C": 1, "G": 1}}

        response = client.get('/result/test-task-id')
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "success"
        assert "result" in data
        assert data["result"]["counts"]["A"] == 1


def test_result_endpoint_failure(client):
    """Test /result endpoint for failed task."""
    with patch.object(app_module, 'AsyncResult') as mock_async:
        mock_result = mock_async.return_value
        mock_result.state = "FAILURE"
        mock_result.result = Exception("Test error")

        response = client.get('/result/test-task-id')
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "failed"
        assert "error" in data