import cv2
from ..config import Config

def process_frame(image_path: str) -> str:
    # Read the image
    frame = cv2.imread(image_path)

    if frame is None:
        raise ValueError(f"Could not read image: {image_path}")

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Resize to standard canvas size
    resized = cv2.resize(gray, (Config.CANVAS_WIDTH, Config.CANVAS_HEIGHT))

    # Save processed image
    processed_path = image_path.replace("uploads", "logs").replace(".jpg", "_processed.jpg")
    cv2.imwrite(processed_path, resized)

    return processed_path


def subtract_background(frame1_path: str, frame2_path: str) -> str:
    # Read both frames
    frame1 = cv2.imread(frame1_path, cv2.IMREAD_GRAYSCALE)
    frame2 = cv2.imread(frame2_path, cv2.IMREAD_GRAYSCALE)

    # Resize both to same size
    frame1 = cv2.resize(frame1, (Config.CANVAS_WIDTH, Config.CANVAS_HEIGHT))
    frame2 = cv2.resize(frame2, (Config.CANVAS_WIDTH, Config.CANVAS_HEIGHT))

    # Find the difference between the two frames
    diff = cv2.absdiff(frame1, frame2)

    # Apply threshold to highlight moving pixels
    _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

    # Save the result
    diff_path = frame2_path.replace("uploads", "logs").replace(".jpg", "_diff.jpg")
    cv2.imwrite(diff_path, thresh)

    return diff_path