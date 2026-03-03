from flask import Flask

from app.db_handeling.config import Config
from app.db_handeling.extensions import db


def create_app(config_object: type[Config] = Config) -> Flask:
    """Application factory for the mentora backend."""
    app = Flask(__name__)
    app.config.from_object(config_object)

    config_object.validate(app.config)
    db.init_app(app)

    return app

