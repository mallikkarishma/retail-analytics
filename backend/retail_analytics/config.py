import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    LOG_DIR       = os.path.join(BASE_DIR, "logs")
    REPORTS_DIR   = os.path.join(BASE_DIR, "reports")
    MODELS_DIR    = os.path.join(BASE_DIR, "models")
    DB_PATH = os.path.join(BASE_DIR, "retail_analytics.db")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    CANVAS_WIDTH  = 640
    CANVAS_HEIGHT = 480

    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "bmp", "tiff", "webp"}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024   # 16 MB

    DEBUG      = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    SECRET_KEY = os.getenv("SECRET_KEY", "retail-dev-secret")

    AISLE_MAX_CAPACITY = 15.0  # seconds — audit triggers above this

    @classmethod
    def ensure_dirs(cls):
        for d in [cls.UPLOAD_FOLDER, cls.LOG_DIR, cls.REPORTS_DIR, cls.MODELS_DIR]:
            os.makedirs(d, exist_ok=True)