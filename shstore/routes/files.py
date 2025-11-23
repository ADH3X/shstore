from flask import Blueprint, send_from_directory, current_app
bp = Blueprint("files", __name__)

UPLOAD_DIR = "/var/data/uploads"

@bp.route("/uploads/<path:filename>")
def uploaded_files(filename):
    upload_dir = current_app.config["UPLOAD_FOLDER"]
    return send_from_directory(upload_dir, filename)