import os
import json
from datetime import datetime
from .config import Config

def extract_and_log(filename: str) -> dict:
    filepath = os.path.join(Config.UPLOAD_FOLDER, filename)

    # Extract metadata
    stat = os.stat(filepath)
    metadata = {
        "filename"  : filename,
        "size_bytes": stat.st_size,
        "uploaded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Save to JSON log
    log_path = os.path.join(Config.LOG_DIR, "metadata_log.json")

    # Load existing log or start fresh
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            log = json.load(f)
    else:
        log = []

    log.append(metadata)

    with open(log_path, "w") as f:
        json.dump(log, f, indent=4)

    return metadata