import threading
import queue
from .yolo_detector import detect_objects, detect_from_video

request_queue = queue.Queue()
result_store = {}

def inference_worker():
    """Runs in background thread — processes YOLO jobs from the queue."""
    while True:
        job = request_queue.get()
        if job is None:
            break

        job_id = job["job_id"]
        job_type = job["type"]

        try:
            if job_type == "image":
                result = detect_objects(job["path"])
            elif job_type == "video":
                result = detect_from_video(job["path"])

            result_store[job_id] = {"status": "done", "result": result}
        except Exception as e:
            result_store[job_id] = {"status": "error", "error": str(e)}

        request_queue.task_done()


def start_worker():
    thread = threading.Thread(target=inference_worker, daemon=True)
    thread.start()
    return thread


def submit_job(job_id: str, path: str, job_type: str = "image"):
    result_store[job_id] = {"status": "processing"}
    request_queue.put({"job_id": job_id, "path": path, "type": job_type})


def get_result(job_id: str):
    return result_store.get(job_id, {"status": "not_found"})