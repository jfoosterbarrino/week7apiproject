from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

login = LoginManager()
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    login.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    from .blueprints.api import bp as api_bp
    app.register_blueprint(api_bp)

    from .blueprints.auth import bp as auth_bp
    app.register_blueprint(auth_bp)
    
    return app