from types import SimpleNamespace
from unittest.mock import patch
import pytest

from app.services.post_service import PostService
from app.services.user_service import UserService
from app.services.file_service import FileService
from app.dao.post_dao import PostDAO
from app.dao.user_dao import UserDAO


def test_unit_mock_dao_lookup_in_post_service():
    fake_post = SimpleNamespace(id=42, user_id=10, content="Fake post", visibility="PUBLIC", status="ACTIVE")
    with patch.object(PostDAO, "find_by_id", return_value=fake_post):
        result = PostService.get_post_for_viewer(42, viewer_id=10)
        assert result is fake_post
        assert result.content == "Fake post"


def test_unit_mock_file_service_save_upload():
    fake_file = SimpleNamespace(filename="photo.png")
    with patch.object(FileService, "save_upload", return_value="/uploads/post_images/mocked_uuid.png") as mock_save:
        with patch.object(PostDAO, "create"):
            with patch("app.db.session.flush"):
                with patch("app.db.session.commit"):
                    post = PostService.create_post(user_id=1, content="Post with mock img", visibility="PUBLIC", image_file=fake_file)
                    mock_save.assert_called_once_with(fake_file, "post_images")
                    assert post.image_path == "/uploads/post_images/mocked_uuid.png"


def test_unit_mock_file_cleanup_on_replacement():
    fake_post = SimpleNamespace(id=1, user_id=5, content="Post", visibility="PUBLIC", status="ACTIVE", image_path="/uploads/post_images/old.jpg")
    fake_new_file = SimpleNamespace(filename="new.jpg")

    with patch.object(PostDAO, "find_by_id", return_value=fake_post):
        with patch.object(FileService, "save_upload", return_value="/uploads/post_images/new.jpg"):
            with patch.object(FileService, "cleanup_file") as mock_cleanup:
                with patch("app.dao.post_hashtag_dao.PostHashtagDAO.delete_by_post_id"):
                    with patch("app.db.session.flush"):
                        with patch.object(PostDAO, "update"):
                            with patch("app.db.session.commit"):
                                PostService.update_post(1, 5, content="Post updated", visibility="PUBLIC", image_file=fake_new_file)
                                mock_cleanup.assert_called_once_with("/uploads/post_images/old.jpg")


def test_unit_mock_db_failure_triggers_cleanup(app):
    fake_file = SimpleNamespace(filename="fail.jpg")
    with app.app_context():
        with patch.object(FileService, "save_upload", return_value="/uploads/post_images/fail.jpg"):
            with patch.object(FileService, "cleanup_file") as mock_cleanup:
                with patch.object(PostDAO, "create", side_effect=ValueError("Simulated DB fail")):
                    with pytest.raises(ValueError, match="Simulated DB fail"):
                        PostService.create_post(1, "Post fail", "PUBLIC", image_file=fake_file)
                    mock_cleanup.assert_called_once_with("/uploads/post_images/fail.jpg")


def test_unit_mock_user_dao_avatar_update():
    fake_user = SimpleNamespace(id=7, profile_picture="/uploads/profile_pictures/old_avatar.jpg")
    fake_avatar_file = SimpleNamespace(filename="avatar.png")

    with patch.object(UserService, "get_user", return_value=fake_user):
        with patch.object(FileService, "save_upload", return_value="/uploads/profile_pictures/new_avatar.png"):
            with patch.object(UserDAO, "update") as mock_update:
                with patch.object(FileService, "cleanup_file") as mock_cleanup:
                    UserService.update_avatar(7, fake_avatar_file)
                    mock_update.assert_called_once_with(fake_user)
                    assert fake_user.profile_picture == "/uploads/profile_pictures/new_avatar.png"
                    mock_cleanup.assert_called_once_with("/uploads/profile_pictures/old_avatar.jpg")
