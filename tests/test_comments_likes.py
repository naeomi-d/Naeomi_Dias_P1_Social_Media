import pytest
from app.services.post_service import PostService
from app.services.comment_service import CommentService
from app.services.like_service import LikeService
from app.models.user import User
import bcrypt


def _create_user(db_session, username, email):
    user = User(
        username=username,
        email=email,
        password_hash=bcrypt.hashpw(b"Pass123!", bcrypt.gensalt()).decode("utf-8"),
        first_name="Commenter",
        last_name="User",
        role="USER",
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    return user


def test_create_and_get_comment_api(client, test_user, user_headers):
    post = PostService.create_post(test_user.id, "Post for comment", "PUBLIC")

    create_res = client.post(f"/api/v1/posts/{post.id}/comments", json={"content": "Great post!"}, headers=user_headers)
    assert create_res.status_code == 201
    comment_id = create_res.get_json()["comment"]["id"]

    get_res = client.get(f"/api/v1/posts/{post.id}/comments", headers=user_headers)
    assert get_res.status_code == 200
    assert len(get_res.get_json()["comments"]) == 1
    assert get_res.get_json()["comments"][0]["id"] == comment_id


def test_empty_comment_rejection(client, test_user, user_headers):
    post = PostService.create_post(test_user.id, "Post for empty comment", "PUBLIC")
    res = client.post(f"/api/v1/posts/{post.id}/comments", json={"content": "   "}, headers=user_headers)
    assert res.status_code == 422
    assert res.get_json()["error"] == "Comment cannot be empty."


def test_delete_own_comment(client, test_user, user_headers):
    post = PostService.create_post(test_user.id, "Post for comment deletion", "PUBLIC")
    comment = CommentService.add_comment(test_user.id, post.id, "Deletable comment")

    del_res = client.delete(f"/api/v1/comments/{comment.id}", headers=user_headers)
    assert del_res.status_code == 204

    get_res = client.get(f"/api/v1/comments/{comment.id}", headers=user_headers)
    assert get_res.status_code == 404


def test_cannot_delete_another_users_comment(client, db_session, test_user, user_headers):
    other_user = _create_user(db_session, "comment_owner", "owner@example.com")
    post = PostService.create_post(test_user.id, "Post with other comment", "PUBLIC")
    other_comment = CommentService.add_comment(other_user.id, post.id, "Owner comment")

    del_res = client.delete(f"/api/v1/comments/{other_comment.id}", headers=user_headers)
    assert del_res.status_code == 403
    assert del_res.get_json()["error"] == "You cannot delete another user's comment."


def test_comment_on_nonexistent_post(client, user_headers):
    res = client.post("/api/v1/posts/99999/comments", json={"content": "Ghost comment"}, headers=user_headers)
    assert res.status_code == 404


def test_like_and_unlike_post_api(client, test_user, user_headers):
    post = PostService.create_post(test_user.id, "Post to like", "PUBLIC")

    like_res = client.post(f"/api/v1/posts/{post.id}/likes", headers=user_headers)
    assert like_res.status_code == 201
    assert like_res.get_json()["message"] == "Post liked successfully."

    status_res = client.get(f"/api/v1/posts/{post.id}/like-status", headers=user_headers)
    assert status_res.status_code == 200
    assert status_res.get_json()["liked"] is True

    unlike_res = client.delete(f"/api/v1/posts/{post.id}/likes/me", headers=user_headers)
    assert unlike_res.status_code == 204

    status_res_after = client.get(f"/api/v1/posts/{post.id}/like-status", headers=user_headers)
    assert status_res_after.get_json()["liked"] is False


def test_duplicate_like_handling(client, test_user, user_headers):
    post = PostService.create_post(test_user.id, "Post for duplicate like", "PUBLIC")
    client.post(f"/api/v1/posts/{post.id}/likes", headers=user_headers)

    dup_res = client.post(f"/api/v1/posts/{post.id}/likes", headers=user_headers)
    assert dup_res.status_code == 409
    assert dup_res.get_json()["error"] == "You have already liked this post."


def test_like_nonexistent_post(client, user_headers):
    res = client.post("/api/v1/posts/99999/likes", headers=user_headers)
    assert res.status_code == 404


def test_unauthenticated_like_attempt(client):
    res = client.post("/api/v1/posts/1/likes")
    assert res.status_code == 401
