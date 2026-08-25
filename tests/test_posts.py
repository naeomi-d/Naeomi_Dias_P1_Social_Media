import pytest
from app.services.post_service import PostService
from app.services.follow_service import FollowService
from app.models.user import User
import bcrypt


def _create_user(db_session, username, email):
    user = User(
        username=username,
        email=email,
        password_hash=bcrypt.hashpw(b"Pass123!", bcrypt.gensalt()).decode("utf-8"),
        first_name="Test",
        last_name="User",
        role="USER",
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    return user


def test_create_post_service(app, test_user):
    with app.app_context():
        post = PostService.create_post(
            user_id=test_user.id,
            content="Hello world! #testing #flask",
            visibility="PUBLIC"
        )
        assert post.id is not None
        assert post.content == "Hello world! #testing #flask"
        assert post.visibility == "PUBLIC"
        assert post.status == "ACTIVE"
        assert len(post.hashtags) == 2


def test_api_create_and_get_post(client, test_user, user_headers):
    payload = {"content": "API post content", "visibility": "PUBLIC"}
    create_res = client.post("/api/v1/posts", json=payload, headers=user_headers)
    assert create_res.status_code == 201
    post_id = create_res.get_json()["post"]["id"]

    get_res = client.get(f"/api/v1/posts/{post_id}", headers=user_headers)
    assert get_res.status_code == 200
    assert get_res.get_json()["post"]["content"] == "API post content"


def test_update_own_post_api(client, test_user, user_headers):
    create_res = client.post("/api/v1/posts", json={"content": "Original content"}, headers=user_headers)
    post_id = create_res.get_json()["post"]["id"]

    update_res = client.patch(f"/api/v1/posts/{post_id}", json={"content": "Updated content"}, headers=user_headers)
    assert update_res.status_code == 200
    assert update_res.get_json()["post"]["content"] == "Updated content"


def test_update_another_users_post_forbidden(client, db_session, user_headers):
    other_user = _create_user(db_session, "other_author", "other@example.com")
    post = PostService.create_post(other_user.id, "Other user post", "PUBLIC")

    response = client.patch(f"/api/v1/posts/{post.id}", json={"content": "Hacked content"}, headers=user_headers)
    assert response.status_code == 403
    assert response.get_json()["error"] == "You cannot edit another user's post."


def test_delete_own_post_api(client, user_headers):
    create_res = client.post("/api/v1/posts", json={"content": "Post to delete"}, headers=user_headers)
    post_id = create_res.get_json()["post"]["id"]

    del_res = client.delete(f"/api/v1/posts/{post_id}", headers=user_headers)
    assert del_res.status_code == 204

    get_res = client.get(f"/api/v1/posts/{post_id}", headers=user_headers)
    assert get_res.status_code == 404


def test_deleted_post_cannot_be_edited(client, user_headers):
    create_res = client.post("/api/v1/posts", json={"content": "Soon deleted"}, headers=user_headers)
    post_id = create_res.get_json()["post"]["id"]

    client.delete(f"/api/v1/posts/{post_id}", headers=user_headers)
    edit_res = client.patch(f"/api/v1/posts/{post_id}", json={"content": "New content"}, headers=user_headers)
    assert edit_res.status_code == 422
    assert edit_res.get_json()["error"] == "Cannot edit a deleted post."


def test_delete_another_users_post_forbidden(client, db_session, user_headers):
    other_user = _create_user(db_session, "other_author2", "other2@example.com")
    post = PostService.create_post(other_user.id, "Other post", "PUBLIC")

    del_res = client.delete(f"/api/v1/posts/{post.id}", headers=user_headers)
    assert del_res.status_code == 403
    assert del_res.get_json()["error"] == "You cannot delete another user's post."


def test_empty_content_rejection(client, user_headers):
    response = client.post("/api/v1/posts", json={"content": "   "}, headers=user_headers)
    assert response.status_code == 422
    assert response.get_json()["error"] == "Post content cannot be empty."


def test_invalid_visibility_rejection(client, user_headers):
    response = client.post("/api/v1/posts", json={"content": "Test", "visibility": "INVALID"}, headers=user_headers)
    assert response.status_code == 422
    assert response.get_json()["error"] == "Invalid post visibility."


def test_private_post_visibility_restriction(client, db_session, test_user, user_headers):
    private_post = PostService.create_post(test_user.id, "Private secret", "PRIVATE")

    other_user = _create_user(db_session, "viewer_user", "viewer@example.com")
    from flask_jwt_extended import create_access_token
    with client.application.app_context():
        token = create_access_token(identity=str(other_user.id), additional_claims={"role": "USER"})
        other_headers = {"Authorization": f"Bearer {token}"}

    own_res = client.get(f"/api/v1/posts/{private_post.id}", headers=user_headers)
    assert own_res.status_code == 200

    other_res = client.get(f"/api/v1/posts/{private_post.id}", headers=other_headers)
    assert other_res.status_code == 403
    assert "private" in other_res.get_json()["error"].lower()


def test_followers_post_visibility_restriction(client, db_session, test_user, user_headers):
    follower_post = PostService.create_post(test_user.id, "For followers", "FOLLOWERS")
    other_user = _create_user(db_session, "follower_candidate", "cand@example.com")

    from flask_jwt_extended import create_access_token
    with client.application.app_context():
        token = create_access_token(identity=str(other_user.id), additional_claims={"role": "USER"})
        other_headers = {"Authorization": f"Bearer {token}"}

    non_follower_res = client.get(f"/api/v1/posts/{follower_post.id}", headers=other_headers)
    assert non_follower_res.status_code == 403

    FollowService.follow_user(other_user.id, test_user.id)
    follower_res = client.get(f"/api/v1/posts/{follower_post.id}", headers=other_headers)
    assert follower_res.status_code == 200
