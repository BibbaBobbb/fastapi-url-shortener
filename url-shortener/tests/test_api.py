def test_create_short_url(client):
    response = client.post(
        "/api/v1/short-urls/",
        json={"target_url": "https://google.com", "slug": "test"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["slug"] == "test"
    assert data["visits"] == 0


def test_create_short_url_generates_slug(client):
    response = client.post(
        "/api/v1/short-urls/",
        json={"target_url": "https://google.com"},
    )
    assert response.status_code == 201
    assert len(response.json()["slug"]) == 6


def test_create_duplicate_slug_returns_409(client):
    body = {"target_url": "https://google.com", "slug": "test"}
    client.post("/api/v1/short-urls/", json=body)
    response = client.post("/api/v1/short-urls/", json=body)
    assert response.status_code == 409


def test_redirect_and_count_visits(client):
    client.post(
        "/api/v1/short-urls/",
        json={"target_url": "https://google.com", "slug": "test"},
    )

    response = client.get("/r/test", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "https://google.com/"

    client.get("/r/test", follow_redirects=False)
    details = client.get("/api/v1/short-urls/test/")
    assert details.json()["visits"] == 2


def test_redirect_not_found(client):
    response = client.get("/r/nope", follow_redirects=False)
    assert response.status_code == 404


def test_partial_update(client):
    client.post(
        "/api/v1/short-urls/",
        json={"target_url": "https://google.com", "slug": "test", "description": "old"},
    )
    response = client.patch(
        "/api/v1/short-urls/test/",
        json={"target_url": "https://ya.ru"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["target_url"] == "https://ya.ru/"
    assert data["description"] == "old"


def test_delete_short_url(client):
    client.post(
        "/api/v1/short-urls/",
        json={"target_url": "https://google.com", "slug": "test"},
    )
    response = client.delete("/api/v1/short-urls/test/")
    assert response.status_code == 204

    response = client.get("/api/v1/short-urls/test/")
    assert response.status_code == 404
