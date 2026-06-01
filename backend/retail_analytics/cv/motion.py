import cv2
import json
import os
import time
import base64
from datetime import datetime
from ..config import Config

PIXEL_CHANGE_THRESHOLD = 15000
SUSPICIOUS_TIME_LIMIT  = 10

def detect_motion_stream(video1_path: str, video2_path: str):
    cap1 = cv2.VideoCapture(video1_path)
    cap2 = cv2.VideoCapture(video2_path)

    fps = cap2.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        fps = 25

    frame_count = 0
    suspicious_frames = 0

    while True:
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()

        if not ret1 or not ret2:
            break

        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

        diff = cv2.absdiff(gray1, gray2)
        _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

        changed_pixels = cv2.countNonZero(thresh)
        current_time = round(frame_count / fps, 2)

        if changed_pixels > PIXEL_CHANGE_THRESHOLD:
            suspicious_frames += 1
        else:
            suspicious_frames = 0

        dwell_time = round(suspicious_frames / fps, 2)
        is_suspicious = dwell_time >= SUSPICIOUS_TIME_LIMIT

        if frame_count % 10 == 0:
            display = cv2.resize(frame2, (320, 240))
            _, buffer = cv2.imencode('.jpg', display, [cv2.IMWRITE_JPEG_QUALITY, 60])
            frame_b64 = base64.b64encode(buffer).decode('utf-8')

            yield {
                "frame"          : frame_count,
                "time_sec"       : current_time,
                "changed_pixels" : changed_pixels,
                "dwell_time_sec" : dwell_time,
                "suspicious"     : is_suspicious,
                "image"          : frame_b64
            }
            # Sleep to match real video speed
            time.sleep(10 / fps)

        frame_count += 1

    cap1.release()
    cap2.release()


def detect_motion(video1_path: str, video2_path: str):
    results = list(detect_motion_stream(video1_path, video2_path))

    log_entry = {
        "timestamp"        : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_frames"     : len(results),
        "suspicious_frames": len([r for r in results if r["suspicious"]]),
        "is_suspicious"    : any(r["suspicious"] for r in results),
        "results"          : results
    }

    log_path = os.path.join(Config.LOG_DIR, "motion_log.json")

    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            log = json.load(f)
    else:
        log = []

    log.append(log_entry)

    with open(log_path, "w") as f:
        json.dump(log, f, indent=4)

    return results