import io
import os
import pytest
from unittest.mock import patch
from werkzeug.datastructures import FileStorage

from app.services.file_service import FileService
from app.services.user_service import UserService
from app.services.post_service import PostService
from app.dao.post_dao import PostDAO


def _make_dummy_image(header=b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01", filename="test.jpg", content_type="image/jpeg", size=128):
    data = header + b"\x00" * (size - len(header))
    stream = io.BytesIO(data)
    return FileStorage(stream=stream, filename=filename, content_type=content_type)


def test_valid_image_uploads_saving(app, tmp_upload_dir):
    with app.app_context():
        jpeg_file = _make_dummy_image(b"\xff\xd8\xff\xe0\x00", "test.jpeg", "image/jpeg")
        png_file = _make_dummy_image(b"\x89PNG\r\n\x1a\n", "test.png", "image/png")
        gif_file = _make_dummy_image(b"GIF89a", "test.gif", "image/gif")

        path1 = FileService.save_upload(jpeg_file, "profile_pictures")
        path2 = FileService.save_upload(png_file, "post_images")
        path3 = FileService.save_upload(gif_file, "post_images")

        assert path1.startswith("/uploads/profile_pictures/")
        assert path2.startswith("/uploads/post_images/")
        assert path3.startswith("/uploads/post_images/")

        real_path1 = FileService.get_safe_file_path(path1)
        assert os.path.exists(real_path1)


def test_invalid_extension_and_magic_bytes(app):
    with app.app_context():
        txt_file = FileStorage(stream=io.BytesIO(b"Plain text content"), filename="doc.txt", content_type="text/plain")
        assert FileService.is_allowed_file(txt_file) is False

        renamed_exe = FileStorage(stream=io.BytesIO(b"MZ\x90\x00\x03Executable binary content"), filename="malicious.jpg", content_type="image/jpeg")
        assert FileService.is_allowed_file(renamed_exe) is False

        spoofed_mime = FileStorage(stream=io.BytesIO(b"Not image bytes"), filename="spoofed.png", content_type="image/png")
        assert FileService.is_allowed_file(spoofed_mime) is False


def test_avatar_upload_api_success_and_cleanup(client, test_user, user_headers, tmp_upload_dir):
    data1 = (io.BytesIO(b"\xff\xd8\xff\xe0\x00" + b"\x00" * 100), "avatar1.jpg", "image/jpeg")
    res1 = client.post("/api/v1/users/me/avatar", data={"avatar": data1}, headers=user_headers, content_type="multipart/form-data")
    assert res1.status_code == 200
    first_path = res1.get_json()["user"]["profile_picture"]
    first_real_path = FileService.get_safe_file_path(first_path)
    assert os.path.exists(first_real_path)

    data2 = (io.BytesIO(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100), "avatar2.png", "image/png")
    res2 = client.post("/api/v1/users/me/avatar", data={"avatar": data2}, headers=user_headers, content_type="multipart/form-data")
    assert res2.status_code == 200
    second_path = res2.get_json()["user"]["profile_picture"]
    second_real_path = FileService.get_safe_file_path(second_path)

    assert os.path.exists(second_real_path)
    assert not os.path.exists(first_real_path)


def test_avatar_upload_missing_and_invalid(client, user_headers):
    res_missing = client.post("/api/v1/users/me/avatar", data={}, headers=user_headers, content_type="multipart/form-data")
    assert res_missing.status_code == 400

    bad_data = (io.BytesIO(b"bad text"), "test.txt", "text/plain")
    res_bad = client.post("/api/v1/users/me/avatar", data={"avatar": bad_data}, headers=user_headers, content_type="multipart/form-data")
    assert res_bad.status_code == 400


def test_post_creation_with_and_without_image(client, user_headers):
    res_no_img = client.post("/api/v1/posts", json={"content": "No image post"}, headers=user_headers)
    assert res_no_img.status_code == 201
    assert res_no_img.get_json()["post"]["image_path"] is None

    img_tuple = (io.BytesIO(b"\xff\xd8\xff\xe0\x00" + b"\x00" * 100), "post_img.jpeg", "image/jpeg")
    res_img = client.post("/api/v1/posts", data={"content": "Image post", "image": img_tuple}, headers=user_headers, content_type="multipart/form-data")
    assert res_img.status_code == 201
    image_path = res_img.get_json()["post"]["image_path"]
    assert image_path is not None
    assert os.path.exists(FileService.get_safe_file_path(image_path))


def test_post_image_replacement_and_cleanup(client, user_headers):
    img1 = (io.BytesIO(b"\xff\xd8\xff\xe0\x00" + b"\x00" * 100), "img1.jpeg", "image/jpeg")
    res1 = client.post("/api/v1/posts", data={"content": "Post v1", "image": img1}, headers=user_headers, content_type="multipart/form-data")
    post_id = res1.get_json()["post"]["id"]
    path1 = res1.get_json()["post"]["image_path"]
    real_path1 = FileService.get_safe_file_path(path1)

    img2 = (io.BytesIO(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100), "img2.png", "image/png")
    res2 = client.put(f"/api/v1/posts/{post_id}", data={"image": img2}, headers=user_headers, content_type="multipart/form-data")
    assert res2.status_code == 200
    path2 = res2.get_json()["post"]["image_path"]
    real_path2 = FileService.get_safe_file_path(path2)

    assert os.path.exists(real_path2)
    assert not os.path.exists(real_path1)


def test_oversized_file_upload_returns_413(client, user_headers):
    large_stream = io.BytesIO(b"\xff\xd8\xff\xe0" + b"\x00" * (6 * 1024 * 1024))
    res = client.post("/api/v1/posts", data={"content": "Big img", "image": (large_stream, "huge.jpg", "image/jpeg")}, headers=user_headers, content_type="multipart/form-data")
    assert res.status_code == 413
    assert res.get_json()["error"] == "File size exceeds maximum limit of 5MB."


def test_failed_db_operation_cleans_up_newly_saved_file(app, test_user):
    with app.app_context():
        file_obj = _make_dummy_image(b"\xff\xd8\xff\xe0", "db_fail.jpg", "image/jpeg")

        with patch.object(PostDAO, "create", side_effect=RuntimeError("Database failure simulation")):
            with pytest.raises(RuntimeError):
                PostService.create_post(test_user.id, "Will fail DB", "PUBLIC", image_file=file_obj)

        files_in_dir = os.listdir(os.path.join(app.config["UPLOAD_FOLDER"], "post_images")) if os.path.exists(os.path.join(app.config["UPLOAD_FOLDER"], "post_images")) else []
        assert len(files_in_dir) == 0
