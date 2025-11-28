from flask import Flask
from config import Config
from app.database import init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Inicializar base de datos
    init_db(app)
    
    # Registrar blueprints
    from app.routes.voters import bp as voters_bp
    from app.routes.candidates import bp as candidates_bp
    from app.routes.votes import bp as votes_bp
    
    app.register_blueprint(voters_bp, url_prefix='/api')
    app.register_blueprint(candidates_bp, url_prefix='/api')
    app.register_blueprint(votes_bp, url_prefix='/api')
    
    return app