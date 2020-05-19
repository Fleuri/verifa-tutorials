import pytest

from app import APP


@pytest.fixture(name="client")
def fixture_client():  # type: ignore
    APP.config["TESTING"] = True
    yield APP.test_client()


def test_api(client):  # type: ignore
    assert b"whoami" in client.get("/api/whoami").data


def test_index(client):  # type: ignore
    assert b"Working" in client.get("/").data
