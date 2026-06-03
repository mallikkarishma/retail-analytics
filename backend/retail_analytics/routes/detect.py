import os
import uuid
from flask import Blueprint, request, jsonify
from ..config import Config
from ..ml.yolo_detector import detect_objects, detect_from_video
from ..ml.inference_worker import submit_job, get_result

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

    job_id = str(uuid.uuid4())
    submit_job(job_id, save_path, job_type="image")

    return jsonify({
        "job_id"  : job_id,
        "filename": unique_name,
        "status"  : "processing"
    }), 202


@detect_bp.route("/detect/result/<job_id>", methods=["GET"])
def detect_result(job_id):
    result = get_result(job_id)
    return jsonify(result), 200


@detect_bp.route("/detect-video", methods=["POST"])
def detect_video():
    if "video" not in request.files:
        return jsonify({"error": "No video provided"}), 400

    file = request.files["video"]
    unique_name = f"{uuid.uuid4().hex}.mp4"
    save_path = os.path.join(Config.UPLOAD_FOLDER, unique_name)
    file.save(save_path)

    job_id = str(uuid.uuid4())
    submit_job(job_id, save_path, job_type="video")

    return jsonify({
        "job_id"  : job_id,
        "filename": unique_name,
        "status"  : "processing"
    }), 202