import requests
import os

from core.main import app
from fastapi.testclient import TestClient
from decouple import config

HOST_URL = os.getenv("HOST_URL", config("HOST_URL"))
client = TestClient(app)


def test_api_main_endpoint():
    response = requests.get(HOST_URL)
    assert response.status_code == 200


def test_404_not_found():
    server_response = requests.get(HOST_URL + 'api/v1/daily-return/7f087edc-f06c-4bde-8159-236f36219d59')
    assert server_response.status_code == 404
