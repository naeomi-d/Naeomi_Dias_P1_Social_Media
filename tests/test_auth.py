import bcrypt
from app.services.auth_service import AuthService


def test_auth_service_hashing_and_registration(db_session):
    user = AuthService.register(
        username="unit_reg_user",
        email="unit_reg@example.com",
        password="SecretPassword123",
        first_name="Unit",
        last_name="Test"
    )
    assert user.id is not None
    assert user.username == "unit_reg_user"
    assert user.password_hash.startswith("$2b$")
    assert bcrypt.checkpw("SecretPassword123".encode("utf-8"), user.password_hash.encode("utf-8"))


def test_api_registration_success(client):
    payload = {
        "username": "new_api_user",
        "email": "new_api@example.com",
        "password": "Password123!",
        "first_name": "New",
        "last_name": "User"
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data["message"] == "Registration successful."
    assert json_data["user"]["username"] == "new_api_user"
    assert "password" not in json_data["user"]
    assert "password_hash" not in json_data["user"]


def test_api_registration_missing_fields(client):
    response = client.post("/api/v1/auth/register", json={"username": "incomplete"})
    assert response.status_code == 400
    assert "required" in response.get_json()["error"].lower()


def test_api_registration_duplicate_username(client, test_user):
    payload = {
        "username": test_user.username,
        "email": "another@example.com",
        "password": "Password123!",
        "first_name": "Another",
        "last_name": "User"
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 422
    assert response.get_json()["error"] == "Username already exists."


def test_api_login_success(client, test_user):
    payload = {
        "username": test_user.username,
        "password": "UserPassword123"
    }
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Login successful."
    assert "access_token" in data
    assert data["user"]["username"] == test_user.username


def test_api_login_incorrect_password(client, test_user):
    payload = {
        "username": test_user.username,
        "password": "WrongPassword!"
    }
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 401
    assert response.get_json()["error"] == "Invalid username or password."


def test_api_login_nonexistent_username(client):
    payload = {
        "username": "ghost_user",
        "password": "Password123"
    }
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 401
    assert response.get_json()["error"] == "Invalid username or password."


def test_api_login_missing_credentials(client):
    response = client.post("/api/v1/auth/login", json={"username": "user_only"})
    assert response.status_code == 400
    assert response.get_json()["error"] == "Username and password are required."


def test_api_login_malformed_json(client):
    response = client.post(
        "/api/v1/auth/login",
        data="invalid_raw_text",
        content_type="application/json"
    )
    assert response.status_code == 400
    assert response.get_json()["error"] == "Request body is required."


def test_protected_endpoint_missing_authorization_header(client):
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401
    assert response.get_json() == {"error": "Authentication required."}


def test_protected_endpoint_invalid_jwt_token(client):
    headers = {"Authorization": "Bearer invalid.jwt.token"}
    response = client.get("/api/v1/users/me", headers=headers)
    assert response.status_code == 401
    assert response.get_json() == {"error": "Invalid authentication token."}


def test_protected_endpoint_malformed_bearer_token(client):
    headers = {"Authorization": "NotBearer invalid_token"}
    response = client.get("/api/v1/users/me", headers=headers)
    assert response.status_code == 401
