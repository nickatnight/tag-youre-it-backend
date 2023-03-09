def test_health_happy_path(test_app):
    response = test_app.get("/v1/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong!"}
