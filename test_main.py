from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_get_recipes():
    response = client.get("/recipes")
    assert response.status_code == 200


def test_create_recipe():
    response = client.post(
        "/recipes",
        json={
            "title": "Test Recipe",
            "cooking_time": 15,
            "description": "Test description",
            "ingredients": [{"name": "Test", "quantity": "1"}],
        },
    )
    assert response.status_code == 201