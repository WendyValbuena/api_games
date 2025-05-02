

# Game of Thrones Character API

This is a RESTful API built with Flask to manage characters from the Game of Thrones universe. It supports character CRUD operations, filtering, pagination, and protected routes using JWT-based authentication.

## Features

- User authentication using JWT
- Protected routes
- Character CRUD operations
- Filtering and pagination
- Pytest-based test coverage

---

## Endpoints

### `/login`
- **Method:** `POST`
- **Description:** Authenticates a user and returns a JWT token.
- **Request Body:**
  ```json
  {
    "username": "user_01",
    "password": "12345qwertz"
  }

Responses:

- **200 OK:** Returns a token.
- **401 Unauthorized:** Invalid credentials.

### `/protected`
- **Method:** GET
- **Description:** Protected route. Requires a valid JWT in the Authorization header.

Responses:

- **200 OK:** Returns a success message.
- **401 Unauthorized:** Missing or invalid token.

### `/characters`
- **Method:** GET
- **Description:** Returns a list of characters. Supports filtering and pagination.

Query Parameters:

- **limit:** Maximum number of characters.
- **skip:** Number of characters to skip.

- **name, house, animal, symbol, nickname, role, strength, death: Filters by field.**
- **age_more_than:** Filter characters older than a certain age.
- **age_less_than:** Filter characters younger than a certain age.

### `/characters/<int:id>`
- **Method:** GET
- **Description:** Returns a specific character by ID.

Responses:

- **200 OK:** Character found.
- **404 Not Found:** Character not found.

### `/characters/filtered`
- **Method:** GET
- **Description:** Returns characters based on advanced filtering (same as /characters)

### `/characters`
- **Method:** POST
- **Description:** Creates a new character.

Request Body Example:

json

  {
    "id": 51,
    "name": "Cersei Lannister",
    "house": "Lannister",
    "animal": null,
    "symbol": "Lion",
    "nickname": "Queen of the Seven Kingdoms",
    "role": "Queen",
    "age": 42,
    "death": 8,
    "strength": "Cunning"
  },

### `/characters/<int:id>`
- **Method:** PUT
- **Description:** Updates a character by ID.

Request Body: Fields to update.

Responses:

- **200 OK:** Character updated.
- **404 Not Found:** Character not found.

### `/characters/<int:id>`
- **Method:** DELETE

Description: Deletes a character by ID.

Responses:

- **200 OK:** Character deleted.
- **404 Not Found:** Character not found


Running Tests and Coverage Report

From the root of the project, run:
PYTHONPATH=. pytest -s -v

To generate an HTML coverage report, run:
PYTHONPATH=. pytest --cov=app --cov-report=html

