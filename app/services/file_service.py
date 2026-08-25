import os
import uuid
from flask import current_app
from werkzeug.utils import secure_filename

from app.exceptions.validation_exceptions import ValidationError

ALLOWED_MIME_TYPES = {
    "image/jpeg",
    "image/jpg",
    "image/pjpeg",
    "image/png",
    "image/x-png",
    "image/gif"
}

class FileService:

    @staticmethod
    def verify_image_signature(file_storage):
        if not file_storage or not hasattr(file_storage, "stream"):
            return False
        try:
            pos = file_storage.stream.tell()
            header = file_storage.stream.read(16)
            file_storage.stream.seek(pos)
        except Exception:
            return False
        if not header or len(header) < 4:
            return False
        if header.startswith(b"\xff\xd8\xff"):
            return True
        if header.startswith(b"\x89PNG\r\n\x1a\n"):
            return True
        if header.startswith(b"GIF87a") or header.startswith(b"GIF89a"):
            return True
        return False

    @staticmethod
    def is_allowed_file(file_storage):
        if not file_storage or not file_storage.filename:
            return False
        filename = file_storage.filename.strip()
        if not filename or "." not in filename:
            return False
        ext = filename.rsplit(".", 1)[1].lower()
        allowed_exts = current_app.config.get("ALLOWED_EXTENSIONS", {"jpg", "jpeg", "png", "gif"})
        if ext not in allowed_exts:
            return False
        content_type = file_storage.content_type
        if content_type and content_type.lower() not in ALLOWED_MIME_TYPES:
            return False
        return FileService.verify_image_signature(file_storage)

    @staticmethod
    def save_upload(file_storage, subfolder):
        if not FileService.is_allowed_file(file_storage):
            raise ValueError("Invalid file type. Only valid JPG, JPEG, PNG, and GIF images are allowed.")

        if subfolder not in {"profile_pictures", "post_images"}:
            raise ValidationError("Invalid upload target directory.")

        filename = secure_filename(file_storage.filename)
        ext = filename.rsplit(".", 1)[1].lower() if "." in filename else "jpg"
        unique_name = f"{uuid.uuid4().hex}.{ext}"

        upload_base = os.path.realpath(current_app.config.get("UPLOAD_FOLDER"))
        target_dir = os.path.realpath(os.path.join(upload_base, subfolder))

        if not target_dir.startswith(upload_base + os.sep) and target_dir != upload_base:
            raise ValidationError("Invalid target path.")

        os.makedirs(target_dir, exist_ok=True)
        file_path = os.path.join(target_dir, unique_name)
        file_storage.save(file_path)

        return f"/uploads/{subfolder}/{unique_name}"

    @staticmethod
    def get_safe_file_path(relative_path):
        if not relative_path or not relative_path.startswith("/uploads/"):
            return None
        upload_base = os.path.realpath(current_app.config.get("UPLOAD_FOLDER"))
        clean_relative = relative_path.replace("/uploads/", "", 1)
        target_path = os.path.realpath(os.path.join(upload_base, clean_relative))
        if not target_path.startswith(upload_base + os.sep):
            return None
        return target_path

    @staticmethod
    def cleanup_file(relative_path):
        target_path = FileService.get_safe_file_path(relative_path)
        if target_path and os.path.exists(target_path) and os.path.isfile(target_path):
            try:
                os.remove(target_path)
            except OSError:
                pass
