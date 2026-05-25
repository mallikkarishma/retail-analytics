import os
import uuid
from flask import Blueprint, request, jsonify
from ..config import Config
from ..cv.motion import detect_motion
from ..database import insert_dwell_record, get_all_records

video_bp = Blueprint("video", __name__)

@video_bp.route("/analyze", methods=["POST"])
def analyze_video():
    if "video1" not in request.files or "video2" not in request.files:
        return jsonify({"error": "Please upload both video1 and video2"}), 400

    def save_video(file):
        unique_name = f"{uuid.uuid4().hex}.mp4"
        save_path = os.path.join(Config.UPLOAD_FOLDER, unique_name)
        file.save(save_path)
        return save_path, unique_name

    path1, name1 = save_video(request.files["video1"])
    path2, name2 = save_video(request.files["video2"])

    aisle_id = request.form.get("aisle_id", "aisle_1")

    results = detect_motion(path1, path2)

    suspicious = [r for r in results if r["suspicious"]]
    max_dwell = max([r["dwell_time_sec"] for r in results], default=0)

    # Save to database
    insert_dwell_record(
        aisle_id       = aisle_id,
        video_file     = name2,
        total_frames   = len(results),
        suspicious_frames = len(suspicious),
        is_suspicious  = len(suspicious) > 0,
        dwell_time_sec = max_dwell
    )

    return jsonify({
        "total_frames"     : len(results),
        "suspicious_frames": len(suspicious),
        "is_suspicious"    : len(suspicious) > 0,
        "max_dwell_sec"    : max_dwell,
        "aisle_id"         : aisle_id,
        "details"          : results[:20]
    }), 200


@video_bp.route("/records", methods=["GET"])
def get_records():
    records = get_all_records()
    return jsonify(records), 200