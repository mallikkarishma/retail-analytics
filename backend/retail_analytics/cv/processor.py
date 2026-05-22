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

    # Save processed image back to same path
    processed_path = image_path.replace("uploads", "logs").replace(".jpg", "_processed.jpg")
    cv2.imwrite(processed_path, resized)

    return processed_path