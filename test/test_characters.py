import pytest
from app.__init__ import create_app
from app.routers.characters import characters_bp
import random
import jwt
import json
import logging

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    
    return app 
def get_auth_token(client):
    login_data = {
        "username": "user_01",
        "password": "12345qwertz"
    }
    response = client.post('/login', json=login_data)
    assert response.status_code == 200
    return response.get_json()["token"]

# 1.GET /home
def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"API de Game of Thrones" in response.data

# 2. GET /characters
def test_get_characters(client):
    response = client.get('/characters')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)
    
# 3. GET /characters?limit=5&skip=0
def test_get_characters_limit_skip(client):
    response = client.get('/characters?limit=5&skip=0')
    data = response.get_json()
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) <= 5

# 4. GET /characters/47
def test_get_character_by_id(client):

    response_valid = client.get('/characters/47')
    assert response_valid.status_code in [200, 404]
    
    response_invalid = client.get('/characters/99')
    assert response_invalid.status_code == 404

# 5. GET /characters/filtered?name=...
def test_filter_characters_by_name(client):
    response = client.get('/characters/filtered?name=jon')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)
    
# 6. POST /characters = new character
def test_add_character(client):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    new_character = {
        "id": None,
        "name": "name of the character",
        "house": "house of the character",
        "animal": "animal of the character",
        "symbol": "symbol of the character",
        "nickname": "nickname of the character",
        "role": "role of the character",
        "strength": "strength of the character",
        "age": 30,
        "death": None
    }

    response = client.post('/characters', json=new_character, headers=headers)
    assert response.status_code == 201

    created = response.get_json()
    assert "id" in created

# 7. PUT /characters/12 = update character
def test_update_character(client):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    response_post = client.post('/characters', json={
        "id": None,
        "name": "Character to update",
        "house": "name of the house",
        "animal": "name of the animal",
        "symbol": "name of the symbol",
        "nickname": "nickname",
        "role": "role",
        "strength": "strength",
        "age": 29,
        "death": None
    }, headers=headers)

    created = response_post.get_json()
    assert "id" in created
    character_id = created["id"]

    updated_data = {
        "name": "Updated Character",
        "house": "Updated House",
        "animal": "Dragon",
        "symbol": "Flame",
        "nickname": "Flamy",
        "role": "King",
        "strength": "Extreme",
        "age": 40,
        "death": None
    }

    response_put = client.put(f"/characters/{character_id}", json=updated_data, headers=headers)
    assert response_put.status_code == 200

    updated = response_put.get_json()
    assert updated["name"] == "Updated Character"
    assert updated["animal"] == "Dragon"

# 8. DELETE /characters/33
def test_delete_existing_character(client):
    
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    
    character_id = random.randint(1, 100) 
    response = client.delete(f'/characters/{character_id}', headers=headers)
   
    assert response.status_code in [200, 404]

    if response.status_code == 200:
        assert "has been deleted" in response.get_json()["message"]
    else:
        assert response.get_json()["error"] == "Character not found"


@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()