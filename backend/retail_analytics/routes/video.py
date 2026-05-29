import os
import uuid
import json
from flask import Blueprint, request, jsonify, Response, stream_with_context
from ..config import Config
from ..cv.motion import detect_motion_stream

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

    aisle_id   = request.form.get("aisle_id", "aisle_1")
    session_id = request.form.get("session_id", str(uuid.uuid4()))

    def generate():
        from ..database import insert_dwell_record
        total_suspicious = 0
        max_dwell = 0
        total_frames = 0

        for result in detect_motion_stream(path1, path2):
            total_frames += 1
            if result["suspicious"]:
                total_suspicious += 1
            if result["dwell_time_sec"] > max_dwell:
                max_dwell = result["dwell_time_sec"]

            yield f"data: {json.dumps(result)}\n\n"

        insert_dwell_record(
            session_id        = session_id,
            aisle_id          = aisle_id,
            video_file        = name2,
            total_frames      = total_frames,
            suspicious_frames = total_suspicious,
            is_suspicious     = total_suspicious > 0,
            dwell_time_sec    = max_dwell
        )

        yield f"data: {json.dumps({'done': True, 'session_id': session_id, 'aisle_id': aisle_id})}\n\n"

    return Response(stream_with_context(generate()), mimetype="text/event-stream")


@video_bp.route("/records", methods=["GET"])
def get_records():
    from ..database import get_all_records
    records = get_all_records()
    return jsonify(records), 200


@video_bp.route("/records/<session_id>", methods=["GET"])
def get_session_records(session_id):
    from ..database import get_records_by_session
    records = get_records_by_session(session_id)
    return jsonify(records), 200