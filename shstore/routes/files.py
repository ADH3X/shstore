from flask import Blueprint, send_from_directory
import os

bp = Blueprint("files", __name__)

UPLOAD_DIR = "/var/data/uploads"

@bp.route("/uploads/<path:filename>")
def uploaded_files(filename):
    return send_from_directory(UPLOAD_DIR, filename)
