from flask import Flask
from flask_cors import CORS
from .config import Config
from .routes.upload import upload_bp
from .routes.video import video_bp
from .routes.congestion import congestion_bp
from .routes.detect import detect_bp
from .database import init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    Config.ensure_dirs()
    CORS(app)

    init_db()

    app.register_blueprint(upload_bp, url_prefix="/api")
    app.register_blueprint(video_bp, url_prefix="/api")
    app.register_blueprint(congestion_bp, url_prefix="/api")
    app.register_blueprint(detect_bp, url_prefix="/api")

    return app