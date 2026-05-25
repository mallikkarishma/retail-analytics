from flask import Flask
from .config import Config
from .routes.upload import upload_bp
from .routes.video import video_bp
from .database import init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    Config.ensure_dirs()

    # Initialize database on startup
    init_db()

    app.register_blueprint(upload_bp, url_prefix="/api")
    app.register_blueprint(video_bp, url_prefix="/api")

    return app