from flask import Flask
from .config import Config
from .routes.upload import upload_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    Config.ensure_dirs()

    app.register_blueprint(upload_bp, url_prefix="/api")

    return app