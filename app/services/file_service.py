import os
import uuid
from flask import current_app
from werkzeug.utils import secure_filename

ALLOWED_MIME_TYPES = {
    "image/jpeg",
    "image/jpg",
    "image/png",
    "image/gif"
}

class FileService:

    @staticmethod
    def is_allowed_file(file_storage):
        if not file_storage or not file_storage.filename:
            return False
        filename = file_storage.filename
        if "." not in filename:
            return False
        ext = filename.rsplit(".", 1)[1].lower()
        allowed_exts = current_app.config.get("ALLOWED_EXTENSIONS", {"jpg", "jpeg", "png", "gif"})
        if ext not in allowed_exts:
            return False
        content_type = file_storage.content_type
        if content_type and content_type.lower() not in ALLOWED_MIME_TYPES:
            return False
        return True

    @staticmethod
    def save_upload(file_storage, subfolder):
        if not FileService.is_allowed_file(file_storage):
            raise ValueError("Invalid file type. Allowed formats are JPG, JPEG, PNG, and GIF.")

        filename = secure_filename(file_storage.filename)
        ext = filename.rsplit(".", 1)[1].lower() if "." in filename else "jpg"
        unique_name = f"{uuid.uuid4().hex}.{ext}"

        upload_base = current_app.config.get("UPLOAD_FOLDER")
        target_dir = os.path.join(upload_base, subfolder)
        os.makedirs(target_dir, exist_ok=True)

        file_path = os.path.join(target_dir, unique_name)
        file_storage.save(file_path)

        relative_path = f"/uploads/{subfolder}/{unique_name}"
        return relative_path

    @staticmethod
    def cleanup_file(relative_path):
        if not relative_path or not relative_path.startswith("/uploads/"):
            return
        upload_base = current_app.config.get("UPLOAD_FOLDER")
        clean_relative = relative_path.replace("/uploads/", "", 1)
        full_path = os.path.normpath(os.path.join(upload_base, clean_relative))
        if full_path.startswith(upload_base) and os.path.exists(full_path):
            try:
                os.remove(full_path)
            except OSError:
                pass
