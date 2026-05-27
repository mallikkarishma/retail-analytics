import os
import uuid
from flask import Blueprint, request, jsonify
from ..config import Config
from ..ml.yolo_detector import detect_objects, detect_from_video

detect_bp = Blueprint("detect", __name__)

@detect_bp.route("/detect", methods=["POST"])
def detect():
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    file = request.files["image"]
    ext = file.filename.rsplit(".", 1)[1].lower()
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    save_path = os.path.join(Config.UPLOAD_FOLDER, unique_name)
    file.save(save_path)

    results = detect_objects(save_path)

    return jsonify({
        "filename"  : unique_name,
        "persons"   : results["persons"],
        "carts"     : results["carts"],
        "detections": results["detections"]
    }), 200


@detect_bp.route("/detect-video", methods=["POST"])
def detect_video():
    if "video" not in request.files:
        return jsonify({"error": "No video provided"}), 400

    file = request.files["video"]
    unique_name = f"{uuid.uuid4().hex}.mp4"
    save_path = os.path.join(Config.UPLOAD_FOLDER, unique_name)
    file.save(save_path)

    results = detect_from_video(save_path)

    return jsonify({
        "filename"       : unique_name,
        "total_persons"  : results["total_persons"],
        "total_carts"    : results["total_carts"],
        "frames_analyzed": results["frames_analyzed"],
        "frame_results"  : results["frame_results"]
    }), 200