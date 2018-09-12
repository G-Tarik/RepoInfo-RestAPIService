import os
from flask import Flask

DEFAULT_CONFIG = '../app_config.py'


def create_app():
    """Create Flask application.

    Using application factory pattern and blueprints.
    To use custom application settings create environment variable
    'API_APP_SETTINGS=/path/to/config_file.py'.

    Returns:
        Flask object

    """
    app = Flask(__name__)
    config_file = os.environ.get('API_APP_SETTINGS', DEFAULT_CONFIG)
    app.config.from_pyfile(config_file)
    app.config.update(SECRET_KEY=os.urandom(24))

    from .endpoints import github_api_bp, root_api_bp
    app.register_blueprint(github_api_bp)
    app.register_blueprint(root_api_bp)

    return app
