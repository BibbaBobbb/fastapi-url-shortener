import os

os.environ["REDIS_DB"] = "15"

import pytest
from fastapi.testclient import TestClient

from core.redis_client import redis_client
from main import app


@pytest.fixture
def client():
    redis_client.flushdb()
    with TestClient(app) as test_client:
        yield test_client
    redis_client.flushdb()
