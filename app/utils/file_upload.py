import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app


ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}


def allowed_file(filename):
    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def save_student_photo(file):
    """
    Save uploaded student photo and return filename.
    """

    if not file or file.filename == "":
        return None

    if not allowed_file(file.filename):
        raise ValueError("Invalid file type")

    # Generate unique filename
    ext = file.filename.rsplit(".", 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"

    upload_folder = os.path.join(
        current_app.root_path,
        "static",
        "uploads",
        "students"
    )

    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, secure_filename(filename))
    file.save(file_path)

    return filename


def delete_student_photo(filename):
    """
    Delete student photo from storage.
    """

    if not filename:
        return

    file_path = os.path.join(
        current_app.root_path,
        "static",
        "uploads",
        "students",
        filename
    )

    if os.path.exists(file_path):
        os.remove(file_path)