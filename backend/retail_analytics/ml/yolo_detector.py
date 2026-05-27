from ultralytics import YOLO
import cv2
import os

# Load pretrained YOLO model
model = YOLO("yolov8n.pt")

# Classes we care about
TARGET_CLASSES = {
    0: "person",
    63: "shopping cart"
}

def detect_objects(image_path: str) -> dict:
    results = model(image_path, verbose=False)

    persons = 0
    carts = 0
    detections = []

    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            confidence = round(float(box.conf[0]), 2)

            if confidence < 0.5:
                continue
            if class_id in TARGET_CLASSES:
                label = TARGET_CLASSES[class_id]

                if label == "person":
                    persons += 1
                elif label == "shopping cart":
                    carts += 1

                detections.append({
                    "label"     : label,
                    "confidence": confidence,
                    "bbox"      : box.xyxy[0].tolist()
                })

    return {
        "persons"   : persons,
        "carts"     : carts,
        "detections": detections
    }


def detect_from_video(video_path: str, sample_every: int = 30) -> dict:
    cap = cv2.VideoCapture(video_path)

    frame_count = 0
    total_persons = 0
    total_carts = 0
    frame_results = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Only process every Nth frame
        if frame_count % sample_every == 0:
            # Save frame temporarily
            temp_path = f"temp_frame_{frame_count}.jpg"
            cv2.imwrite(temp_path, frame)

            # Run YOLO on frame
            result = detect_objects(temp_path)
            os.remove(temp_path)

            total_persons += result["persons"]
            total_carts   += result["carts"]

            frame_results.append({
                "frame"  : frame_count,
                "persons": result["persons"],
                "carts"  : result["carts"]
            })

        frame_count += 1

    cap.release()

    return {
        "total_persons": total_persons,
        "total_carts"  : total_carts,
        "frames_analyzed": len(frame_results),
        "frame_results": frame_results
    }