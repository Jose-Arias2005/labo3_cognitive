import logging
from flask import Flask
from app.config import Config
from app.extensions import mail

def create_app(config_class=Config):
    # Inicializar app
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializar extensiones
    mail.init_app(app)
    
    logging.basicConfig(level=logging.INFO)

    # Registrar blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.usuario_routes import usuario_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(usuario_bp)

    # Registrar teardown
    from app.repositories.db import close_db
    app.teardown_appcontext(close_db)

    return app
