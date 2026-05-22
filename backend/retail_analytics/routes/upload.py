import os
import uuid
from flask import Blueprint, request, jsonify
from ..config import Config
from ..metadata import extract_and_log
from ..cv.processor import process_frame

upload_bp = Blueprint("upload", __name__)

def allowed_file(filename):
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@upload_bp.route("/upload", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        return jsonify({"error": "No image part in request"}), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed"}), 400

    ext = file.filename.rsplit(".", 1)[1].lower()
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    save_path = os.path.join(Config.UPLOAD_FOLDER, unique_name)

    file.save(save_path)

    # Log metadata
    metadata = extract_and_log(unique_name)

    # Process frame - grayscale and resize
    processed_path = process_frame(save_path)

    return jsonify({
        "message"       : "Image uploaded and processed successfully",
        "filename"      : unique_name,
        "metadata"      : metadata,
        "processed_path": processed_path
    }), 201