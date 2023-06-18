import pytest
from fastapi.testclient import TestClient

from main import MyApp, app


class TestConstructPayload:
    # note we test the function not the endpoint
    def test_happy(self):
        assert MyApp.construct_payload("test", 1) == "endpoint called with payload: test 1"


class TestEndpoint:
    def test_endpoint(self):
        my_app = MyApp("config/config.yaml")
        with TestClient(app) as client:
            response = client.post("/endpoint", json={"string": "test", "integer": 10})
            assert response.status_code == 200
            assert response.json() == {"message": "endpoint called with payload: test 10"}
