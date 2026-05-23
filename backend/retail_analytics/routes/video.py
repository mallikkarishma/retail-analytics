import os
import uuid
from flask import Blueprint, request, jsonify
from ..config import Config
from ..cv.motion import detect_motion

video_bp = Blueprint("video", __name__)

@video_bp.route("/analyze", methods=["POST"])
def analyze_video():
    if "video1" not in request.files or "video2" not in request.files:
        return jsonify({"error": "Please upload both video1 and video2"}), 400

    def save_video(file):
        unique_name = f"{uuid.uuid4().hex}.mp4"
        save_path = os.path.join(Config.UPLOAD_FOLDER, unique_name)
        file.save(save_path)
        return save_path

    path1 = save_video(request.files["video1"])
    path2 = save_video(request.files["video2"])

    results = detect_motion(path1, path2)

    suspicious = [r for r in results if r["suspicious"]]

    return jsonify({
        "total_frames"     : len(results),
        "suspicious_frames": len(suspicious),
        "is_suspicious"    : len(suspicious) > 0,
        "details"          : results[:20]
    }), 200