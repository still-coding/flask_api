import pytest

from ..main import app


@pytest.fixture()
def client():
    yield app.test_client()


@pytest.mark.html_endpoints
@pytest.mark.parametrize(
    "route, response_data_part",
    [["/", "swagger-ui"], ["/keys_page/", "table-hover table-striped table-dark"]],
)
def test_html_pages(client, route, response_data_part):
    response = client.get(route)
    assert response.status_code == 200
    data = response.data.decode("utf-8")
    assert data.startswith("<!DOCTYPE html>")
    assert response_data_part in data


@pytest.mark.json_endpoints
def test_no_keys(client):
    response = client.get("/keys/")
    assert response.status_code == 200
    assert response.json == []


@pytest.mark.json_endpoints
def test_can_create(client):
    payload = {"key": "test_key0", "value": "test_value0"}
    response = client.post("/keys/", json=payload)
    assert response.status_code == 201
    assert response.json == payload


@pytest.mark.json_endpoints
def test_cant_create_same(client):
    payload = {"key": "test_key0", "value": "test_value0"}
    response = client.post("/keys/", json=payload)
    assert response.status_code == 409


@pytest.fixture()
def create_3_keys(client):
    for i in range(1, 4):
        payload = {"key": f"test_key{i}", "value": f"test_value{i}"}
        client.post("/keys/", json=payload)


@pytest.mark.json_endpoints
def test_can_get_all_4_keys(client, create_3_keys):
    expected = []
    for i in range(4):
        expected.append({"key": f"test_key{i}", "value": f"test_value{i}"})
    response = client.get("/keys/")
    assert response.status_code == 200
    assert len(response.json) == 4
    assert response.json == expected


@pytest.mark.json_endpoints
def test_can_get_single_value(client):
    expected_value = "test_value2"
    key = "test_key2"
    response = client.get(f"/keys/{key}")
    assert response.status_code == 200
    assert response.json == {"key": key, "value": expected_value}


@pytest.mark.json_endpoints
def test_cant_get_absent_key(client):
    key = "brnlfjlnngjlxbkfkfjh"
    response = client.get(f"/keys/{key}")
    assert response.status_code == 404


@pytest.mark.json_endpoints
def test_can_change_value(client):
    key = "test_key1"
    payload = {"value": "test_value420"}
    response = client.put(f"/keys/{key}", json=payload)
    assert response.status_code == 200
    assert response.json == {"key": key, "value": payload["value"]}


@pytest.mark.json_endpoints
def test_cant_change_value_of_absent_key(client):
    key = "brnlfjlnngjlxbkfkfjh"
    response = client.put(f"/keys/{key}", json={"value": "test_value420"})
    assert response.status_code == 404


@pytest.mark.json_endpoints
def test_cant_change_value_without_value(client):
    key = "test_key0"
    response = client.put(f"/keys/{key}", json={})
    assert response.status_code == 400


@pytest.mark.json_endpoints
def test_cant_change_value_without_payload(client):
    key = "test_key0"
    response = client.put(f"/keys/{key}")
    assert response.status_code == 415
