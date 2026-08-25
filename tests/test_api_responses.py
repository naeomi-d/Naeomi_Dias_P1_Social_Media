import io
import pytest
from app.services.post_service import PostService


def test_status_200_ok(client, user_headers):
    res = client.get("/api/v1/users/me", headers=user_headers)
    assert res.status_code == 200
    assert res.content_type == "application/json"
    assert "user" in res.get_json()


def test_status_201_created(client, user_headers):
    res = client.post("/api/v1/posts", json={"content": "201 Created test"}, headers=user_headers)
    assert res.status_code == 201
    assert res.content_type == "application/json"
    assert "post" in res.get_json()


def test_status_204_no_content(client, test_user, user_headers):
    post = PostService.create_post(test_user.id, "Post for 204", "PUBLIC")
    res = client.delete(f"/api/v1/posts/{post.id}", headers=user_headers)
    assert res.status_code == 204
    assert res.data == b""


def test_status_400_bad_request(client, user_headers):
    res = client.post("/api/v1/posts", data="raw_not_json", headers=user_headers, content_type="application/json")
    assert res.status_code == 400
    assert res.content_type == "application/json"
    assert "error" in res.get_json()


def test_status_401_unauthorized(client):
    res = client.get("/api/v1/posts")
    assert res.status_code == 401
    assert res.content_type == "application/json"
    assert res.get_json() == {"error": "Authentication required."}


def test_status_403_forbidden(client, user_headers):
    res = client.get("/api/v1/reports", headers=user_headers)
    assert res.status_code == 403
    assert res.content_type == "application/json"
    assert res.get_json() == {"error": "Access denied."}


def test_status_404_not_found(client, user_headers):
    res = client.get("/api/v1/posts/999999", headers=user_headers)
    assert res.status_code == 404
    assert res.content_type == "application/json"
    assert res.get_json() == {"error": "Post not found."}


def test_status_409_conflict(client, test_user, user_headers):
    post = PostService.create_post(test_user.id, "Post for 409", "PUBLIC")
    client.post(f"/api/v1/posts/{post.id}/likes", headers=user_headers)
    dup_res = client.post(f"/api/v1/posts/{post.id}/likes", headers=user_headers)
    assert dup_res.status_code == 409
    assert dup_res.content_type == "application/json"
    assert "error" in dup_res.get_json()


def test_status_413_payload_too_large(client, user_headers):
    huge_stream = io.BytesIO(b"\xff\xd8\xff\xe0" + b"\x00" * (6 * 1024 * 1024))
    res = client.post("/api/v1/posts", data={"content": "Huge", "image": (huge_stream, "big.jpg", "image/jpeg")}, headers=user_headers, content_type="multipart/form-data")
    assert res.status_code == 413
    assert res.content_type == "application/json"
    assert res.get_json() == {"error": "File size exceeds maximum limit of 5MB."}


def test_status_422_unprocessable_entity(client, user_headers):
    res = client.post("/api/v1/posts", json={"content": "  "}, headers=user_headers)
    assert res.status_code == 422
    assert res.content_type == "application/json"
    assert res.get_json() == {"error": "Post content cannot be empty."}
